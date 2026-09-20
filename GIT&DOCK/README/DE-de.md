<p align="center"><img src="../assets/DE-de/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <b>🇩🇪 Deutsch</b> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/tests-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — der Source-Filmmaker-Editor in einer modernen Hülle: derselbe Inhalt, dasselbe Sitzungsformat, dasselbe Datenmodell, eine Oberfläche im Geist der Steam-Bibliothek und des Unreal-Engine-5-Editors.</p>

---

## Reifegrad

<p align="center"><img src="../assets/DE-de/sidebar.svg" alt="Reifegrad" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Gesamtreife für eine Veröffentlichung: 41%</b></p>

<p align="center"><a href="../assets/DE-de/sidebar.md"><img alt="Reifegrad im Detail" src="https://img.shields.io/badge/Reifegrad_im_Detail-66c0f4?style=for-the-badge"></a></p>

## Die Idee

Source Filmmaker ist ein starkes Werkzeug, dessen Oberfläche im Jahr 2012 geblieben ist. C2UI ersetzt es nicht und baut es nicht um: Das Ziel ist schlicht, SFM etwas moderner und bequemer zu machen.

Der Editor findet das installierte SFM, bindet es als Inhaltsbibliothek ein — Modelle, Materialien, Texturen, Sitzungen — und arbeitet mit denselben Dateien im selben Format. Alles, was in SFM entstanden ist, öffnet sich in C2UI, und umgekehrt.

Das erste Ziel ist volle Kompatibilität mit SFM, Knochen und Rigs eingeschlossen. Danach das, was SFM gefehlt hat.

```
  ┌──────────────┐    "wo ist SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  eigene UI   │ ◀───── eingebunden ───────│    tf/  hl2/  tf_movies/ …   │
  │  eig. Render │       nur lesen       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Der Editor mit geöffnetem Meet the Heavy" width="100%"><br><sub>Der Editor heute, mit Valves „Meet the Heavy“: Shots und Ton auf der Zeitleiste, der Sitzungsbaum, der erste Shot durch seine eigene Kamera, Figuren in Pose und mit Mimik aus der Sitzung.</sub></p>

## Was es anders macht

- **Portabel.** Nichts wird außerhalb des Programmordners geschrieben: Einstellungen unter `App/User`, Caches unter `App/Cache`, Temporäres unter `App/Temporary`. Ordner löschen — weg.
- **Startet nie SFM.** Kein Prozess zu steuern, keine Fenster zu kapern. Die Installation wird wie ein Inhaltspaket gelesen.
- **Formate geprüft, nicht angenommen.** Jeder Leser wurde an der echten Installation verglichen; wo ein Format etwas Überraschendes tut, sagt es der Code.
- **Speichern ist exakt.** Eine unverändert gelesene und geschriebene Sitzung ist dieselbe Datei.
- **Die Engine hat keine Abhängigkeiten.** `Core/` und alle Tests laufen auf nacktem Python; nur das Fenster braucht Qt und OpenGL.

## Starten

Benötigt Windows, Python 3.13 und eine Source-Filmmaker-Installation.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Beim ersten Start wird SFM über Steam gesucht; wird es nicht gefunden, fragt das Programm. <kbd>Strg</kbd>+<kbd>O</kbd> öffnet eine Sitzung, <kbd>Leertaste</kbd> spielt ab, <kbd>C</kbd> blickt durch die Shot-Kamera, <kbd>T</kbd>/<kbd>R</kbd> verschieben/drehen, <kbd>M</kbd> Motion-Editor, <kbd>Strg</kbd>+<kbd>Z</kbd> macht rückgängig, <kbd>Strg</kbd>+<kbd>S</kbd> speichert. Panels werden am Titel gezogen. Die Tests brauchen nichts:

```bash
python Testing/run.py
```

## Aufbau

```
C2UI_SDK/
├── README.md
├── Core/              Engine: Formate, virtuelles Dateisystem, Index, Brücken
├── App/               der Editor: Inhaltsbibliothek, Renderer, Fenster
├── Tools/             Lokalisierung, UI-Werkzeuge, Plugins (später)
│   └── Launcher/      der Starter
├── Testing/           Tests, byteexakte Fixtures, ein Runner
└── GIT&DOCK/          diese README in anderen Sprachen
```

## Fahrplan

1. **Source-Shading** — VertexLitGeneric wie SFM es zeichnet: Phong, Rim, Lightwarp, Szenenlichter.
2. **Karten** — `.bsp` als Hintergrund.
3. **Export** — Bild und Video.
4. **Plugins** — das `.c2plg`-Format; dann Themes und Arbeitsbereiche.

## Lizenz und Dank

Der eigene Code von C2UI steht unter der **C2UI-Lizenz**: frei für private und nicht-kommerzielle Zwecke; kommerzielle Nutzung nur mit schriftlicher Zustimmung des Autors; geänderte Versionen müssen auf das Originalprojekt und seinen Autor Arkomiko verweisen. Plugins und Addons stehen unter der Lizenz **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 und die Source-Engine gehören Valve; das Projekt liest ihre Formate, enthält keine ihrer Dateien und arbeitet nur mit deiner eigenen SFM-Kopie aus Steam.

<p align="center"><a href="../LICENSE/DE-de.md"><img alt="Lizenztext" src="https://img.shields.io/badge/Lizenztext-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 Modelle direkt aus der Installation gerendert" width="60%"><br><sub>Vierundsechzig zufällige Modelle aus der Installation, gezeichnet vom eigenen Renderer von C2UI.</sub></p>
