<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <b>🇮🇳 தமிழ்</b> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E0%AE%A8%E0%AE%BF%E0%AE%B2%E0%AF%88-%E0%AE%AE%E0%AF%81%E0%AE%A9%E0%AF%8D--%E0%AE%86%E0%AE%B2%E0%AF%8D%E0%AE%AA%E0%AE%BE-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E0%AE%9A%E0%AF%8B%E0%AE%A4%E0%AE%A9%E0%AF%88%E0%AE%95%E0%AE%B3%E0%AF%8D-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — Source Filmmaker எடிட்டரை நான் மீண்டும் கட்டமைத்தது: அதே உள்ளடக்கம், அதே அமர்வு வடிவம், அதே தரவு மாதிரி — Steam நூலகத்திடமிருந்து தோற்றத்தையும், Unreal Engine 5 எடிட்டரிடமிருந்து அமைப்பையும் பெற்ற ஓட்டில்.</p>

---

## யோசனை

Source Filmmaker 2012 இடைமுகத்தில் உள்ள சிறந்த கருவி. நான் `sfm.exe` மேல் தோல் போட விரும்பவில்லை, அதன் சாளரங்களை ஒவ்வொன்றாக கைப்பற்றவும் விரும்பவில்லை. **SFM எங்கே நிறுவப்பட்டுள்ளது என்று கேட்கும்**, Garry's Mod Counter-Strike ஐ ஏற்றுவது போல அந்த நிறுவலை ஏற்றும், அந்தக் கோப்புகளின் மேல் எல்லாவற்றையும் தானே செய்யும் — மாதிரிகள், பொருட்கள், அமைப்புகள், அமர்வுகள், அனிமேஷன் — SFM ஐ ஒருபோதும் தொடங்காத எடிட்டர் எனக்கு வேண்டும்.

இலக்கு **SFM உடன் ஒன்றுக்கு ஒன்று அம்ச சமநிலை** (எலும்புகள் மற்றும் ரிக்குகள் உட்பட), பின்னர் SFM ஒருபோதும் பெறாதவை.

