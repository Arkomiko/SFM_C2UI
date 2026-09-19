"""
The C2UI editor.

Everything the editor writes goes through `locations`, which keeps every path
inside the application folder. Content is reached through `ContentLibrary`,
which mounts an installation via `Core.API` and keeps its index in
`App/Cache/content`.
"""
from . import locations
from .content_library import ContentLibrary, LibraryState

__all__ = ["locations", "ContentLibrary", "LibraryState"]
