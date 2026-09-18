# Data

Everything shipped with the program: the defaults used until the user overrides
them in `App/User`.

| Folder | Contents |
|---|---|
| `Img/` | All program images and icons |
| `sound/` | All program sounds |
| `scripts/` | Scripts belonging to the program |
| `loc_id/` | Translation map - every element is an ID; English lives here too |
| `window/` | Docking and snapping behaviour: how windows attach, group and resize |
| `workspaces/` | Concrete ready-made layouts, and the defaults used when the user has none |
| `theme/` | Default style and colours, used when the user has no theme |
| `plugins-base/` | The plugin system plus the bundled base plugins |

`window/` is *behaviour*, `workspaces/` is *arrangement*: the first decides how a
window may snap to another, the second decides where the windows actually are.

Only folders here, each named so its purpose is obvious. More may appear during
development - that is expected.
