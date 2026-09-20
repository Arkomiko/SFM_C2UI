# Pregătirea C2UI în detaliu

<details align="center"><summary>&nbsp;🌐 <b>🇲🇩 Moldovenească</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../RU-ru/sidebar.md">🇷🇺<br>Русский</a></td><td align="center"><a href="../EN-en/sidebar.md">🇬🇧<br>English</a></td><td align="center"><a href="../PL-pl/sidebar.md">🇵🇱<br>Polski</a></td><td align="center"><a href="../UK-ua/sidebar.md">🇺🇦<br>Українська</a></td><td align="center"><a href="../DE-de/sidebar.md">🇩🇪<br>Deutsch</a></td><td align="center"><b>🇲🇩<br>Moldovenească</b></td><td align="center"><a href="../SL-si/sidebar.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="../BE-by/sidebar.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="../KK-kz/sidebar.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="../JA-jp/sidebar.md">🇯🇵<br>日本語</a></td><td align="center"><a href="../ZH-cn/sidebar.md">🇨🇳<br>中文</a></td><td align="center"><a href="../SV-se/sidebar.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="../ES-es/sidebar.md">🇪🇸<br>Español</a></td><td align="center"><a href="../HI-in/sidebar.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="../PT-pt/sidebar.md">🇵🇹<br>Português</a></td><td align="center"><a href="../BN-bd/sidebar.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="../FR-fr/sidebar.md">🇫🇷<br>Français</a></td><td align="center"><a href="../TE-in/sidebar.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="../MR-in/sidebar.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="../TA-in/sidebar.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="../TR-tr/sidebar.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="../UR-pk/sidebar.md">🇵🇰<br>اردو</a></td><td align="center"><a href="../VI-vn/sidebar.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="../GU-in/sidebar.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="../IT-it/sidebar.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="../KO-kr/sidebar.md">🇰🇷<br>한국어</a></td><td align="center"><a href="../AR-sa/sidebar.md">🇸🇦<br>العربية</a></td><td align="center"><a href="../JV-id/sidebar.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="../ML-in/sidebar.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="../NE-np/sidebar.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="../UZ-uz/sidebar.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="../OR-in/sidebar.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="sidebar.svg" alt="Grad de pregătire" width="320"></p>

<p align="center"><img alt="49%" src="https://img.shields.io/badge/49%25-e0a800?style=flat-square"> <b>Pregătire generală pentru lansare: 49%</b></p>

Fiecare zonă se deschide: ce funcționează deja și ce nu există încă. Procentele sunt o estimare față de posibilitățile SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Găsirea și montarea SFM

Registrul Steam → `libraryfolders.vdf` → căile din `gameinfo.txt` în ordinea motorului. Șase montări pe o instalare standard. Nimic nu se scrie în afara folderului aplicației.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Index de conținut

70 199 fișiere în 1,1 s la rece / 0,02 s din cache; suprascrierile între montări sunt rezolvate exact ca în motor.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modele — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Versiunile 44, 48, 49. Schelet, mesh-uri, toate nivelurile de detaliu, grupuri de corp. 1 500 de modele încărcate, 0 eșecuri.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Materiale — <code>.vmt</code>

Toate cele 19 554 de materiale livrate se citesc; `patch`, blocuri DX, proxy-uri.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Texturi — <code>.vtf</code>

Versiunile 7.0–7.5, DXT1/3/5 și toate formatele necomprimate, cubemap-uri, mip-uri. DXT merge pe GPU fără decodare.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sesiuni — <code>.dmx</code>

Binar 1–5 și KeyValues2. Fiecare sesiune și fișier de particule din instalare se rescrie **octet cu octet** identic.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Sesiunea pe ecran

Cadre și piste de sunet pe cronologie, arborele elementelor, scena fiecărui cadru prin camera sa. Încă nu: hărți, particule, sunet.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animație

Canale și loguri evaluate la cursor; derulare și redare. Oasele, camerele și vizibilitatea urmează sesiunea.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Fețe

Controlere flex, regulile compilate și animația de vârfuri — personajele vorbesc și au expresii. Încă nu: hărți de riduri.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rig-uri

Expresii, constrângeri point/orient/parent/aim, IK cu două oase. Încă nu: graful complet al operatorilor, crearea de rig-uri.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Editare

Selectare prin clic, manipulator de mutare/rotire, inspector pentru orice atribut, cheie la cursor, anulare/refacere, salvare exactă la octet.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Selecție de timp cu hold și falloff pe riglă; o modificare se întinde peste ea ca în SFM. Încă nu: presetări, straturi.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Editor de grafice

Curbele fiecărui log al elementului selectat: X/Y/Z, pitch/yaw/roll, scalari. Cheile se trag în timp și valoare cu previzualizare live, dublu clic inserează, Delete șterge; axa timpului e cea a cronologiei. Încă nu: tangente și tipuri de curbe, scalarea unui grup de chei.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Andocarea panourilor

Trageți panourile pe o busolă de ținte cu previzualizare, ca în UE5 și Visual Studio. Încă nu: aranjări salvate, teme.

### <img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> Umbrire Source

Luminile sesiunii (DmeProjectedLight): frustum, atenuarea Source, estompare până la maxDistance; half-lambert, $lightwarptexture, phong ($phongexponent/boost/fresnelranges), $rimlight, $selfillum. Lumea hărții prin lightmap-uri. Încă nu: umbre, texturi gobo, $bumpmap, $envmap, cuburi ambientale, skybox.

### <img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> Hărți — <code>.bsp</code>

Versiunile 19–21: geometria lumii, teren displacement, entități brush, prop-uri statice, materialele din pak-ul hărții. Eliminare în afara camerei. Încă nu: lightmap-uri, skybox, apă, prop_dynamic.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Randare în imagine și video

Neînceput.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugin-uri <code>.c2plg</code>

Neînceput.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Teme și spații de lucru

Amânat intenționat: un singur aspect până când editorul are ce stiliza.

**Nu este gata de lansare.** Fundația — fiecare format de fișier folosit de SFM, citit corect și verificat pe întreaga instalare — există și este testată; o sesiune poate fi deschisă, redată, modificată și salvată. Lipsește *confortul* lucrului: editorul de grafice, umbrirea Source, hărțile, exportul. Fără număr de versiune până când un animator poate lucra o zi întreagă în el.

<p align="center"><a href="../../README/RO-md.md"><img alt="← Înapoi la README" src="https://img.shields.io/badge/%E2%86%90_%C3%8Enapoi_la_README-1b2838?style=for-the-badge"></a></p>