```
  ┌──────────────┐    "SFM எங்கே?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  சொந்த UI     │ ◀─────   ஏற்றம்    ───────│    tf/  hl2/  tf_movies/ …   │
  │  சொந்த ரெண்டர்  │      படிக்க மட்டும்      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## தயார்நிலை

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>வெளியீட்டுக்கான மொத்த தயார்நிலை: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy திறந்த எடிட்டர்" width="100%"><br><sub>இன்றைய எடிட்டர், Valve இன் Meet the Heavy திறந்து: காலக்கோட்டில் ஷாட்கள் மற்றும் ஒலி, அமர்வு மரம், முதல் ஷாட் அதன் சொந்த கேமரா வழியாக, அமர்வின்படி நிலை மற்றும் முகங்களுடன் கதாபாத்திரங்கள்.</sub></p>

என்ன முடிந்தது, என்ன முடியவில்லை என்பதைப் பார்க்க ஒரு பகுதியை விரிக்கவும். சதவீதங்கள் SFM செய்யக்கூடியதற்கு எதிராக எனது நேர்மையான மதிப்பீடு.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM ஐக் கண்டறிந்து ஏற்றுதல்</b></summary>

Steam பதிவகம் → `libraryfolders.vdf` → `gameinfo.txt` தேடல் பாதைகள், எஞ்சின் வரிசையில். நிலையான நிறுவலில் ஆறு ஏற்றங்கள். பயன்பாட்டு கோப்புறைக்கு வெளியே எதுவும் எழுதப்படாது.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>உள்ளடக்க அட்டவணை</b></summary>

70 199 கோப்புகள் 1.1 வி குளிர் / 0.02 வி கேஷிலிருந்து; ஏற்றங்களுக்கு இடையிலான மேலெழுதல்கள் எஞ்சின் போலவே தீர்க்கப்படுகின்றன.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>மாதிரிகள் — <code></code> <code></code> <code></code></b></summary>

பதிப்புகள் 44, 48, 49. எலும்புக்கூடு, மெஷ்கள், எல்லா விவர நிலைகள், உடல் குழுக்கள். 1 500 மாதிரிகள் ஏற்றப்பட்டன, 0 தோல்விகள்.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>பொருட்கள் — <code></code></b></summary>

எல்லா 19 554 பொருட்களும் படிக்கப்படுகின்றன; `patch`, DX தொகுதிகள், ப்ராக்ஸிகள்.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>அமைப்புகள் — <code></code></b></summary>

பதிப்புகள் 7.0–7.5, DXT1/3/5 மற்றும் எல்லா அழுத்தப்படாத வடிவங்கள், கியூப்மேப்கள், மிப்கள். DXT டிகோட் இல்லாமல் GPU க்கு செல்கிறது.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>அமர்வுகள் — <code></code></b></summary>

பைனரி 1–5 மற்றும் KeyValues2. நிறுவலின் ஒவ்வொரு அமர்வும் துகள் கோப்பும் **பைட் பைட்டாக** திரும்ப எழுதப்படுகிறது.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>திரையில் அமர்வு</b></summary>

காலக்கோட்டில் ஷாட்கள் மற்றும் ஒலி தடங்கள், உறுப்பு மரம், ஒவ்வொரு ஷாட்டின் காட்சி அதன் கேமரா வழியாக. இன்னும் இல்லை: வரைபடங்கள், துகள்கள், ஒலி.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>அனிமேஷன்</b></summary>

கர்சரில் சேனல்கள் மற்றும் பதிவுகள் மதிப்பிடப்படுகின்றன; ஸ்க்ரப் மற்றும் ப்ளே. எலும்புகள், கேமராக்கள், தெரிவுநிலை அமர்வைப் பின்பற்றுகின்றன.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>முகங்கள்</b></summary>

Flex கட்டுப்படுத்திகள், தொகுக்கப்பட்ட விதிகள் மற்றும் வெர்டெக்ஸ் அனிமேஷன் — கதாபாத்திரங்கள் பேசுகின்றன, உணர்ச்சிகளைக் காட்டுகின்றன. இன்னும் இல்லை: சுருக்க வரைபடங்கள்.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>ரிக்குகள்</b></summary>

வெளிப்பாடுகள், point/orient/parent/aim கட்டுப்பாடுகள், இரு-எலும்பு IK. இன்னும் இல்லை: முழு ஆபரேட்டர் சார்பு வரைபடம், ரிக் உருவாக்கம்.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>திருத்தம்</b></summary>

கிளிக் தேர்வு, நகர்த்து/சுழற்று மானிபுலேட்டர், எந்த பண்புக்கும் இன்ஸ்பெக்டர், கர்சரில் கீ, செயல்தவிர்/மீண்டும், பைட்-துல்லிய சேமிப்பு. இன்னும் இல்லை: கிராஃப் எடிட்டர்.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>மோஷன் எடிட்டர்</b></summary>

ரூலரில் ஹோல்ட் மற்றும் ஃபால்ஆஃப் உடன் நேர தேர்வு; திருத்தம் SFM போல அதன் மேல் பரவுகிறது. இன்னும் இல்லை: முன்னமைவுகள், அடுக்குகள்.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>பேனல் டாக்கிங்</b></summary>

UE5 மற்றும் Visual Studio போல, முன்னோட்டத்துடன் இலக்குகளின் திசைகாட்டியில் பேனல்களை இழுக்கவும். இன்னும் இல்லை: சேமித்த அமைப்புகள், தீம்கள்.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source ஷேடிங்</b></summary>

அமைப்பு மற்றும் எளிய ஒளி மட்டும். இன்னும் இல்லை: phong, rim, lightwarp, காட்சி ஒளிகள், நிழல்கள்.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>வரைபடங்கள் — <code></code></b></summary>

தொடங்கவில்லை.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>படம் மற்றும் வீடியோவாக ரெண்டர்</b></summary>

தொடங்கவில்லை.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>செருகுநிரல்கள் <code></code></b></summary>

தொடங்கவில்லை.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>தீம்கள் மற்றும் பணியிடங்கள்</b></summary>

வேண்டுமென்றே பின்னர்: எடிட்டரில் அலங்கரிக்கத் தகுந்தது வரும் வரை ஒரே தோற்றம்.

</details>

**வெளியீட்டுக்கு தயாராக இல்லை.** அடித்தளம் — SFM பயன்படுத்தும் ஒவ்வொரு கோப்பு வடிவமும், சரியாகப் படித்து முழு நிறுவலிலும் சரிபார்க்கப்பட்டது — உள்ளது மற்றும் சோதிக்கப்பட்டது; அமர்வைத் திறக்க, இயக்க, மாற்ற, சேமிக்க முடியும். இல்லாதது வேலையின் *வசதி*: கிராஃப் எடிட்டர், Source ஷேடிங், வரைபடங்கள், ஏற்றுமதி. ஒரு அனிமேட்டர் இதில் ஒரு நாள் வேலை செய்ய முடியும் வரை பதிப்பு எண் இல்லை.

## என்ன வேறுபாடு

- **கையடக்கம்.** பயன்பாட்டு கோப்புறைக்கு வெளியே எதுவும் எழுதப்படாது: அமைப்புகள் `App/User`, கேஷ் `App/Cache`, தற்காலிகம் `App/Temporary`. கோப்புறையை நீக்குங்கள், தடயம் இல்லை.
- **SFM ஐ ஒருபோதும் இயக்காது.** இயக்க செயல்முறை இல்லை, கைப்பற்ற சாளரங்கள் இல்லை. நிறுவல் உள்ளடக்க தொகுப்பாகப் படிக்கப்படுகிறது.
- **வடிவங்கள் சரிபார்க்கப்பட்டன, ஊகிக்கப்படவில்லை.** ஒவ்வொரு ரீடரும் உண்மையான நிறுவலுடன் சரிபார்க்கப்பட்டது; வடிவம் ஆச்சரியமானதைச் செய்யும் இடத்தில், குறியீடு சொல்கிறது.
- **சேமிப்பு துல்லியம்.** மாற்றமின்றி படித்து எழுதிய அமர்வு அதே கோப்பு.
- **எஞ்சினுக்கு சார்புகள் இல்லை.** `Core/` மற்றும் முழு சோதனைத் தொகுப்பும் தூய Python இல் இயங்கும்; சாளரத்திற்கு மட்டும் Qt மற்றும் OpenGL தேவை.

## இயக்குதல்

Windows, Python 3.13 மற்றும் Source Filmmaker நிறுவல் தேவை.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

முதல் தொடக்கத்தில் Steam வழியாக SFM ஐத் தேடுகிறது; கிடைக்காவிட்டால் கேட்கிறது. <kbd>Ctrl</kbd>+<kbd>O</kbd> அமர்வைத் திறக்கிறது, <kbd>Space</kbd> ப்ளே, <kbd>C</kbd> ஷாட் கேமரா, <kbd>T</kbd>/<kbd>R</kbd> நகர்த்து/சுழற்று, <kbd>M</kbd> மோஷன் எடிட்டர், <kbd>Ctrl</kbd>+<kbd>Z</kbd> செயல்தவிர், <kbd>Ctrl</kbd>+<kbd>S</kbd> சேமி. பேனல்கள் தலைப்பால் இழுக்கப்படுகின்றன. சோதனைகளுக்கு எதுவும் தேவையில்லை:

```bash
python Testing/run.py
```

## அமைப்பு

```
C2UI_SDK/
├── c2ui.py            லாஞ்சர்
├── Core/              எஞ்சின்: வடிவங்கள், மெய்நிகர் கோப்பு முறைமை, அட்டவணை, பாலங்கள்
├── App/               எடிட்டர்: உள்ளடக்க நூலகம், ரெண்டரர், சாளரம்
├── Tools/             உள்ளூர்மயமாக்கல், UI கருவிகள், செருகுநிரல்கள் (பின்னர்)
├── Testing/           சோதனைகள், பைட்-துல்லிய ஃபிக்ஸ்சர்கள், ஒரு ரன்னர்
└── GIT&DOCK/README/   இந்த README பிற மொழிகளில்
```

## வழித்திட்டம்

1. **கிராஃப் எடிட்டர்** — வளைவுகள் மற்றும் கீகள், கண்ணுக்கு.
2. **Source ஷேடிங்** — SFM வரைவது போல VertexLitGeneric: phong, rim, lightwarp, காட்சி ஒளிகள்.
3. **வரைபடங்கள்** — பின்னணிக்கு `.bsp`.
4. **வெளியீடு** — படம் மற்றும் வீடியோ ஏற்றுமதி.
5. **செருகுநிரல்கள்** — `.c2plg` வடிவம்; பின்னர் தீம்கள் மற்றும் பணியிடங்கள்.

## உரிமம் மற்றும் நன்றி

Source Filmmaker, Team Fortress 2 மற்றும் Source எஞ்சின் Valve க்கு சொந்தமானவை. இந்தத் திட்டம் அவற்றின் கோப்பு வடிவங்களைப் படிக்கிறது, அவற்றின் கோப்புகளைச் சேர்க்காது, Steam வழியாக உங்களிடம் ஏற்கனவே உள்ள SFM நகலுடன் மட்டுமே வேலை செய்கிறது.

C2UI இன் சொந்த குறியீட்டின் உரிமம் இன்னும் தேர்ந்தெடுக்கப்படவில்லை — அதுவரை அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை. Issues மற்றும் pull requests வரவேற்கப்படுகின்றன.

<p align="center"><img src="../../.github/assets/models.png" alt="நிறுவலிலிருந்து நேரடியாக ரெண்டர் செய்த 64 மாதிரிகள்" width="60%"><br><sub>நிறுவலிலிருந்து சீரற்று தேர்ந்தெடுத்த அறுபத்து நான்கு மாதிரிகள், C2UI இன் சொந்த ரெண்டரரால் வரையப்பட்டவை.</sub></p>
