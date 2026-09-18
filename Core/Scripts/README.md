# Core/Scripts - user plugins, macros and custom Python scripts

Every sub-folder with a `plugin.json` is a plugin:

```
Core/Scripts/my_plugin/
    plugin.json      {"id": "my_plugin", "name": "My Plugin", "version": "0.1.0", "enabled": true}
    __init__.py      def register(api): ...      def unregister(api): ...  (optional)
```

`register(api)` receives a `PluginAPI` (see `Core/Library/plugin_loader.py`):

| member | purpose |
|---|---|
| `api.register_action(id, text, callback, icon="", shortcut="", checkable=False)` | add a command usable from menus/toolbars/shortcuts |
| `api.register_panel(PanelClass)` | add a dockable panel (subclass `Core.Library.panels.C2UIPanel`) |
| `api.open_panel(panel_id)` | show a panel |
| `api.add_menu_action(menu_title, action_id)` | append an action to a top-level menu |
| `api.sfm_call(method, params)` | synchronous call into SFM through the bridge |
| `api.events.subscribe(topic, fn)` | listen to app / SFM events |
| `api.status(text)` | status-bar message |
| `api.log`, `api.settings`, `api.tr` | logging, user settings, localisation |

Disable a plugin by setting `"enabled": false` in its manifest or by adding its id to
`plugins.disabled` in the user settings.  `main.py --safe-mode` skips all plugins.
