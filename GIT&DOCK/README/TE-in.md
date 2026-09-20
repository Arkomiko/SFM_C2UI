<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <b>🇮🇳 తెలుగు</b> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E0%B0%B8%E0%B1%8D%E0%B0%A5%E0%B0%BF%E0%B0%A4%E0%B0%BF-%E0%B0%AA%E0%B1%8D%E0%B0%B0%E0%B1%80--%E0%B0%86%E0%B0%B2%E0%B1%8D%E0%B0%AB%E0%B0%BE-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E0%B0%AA%E0%B0%B0%E0%B1%80%E0%B0%95%E0%B1%8D%E0%B0%B7%E0%B0%B2%E0%B1%81-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — Source Filmmaker ఎడిటర్‌ను నేను తిరిగి నిర్మించినది: అదే కంటెంట్, అదే సెషన్ ఫార్మాట్, అదే డేటా మోడల్ — Steam లైబ్రరీ నుండి రూపాన్ని, Unreal Engine 5 ఎడిటర్ నుండి లేఅవుట్‌ను తీసుకున్న షెల్‌లో.</p>

---

## ఆలోచన

Source Filmmaker 2012 ఇంటర్‌ఫేస్‌లో ఉన్న గొప్ప సాధనం. నేను `sfm.exe` మీద స్కిన్ వేయాలనుకోను, దాని విండోలను ఒక్కొక్కటిగా స్వాధీనం చేసుకోవాలనుకోను. **SFM ఎక్కడ ఇన్‌స్టాల్ అయిందో అడిగే**, Garry's Mod Counter-Strike ను మౌంట్ చేసినట్లు ఆ ఇన్‌స్టాలేషన్‌ను మౌంట్ చేసే, ఆ ఫైళ్ల మీద అన్నీ స్వయంగా చేసే — మోడల్స్, మెటీరియల్స్, టెక్స్చర్లు, సెషన్లు, యానిమేషన్ — SFM ను ఎప్పుడూ ప్రారంభించని ఎడిటర్ నాకు కావాలి.

లక్ష్యం **SFM తో ఒకటికి ఒకటి ఫీచర్ సమానత్వం** (ఎముకలు, రిగ్‌లతో సహా), తర్వాత SFM కి ఎప్పుడూ లేనివి.

