# App

The C2UI editor itself.

| Folder | Lifetime |
|---|---|
| `Data/` | Ships with the program, read-only |
| `User/` | Belongs to the user - **never deleted automatically** |
| `Cache/` | Regenerable, shared by every session, survives restarts |
| `Temporary/` | Session scratch, cleared on start |
| `Legal/` | Licences |

This folder contains **only folders**. Anything loose here is a mistake.
