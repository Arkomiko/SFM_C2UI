# Pripravljenost C2UI — podrobno

<details align="center"><summary>&nbsp;🌐 <b>🇸🇮 Slovenščina</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><b>🇸🇮<br>Slovenščina</b></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/SL-si.svg" alt="Pripravljenost" width="100%"></p>

<p align="center"><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Skupna pripravljenost za izdajo: 15%</b></p>

> [!IMPORTANT]
> **Razvoj je začasno ustavljen.** Repozitorij ostaja odprt: koda, dokumentacija in zgodovina so tu, vse spodaj opisano deluje tako, kot je opisano. Številke pripravljenosti, prijave in načrt odražajo stanje ob ustavitvi.

Vsako področje se razpre: kaj že deluje in česa še ni. Odstotki so ocena glede na zmožnosti SFM.

Vsak odstotek meri **področje glede na to, kar na njem zmore SFM**, ne glede na načrtovano. Skupna številka meri celoten izdelek ob SFM in je precej nižja: formati se berejo v celoti, a biti Source Filmmaker pomeni okoli 350 vrst elementov `Dme*`, od katerih jih pogon pozna 23.

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

Posnetki in zvočne sledi na časovnici, drevo elementov, scena posnetka skozi njegovo kamero, zemljevid posnetka. Še ne: delci, zvok.

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

### <img alt="75%" src="https://img.shields.io/badge/75%25-3b9c5b?style=flat-square"> Senčenje Source

Luči seje (DmeProjectedLight): frustum, dušenje Source, pojemanje do maxDistance; half-lambert, $lightwarptexture, phong, $rimlight, $selfillum. Svet zemljevida po lightmapih; modele osvetljujejo ambient kocke in luči zemljevida. Še ne: sence, gobo teksture, $bumpmap, $envmap.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Zemljevidi — <code>.bsp</code>

Različice 19–21: geometrija sveta, displacement teren, brush entitete, statični propi, pak materiali zemljevida, lightmapi, skybox okoli kamere. Odstranjevanje po frustumu. Še ne: voda, prop_dynamic.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Upodabljanje v sliko in video

Zaporedja PNG/TGA in filmi AVI/MP4 iz seje: cela seja, trenutni posnetek ali obseg; prednastavitve; File → Export, Ctrl+E. Še ne: zvok v filmu.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Vtičniki <code>.c2plg</code>

Ni začeto.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Teme in delovni prostori

Namerno pozneje: en videz, dokler urejevalnik nima česa oblikovati.

**Ni pripravljen za izdajo.** Temelj — vsak format datotek, ki ga SFM uporablja, pravilno prebran in preverjen na celotni namestitvi — stoji in je testiran; sejo je mogoče odpreti, predvajati, spremeniti in shraniti. Manjka *udobje* dela: urejevalnik grafov, senčenje Source, zemljevidi, izvoz. Brez številke različice, dokler animator v njem ne more opraviti dneva dela.

<p align="center"><a href="../README/SL-si.md"><img alt="← Nazaj na README" src="https://img.shields.io/badge/%E2%86%90_Nazaj_na_README-1b2838?style=for-the-badge"></a></p>