```
  ┌──────────────┐    "SFM ఎక్కడ?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  సొంత UI     │ ◀─────   మౌంట్    ───────│    tf/  hl2/  tf_movies/ …   │
  │  సొంత రెండర్  │      చదవడం మాత్రమే      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## సిద్ధత

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>విడుదలకు మొత్తం సిద్ధత: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy తెరిచిన ఎడిటర్" width="100%"><br><sub>నేటి ఎడిటర్, Valve యొక్క Meet the Heavy తెరిచి: టైమ్‌లైన్‌లో షాట్లు మరియు ధ్వని, సెషన్ ట్రీ, మొదటి షాట్ దాని సొంత కెమెరా ద్వారా, సెషన్ ప్రకారం భంగిమలు మరియు ముఖాలతో పాత్రలు.</sub></p>

ఏమి పూర్తయింది, ఏమి కాలేదు చూడటానికి ఒక విభాగాన్ని విస్తరించండి. శాతాలు SFM చేయగలిగినదానికి వ్యతిరేకంగా నా నిజాయితీ అంచనా.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM ను కనుగొని మౌంట్ చేయడం</b></summary>

Steam రిజిస్ట్రీ → `libraryfolders.vdf` → `gameinfo.txt` శోధన మార్గాలు, ఇంజిన్ క్రమంలో. ప్రామాణిక ఇన్‌స్టాల్‌లో ఆరు మౌంట్లు. అప్లికేషన్ ఫోల్డర్ వెలుపల ఏమీ రాయబడదు.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>కంటెంట్ ఇండెక్స్</b></summary>

70 199 ఫైళ్లు 1.1 సె కోల్డ్ / 0.02 సె క్యాష్ నుండి; మౌంట్ల మధ్య ఓవర్‌రైడ్‌లు ఇంజిన్ లాగానే పరిష్కరించబడతాయి.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>మోడల్స్ — <code></code> <code></code> <code></code></b></summary>

వెర్షన్లు 44, 48, 49. అస్థిపంజరం, మెష్‌లు, అన్ని వివరాల స్థాయిలు, బాడీ గ్రూపులు. 1 500 మోడల్స్ లోడ్, 0 వైఫల్యాలు.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>మెటీరియల్స్ — <code></code></b></summary>

అన్ని 19 554 మెటీరియల్స్ చదవబడతాయి; `patch`, DX బ్లాక్‌లు, ప్రాక్సీలు.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>టెక్స్చర్లు — <code></code></b></summary>

వెర్షన్లు 7.0–7.5, DXT1/3/5 మరియు అన్ని అన్‌కంప్రెస్డ్ ఫార్మాట్లు, క్యూబ్‌మ్యాప్‌లు, మిప్‌లు. DXT డీకోడ్ లేకుండా GPU కి వెళ్తుంది.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>సెషన్లు — <code></code></b></summary>

బైనరీ 1–5 మరియు KeyValues2. ఇన్‌స్టాల్‌లోని ప్రతి సెషన్ మరియు పార్టికల్ ఫైల్ **బైట్ బై బైట్** తిరిగి రాయబడుతుంది.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>తెరపై సెషన్</b></summary>

టైమ్‌లైన్‌లో షాట్లు మరియు సౌండ్ ట్రాక్‌లు, ఎలిమెంట్ ట్రీ, ప్రతి షాట్ దృశ్యం దాని కెమెరా ద్వారా. ఇంకా లేదు: మ్యాప్‌లు, పార్టికల్స్, ధ్వని.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>యానిమేషన్</b></summary>

కర్సర్ వద్ద ఛానెల్‌లు మరియు లాగ్‌లు మూల్యాంకనం; స్క్రబ్ మరియు ప్లే. ఎముకలు, కెమెరాలు మరియు దృశ్యమానత సెషన్‌ను అనుసరిస్తాయి.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>ముఖాలు</b></summary>

Flex కంట్రోలర్లు, కంపైల్ చేసిన నియమాలు మరియు వర్టెక్స్ యానిమేషన్ — పాత్రలు మాట్లాడతాయి, భావాలు చూపిస్తాయి. ఇంకా లేదు: రింకిల్ మ్యాప్‌లు.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>రిగ్‌లు</b></summary>

ఎక్స్‌ప్రెషన్లు, point/orient/parent/aim కన్‌స్ట్రెయింట్లు, రెండు-ఎముకల IK. ఇంకా లేదు: పూర్తి ఆపరేటర్ డిపెండెన్సీ గ్రాఫ్, రిగ్ సృష్టి.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>ఎడిటింగ్</b></summary>

క్లిక్ ఎంపిక, మూవ్/రొటేట్ మానిప్యులేటర్, ఏ అట్రిబ్యూట్‌కైనా ఇన్‌స్పెక్టర్, కర్సర్ వద్ద కీ, అన్‌డు/రీడు, బైట్-ఖచ్చిత సేవ్. ఇంకా లేదు: గ్రాఫ్ ఎడిటర్.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>మోషన్ ఎడిటర్</b></summary>

రూలర్‌పై హోల్డ్ మరియు ఫాల్ఆఫ్‌తో సమయ ఎంపిక; ఎడిట్ SFM లాగా దానిపై వ్యాపిస్తుంది. ఇంకా లేదు: ప్రీసెట్లు, లేయర్లు.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>ప్యానెల్ డాకింగ్</b></summary>

UE5 మరియు Visual Studio లాగా, ప్రివ్యూతో లక్ష్యాల కంపాస్‌పై ప్యానెల్‌లను లాగండి. ఇంకా లేదు: సేవ్ చేసిన లేఅవుట్లు, థీమ్‌లు.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source షేడింగ్</b></summary>

టెక్స్చర్ మరియు సాధారణ కాంతి మాత్రమే. ఇంకా లేదు: phong, rim, lightwarp, సీన్ లైట్లు, నీడలు.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>మ్యాప్‌లు — <code></code></b></summary>

ప్రారంభించలేదు.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>చిత్రం మరియు వీడియోకు రెండర్</b></summary>

ప్రారంభించలేదు.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>ప్లగిన్‌లు <code></code></b></summary>

ప్రారంభించలేదు.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>థీమ్‌లు మరియు వర్క్‌స్పేస్‌లు</b></summary>

ఉద్దేశపూర్వకంగా తర్వాత: ఎడిటర్‌లో అలంకరించడానికి విలువైనది వచ్చే వరకు ఒకే రూపం.

</details>

**విడుదలకు సిద్ధంగా లేదు.** పునాది — SFM ఉపయోగించే ప్రతి ఫైల్ ఫార్మాట్, సరిగ్గా చదివి పూర్తి ఇన్‌స్టాలేషన్‌పై ధృవీకరించినది — ఉంది మరియు పరీక్షించబడింది; సెషన్ తెరవగలరు, ప్లే చేయగలరు, మార్చగలరు, సేవ్ చేయగలరు. లోపించినది పని *సౌకర్యం*: గ్రాఫ్ ఎడిటర్, Source షేడింగ్, మ్యాప్‌లు, ఎగుమతి. యానిమేటర్ ఇందులో ఒక రోజు పని చేయగలిగే వరకు వెర్షన్ నంబర్ లేదు.

## ఏది భిన్నం

- **పోర్టబుల్.** అప్లికేషన్ ఫోల్డర్ వెలుపల ఏమీ రాయబడదు: సెట్టింగ్‌లు `App/User`, క్యాష్ `App/Cache`, తాత్కాలికం `App/Temporary`. ఫోల్డర్ తొలగించండి, ఆనవాళ్లు లేవు.
- **SFM ను ఎప్పుడూ నడపదు.** నడిపించే ప్రాసెస్ లేదు, స్వాధీనం చేసుకునే విండోలు లేవు. ఇన్‌స్టాలేషన్ కంటెంట్ ప్యాక్ లాగా చదవబడుతుంది.
- **ఫార్మాట్లు ధృవీకరించబడ్డాయి, ఊహించలేదు.** ప్రతి రీడర్ నిజమైన ఇన్‌స్టాలేషన్‌తో తనిఖీ చేయబడింది; ఫార్మాట్ ఆశ్చర్యకరమైనది చేస్తే, కోడ్ చెబుతుంది.
- **సేవ్ ఖచ్చితం.** మార్పు లేకుండా చదివి రాసిన సెషన్ అదే ఫైల్.
- **ఇంజిన్‌కు డిపెండెన్సీలు లేవు.** `Core/` మరియు మొత్తం టెస్ట్ సూట్ స్వచ్ఛమైన Python పై నడుస్తాయి; విండోకు మాత్రమే Qt మరియు OpenGL కావాలి.

## నడపడం

Windows, Python 3.13 మరియు Source Filmmaker ఇన్‌స్టాలేషన్ అవసరం.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

మొదటి ప్రారంభంలో Steam ద్వారా SFM ను వెతుకుతుంది; దొరకకపోతే అడుగుతుంది. <kbd>Ctrl</kbd>+<kbd>O</kbd> సెషన్ తెరుస్తుంది, <kbd>Space</kbd> ప్లే, <kbd>C</kbd> షాట్ కెమెరా, <kbd>T</kbd>/<kbd>R</kbd> మూవ్/రొటేట్, <kbd>M</kbd> మోషన్ ఎడిటర్, <kbd>Ctrl</kbd>+<kbd>Z</kbd> అన్‌డు, <kbd>Ctrl</kbd>+<kbd>S</kbd> సేవ్. ప్యానెల్‌లు శీర్షిక ద్వారా లాగబడతాయి. పరీక్షలకు ఏమీ అవసరం లేదు:

```bash
python Testing/run.py
```

## నిర్మాణం

```
C2UI_SDK/
├── c2ui.py            లాంచర్
├── Core/              ఇంజిన్: ఫార్మాట్లు, వర్చువల్ ఫైల్ సిస్టమ్, ఇండెక్స్, బ్రిడ్జ్‌లు
├── App/               ఎడిటర్: కంటెంట్ లైబ్రరీ, రెండరర్, విండో
├── Tools/             స్థానికీకరణ, UI టూల్స్, ప్లగిన్‌లు (తర్వాత)
├── Testing/           పరీక్షలు, బైట్-ఖచ్చిత ఫిక్స్చర్లు, ఒక రన్నర్
└── GIT&DOCK/README/   ఈ README ఇతర భాషల్లో
```

## రోడ్‌మ్యాప్

1. **గ్రాఫ్ ఎడిటర్** — వక్రాలు మరియు కీలు, కంటికి.
2. **Source షేడింగ్** — SFM గీసినట్లు VertexLitGeneric: phong, rim, lightwarp, సీన్ లైట్లు.
3. **మ్యాప్‌లు** — నేపథ్యాల కోసం `.bsp`.
4. **అవుట్‌పుట్** — చిత్రం మరియు వీడియో ఎగుమతి.
5. **ప్లగిన్‌లు** — `.c2plg` ఫార్మాట్; తర్వాత థీమ్‌లు మరియు వర్క్‌స్పేస్‌లు.

## లైసెన్స్ మరియు కృతజ్ఞతలు

Source Filmmaker, Team Fortress 2 మరియు Source ఇంజిన్ Valve కు చెందినవి. ఈ ప్రాజెక్ట్ వారి ఫైల్ ఫార్మాట్లను చదువుతుంది, వారి ఫైళ్లను చేర్చదు, Steam ద్వారా మీకు ఇప్పటికే ఉన్న SFM కాపీతో మాత్రమే పనిచేస్తుంది.

C2UI సొంత కోడ్ లైసెన్స్ ఇంకా ఎంచుకోలేదు — అప్పటివరకు అన్ని హక్కులు రిజర్వ్. Issues మరియు pull requests స్వాగతం.

<p align="center"><img src="../../.github/assets/models.png" alt="ఇన్‌స్టాలేషన్ నుండి నేరుగా రెండర్ చేసిన 64 మోడల్స్" width="60%"><br><sub>ఇన్‌స్టాలేషన్ నుండి యాదృచ్ఛికంగా ఎంచుకున్న అరవై నాలుగు మోడల్స్, C2UI సొంత రెండరర్‌తో గీసినవి.</sub></p>
