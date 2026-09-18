# Source 2 engine SDK goes here

Ships with Source 2 titles that expose their tools, such as Half-Life: Alyx.

Expected layout inside this folder: `game/ and content/`

Used by: (reserved)

## Why this folder is empty

Valve's SDKs may not be redistributed, so C2UI ships the structure and the
bridge that reads it - never the SDK itself. `.gitignore` keeps whatever you put
here out of commits.

Drop the SDK in this folder, or point the setup step at a local installation.
Until then the matching bridge reports "SDK not available" and the editor still
starts normally.
