"""
C2UI Core Library.

Contains the four managers that drive the editor shell:

* ThemeManager      - JSON tokens -> QSS / QPalette
* LayoutManager     - JSON layouts -> dock widget tree
* ContextManager    - actions, modes, shortcuts, selection
* WorkspaceManager  - bundles the above into a workspace

plus the supporting infrastructure (paths, settings, events, localization, panels, ui).
"""

__version__ = "0.1.0"
