<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <b>🇲🇩 Moldovenească</b> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/stare-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/teste-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — este reconstrucția mea a editorului Source Filmmaker: același conținut, același format de sesiune, același model de date — într-o coajă care își ia aspectul de la biblioteca Steam și aranjarea de la editorul Unreal Engine 5.</p>

---

## Ideea

Source Filmmaker este un instrument excelent într-o interfață din 2012. Nu vreau un skin peste `sfm.exe` și nu vreau să-i capturez ferestrele una câte una. Vreau un editor care **întreabă unde este instalat SFM**, montează acea instalare așa cum Garry's Mod montează Counter-Strike și face totul singur peste acele fișiere — modele, materiale, texturi, sesiuni, animație — fără să pornească vreodată SFM.

Ținta este **paritate de funcții cu SFM, unu la unu** (inclusiv oase și rig-uri), apoi lucrurile pe care SFM nu le-a avut niciodată.

```
  ┌──────────────┐    "unde e SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI propriu  │ ◀─────  montat   ───────│    tf/  hl2/  tf_movies/ …   │
  │  render prop. │      doar citire      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Grad de pregătire

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Pregătire generală pentru lansare: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Editorul cu Meet the Heavy deschis" width="100%"><br><sub>Editorul azi, cu sesiunea Valve „Meet the Heavy” deschisă: cadre și sunet pe cronologie, arborele sesiunii, primul cadru văzut prin propria cameră, personaje în pozele și cu fețele din sesiune.</sub></p>

Deschideți o zonă ca să vedeți exact ce este gata și ce nu. Procentele sunt estimarea mea sinceră față de ce poate SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Găsirea și montarea SFM</b></summary>

Registrul Steam → `libraryfolders.vdf` → căile din `gameinfo.txt` în ordinea motorului. Șase montări pe o instalare standard. Nimic nu se scrie în afara folderului aplicației.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Index de conținut</b></summary>

70 199 fișiere în 1,1 s la rece / 0,02 s din cache; suprascrierile între montări sunt rezolvate exact ca în motor.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modele — `.mdl` `.vvd` `.vtx`</b></summary>

Versiunile 44, 48, 49. Schelet, mesh-uri, toate nivelurile de detaliu, grupuri de corp. 1 500 de modele încărcate, 0 eșecuri.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Materiale — `.vmt`</b></summary>

Toate cele 19 554 de materiale livrate se citesc; `patch`, blocuri DX, proxy-uri.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Texturi — `.vtf`</b></summary>

Versiunile 7.0–7.5, DXT1/3/5 și toate formatele necomprimate, cubemap-uri, mip-uri. DXT merge pe GPU fără decodare.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Sesiuni — `.dmx`</b></summary>

Binar 1–5 și KeyValues2. Fiecare sesiune și fișier de particule din instalare se rescrie **octet cu octet** identic.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Sesiunea pe ecran</b></summary>

Cadre și piste de sunet pe cronologie, arborele elementelor, scena fiecărui cadru prin camera sa. Încă nu: hărți, particule, sunet.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animație</b></summary>

Canale și loguri evaluate la cursor; derulare și redare. Oasele, camerele și vizibilitatea urmează sesiunea.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Fețe</b></summary>

Controlere flex, regulile compilate și animația de vârfuri — personajele vorbesc și au expresii. Încă nu: hărți de riduri.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Rig-uri</b></summary>

Expresii, constrângeri point/orient/parent/aim, IK cu două oase. Încă nu: graful complet al operatorilor, crearea de rig-uri.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Editare</b></summary>

Selectare prin clic, manipulator de mutare/rotire, inspector pentru orice atribut, cheie la cursor, anulare/refacere, salvare exactă la octet. Încă nu: editorul de grafice.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Selecție de timp cu hold și falloff pe riglă; o modificare se întinde peste ea ca în SFM. Încă nu: presetări, straturi.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Andocarea panourilor</b></summary>

Trageți panourile pe o busolă de ținte cu previzualizare, ca în UE5 și Visual Studio. Încă nu: aranjări salvate, teme.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Umbrire Source</b></summary>

Doar textură și o lumină simplă. Încă nu: phong, rim, lightwarp, lumini de scenă, umbre.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Hărți — `.bsp`</b></summary>

Neînceput.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Randare în imagine și video</b></summary>

Neînceput.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Plugin-uri `.c2plg`</b></summary>

Neînceput.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Teme și spații de lucru</b></summary>

Amânat intenționat: un singur aspect până când editorul are ce stiliza.

</details>

**Nu este gata de lansare.** Fundația — fiecare format de fișier folosit de SFM, citit corect și verificat pe întreaga instalare — există și este testată; o sesiune poate fi deschisă, redată, modificată și salvată. Lipsește *confortul* lucrului: editorul de grafice, umbrirea Source, hărțile, exportul. Fără număr de versiune până când un animator poate lucra o zi întreagă în el.

## Prin ce diferă

- **Portabil.** Nimic nu se scrie în afara folderului aplicației: setări în `App/User`, cache în `App/Cache`, temporare în `App/Temporary`. Ștergeți folderul și nu rămâne nimic.
- **Nu pornește niciodată SFM.** Niciun proces de condus, nicio fereastră de capturat. Instalarea se citește ca un pachet de conținut.
- **Formate verificate, nu presupuse.** Fiecare cititor a fost verificat pe instalarea reală; unde un format face ceva surprinzător, codul o spune.
- **Salvarea este exactă.** O sesiune citită și scrisă nemodificată este același fișier.
- **Motorul nu are dependențe.** `Core/` și toate testele rulează pe Python simplu; doar fereastra are nevoie de Qt și OpenGL.

## Rulare

Necesită Windows, Python 3.13 și o instalare Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

La prima pornire SFM este căutat prin Steam; dacă nu este găsit, programul întreabă. <kbd>Ctrl</kbd>+<kbd>O</kbd> deschide o sesiune, <kbd>Space</kbd> redă, <kbd>C</kbd> privește prin camera cadrului, <kbd>T</kbd>/<kbd>R</kbd> mută/rotește, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> anulează, <kbd>Ctrl</kbd>+<kbd>S</kbd> salvează. Panourile se trag de titlu. Testele nu au nevoie de nimic:

```bash
python Testing/run.py
```

## Structură

```
C2UI_SDK/
├── c2ui.py            lansatorul
├── Core/              motor: formate, sistem de fișiere virtual, index, punți
├── App/               editorul: biblioteca de conținut, renderer, fereastră
├── Tools/             localizare, unelte UI, plugin-uri (mai târziu)
├── Testing/           teste, fixture-uri exacte la octet, un singur runner
└── GIT&DOCK/README/   acest README în alte limbi
```

## Plan

1. **Editor de grafice** — curbe și chei, văzute.
2. **Umbrire Source** — VertexLitGeneric așa cum îl desenează SFM: phong, rim, lightwarp, lumini de scenă.
3. **Hărți** — `.bsp` pentru fundal.
4. **Export** — imagine și video.
5. **Plugin-uri** — formatul `.c2plg`; apoi teme și spații de lucru.

## Licență și mulțumiri

Source Filmmaker, Team Fortress 2 și motorul Source aparțin Valve. Proiectul citește formatele lor de fișiere, nu livrează niciun fișier de-al lor și funcționează doar cu copia de SFM pe care o aveți deja prin Steam.

Licența pentru codul propriu C2UI nu a fost încă aleasă — până atunci, toate drepturile rezervate. Issues și pull requests sunt binevenite.

<p align="center"><img src="../../.github/assets/models.png" alt="64 de modele randate direct din instalare" width="60%"><br><sub>Șaizeci și patru de modele alese la întâmplare din instalare, desenate de renderer-ul propriu al C2UI.</sub></p>
