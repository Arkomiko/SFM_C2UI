# C2UI లాంచర్

<details align="center"><summary>&nbsp;🌐 <b>🇮🇳 తెలుగు</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><b>🇮🇳<br>తెలుగు</b></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` నుండే ప్రాజెక్ట్ ప్రారంభమవుతుంది: శీర్షిక, ఒక్క పంక్తి వివరణ మరియు మూడు బటన్లతో కూడిన చిన్న ముదురు విండో. ఇది Python అవసరం లేని ఒకే ఎగ్జిక్యూటబుల్‌గా తయారవుతుంది, ప్రాజెక్ట్‌ను తానే కనుగొంటుంది — `App`, `Core`, `Launcher` కలిసి కనిపించే వరకు తన స్థానం నుండి పైకి వెళ్తుంది.

<p align="center"><img src="../assets/launcher.png" alt="C2UI లాంచర్" width="562"><br><sub>లాంచర్ విండో: «Dev-mode» శీర్షిక, వివరణ పంక్తి మరియు మూడు బటన్లు.</sub></p>

> [!NOTE]
> **లాంచర్ ఇంటర్‌ఫేస్ ప్రస్తుతం రష్యన్‌లో మాత్రమే — ఇది తాత్కాలిక పరిష్కారం.** శీర్షిక, వివరణ మరియు బటన్ల పదాలు కోడ్‌లోనే ఉన్నాయి; ఎడిటర్ స్థానికీకరణతో (`Tools/Localization`) పాటు, పూర్తయిన App కోసం లాంచర్ తిరిగి రాసినప్పుడు అనువాదాలు వస్తాయి. ప్రాజెక్ట్ మిగతా పత్రాలు ఇప్పటికే 32 భాషల్లో ఉన్నాయి.

## మూడు బటన్లు

| | |
|---|---|
| <code>Запустить Core</code> | ఎడిటర్‌ను ప్రారంభిస్తుంది — వ్యూపోర్ట్, టైమ్‌లైన్, ప్యానెళ్లతో కూడిన C2UI విండో. |
| <code>Запустить App</code> | నిష్క్రియం: ప్రత్యేక App ఇంకా లేదు. |
| <code>Выйти</code> | లాంచర్‌ను మూసివేస్తుంది. |

## సోర్స్ నుండి అమలు

Windows, Python 3.13 మరియు ఇన్‌స్టాల్ చేసిన Source Filmmaker అవసరం.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

ఒకే ఫైల్ `Launcher/Launcher-C2UI.exe` నిర్మాణం (git లో ఉంచరు — సోర్స్ నుండి తిరిగి నిర్మిస్తారు):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## ఎడిటర్ లేకుండా ఇంజిన్

`Launcher/core.py` `Core`ని ఒంటరిగా ప్రారంభిస్తుంది: ఇన్‌స్టాలేషన్‌ను మౌంట్ చేసి, ఇండెక్స్ చేసి, ఇంజిన్ పై చిన్న షెల్ ఇస్తుంది — మోడళ్లు, మెటీరియల్స్, టెక్స్చర్లు, మ్యాప్‌లు, సెషన్లు మరియు వాటి గణన. ఇదీ తాత్కాలికమే: App విండో లేకుండా నడిచినప్పుడు ఎడిటరే ఏకైక ప్రవేశ ద్వారం అవుతుంది.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## తర్వాత ఏమి మారుతుంది

- App వచ్చాక విండోను తిరిగి రాస్తారు — రూపం మరియు అనువాదాలతో.
- «Запустить App» బటన్ పనిచేయడం మొదలవుతుంది.
- ఎడిటర్‌ను విండో లేకుండా ప్రారంభించగలిగితే `core.py` పోతుంది.
- నిర్మించిన `.exe` GitHub విడుదలలతో జత చేస్తారు.

<p align="center"><a href="../README/TE-in.md"><img alt="← README కి తిరిగి" src="https://img.shields.io/badge/%E2%86%90_README_%E0%B0%95%E0%B0%BF_%E0%B0%A4%E0%B0%BF%E0%B0%B0%E0%B0%BF%E0%B0%97%E0%B0%BF-1b2838?style=for-the-badge"></a></p>
