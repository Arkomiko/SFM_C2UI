<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <b>🇸🇮 Slovenščina</b> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/stanje-pred--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/testov-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — je moja prenova urejevalnika Source Filmmaker: ista vsebina, isti format seje, isti podatkovni model — v lupini, ki si videz sposodi od knjižnice Steam, postavitev pa od urejevalnika Unreal Engine 5.</p>

---

## Zamisel

Source Filmmaker je odlično orodje v vmesniku iz leta 2012. Nočem preobleke čez `sfm.exe` in nočem prevzemati njegovih oken enega za drugim. Hočem urejevalnik, ki **vpraša, kje je SFM nameščen**, to namestitev priklopi tako, kot Garry's Mod priklopi Counter-Strike, in vse naredi sam na teh datotekah — modeli, materiali, teksture, seje, animacija — ne da bi SFM sploh kdaj zagnal.

Cilj je **enakovredna funkcionalnost s SFM, ena proti ena** (vključno s kostmi in rigi), potem pa tisto, česar SFM nikoli ni dobil.

```
  ┌──────────────┐    "kje je SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  lastni UI   │ ◀─────  priklop  ───────│    tf/  hl2/  tf_movies/ …   │
  │  lastni render │      samo branje      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Pripravljenost

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Skupna pripravljenost za izdajo: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Urejevalnik z odprto sejo Meet the Heavy" width="100%"><br><sub>Urejevalnik danes, z odprto Valvovo sejo »Meet the Heavy«: posnetki in zvok na časovnici, drevo seje, prvi posnetek skozi lastno kamero, liki v pozah in z obrazi iz seje.</sub></p>

Razprite področje, da vidite, kaj točno je narejeno in kaj ne. Odstotki so moja poštena ocena glede na to, kar zmore SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Iskanje in priklop SFM</b></summary>

Register Steam → `libraryfolders.vdf` → poti iz `gameinfo.txt` v vrstnem redu pogona. Šest priklopov na običajni namestitvi. Nič se ne zapiše zunaj mape programa.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Kazalo vsebine</b></summary>

70 199 datotek v 1,1 s hladno / 0,02 s iz predpomnilnika; prekrivanja med priklopi se razrešijo kot v pogonu.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modeli — `.mdl` `.vvd` `.vtx`</b></summary>

Različice 44, 48, 49. Okostje, mreže, vse ravni podrobnosti, skupine telesa. 1 500 modelov naloženih, 0 napak.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Materiali — `.vmt`</b></summary>

Vseh 19 554 priloženih materialov se prebere; `patch`, bloki DX, proxyji.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Teksture — `.vtf`</b></summary>

Različice 7.0–7.5, DXT1/3/5 in vsi nestisnjeni formati, cubemapi, mipi. DXT gre na GPU brez dekodiranja.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Seje — `.dmx`</b></summary>

Binarno 1–5 in KeyValues2. Vsaka seja in datoteka delcev iz namestitve se zapiše nazaj **bajt za bajtom** enako.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Seja na zaslonu</b></summary>

Posnetki in zvočne steze na časovnici, drevo elementov, prizor vsakega posnetka skozi njegovo kamero. Še ne: zemljevidi, delci, zvok.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animacija</b></summary>

Kanali in dnevniki ovrednoteni pri kazalcu; drsenje in predvajanje. Kosti, kamere in vidnost sledijo seji.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Obrazi</b></summary>

Flex kontrolniki, prevedena pravila in animacija oglišč — liki govorijo in kažejo čustva. Še ne: zemljevidi gub.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Rigi</b></summary>

Izrazi, omejitve point/orient/parent/aim, dvokostni IK. Še ne: celoten graf odvisnosti operatorjev, ustvarjanje rigov.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Urejanje</b></summary>

Izbira s klikom, manipulator za premik/vrtenje, inšpektor za vsak atribut, ključ pri kazalcu, razveljavi/ponovi, bajtno natančno shranjevanje. Še ne: urejevalnik grafov.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Časovna izbira s hold in falloff na ravnilu; sprememba se razporedi čez njo kot v SFM. Še ne: prednastavitve, plasti.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Sidranje plošč</b></summary>

Vlečenje plošč na kompas ciljev s predogledom, kot v UE5 in Visual Studiu. Še ne: shranjene postavitve, teme.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Senčenje Source</b></summary>

Samo tekstura in preprosta luč. Še ne: phong, rim, lightwarp, luči prizora, sence.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Zemljevidi — `.bsp`</b></summary>

Ni začeto.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Upodabljanje v sliko in video</b></summary>

Ni začeto.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Vtičniki `.c2plg`</b></summary>

Ni začeto.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Teme in delovni prostori</b></summary>

Namerno pozneje: en videz, dokler urejevalnik nima česa oblikovati.

</details>

**Ni pripravljen za izdajo.** Temelj — vsak format datotek, ki ga SFM uporablja, pravilno prebran in preverjen na celotni namestitvi — stoji in je testiran; sejo je mogoče odpreti, predvajati, spremeniti in shraniti. Manjka *udobje* dela: urejevalnik grafov, senčenje Source, zemljevidi, izvoz. Brez številke različice, dokler animator v njem ne more opraviti dneva dela.

## Po čem se razlikuje

- **Prenosljiv.** Nič se ne zapiše zunaj mape programa: nastavitve v `App/User`, predpomnilnik v `App/Cache`, začasno v `App/Temporary`. Izbrišite mapo in ni sledu.
- **Nikoli ne zažene SFM.** Ni procesa za krmiljenje, ni oken za prevzem. Namestitev se bere kot paket vsebine.
- **Formati preverjeni, ne predpostavljeni.** Vsak bralnik je bil preverjen na pravi namestitvi; kjer format naredi kaj presenetljivega, koda to pove.
- **Shranjevanje je natančno.** Seja, prebrana in zapisana nespremenjena, je ista datoteka.
- **Pogon nima odvisnosti.** `Core/` in vsi testi tečejo na golem Pythonu; le okno potrebuje Qt in OpenGL.

## Zagon

Potrebuje Windows, Python 3.13 in nameščen Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Ob prvem zagonu se SFM poišče prek Steama; če ga ne najde, program vpraša. <kbd>Ctrl</kbd>+<kbd>O</kbd> odpre sejo, <kbd>Preslednica</kbd> predvaja, <kbd>C</kbd> pogleda skozi kamero posnetka, <kbd>T</kbd>/<kbd>R</kbd> premik/vrtenje, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> razveljavi, <kbd>Ctrl</kbd>+<kbd>S</kbd> shrani. Plošče se vlečejo za naslov. Testi ne potrebujejo ničesar:

```bash
python Testing/run.py
```

## Zgradba

```
C2UI_SDK/
├── c2ui.py            zaganjalnik
├── Core/              pogon: formati, navidezni datotečni sistem, kazalo, mostovi
├── App/               urejevalnik: knjižnica vsebine, upodabljalnik, okno
├── Tools/             lokalizacija, orodja UI, vtičniki (pozneje)
├── Testing/           testi, bajtno natančne fiksture, en zaganjalnik
└── GIT&DOCK/README/   ta README v drugih jezikih
```

## Načrt

1. **Urejevalnik grafov** — krivulje in ključi na očeh.
2. **Senčenje Source** — VertexLitGeneric, kot ga riše SFM: phong, rim, lightwarp, luči prizora.
3. **Zemljevidi** — `.bsp` za ozadje.
4. **Izvoz** — slika in video.
5. **Vtičniki** — format `.c2plg`; nato teme in delovni prostori.

## Licenca in zasluge

Source Filmmaker, Team Fortress 2 in pogon Source so Valvovi. Projekt bere njihove formate datotek, ne prilaga nobene njihove datoteke in deluje le z vašo kopijo SFM iz Steama.

Licenca za lastno kodo C2UI še ni izbrana — do takrat so vse pravice pridržane. Issues in pull requesti so kljub temu dobrodošli.

<p align="center"><img src="../../.github/assets/models.png" alt="64 modelov, upodobljenih naravnost iz namestitve" width="60%"><br><sub>Štiriinšestdeset naključnih modelov iz namestitve, ki jih je narisal lastni upodabljalnik C2UI.</sub></p>
