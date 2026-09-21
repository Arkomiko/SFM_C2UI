"""
The export dialog: what to render, at what size and rate, and where to.

One dialog for images and movies.  The defaults come from the session - its
movie size and frame rate, the whole sequence - and the last choices are kept
in the settings so the next export starts where the previous one left off.

    dialog = ExportDialog(session, current_shot, settings, parent)
    if dialog.exec():
        export_settings = dialog.export_settings()
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFileDialog,
                               QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QRadioButton, QSpinBox, QVBoxLayout, QWidget)

from Core.API.dmx import Time
from Core.API.session import FilmClip, Session

from ..export import DEFAULT_FOLDER, IMAGE_KINDS, MOVIE_KINDS, ExportSettings, frame_times, mp4_available
from ..settings import Settings

__all__ = ["ExportDialog"]

#: common frame sizes, offered next to the free width / height fields
PRESETS = (("Session", None), ("1280 x 720", (1280, 720)), ("1920 x 1080", (1920, 1080)),
           ("2560 x 1440", (2560, 1440)), ("3840 x 2160", (3840, 2160)), ("Custom", None))


class ExportDialog(QDialog):
    """Collects an `ExportSettings` from the user."""

    def __init__(self, session: Session, current_shot: Optional[FilmClip], settings: Settings,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Export")
        self.session = session
        self.current_shot = current_shot
        self.settings = settings
        clip = session.active_clip
        self._duration = clip.time_frame.duration.seconds if clip is not None else 0.0
        movie_w, movie_h = session.movie_size
        self.count = QLabel()                      # frames in the range; also shows a refusal

        # -- what
        self.kind = QComboBox()
        for key, (label, _ext) in IMAGE_KINDS.items():
            self.kind.addItem(label, key)
        for key, (label, _ext) in MOVIE_KINDS.items():
            self.kind.addItem(label, key)
        if not mp4_available():
            index = self.kind.findData("mp4")
            self.kind.setItemText(index, MOVIE_KINDS["mp4"][0] + " - no encoder")
            self.kind.model().item(index).setEnabled(False)
        self.kind.currentIndexChanged.connect(self._kind_changed)

        self.path = QLineEdit()
        browse = QPushButton("Browse...")
        browse.clicked.connect(self._browse)
        path_row = QHBoxLayout()
        path_row.addWidget(self.path, 1)
        path_row.addWidget(browse)
        self.name = QLineEdit("frame")
        self.quality = QSpinBox()
        self.quality.setRange(1, 100)
        self.quality.setValue(90)

        what = QGroupBox("Output")
        form = QFormLayout(what)
        form.addRow("Format", self.kind)
        form.addRow("Where", path_row)
        self.name_label = QLabel("File name")
        form.addRow(self.name_label, self.name)
        self.quality_label = QLabel("Quality")
        form.addRow(self.quality_label, self.quality)

        # -- how big, how fast
        self.preset = QComboBox()
        for label, _size in PRESETS:
            self.preset.addItem(label)
        self.preset.currentIndexChanged.connect(self._preset_changed)
        self.width = QSpinBox()
        self.width.setRange(16, 8192)
        self.width.setValue(movie_w)
        self.height = QSpinBox()
        self.height.setRange(16, 8192)
        self.height.setValue(movie_h)
        for spin in (self.width, self.height):
            spin.valueChanged.connect(self._size_edited)
        size_row = QHBoxLayout()
        size_row.addWidget(self.width)
        size_row.addWidget(QLabel("x"))
        size_row.addWidget(self.height)
        size_row.addWidget(self.preset, 1)
        self.fps = QDoubleSpinBox()
        self.fps.setRange(1.0, 240.0)
        self.fps.setDecimals(3)
        self.fps.setValue(session.frame_rate)
        self.fps.valueChanged.connect(self._update_count)
        self.passes = QSpinBox()
        self.passes.setRange(1, 256)
        self.passes.setValue(16)
        self.passes.setToolTip("Renders per frame, spread over the camera's shutter (motion blur) "
                               "and its aperture (depth of field); 1 is sharp and quick")

        frame = QGroupBox("Frame")
        form = QFormLayout(frame)
        form.addRow("Size", size_row)
        form.addRow("Frames per second", self.fps)
        form.addRow("Samples per frame", self.passes)

        # -- which part
        self.whole = QRadioButton("Whole sequence")
        self.shot = QRadioButton("Current shot")
        self.custom = QRadioButton("From / to (seconds)")
        self.start = QDoubleSpinBox()
        self.end = QDoubleSpinBox()
        for spin in (self.start, self.end):
            spin.setRange(0.0, max(self._duration, 0.001))
            spin.setDecimals(3)
            spin.valueChanged.connect(self._update_count)
        self.end.setValue(self._duration)
        self.shot.setEnabled(current_shot is not None)
        for radio in (self.whole, self.shot, self.custom):
            radio.toggled.connect(self._range_changed)
        range_row = QHBoxLayout()
        range_row.addWidget(self.custom)
        range_row.addWidget(self.start)
        range_row.addWidget(QLabel("-"))
        range_row.addWidget(self.end)
        span = QGroupBox("Range")
        column = QVBoxLayout(span)
        column.addWidget(self.whole)
        column.addWidget(self.shot)
        column.addLayout(range_row)
        column.addWidget(self.count)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Export")
        buttons.accepted.connect(self._accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(what)
        layout.addWidget(frame)
        layout.addWidget(span)
        layout.addWidget(buttons)
        self._restore()
        self._kind_changed()
        self._range_changed()

    # -- state ---------------------------------------------------------------------
    def _restore(self) -> None:
        """Start from the last export's choices."""
        kind = self.settings.get("export.kind") or "png"
        index = self.kind.findData(kind)
        if index >= 0 and self.kind.model().item(index).isEnabled():
            self.kind.setCurrentIndex(index)
        self.path.setText(self.settings.get("export.folder") or str(DEFAULT_FOLDER))
        self.quality.setValue(int(self.settings.get("export.quality") or 90))
        self.passes.setValue(int(self.settings.get("export.passes") or 16))
        self.whole.setChecked(True)
        self._size_edited()

    def _remember(self) -> None:
        self.settings.set("export.kind", self.kind.currentData())
        folder = Path(self.path.text())
        self.settings.set("export.folder", str(folder if not self._is_movie() else folder.parent))
        self.settings.set("export.quality", self.quality.value())
        self.settings.set("export.passes", self.passes.value())

    def _is_movie(self) -> bool:
        return self.kind.currentData() in MOVIE_KINDS

    def _kind_changed(self) -> None:
        movie = self._is_movie()
        self.name.setVisible(not movie)
        self.name_label.setVisible(not movie)
        lossy = self.kind.currentData() in ("jpg", "avi", "mp4")
        self.quality.setVisible(lossy)
        self.quality_label.setVisible(lossy)
        text = self.path.text()
        folder = Path(text) if text else DEFAULT_FOLDER
        if movie:
            if not folder.suffix or folder.suffix.lower() not in (".avi", ".mp4"):
                self.path.setText(str(folder / f"{self._stem()}.{MOVIE_KINDS[self.kind.currentData()][1]}"))
            else:
                self.path.setText(str(folder.with_suffix("." + MOVIE_KINDS[self.kind.currentData()][1])))
        elif folder.suffix.lower() in (".avi", ".mp4"):
            self.path.setText(str(folder.parent))

    def _stem(self) -> str:
        clip = self.session.active_clip
        return (clip.name if clip is not None and clip.name else self.session.name or "movie").replace(" ", "_")

    def _preset_changed(self) -> None:
        label, size = PRESETS[self.preset.currentIndex()]
        if label == "Session":
            size = self.session.movie_size
        if size is not None:
            self.width.blockSignals(True)
            self.height.blockSignals(True)
            self.width.setValue(size[0])
            self.height.setValue(size[1])
            self.width.blockSignals(False)
            self.height.blockSignals(False)

    def _size_edited(self) -> None:
        """Match the preset box to the numbers typed."""
        size = (self.width.value(), self.height.value())
        for index, (label, preset) in enumerate(PRESETS):
            if label == "Session":
                preset = self.session.movie_size
            if preset == size:
                break
        else:
            index = len(PRESETS) - 1
        self.preset.blockSignals(True)
        self.preset.setCurrentIndex(index)
        self.preset.blockSignals(False)

    def _range_changed(self) -> None:
        custom = self.custom.isChecked()
        self.start.setEnabled(custom)
        self.end.setEnabled(custom)
        self._update_count()

    def _span(self):
        """(start, end) in sequence time for the chosen range."""
        if self.shot.isChecked() and self.current_shot is not None:
            frame = self.current_shot.time_frame
            return frame.start, frame.end
        if self.custom.isChecked():
            return Time.from_seconds(self.start.value()), Time.from_seconds(self.end.value())
        return Time(0), Time.from_seconds(self._duration)

    def _update_count(self) -> None:
        start, end = self._span()
        frames = len(frame_times(start, end, self.fps.value()))
        self.count.setText(f"{frames} frames, {start.seconds:.3f} - {end.seconds:.3f} s")

    def _browse(self) -> None:
        if self._is_movie():
            ext = MOVIE_KINDS[self.kind.currentData()][1]
            path, _filter = QFileDialog.getSaveFileName(self, "Export movie", self.path.text(),
                                                        f"{ext.upper()} movie (*.{ext})")
        else:
            path = QFileDialog.getExistingDirectory(self, "Export frames into", self.path.text())
        if path:
            self.path.setText(path)

    def _accept(self) -> None:
        problem = self.export_settings().check()
        if problem:
            self.count.setText(problem)
            return
        self._remember()
        self.accept()

    # -- result --------------------------------------------------------------------
    def export_settings(self) -> ExportSettings:
        """What the dialog says, as settings for `export`."""
        start, end = self._span()
        return ExportSettings(Path(self.path.text()), self.width.value(), self.height.value(),
                              self.fps.value(), start, end, kind=self.kind.currentData(),
                              quality=self.quality.value(), name=self.name.text().strip() or "frame",
                              passes=self.passes.value())
