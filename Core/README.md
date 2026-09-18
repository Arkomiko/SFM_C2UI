# Core

The engine. Everything here is shared by every program built on C2UI - the
editor in `App/` and the utilities in `Tools/` - and nothing here is specific to
one product.

| Folder | Purpose |
|---|---|
| `dev-kit/` | External SDKs and the bridges that read them |
| `Code/` | Engine source code |
| `API/` | Public contract: how App and third-party developers talk to Core |
| `Resources/` | Static assets available to any core-based program |

Core is **read-only at runtime**. It holds no settings, no cache and no session
data, so the editor works when installed somewhere unwritable such as
`Program Files`. Anything that changes lives in `App/User`, `App/Cache` or
`App/Temporary`; paths to installed games are passed in from
`App/User/Settings` through the API.
