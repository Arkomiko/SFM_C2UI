# dev-kit

Every external SDK lives here, next to the bridge that reads it.

## SDK slots

| Folder | SDK |
|---|---|
| `sfm_sdk/` | Source Filmmaker SDK |
| `source_sdk/` | Source engine SDK |
| `source2_sdk/` | Source 2 engine SDK |
| `steam_sdk/` | Steamworks SDK - reserved, see below |

**The SDK folders ship empty.** Valve's SDKs may not be redistributed, so this
repository carries the structure and the bridges but never Valve's files. Each
slot has a `PLACE_SDK_HERE.md` naming the source and the expected layout, and
`.gitignore` keeps their contents out of commits.

## Bridges

A bridge turns one external thing into data C2UI understands. Bridges are ours,
they live in the repository, and each one reports a clear "not available" state
instead of failing when its source is missing.

| Folder | Reads |
|---|---|
| `bridge_sfm/` | A Source Filmmaker installation: content mounts from `gameinfo.txt`, models, materials, sessions |
| `bridge_workshop/` | Workshop content installed into SFM |
| `bridge_steam/` | The local Steam library - which Source games are installed |
| `bridge_gmod/` | A Garry's Mod installation |

`bridge_steam` needs no SDK at all: Steam's own `libraryfolders.vdf` and
`appmanifest_*.acf` files answer "is Portal 2 installed" by themselves. The
`steam_sdk/` slot stays reserved for the day C2UI needs to *publish* to the
Workshop, which is the only part that requires Steamworks.
