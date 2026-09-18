# Steamworks SDK goes here

https://partner.steamgames.com/downloads/list - a Steamworks account is required.

Expected layout inside this folder: `public/ and redistributable_bin/`

Used by: (reserved - see below)

## Why this folder is empty

Valve's SDKs may not be redistributed, so C2UI ships the structure and the
bridge that reads it - never the SDK itself. `.gitignore` keeps whatever you put
here out of commits.

Drop the SDK in this folder, or point the setup step at a local installation.
Until then the matching bridge reports "SDK not available" and the editor still
starts normally.

## Reserved, not required

Nothing in C2UI needs this SDK today. Detecting which Source games are installed
is done by reading Steam's own `libraryfolders.vdf` and `appmanifest_*.acf`
files, which `bridge_steam` does without any SDK.

This slot exists for the day C2UI needs to *publish* to the Steam Workshop -
that is the part that genuinely requires Steamworks.
