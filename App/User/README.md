# User

Everything the user owns.

**Nothing in this folder is ever deleted by the program.** Loose files are
ignored rather than removed; only folders - and the archives noted below - mean
anything.

| Folder | Contents |
|---|---|
| `Themes/` | Folders or `.zip`. A theme changes colours and icons only |
| `Workspaces/` | Folders or `.zip`. A workspace changes layout, sizes, window behaviour and shortcuts - the whole shape of the editor, while the program and Core stay the same |
| `Locales/` | Translations as folders, in any language the user likes. Missing entries fall back to English, and several locales can be combined |
| `Settings/` | User settings, including where Source Filmmaker, Steam and other sources are installed |
| `Plug-ins/` | See below |

`Settings/` is the single place that knows where the installed games are; Core
receives those paths through the API rather than looking for them itself.

## Plug-ins

| Folder | Standard |
|---|---|
| `Editor/` | C2UI's own format: folders, `.zip` or `.c2ui-plug`, authored with the plugin tool or against Core |
| `Video/` | OBS and After Effects style plugins |
| `Audio/` | VST, VST3 and CLAP |

`Video/` and `Audio/` may hold the real files *or* shortcuts pointing at them,
and the user may arrange them into sub-folders however they like - the same way
FL Studio treats a plugin folder.
