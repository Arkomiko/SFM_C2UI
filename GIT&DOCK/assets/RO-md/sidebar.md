# Pregătirea C2UI în detaliu

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <b>🇲🇩 Moldovenească</b> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Grad de pregătire" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Pregătire generală pentru lansare: 41%</b></p>

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

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Umbrire Source

Doar textură și o lumină simplă. Încă nu: phong, rim, lightwarp, lumini de scenă, umbre.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Hărți — <code>.bsp</code>

Neînceput.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Randare în imagine și video

Neînceput.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugin-uri <code>.c2plg</code>

Neînceput.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Teme și spații de lucru

Amânat intenționat: un singur aspect până când editorul are ce stiliza.

**Nu este gata de lansare.** Fundația — fiecare format de fișier folosit de SFM, citit corect și verificat pe întreaga instalare — există și este testată; o sesiune poate fi deschisă, redată, modificată și salvată. Lipsește *confortul* lucrului: editorul de grafice, umbrirea Source, hărțile, exportul. Fără număr de versiune până când un animator poate lucra o zi întreagă în el.

<p align="center"><a href="../../README/RO-md.md"><img alt="← Înapoi la README" src="https://img.shields.io/badge/%E2%86%90_%C3%8Enapoi_la_README-1b2838?style=for-the-badge"></a></p>
