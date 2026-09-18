# API

The contract between Core and everything built on it - `App/`, the utilities in
`Tools/` and third-party plugins.

Interfaces, types and their documentation only; no implementation. Any change
here is a breaking change for every plugin in the wild, so this surface is kept
deliberately small and versioned.

The three tools in `Tools/` are built strictly against this API on purpose: if a
tool cannot be written with it, the API is missing something.
