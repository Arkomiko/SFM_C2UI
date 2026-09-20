<p align="center"><img src="../assets/SL-si/banner.png" alt="C2UI" width="100%"></p>

<details align="center"><summary>&nbsp;🌐 <b>🇸🇮 Slovenščina</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../../README.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><b>🇸🇮<br>Slovenščina</b></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/stanje-pred--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/testov-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — urejevalnik Source Filmmaker v sodobni lupini: ista vsebina, isti format seje, isti podatkovni model, vmesnik v duhu knjižnice Steam in urejevalnika Unreal Engine 5.</p>

---

## Pripravljenost

<p align="center"><img src="../assets/SL-si/sidebar.svg" alt="Pripravljenost" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Skupna pripravljenost za izdajo: 41%</b></p>

<p align="center"><a href="../assets/SL-si/sidebar.md"><img alt="Pripravljenost podrobno" src="https://img.shields.io/badge/Pripravljenost_podrobno-66c0f4?style=for-the-badge"></a></p>

## Zamisel

Source Filmmaker je močno orodje, katerega vmesnik je ostal v letu 2012. C2UI ga ne nadomešča in ne predeluje: cilj je preprosto narediti SFM malo sodobnejši in udobnejši.

Urejevalnik najde nameščeni SFM, ga priključi kot knjižnico vsebine — modeli, materiali, teksture, seje — in dela z istimi datotekami v istem formatu. Vse, kar je nastalo v SFM, se odpre v C2UI, in obratno.

Prvi cilj je polna združljivost s SFM, vključno s kostmi in rigi. Potem tisto, česar je SFM manjkalo.

```
  ┌──────────────┐    "kje je SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  lastni UI   │ ◀─────  priklop  ───────│    tf/  hl2/  tf_movies/ …   │
  │  lastni render │      samo branje      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Urejevalnik z odprto sejo Meet the Heavy" width="100%"><br><sub>Urejevalnik danes, z odprto Valvovo sejo »Meet the Heavy«: posnetki in zvok na časovnici, drevo seje, prvi posnetek skozi lastno kamero, liki v pozah in z obrazi iz seje.</sub></p>

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
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Ob prvem zagonu se SFM poišče prek Steama; če ga ne najde, program vpraša. <kbd>Ctrl</kbd>+<kbd>O</kbd> odpre sejo, <kbd>Preslednica</kbd> predvaja, <kbd>C</kbd> pogleda skozi kamero posnetka, <kbd>T</kbd>/<kbd>R</kbd> premik/vrtenje, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> razveljavi, <kbd>Ctrl</kbd>+<kbd>S</kbd> shrani. Plošče se vlečejo za naslov. Testi ne potrebujejo ničesar:

```bash
python Testing/run.py
```

## Zgradba

```
C2UI_SDK/
├── README.md
├── Core/              pogon: formati, navidezni datotečni sistem, kazalo, mostovi
├── App/               urejevalnik: knjižnica vsebine, upodabljalnik, okno
├── Tools/             lokalizacija, orodja UI, vtičniki (pozneje)
│   └── Launcher/      zaganjalnik
├── Testing/           testi, bajtno natančne fiksture, en zaganjalnik
└── GIT&DOCK/          ta README v drugih jezikih
```

## Načrt

1. **Senčenje Source** — VertexLitGeneric, kot ga riše SFM: phong, rim, lightwarp, luči prizora.
2. **Zemljevidi** — `.bsp` za ozadje.
3. **Izvoz** — slika in video.
4. **Vtičniki** — format `.c2plg`; nato teme in delovni prostori.

## Licenca in zasluge

Lastna koda C2UI je pod **licenco C2UI**: prosto za osebno in nekomercialno rabo; komercialna raba le s pisnim soglasjem avtorja; spremenjene različice morajo navesti izvirni projekt in njegovega avtorja Arkomiko. Vtičniki in dodatki so pod licenco **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 in pogon Source so Valvovi; projekt bere njihove formate, ne vsebuje njihovih datotek in deluje le z vašo kopijo SFM iz Steama.

<p align="center"><a href="../LICENSE/SL-si.md"><img alt="Besedilo licence" src="https://img.shields.io/badge/Besedilo_licence-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 modelov, upodobljenih naravnost iz namestitve" width="60%"><br><sub>Štiriinšestdeset naključnih modelov iz namestitve, ki jih je narisal lastni upodabljalnik C2UI.</sub></p>
