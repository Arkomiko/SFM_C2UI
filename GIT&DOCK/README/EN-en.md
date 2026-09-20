<p align="center"><img src="../assets/EN-en/banner.png" alt="C2UI" width="100%"></p>

<details align="center"><summary>&nbsp;🌐 <b>🇬🇧 English</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../../README.md">🇷🇺<br>Русский</a></td><td align="center"><b>🇬🇧<br>English</b></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/tests-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — the Source Filmmaker editor in a modern shell: the same content, the same session format, the same data model, with an interface in the spirit of the Steam library and the Unreal Engine 5 editor.</p>

---

## Readiness

<p align="center"><img src="../assets/EN-en/sidebar.svg" alt="Readiness" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Overall readiness for release: 41%</b></p>

<p align="center"><a href="../assets/EN-en/sidebar.md"><img alt="Readiness in detail" src="https://img.shields.io/badge/Readiness_in_detail-66c0f4?style=for-the-badge"></a></p>

## The idea

Source Filmmaker is a strong tool whose interface stayed in 2012. C2UI does not replace or remake it: the goal is simply to make SFM a little more modern and more comfortable.

The editor finds the installed SFM, attaches it as a content library — models, materials, textures, sessions — and works with the same files in the same format. Anything made in SFM opens in C2UI, and the other way round.

The first goal is full compatibility with SFM, bones and rigs included. After that, what SFM was missing.

```
  ┌──────────────┐    "where is SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  own UI      │ ◀─────  mounted  ───────│    tf/  hl2/  tf_movies/ …   │
  │  own render  │       read only       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="The editor with Meet the Heavy open" width="100%"><br><sub>The editor today, with Valve's Meet the Heavy open: shots and sound on the timeline, the session tree, the first shot seen through its own camera, characters posed and facing as the session says.</sub></p>

## What makes it different

- **Portable.** Nothing is written outside the application folder: settings under `App/User`, caches under `App/Cache`, scratch under `App/Temporary`. Delete the folder and it is gone.
- **Never runs SFM.** No process to drive, no windows to hijack. The installation is read like a content pack.
- **Formats verified, not assumed.** Every reader was checked against the real installation; where a format does something surprising, the code says so.
- **Saving is exact.** A session read and written unchanged is the same file.
- **The engine has no dependencies.** `Core/` and the whole test suite run on a bare Python; only the window needs Qt and OpenGL.

## Running it

Requires Windows, Python 3.13 and a Source Filmmaker installation.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

On first start it looks for SFM through Steam; if it cannot find it, it asks. <kbd>Ctrl</kbd>+<kbd>O</kbd> opens a session, <kbd>Space</kbd> plays, <kbd>C</kbd> looks through the shot camera, <kbd>T</kbd>/<kbd>R</kbd> move/rotate, <kbd>M</kbd> the motion editor, <kbd>G</kbd> the graph editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> undoes, <kbd>Ctrl</kbd>+<kbd>S</kbd> saves. The camera works as in SFM: right button looks around, with it held <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> <kbd>Z</kbd><kbd>X</kbd> fly (<kbd>Shift</kbd> faster), middle pans, the wheel dollies, <kbd>Alt</kbd>+left orbits. Clicking a character picks the bone under the cursor (or its rig handle). Panels are dragged by their title. The tests need nothing at all:

```bash
python Testing/run.py
```

## Layout

```
C2UI_SDK/
├── README.md
├── Core/              engine: formats, virtual file system, index, bridges
├── App/               the editor: content library, renderer, window
├── Tools/             localisation, UI tooling, plugins (later)
│   └── Launcher/      the launcher
├── Testing/           tests, byte-exact fixtures, one runner
└── GIT&DOCK/          this README in other languages
```

## Roadmap

1. **Source shading** — VertexLitGeneric as SFM draws it: phong, rim, lightwarp, scene lights.
2. **Maps** — `.bsp` for backgrounds.
3. **Output** — image and video export.
4. **Plugins** — the `.c2plg` format; then themes and workspaces.

## Licence and credits

C2UI's own code is under the **C2UI licence**: free for personal and non-commercial use; commercial use only with the author's written consent; modified versions must credit the original project and its author, Arkomiko. Plugins and addons are under the **C2UI — Plugins & Addons (C2UI‑Pl&AD)** licence.

Source Filmmaker, Team Fortress 2 and the Source engine are Valve's; this project reads their formats, ships none of their files and works only with your own copy of SFM from Steam.

<p align="center"><a href="../LICENSE/EN-en.md"><img alt="Licence text" src="https://img.shields.io/badge/Licence_text-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 models rendered straight from the installation" width="60%"><br><sub>Sixty-four models picked at random from the installation, rendered by C2UI's own renderer.</sub></p>
