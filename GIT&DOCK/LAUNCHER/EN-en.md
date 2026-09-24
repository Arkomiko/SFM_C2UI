# The C2UI launcher

<details align="center"><summary>&nbsp;🌐 <b>🇬🇧 English</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><b>🇬🇧<br>English</b></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` is what the project is started from: a small dark window with a title, one line of description and three buttons. It builds into a single executable that needs no installed Python, and it finds the project by itself — walking up from wherever it sits until it sees `App`, `Core` and `Launcher` together.

<p align="center"><img src="../assets/launcher.png" alt="The C2UI launcher" width="562"><br><sub>The launcher window: the “Dev-mode” title, the description line and three buttons.</sub></p>

> [!NOTE]
> **The launcher's interface is in Russian only for now — a temporary solution.** The title, the description and the button captions are hard-coded; translations arrive together with the editor's localisation (`Tools/Localization`) when the launcher is rewritten for a finished App. The rest of the project's documentation is already in 32 languages.

## The three buttons

| | |
|---|---|
| <code>Запустить Core</code> | Starts the editor — the C2UI window with its viewport, timeline and panels. |
| <code>Запустить App</code> | Greyed out: there is no separate App yet. |
| <code>Выйти</code> | Closes the launcher. |

## Running from source

Windows, Python 3.13 and an installed Source Filmmaker are needed.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Building the single file `Launcher/Launcher-C2UI.exe` (not kept in git — it is rebuilt from source):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## The engine without the editor

`Launcher/core.py` starts `Core` on its own: it mounts an installation, indexes it and gives a small shell over the engine — models, materials, textures, maps, sessions and their evaluation. Temporary as well: once App can run headless, the editor becomes the single entry point.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## What changes later

- The window is rewritten when App exists, with its look and its translations.
- The “Запустить App” button starts working.
- `core.py` goes once the editor can be started without a window.
- The built `.exe` is attached to GitHub releases.

<p align="center"><a href="../README/EN-en.md"><img alt="← Back to the README" src="https://img.shields.io/badge/%E2%86%90_Back_to_the_README-1b2838?style=for-the-badge"></a></p>
