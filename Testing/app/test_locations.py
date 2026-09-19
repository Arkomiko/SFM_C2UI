"""The portability rule: the editor writes nothing outside its own folder."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from App.Code import locations

WRITABLE = [
    "USER", "SETTINGS", "USER_THEMES", "USER_WORKSPACES", "USER_LOCALES", "USER_PLUGINS",
    "CACHE", "CONTENT_CACHE", "THUMBNAIL_CACHE", "MATERIAL_CACHE", "SHADER_CACHE", "TEMPORARY",
]


def test_every_writable_path_is_inside_the_app():
    for name in WRITABLE:
        path = getattr(locations, name)
        assert locations.is_inside_app(path), f"{name} escapes the application folder: {path}"


def test_cache_lives_under_app_cache():
    assert locations.CONTENT_CACHE == locations.APP_ROOT / "Cache" / "content"
    assert locations.CACHE.parent == locations.APP_ROOT


def test_user_data_lives_under_app_user():
    assert locations.SETTINGS == locations.APP_ROOT / "User" / "Settings"


def test_nothing_points_at_roaming_profiles():
    suspects = [os.environ.get("APPDATA"), os.environ.get("LOCALAPPDATA")]
    for name in WRITABLE:
        text = str(getattr(locations, name))
        for suspect in suspects:
            if suspect:
                assert suspect.lower() not in text.lower(), f"{name} points into {suspect}"


def test_ensure_dirs_creates_the_tree():
    locations.ensure_dirs()
    for name in WRITABLE:
        assert getattr(locations, name).is_dir(), name


def test_is_inside_app_rejects_outside_paths():
    assert not locations.is_inside_app(Path("C:/Windows"))
    assert not locations.is_inside_app(locations.PROJECT_ROOT.parent / "elsewhere")
    assert locations.is_inside_app(locations.CACHE / "content" / "content.db")


def test_session_folders_are_unique_and_inside_temporary():
    a = locations.new_session_dir()
    b = locations.new_session_dir()
    try:
        assert a != b
        assert a.parent == locations.TEMPORARY
        assert locations.is_inside_app(a)
    finally:
        locations.clear_temporary()


def test_clear_temporary_removes_sessions_but_keeps_the_folder():
    folder = locations.new_session_dir()
    (folder / "junk.txt").write_text("scratch", encoding="utf-8")
    removed = locations.clear_temporary()
    assert removed >= 1
    assert locations.TEMPORARY.is_dir()
    assert not folder.exists()


def test_clear_temporary_can_keep_the_current_session():
    keep = locations.new_session_dir()
    other = locations.new_session_dir()
    try:
        locations.clear_temporary(keep=[keep])
        assert keep.exists()
        assert not other.exists()
    finally:
        locations.clear_temporary()


def test_clear_temporary_never_touches_user_data():
    marker = locations.SETTINGS / "keep_me.json"
    locations.ensure_dirs()
    marker.write_text("{}", encoding="utf-8")
    try:
        locations.clear_temporary()
        assert marker.is_file(), "clearing Temporary must not reach into User"
    finally:
        marker.unlink(missing_ok=True)


def test_clear_cache_keeps_the_folders():
    locations.ensure_dirs()
    probe = locations.THUMBNAIL_CACHE / "probe.bin"
    probe.write_bytes(b"x")
    removed = locations.clear_cache()
    assert removed >= 1
    assert locations.THUMBNAIL_CACHE.is_dir()
    assert not probe.exists()


def test_clear_cache_never_touches_user_data():
    locations.ensure_dirs()
    marker = locations.USER_THEMES / "mytheme.txt"
    marker.write_text("mine", encoding="utf-8")
    try:
        locations.clear_cache()
        assert marker.is_file(), "clearing Cache must not reach into User"
    finally:
        marker.unlink(missing_ok=True)


def test_cleaning_keeps_the_placeholders_that_hold_the_folders():
    # .gitkeep is what makes these folders exist in a fresh checkout; wiping the
    # cache must not quietly remove them from the project
    locations.ensure_dirs()
    keepers = []
    for folder in (locations.CONTENT_CACHE, locations.THUMBNAIL_CACHE,
                   locations.MATERIAL_CACHE, locations.SHADER_CACHE, locations.TEMPORARY):
        placeholder = folder / ".gitkeep"
        if not placeholder.exists():
            placeholder.write_text("", encoding="utf-8")
        keepers.append(placeholder)

    locations.clear_cache()
    locations.clear_temporary()

    for placeholder in keepers:
        assert placeholder.is_file(), f"{placeholder} was removed by cleaning"
