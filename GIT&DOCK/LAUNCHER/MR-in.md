# C2UI लाँचर

<details align="center"><summary>&nbsp;🌐 <b>🇮🇳 मराठी</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><b>🇮🇳<br>मराठी</b></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` हेच प्रकल्प सुरू होण्याचे ठिकाण: शीर्षक, एका ओळीचे वर्णन आणि तीन बटणे असलेली छोटी गडद विंडो. ती एका एक्झिक्युटेबलमध्ये तयार होते, ज्याला Python इन्स्टॉल असण्याची गरज नाही, आणि प्रकल्प स्वतःच शोधते — आपल्या जागेवरून वर जात, `App`, `Core` आणि `Launcher` एकत्र दिसेपर्यंत.

<p align="center"><img src="../assets/launcher.png" alt="C2UI लाँचर" width="562"><br><sub>लाँचरची विंडो: «Dev-mode» शीर्षक, वर्णनाची ओळ आणि तीन बटणे.</sub></p>

> [!NOTE]
> **लाँचरचा इंटरफेस सध्या फक्त रशियनमध्ये आहे — हा तात्पुरता उपाय आहे.** शीर्षक, वर्णन आणि बटणांचे शब्द कोडमध्ये लिहिलेले आहेत; भाषांतरे एडिटरच्या स्थानिकीकरणासोबत (`Tools/Localization`) तेव्हा येतील, जेव्हा तयार App साठी लाँचर पुन्हा लिहिला जाईल. प्रकल्पाची उरलेली कागदपत्रे आधीच 32 भाषांत आहेत.

## तीन बटणे

| | |
|---|---|
| <code>Запустить Core</code> | एडिटर सुरू करते — व्ह्यूपोर्ट, टाइमलाइन आणि पॅनेल असलेली C2UI विंडो. |
| <code>Запустить App</code> | निष्क्रिय: वेगळे App अजून नाही. |
| <code>Выйти</code> | लाँचर बंद करते. |

## स्रोतातून चालवणे

Windows, Python 3.13 आणि इन्स्टॉल केलेला Source Filmmaker लागतो.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

एकाच फाइलची बांधणी `Launcher/Launcher-C2UI.exe` (git मध्ये ठेवली जात नाही — स्रोतातून पुन्हा तयार होते):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## एडिटरशिवाय इंजिन

`Launcher/core.py` फक्त `Core` सुरू करते: इन्स्टॉलेशन माउंट करते, निर्देशांक बनवते आणि इंजिनवर एक छोटे शेल देते — मॉडेल, मटेरियल, टेक्स्चर, नकाशे, सेशन आणि त्यांची गणना. हेही तात्पुरते: App विंडोशिवाय चालू लागल्यावर एडिटरच एकमेव प्रवेशबिंदू राहील.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## पुढे काय बदलेल

- App आल्यावर विंडो पुन्हा लिहिली जाईल — रूप आणि भाषांतरांसह.
- «Запустить App» बटण काम करू लागेल.
- एडिटर विंडोशिवाय सुरू करता आला की `core.py` जाईल.
- तयार `.exe` GitHub प्रकाशनांसोबत दिला जाईल.

<p align="center"><a href="../README/MR-in.md"><img alt="← README कडे परत" src="https://img.shields.io/badge/%E2%86%90_README_%E0%A4%95%E0%A4%A1%E0%A5%87_%E0%A4%AA%E0%A4%B0%E0%A4%A4-1b2838?style=for-the-badge"></a></p>
