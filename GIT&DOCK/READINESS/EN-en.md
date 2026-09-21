# C2UI readiness in detail

<details align="center"><summary>&nbsp;🌐 <b>🇬🇧 English</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><b>🇬🇧<br>English</b></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/EN-en.svg" alt="Readiness" width="100%"></p>

<p align="center"><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Overall readiness for release: 55%</b></p>

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

Shots and sound tracks on a timeline, the element tree, each shot's scene through its camera, the shot's map. Not yet: particles, sound.

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

### <img alt="65%" src="https://img.shields.io/badge/65%25-e0a800?style=flat-square"> Source shading

Session lights (DmeProjectedLight): frustum, Source's attenuation, fade to maxDistance; half-lambert, $lightwarptexture, phong, $rimlight, $selfillum. The map's world by its lightmaps; models lit by the map's ambient cubes and world lights. Not yet: shadows, gobo textures, $bumpmap, $envmap.

### <img alt="65%" src="https://img.shields.io/badge/65%25-e0a800?style=flat-square"> Maps — <code>.bsp</code>

Versions 19–21: world geometry, displacement terrain, brush entities, static props, the map's own pak materials, lightmaps, the skybox around the camera. Frustum culling. Not yet: water, prop_dynamic.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rendering to image and video

PNG/TGA sequences and AVI/MP4 movies from the session: the whole session, the current shot or a range; presets; File → Export, Ctrl+E. Not yet: sound in the movie.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugins <code>.c2plg</code>

Not started.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Themes and workspaces

Deliberately later: one look until the editor has something worth theming.

**Not ready for release.** The foundation — every file format SFM uses, read correctly and verified against the whole installation — is in place and tested, and a session can be opened, played, changed and saved. What is missing is the *comfort* of working: the graph editor, Source shading, maps, export. No version number until an animator can do a day's work in it.

<p align="center"><a href="../README/EN-en.md"><img alt="← Back to the README" src="https://img.shields.io/badge/%E2%86%90_Back_to_the_README-1b2838?style=for-the-badge"></a></p>
