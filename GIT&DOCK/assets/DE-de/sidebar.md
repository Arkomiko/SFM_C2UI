# Reifegrad von C2UI im Detail

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <b>🇩🇪 Deutsch</b> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Reifegrad" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Gesamtreife für eine Veröffentlichung: 41%</b></p>

Jeder Bereich lässt sich aufklappen: was schon funktioniert und was noch fehlt. Die Prozente sind eine Einschätzung gegenüber dem, was SFM kann.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> SFM finden und einbinden

Steam-Registry → `libraryfolders.vdf` → Suchpfade aus `gameinfo.txt` in der Reihenfolge der Engine. Sechs Einbindungen bei einer Standardinstallation. Nichts wird außerhalb des Programmordners geschrieben.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Inhaltsindex

70 199 Dateien in 1,1 s kalt / 0,02 s aus dem Cache; Überschreibungen zwischen Einbindungen werden wie in der Engine aufgelöst.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modelle — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Versionen 44, 48, 49. Skelett, Meshes, alle Detailstufen, Body-Gruppen. 1 500 Modelle geladen, 0 Fehler.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Materialien — <code>.vmt</code>

Alle 19 554 mitgelieferten Materialien werden gelesen; `patch`, DX-Blöcke, Proxies.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Texturen — <code>.vtf</code>

Versionen 7.0–7.5, DXT1/3/5 und alle unkomprimierten Formate, Cubemaps, Mips. DXT geht ohne Dekodierung auf die GPU.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sitzungen — <code>.dmx</code>

Binär 1–5 und KeyValues2. Jede Sitzung und Partikeldatei der Installation wird **Byte für Byte** identisch zurückgeschrieben.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Sitzung auf dem Bildschirm

Shots und Tonspuren auf der Zeitleiste, der Elementbaum, die Szene jedes Shots durch seine Kamera. Noch nicht: Karten, Partikel, Ton.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animation

Kanäle und Logs am Cursor ausgewertet; Scrubben und Abspielen. Knochen, Kameras und Sichtbarkeit folgen der Sitzung.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Gesichter

Flex-Controller, die kompilierten Regeln und Vertex-Animation — Figuren sprechen und zeigen Mimik. Noch nicht: Wrinkle-Maps.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rigs

Ausdrücke, Point/Orient/Parent/Aim-Constraints, Zwei-Knochen-IK. Noch nicht: der volle Operator-Abhängigkeitsgraph, Rig-Erstellung.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Bearbeiten

Klick zum Auswählen, Manipulator zum Verschieben/Drehen, Inspektor für jedes Attribut, Key am Cursor, Rückgängig/Wiederholen, byteexaktes Speichern.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion-Editor

Zeitauswahl mit Hold und Falloff auf dem Lineal; eine Änderung verteilt sich darüber wie in SFM. Noch nicht: Presets, Ebenen.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Graph-Editor

Kurven jedes Logs des gewählten Elements: X/Y/Z, Pitch/Yaw/Roll, Skalare. Keys werden in Zeit und Wert mit Live-Vorschau gezogen, Doppelklick fügt ein, Entf löscht; die Zeitachse ist die der Zeitleiste. Noch nicht: Tangenten und Kurventypen, Skalieren einer Key-Gruppe.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Panel-Docking

Panels auf einen Zielkompass mit Vorschau ziehen, wie in UE5 und Visual Studio. Noch nicht: gespeicherte Layouts, Themes.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source-Shading

Nur Textur und ein einfaches Licht. Noch nicht: Phong, Rim, Lightwarp, Szenenlichter, Schatten.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Karten — <code>.bsp</code>

Nicht begonnen.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Rendern in Bild und Video

Nicht begonnen.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugins <code>.c2plg</code>

Nicht begonnen.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Themes und Arbeitsbereiche

Bewusst später: ein Look, bis der Editor etwas hat, das sich zu gestalten lohnt.

**Nicht veröffentlichungsreif.** Das Fundament — jedes Dateiformat, das SFM nutzt, korrekt gelesen und an der ganzen Installation geprüft — steht und ist getestet; eine Sitzung lässt sich öffnen, abspielen, ändern und speichern. Es fehlt der *Komfort* der Arbeit: Graph-Editor, Source-Shading, Karten, Export. Keine Versionsnummer, bevor ein Animator einen Arbeitstag darin verbringen kann.

<p align="center"><a href="../../README/DE-de.md"><img alt="← Zurück zur README" src="https://img.shields.io/badge/%E2%86%90_Zur%C3%BCck_zur_README-1b2838?style=for-the-badge"></a></p>
