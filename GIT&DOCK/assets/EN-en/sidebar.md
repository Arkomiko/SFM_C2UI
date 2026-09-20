# C2UI readiness in detail

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <b>🇬🇧 English</b> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Readiness" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Overall readiness for release: 41%</b></p>

Each area expands: what already works and what does not yet. The percentages are an estimate against what SFM can do.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Finding and mounting SFM

Steam registry → `libraryfolders.vdf` → the search paths of `gameinfo.txt`, in the engine's own order. Six mounts on a stock install. Nothing is written outside the application folder.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Content index

70 199 files in 1.1 s cold / 0.02 s warm; overrides between mounts resolved exactly as the engine does.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Models — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Versions 44, 48, 49. Skeleton, meshes, every level of detail, body groups. 1 500 models loaded, 0 failures.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Materials — <code>.vmt</code>

All 19 554 shipped materials parse; `patch`, DX-level blocks, proxies.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Textures — <code>.vtf</code>

Versions 7.0–7.5, DXT1/3/5 and every uncompressed format, cubemaps, mips. DXT goes to the GPU without decoding.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sessions — <code>.dmx</code>

Binary 1–5 and KeyValues2. Every session and particle file in the install writes back **byte for byte**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Session on screen

Shots and sound tracks on a timeline, the element tree, each shot's scene through its camera. Not yet: maps, particles, sound.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animation

Channels and logs evaluated at the cursor; scrub and play. Bones, cameras and visibility follow the session.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Faces

Flex controllers, the compiled rules and vertex animation — characters talk and emote. Not yet: wrinkle maps.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rigs

Expressions, point/orient/parent/aim constraints, two-bone IK. Not yet: the full operator dependency graph, rig creation.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Editing

Click to select, a move/rotate manipulator, an inspector for any attribute, a key at the cursor, undo/redo, byte-exact save.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

A time selection with hold and falloff on the ruler; an edit spreads over it as in SFM. Not yet: presets, layers.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Graph editor

Curves of every log driving the selected element: X/Y/Z, pitch/yaw/roll, scalars. Keys drag in time and value with a live preview, double-click inserts, Delete removes; the time axis is the timeline's. Not yet: tangents and curve types, scaling a group of keys.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Panel docking

Drag panels onto a compass of targets with a preview, as in UE5 and Visual Studio. Not yet: saved layouts, themes.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source shading

Texture and a simple light only. Not yet: phong, rim, lightwarp, scene lights, shadows.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Maps — <code>.bsp</code>

Not started.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Rendering to image and video

Not started.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugins <code>.c2plg</code>

Not started.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Themes and workspaces

Deliberately later: one look until the editor has something worth theming.

**Not ready for release.** The foundation — every file format SFM uses, read correctly and verified against the whole installation — is in place and tested, and a session can be opened, played, changed and saved. What is missing is the *comfort* of working: the graph editor, Source shading, maps, export. No version number until an animator can do a day's work in it.

<p align="center"><a href="../../README/EN-en.md"><img alt="← Back to the README" src="https://img.shields.io/badge/%E2%86%90_Back_to_the_README-1b2838?style=for-the-badge"></a></p>
