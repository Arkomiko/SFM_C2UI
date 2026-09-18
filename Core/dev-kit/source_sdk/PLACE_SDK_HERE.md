# Source engine SDK goes here

Valve publishes it at https://github.com/ValveSoftware/source-sdk-2013 under the Source SDK licence.

Expected layout inside this folder: `sp/src/ and mp/src/`

Used by: bridge_sfm, bridge_gmod

## Why this folder is empty

Valve's SDKs may not be redistributed, so C2UI ships the structure and the
bridge that reads it - never the SDK itself. `.gitignore` keeps whatever you put
here out of commits.

Drop the SDK in this folder, or point the setup step at a local installation.
Until then the matching bridge reports "SDK not available" and the editor still
starts normally.
