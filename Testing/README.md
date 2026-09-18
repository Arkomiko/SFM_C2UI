# Testing

All automated tests, kept out of `Core/` and `App/` so neither ships with test
code and both stay "folders only" as designed.

| Folder | Covers |
|---|---|
| `core/` | The engine: API contract, bridges, dev-kit slot handling |
| `app/` | The editor: settings, layouts, panels, user data rules |
| `tools/` | The utilities in `Tools/` |
| `fixtures/` | Shared sample data: fake installations, small models, materials, sessions |

`fixtures/` is shared on purpose - a fake SFM installation is needed by both the
bridge tests and the editor tests, and duplicating it would let the two drift
apart.

If Core is ever split into its own repository, `core/` and the fixtures it uses
move with it.
