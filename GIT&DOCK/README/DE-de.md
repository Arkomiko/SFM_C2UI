<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <b>🇩🇪 Deutsch</b> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/tests-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — ist mein Neubau des Source-Filmmaker-Editors: derselbe Inhalt, dasselbe Sitzungsformat, dasselbe Datenmodell — in einer Hülle, die ihr Aussehen von der Steam-Bibliothek und ihr Layout vom Unreal-Engine-5-Editor entlehnt.</p>

---

## Die Idee

Source Filmmaker ist ein großartiges Werkzeug in einer Oberfläche von 2012. Ich will keinen Skin über `sfm.exe` legen und seine Fenster nicht eines nach dem anderen kapern. Ich will einen Editor, der **fragt, wo SFM installiert ist**, diese Installation so einbindet, wie Garry's Mod Counter-Strike einbindet, und alles selbst auf diesen Dateien tut — Modelle, Materialien, Texturen, Sitzungen, Animation — ohne SFM je zu starten.

Das Ziel ist **Funktionsgleichheit mit SFM, eins zu eins** (einschließlich Knochen und Rigs), und dann das, was SFM nie bekam.

```
  ┌──────────────┐    "wo ist SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  eigene UI   │ ◀───── eingebunden ───────│    tf/  hl2/  tf_movies/ …   │
  │  eig. Render │       nur lesen       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Reifegrad

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Gesamtreife für eine Veröffentlichung: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Der Editor mit geöffnetem Meet the Heavy" width="100%"><br><sub>Der Editor heute, mit Valves „Meet the Heavy“: Shots und Ton auf der Zeitleiste, der Sitzungsbaum, der erste Shot durch seine eigene Kamera, Figuren in Pose und mit Mimik aus der Sitzung.</sub></p>

Einen Bereich aufklappen, um genau zu sehen, was fertig ist und was nicht. Die Prozente sind meine ehrliche Schätzung gegenüber dem, was SFM kann.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM finden und einbinden</b></summary>

Steam-Registry → `libraryfolders.vdf` → Suchpfade aus `gameinfo.txt` in der Reihenfolge der Engine. Sechs Einbindungen bei einer Standardinstallation. Nichts wird außerhalb des Programmordners geschrieben.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Inhaltsindex</b></summary>

70 199 Dateien in 1,1 s kalt / 0,02 s aus dem Cache; Überschreibungen zwischen Einbindungen werden wie in der Engine aufgelöst.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modelle — <code></code> <code></code> <code></code></b></summary>

Versionen 44, 48, 49. Skelett, Meshes, alle Detailstufen, Body-Gruppen. 1 500 Modelle geladen, 0 Fehler.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Materialien — <code></code></b></summary>

Alle 19 554 mitgelieferten Materialien werden gelesen; `patch`, DX-Blöcke, Proxies.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Texturen — <code></code></b></summary>

Versionen 7.0–7.5, DXT1/3/5 und alle unkomprimierten Formate, Cubemaps, Mips. DXT geht ohne Dekodierung auf die GPU.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Sitzungen — <code></code></b></summary>

Binär 1–5 und KeyValues2. Jede Sitzung und Partikeldatei der Installation wird **Byte für Byte** identisch zurückgeschrieben.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Sitzung auf dem Bildschirm</b></summary>

Shots und Tonspuren auf der Zeitleiste, der Elementbaum, die Szene jedes Shots durch seine Kamera. Noch nicht: Karten, Partikel, Ton.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animation</b></summary>

Kanäle und Logs am Cursor ausgewertet; Scrubben und Abspielen. Knochen, Kameras und Sichtbarkeit folgen der Sitzung.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Gesichter</b></summary>

Flex-Controller, die kompilierten Regeln und Vertex-Animation — Figuren sprechen und zeigen Mimik. Noch nicht: Wrinkle-Maps.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Rigs</b></summary>

Ausdrücke, Point/Orient/Parent/Aim-Constraints, Zwei-Knochen-IK. Noch nicht: der volle Operator-Abhängigkeitsgraph, Rig-Erstellung.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Bearbeiten</b></summary>

Klick zum Auswählen, Manipulator zum Verschieben/Drehen, Inspektor für jedes Attribut, Key am Cursor, Rückgängig/Wiederholen, byteexaktes Speichern. Noch nicht: der Graph-Editor.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion-Editor</b></summary>

Zeitauswahl mit Hold und Falloff auf dem Lineal; eine Änderung verteilt sich darüber wie in SFM. Noch nicht: Presets, Ebenen.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Panel-Docking</b></summary>

Panels auf einen Zielkompass mit Vorschau ziehen, wie in UE5 und Visual Studio. Noch nicht: gespeicherte Layouts, Themes.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source-Shading</b></summary>

Nur Textur und ein einfaches Licht. Noch nicht: Phong, Rim, Lightwarp, Szenenlichter, Schatten.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Karten — <code></code></b></summary>

Nicht begonnen.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Rendern in Bild und Video</b></summary>

Nicht begonnen.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Plugins <code></code></b></summary>

Nicht begonnen.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Themes und Arbeitsbereiche</b></summary>

Bewusst später: ein Look, bis der Editor etwas hat, das sich zu gestalten lohnt.

</details>

**Nicht veröffentlichungsreif.** Das Fundament — jedes Dateiformat, das SFM nutzt, korrekt gelesen und an der ganzen Installation geprüft — steht und ist getestet; eine Sitzung lässt sich öffnen, abspielen, ändern und speichern. Es fehlt der *Komfort* der Arbeit: Graph-Editor, Source-Shading, Karten, Export. Keine Versionsnummer, bevor ein Animator einen Arbeitstag darin verbringen kann.

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
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Beim ersten Start wird SFM über Steam gesucht; wird es nicht gefunden, fragt das Programm. <kbd>Strg</kbd>+<kbd>O</kbd> öffnet eine Sitzung, <kbd>Leertaste</kbd> spielt ab, <kbd>C</kbd> blickt durch die Shot-Kamera, <kbd>T</kbd>/<kbd>R</kbd> verschieben/drehen, <kbd>M</kbd> Motion-Editor, <kbd>Strg</kbd>+<kbd>Z</kbd> macht rückgängig, <kbd>Strg</kbd>+<kbd>S</kbd> speichert. Panels werden am Titel gezogen. Die Tests brauchen nichts:

```bash
python Testing/run.py
```

## Aufbau

```
C2UI_SDK/
├── c2ui.py            der Starter
├── Core/              Engine: Formate, virtuelles Dateisystem, Index, Brücken
├── App/               der Editor: Inhaltsbibliothek, Renderer, Fenster
├── Tools/             Lokalisierung, UI-Werkzeuge, Plugins (später)
├── Testing/           Tests, byteexakte Fixtures, ein Runner
└── GIT&DOCK/README/   diese README in anderen Sprachen
```

## Fahrplan

1. **Graph-Editor** — Kurven und Keys sichtbar.
2. **Source-Shading** — VertexLitGeneric wie SFM es zeichnet: Phong, Rim, Lightwarp, Szenenlichter.
3. **Karten** — `.bsp` als Hintergrund.
4. **Export** — Bild und Video.
5. **Plugins** — das `.c2plg`-Format; dann Themes und Arbeitsbereiche.

## Lizenz und Dank

Source Filmmaker, Team Fortress 2 und die Source-Engine gehören Valve. Dieses Projekt liest ihre Dateiformate, liefert keine ihrer Dateien mit und arbeitet nur mit einer SFM-Kopie, die du bereits über Steam hast.

Die Lizenz für den eigenen Code von C2UI ist noch nicht gewählt — bis dahin alle Rechte vorbehalten. Issues und Pull Requests sind trotzdem willkommen.

<p align="center"><img src="../../.github/assets/models.png" alt="64 Modelle direkt aus der Installation gerendert" width="60%"><br><sub>Vierundsechzig zufällige Modelle aus der Installation, gezeichnet vom eigenen Renderer von C2UI.</sub></p>
