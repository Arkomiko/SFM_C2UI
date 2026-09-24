# Der C2UI-Launcher

<details align="center"><summary>&nbsp;🌐 <b>🇩🇪 Deutsch</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><b>🇩🇪<br>Deutsch</b></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` ist das, womit das Projekt gestartet wird: ein kleines dunkles Fenster mit Titel, einer Beschreibungszeile und drei Schaltflächen. Es wird zu einer einzigen ausführbaren Datei gebaut, die kein installiertes Python braucht, und findet das Projekt selbst — es geht von seinem Ort aufwärts, bis es `App`, `Core` und `Launcher` beieinander sieht.

<p align="center"><img src="../assets/launcher.png" alt="Der C2UI-Launcher" width="562"><br><sub>Das Launcher-Fenster: der Titel „Dev-mode“, die Beschreibungszeile und drei Schaltflächen.</sub></p>

> [!NOTE]
> **Die Oberfläche des Launchers ist vorerst nur auf Russisch — eine vorläufige Lösung.** Titel, Beschreibung und Beschriftungen stehen fest im Code; Übersetzungen kommen mit der Lokalisierung des Editors (`Tools/Localization`), wenn der Launcher für ein fertiges App neu geschrieben wird. Die übrige Dokumentation des Projekts gibt es bereits in 32 Sprachen.

## Die drei Schaltflächen

| | |
|---|---|
| <code>Запустить Core</code> | Startet den Editor — das C2UI-Fenster mit Viewport, Zeitleiste und Panels. |
| <code>Запустить App</code> | Ausgegraut: ein eigenständiges App gibt es noch nicht. |
| <code>Выйти</code> | Schließt den Launcher. |

## Start aus dem Quelltext

Windows, Python 3.13 und eine installierte Kopie von Source Filmmaker werden gebraucht.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Bau der einen Datei `Launcher/Launcher-C2UI.exe` (nicht in git — sie wird aus dem Quelltext neu gebaut):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Die Engine ohne den Editor

`Launcher/core.py` startet `Core` allein: mountet eine Installation, indiziert sie und gibt eine kleine Shell über die Engine — Modelle, Materialien, Texturen, Karten, Sitzungen und ihre Auswertung. Ebenfalls vorläufig: sobald App ohne Fenster läuft, wird der Editor der einzige Einstiegspunkt.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Was sich später ändert

- Das Fenster wird mit App neu geschrieben — samt Gestaltung und Übersetzungen.
- Die Schaltfläche „Запустить App“ fängt an zu arbeiten.
- `core.py` verschwindet, sobald der Editor ohne Fenster startbar ist.
- Die gebaute `.exe` liegt den GitHub-Releases bei.

<p align="center"><a href="../README/DE-de.md"><img alt="← Zurück zur README" src="https://img.shields.io/badge/%E2%86%90_Zur%C3%BCck_zur_README-1b2838?style=for-the-badge"></a></p>
