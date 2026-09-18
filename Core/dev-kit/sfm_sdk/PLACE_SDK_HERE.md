# Source Filmmaker SDK goes here

Ships with Source Filmmaker itself, in `<SFM>/game/sdktools`.

Expected layout inside this folder: `sdktools/`

Used by: bridge_sfm

## Why this folder is empty

Valve's SDKs may not be redistributed, so C2UI ships the structure and the
bridge that reads it - never the SDK itself. `.gitignore` keeps whatever you put
here out of commits.

Drop the SDK in this folder, or point the setup step at a local installation.
Until then the matching bridge reports "SDK not available" and the editor still
starts normally.
