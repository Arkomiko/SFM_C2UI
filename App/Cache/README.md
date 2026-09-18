# Cache

Regenerable data that is expensive to rebuild, **shared by every session** and
kept across restarts.

| Folder | Contents |
|---|---|
| `content/` | Indexes of mounted installations - what models, materials and sounds exist and where |
| `thumbnails/` | Rendered previews of models and materials |
| `materials/` | Decoded textures |
| `shaders/` | Compiled shaders |

Entries are keyed by the source file (path plus size and timestamp), never by
session: a cache that died with its session would force the editor to re-index
thousands of models on every launch.

Deleting anything here is always safe. The next run rebuilds it, just slower.
