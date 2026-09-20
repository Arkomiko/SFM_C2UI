# Pripravljenost C2UI — podrobno

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <b>🇸🇮 Slovenščina</b> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Pripravljenost" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Skupna pripravljenost za izdajo: 41%</b></p>

Vsako področje se razpre: kaj že deluje in česa še ni. Odstotki so ocena glede na zmožnosti SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Iskanje in priklop SFM

Register Steam → `libraryfolders.vdf` → poti iz `gameinfo.txt` v vrstnem redu pogona. Šest priklopov na običajni namestitvi. Nič se ne zapiše zunaj mape programa.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Kazalo vsebine

70 199 datotek v 1,1 s hladno / 0,02 s iz predpomnilnika; prekrivanja med priklopi se razrešijo kot v pogonu.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modeli — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Različice 44, 48, 49. Okostje, mreže, vse ravni podrobnosti, skupine telesa. 1 500 modelov naloženih, 0 napak.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Materiali — <code>.vmt</code>

Vseh 19 554 priloženih materialov se prebere; `patch`, bloki DX, proxyji.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Teksture — <code>.vtf</code>

Različice 7.0–7.5, DXT1/3/5 in vsi nestisnjeni formati, cubemapi, mipi. DXT gre na GPU brez dekodiranja.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Seje — <code>.dmx</code>

Binarno 1–5 in KeyValues2. Vsaka seja in datoteka delcev iz namestitve se zapiše nazaj **bajt za bajtom** enako.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Seja na zaslonu

Posnetki in zvočne steze na časovnici, drevo elementov, prizor vsakega posnetka skozi njegovo kamero. Še ne: zemljevidi, delci, zvok.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animacija

Kanali in dnevniki ovrednoteni pri kazalcu; drsenje in predvajanje. Kosti, kamere in vidnost sledijo seji.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Obrazi

Flex kontrolniki, prevedena pravila in animacija oglišč — liki govorijo in kažejo čustva. Še ne: zemljevidi gub.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rigi

Izrazi, omejitve point/orient/parent/aim, dvokostni IK. Še ne: celoten graf odvisnosti operatorjev, ustvarjanje rigov.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Urejanje

Izbira s klikom, manipulator za premik/vrtenje, inšpektor za vsak atribut, ključ pri kazalcu, razveljavi/ponovi, bajtno natančno shranjevanje.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Časovna izbira s hold in falloff na ravnilu; sprememba se razporedi čez njo kot v SFM. Še ne: prednastavitve, plasti.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Urejevalnik grafov

Krivulje vsakega dnevnika izbranega elementa: X/Y/Z, pitch/yaw/roll, skalarji. Ključi se vlečejo po času in vrednosti s predogledom v živo, dvojni klik vstavi, Delete briše; časovna os je časovnica. Še ne: tangente in vrste krivulj, skaliranje skupine ključev.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Sidranje plošč

Vlečenje plošč na kompas ciljev s predogledom, kot v UE5 in Visual Studiu. Še ne: shranjene postavitve, teme.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Senčenje Source

Samo tekstura in preprosta luč. Še ne: phong, rim, lightwarp, luči prizora, sence.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Zemljevidi — <code>.bsp</code>

Ni začeto.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Upodabljanje v sliko in video

Ni začeto.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Vtičniki <code>.c2plg</code>

Ni začeto.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Teme in delovni prostori

Namerno pozneje: en videz, dokler urejevalnik nima česa oblikovati.

**Ni pripravljen za izdajo.** Temelj — vsak format datotek, ki ga SFM uporablja, pravilno prebran in preverjen na celotni namestitvi — stoji in je testiran; sejo je mogoče odpreti, predvajati, spremeniti in shraniti. Manjka *udobje* dela: urejevalnik grafov, senčenje Source, zemljevidi, izvoz. Brez številke različice, dokler animator v njem ne more opraviti dneva dela.

<p align="center"><a href="../../README/SL-si.md"><img alt="← Nazaj na README" src="https://img.shields.io/badge/%E2%86%90_Nazaj_na_README-1b2838?style=for-the-badge"></a></p>
