# C2UI लॉन्चर

<details align="center"><summary>&nbsp;🌐 <b>🇮🇳 हिन्दी</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><b>🇮🇳<br>हिन्दी</b></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` वही है जहाँ से प्रोजेक्ट शुरू होता है: शीर्षक, एक पंक्ति के विवरण और तीन बटनों वाली एक छोटी गहरी विंडो। यह एक ही एक्ज़ीक्यूटेबल में बनती है जिसे इंस्टॉल किए Python की ज़रूरत नहीं, और प्रोजेक्ट खुद ढूँढ़ लेती है — अपनी जगह से ऊपर चलते हुए जब तक `App`, `Core` और `Launcher` साथ न दिख जाएँ।

<p align="center"><img src="../assets/launcher.png" alt="C2UI लॉन्चर" width="562"><br><sub>लॉन्चर विंडो: «Dev-mode» शीर्षक, विवरण पंक्ति और तीन बटन।</sub></p>

> [!NOTE]
> **लॉन्चर का इंटरफ़ेस फ़िलहाल केवल रूसी में है — यह अस्थायी समाधान है।** शीर्षक, विवरण और बटनों के शब्द कोड में लिखे हैं; अनुवाद एडिटर के स्थानीयकरण (`Tools/Localization`) के साथ तब आएँगे जब तैयार App के लिए लॉन्चर फिर से लिखा जाएगा। प्रोजेक्ट का बाकी दस्तावेज़ीकरण पहले से 32 भाषाओं में है।

## तीन बटन

| | |
|---|---|
| <code>Запустить Core</code> | एडिटर शुरू करता है — व्यूपोर्ट, टाइमलाइन और पैनलों वाली C2UI विंडो। |
| <code>Запустить App</code> | निष्क्रिय: अलग App अभी नहीं है। |
| <code>Выйти</code> | लॉन्चर बंद करता है। |

## स्रोत से चलाना

Windows, Python 3.13 और इंस्टॉल किया हुआ Source Filmmaker चाहिए।

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

एकल फ़ाइल `Launcher/Launcher-C2UI.exe` बनाना (git में नहीं रखी जाती — स्रोत से फिर बनती है):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## एडिटर के बिना इंजन

`Launcher/core.py` केवल `Core` चलाता है: इंस्टॉलेशन माउंट करता है, इंडेक्स बनाता है और इंजन के ऊपर एक छोटा शेल देता है — मॉडल, मटेरियल, टेक्सचर, मैप, सेशन और उनका मूल्यांकन। यह भी अस्थायी है: जब App बिना विंडो चल सकेगा, एडिटर ही एकमात्र प्रवेश बिंदु रहेगा।

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## आगे क्या बदलेगा

- App बनने पर विंडो फिर से लिखी जाएगी — रूप और अनुवादों के साथ।
- «Запустить App» बटन काम करने लगेगा।
- एडिटर बिना विंडो चलने लगे तो `core.py` हट जाएगा।
- बना हुआ `.exe` GitHub रिलीज़ के साथ दिया जाएगा।

<p align="center"><a href="../README/HI-in.md"><img alt="← README पर वापस" src="https://img.shields.io/badge/%E2%86%90_README_%E0%A4%AA%E0%A4%B0_%E0%A4%B5%E0%A4%BE%E0%A4%AA%E0%A4%B8-1b2838?style=for-the-badge"></a></p>
