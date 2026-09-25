# Reifegrad von C2UI im Detail

<details align="center"><summary>&nbsp;🌐 <b>🇩🇪 Deutsch</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><b>🇩🇪<br>Deutsch</b></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/DE-de.svg" alt="Reifegrad" width="100%"></p>

<p align="center"><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Gesamtreife für eine Veröffentlichung: 15%</b></p>

> [!IMPORTANT]
> **Die Entwicklung ist pausiert.** Das Repository bleibt offen: Code, Dokumentation und Historie sind vorhanden, und alles unten Beschriebene funktioniert wie beschrieben. Die Bereitschaftszahlen, die Issues und die Roadmap geben den Stand zum Zeitpunkt der Pause wieder.

Jeder Bereich lässt sich aufklappen: was schon funktioniert und was noch fehlt. Die Prozente sind eine Einschätzung gegenüber dem, was SFM kann.

Jeder Prozentwert misst **einen Bereich an dem, was SFM in diesem Bereich leistet**, nicht am Geplanten. Die Gesamtzahl misst das ganze Produkt neben SFM und liegt weit darunter: die Formate werden vollständig gelesen, aber Source Filmmaker zu sein heißt rund 350 `Dme*`-Elementtypen, von denen die Engine 23 kennt.

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

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Sitzung auf dem Schirm

Shots und Tonspuren auf der Zeitleiste, der Elementbaum, die Szene jedes Shots durch seine Kamera, die Karte des Shots. Noch nicht: Partikel, Ton.

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

### <img alt="75%" src="https://img.shields.io/badge/75%25-3b9c5b?style=flat-square"> Source-Shading

Sitzungslichter (DmeProjectedLight): Frustum, Source-Abschwächung, Ausblenden bis maxDistance; Half-Lambert, $lightwarptexture, Phong, $rimlight, $selfillum. Die Welt der Karte über ihre Lightmaps; Modelle durch Ambient-Cubes und World-Lights der Karte beleuchtet. Noch nicht: Schatten, Gobo-Texturen, $bumpmap, $envmap.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Karten — <code>.bsp</code>

Versionen 19–21: Weltgeometrie, Displacement-Gelände, Brush-Entities, statische Props, die Pak-Materialien der Karte, Lightmaps, die Skybox um die Kamera. Frustum-Culling. Noch nicht: Wasser, prop_dynamic.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Rendern in Bild und Video

PNG/TGA-Sequenzen und AVI/MP4-Filme aus der Sitzung: ganze Sitzung, aktueller Shot oder ein Bereich; Presets; File → Export, Strg+E. Noch nicht: Ton im Film.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugins <code>.c2plg</code>

Nicht begonnen.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Themes und Arbeitsbereiche

Bewusst später: ein Look, bis der Editor etwas hat, das sich zu gestalten lohnt.

**Nicht veröffentlichungsreif.** Das Fundament — jedes Dateiformat, das SFM nutzt, korrekt gelesen und an der ganzen Installation geprüft — steht und ist getestet; eine Sitzung lässt sich öffnen, abspielen, ändern und speichern. Es fehlt der *Komfort* der Arbeit: Graph-Editor, Source-Shading, Karten, Export. Keine Versionsnummer, bevor ein Animator einen Arbeitstag darin verbringen kann.

<p align="center"><a href="../README/DE-de.md"><img alt="← Zurück zur README" src="https://img.shields.io/badge/%E2%86%90_Zur%C3%BCck_zur_README-1b2838?style=for-the-badge"></a></p>
