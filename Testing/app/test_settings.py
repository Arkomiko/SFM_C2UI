"""
Settings: defaults, round trip, tolerance of a bad file, atomic save.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from App.Code.settings import DEFAULTS, Settings


def _tmp():
    return Path(tempfile.mkdtemp(prefix="c2ui_settings_")) / "settings.json"


def test_defaults_when_no_file():
    s = Settings.load(_tmp())
    assert s.get("content.source") == DEFAULTS["content.source"]
    assert s.get("nothing", 5) == 5
    assert not s.dirty


def test_round_trip():
    path = _tmp()
    s = Settings.load(path)
    s.set("content.sfm_path", r"D:\Games\SFM")
    assert s.dirty and s.save()
    assert not s.dirty and not s.save()               # nothing new to write
    again = Settings.load(path)
    assert again.get("content.sfm_path") == r"D:\Games\SFM"
    assert json.loads(path.read_text(encoding="utf-8"))["content.sfm_path"] == r"D:\Games\SFM"


def test_setting_the_same_value_is_not_a_change():
    s = Settings.load(_tmp())
    s.set("content.source", "sfm")
    assert not s.dirty


def test_unreadable_file_is_treated_as_absent():
    path = _tmp()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{ not json", encoding="utf-8")
    s = Settings.load(path)
    assert s.get("content.source") == "sfm"


def test_save_leaves_no_temporary_file_behind():
    path = _tmp()
    s = Settings.load(path)
    s.set("a", 1)
    s.save()
    assert [p.name for p in path.parent.iterdir()] == ["settings.json"]
