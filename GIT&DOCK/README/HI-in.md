<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <b>🇮🇳 हिन्दी</b> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BF%E0%A4%A4%E0%A4%BF-%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A5%80--%E0%A4%85%E0%A4%B2%E0%A5%8D%E0%A4%AB%E0%A4%BC%E0%A4%BE-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E0%A4%AA%E0%A4%B0%E0%A5%80%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A4%A3-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — Source Filmmaker के एडिटर का मेरा पुनर्निर्माण है: वही कंटेंट, वही सेशन फ़ॉर्मैट, वही डेटा मॉडल — एक ऐसे खोल में जो अपना रूप Steam लाइब्रेरी से और अपना लेआउट Unreal Engine 5 एडिटर से लेता है।</p>

---

## विचार

Source Filmmaker 2012 के इंटरफ़ेस में एक शानदार टूल है। मैं `sfm.exe` पर स्किन नहीं चढ़ाना चाहता, और न ही उसकी विंडो एक-एक करके हथियाना चाहता हूँ। मुझे ऐसा एडिटर चाहिए जो **पूछे कि SFM कहाँ इंस्टॉल है**, उस इंस्टॉलेशन को वैसे माउंट करे जैसे Garry's Mod Counter-Strike को माउंट करता है, और उन फ़ाइलों के ऊपर सब कुछ खुद करे — मॉडल, मटीरियल, टेक्सचर, सेशन, एनिमेशन — SFM को कभी लॉन्च किए बिना।

लक्ष्य है **SFM के साथ एक-से-एक फ़ीचर समानता** (हड्डियाँ और रिग समेत), फिर वह जो SFM को कभी नहीं मिला।

```
  ┌──────────────┐    "SFM कहाँ है?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  अपना UI     │ ◀─────   माउंट   ───────│    tf/  hl2/  tf_movies/ …   │
  │  अपना रेंडर  │       केवल पढ़ना       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## तैयारी

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>रिलीज़ के लिए कुल तैयारी: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy खुला हुआ एडिटर" width="100%"><br><sub>आज का एडिटर, Valve का Meet the Heavy खुला हुआ: टाइमलाइन पर शॉट और ध्वनि, सेशन ट्री, पहला शॉट उसके अपने कैमरे से, सेशन के अनुसार पोज़ और चेहरों वाले किरदार।</sub></p>

यह देखने के लिए कि क्या बना है और क्या नहीं, किसी क्षेत्र को खोलें। प्रतिशत SFM की क्षमताओं के मुकाबले मेरा ईमानदार अनुमान है।

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM खोजना और माउंट करना</b></summary>

Steam रजिस्ट्री → `libraryfolders.vdf` → `gameinfo.txt` के खोज पथ, इंजन के क्रम में। मानक इंस्टॉलेशन पर छह माउंट। एप्लिकेशन फ़ोल्डर के बाहर कुछ नहीं लिखा जाता।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>कंटेंट इंडेक्स</b></summary>

70 199 फ़ाइलें 1.1 सेकंड ठंडा / 0.02 सेकंड कैश से; माउंट के बीच ओवरराइड ठीक इंजन की तरह हल होते हैं।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>मॉडल — `.mdl` `.vvd` `.vtx`</b></summary>

संस्करण 44, 48, 49। कंकाल, मेश, हर विवरण स्तर, बॉडी ग्रुप। 1 500 मॉडल लोड, 0 विफलता।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>मटीरियल — `.vmt`</b></summary>

सभी 19 554 शामिल मटीरियल पढ़े जाते हैं; `patch`, DX ब्लॉक, प्रॉक्सी।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>टेक्सचर — `.vtf`</b></summary>

संस्करण 7.0–7.5, DXT1/3/5 और सभी असंपीड़ित फ़ॉर्मैट, क्यूबमैप, मिप। DXT बिना डिकोड किए GPU में जाता है।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>सेशन — `.dmx`</b></summary>

बाइनरी 1–5 और KeyValues2। इंस्टॉलेशन का हर सेशन और पार्टिकल फ़ाइल **बाइट दर बाइट** वापस लिखी जाती है।

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>स्क्रीन पर सेशन</b></summary>

टाइमलाइन पर शॉट और साउंड ट्रैक, एलिमेंट ट्री, हर शॉट का दृश्य उसके कैमरे से। अभी नहीं: मैप, पार्टिकल, ध्वनि।

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>एनिमेशन</b></summary>

चैनल और लॉग कर्सर पर मूल्यांकित; स्क्रब और प्ले। हड्डियाँ, कैमरे और दृश्यता सेशन का अनुसरण करते हैं।

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>चेहरे</b></summary>

Flex कंट्रोलर, संकलित नियम और वर्टेक्स एनिमेशन — किरदार बोलते और भाव दिखाते हैं। अभी नहीं: झुर्री मैप।

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>रिग</b></summary>

एक्सप्रेशन, point/orient/parent/aim कंस्ट्रेंट, दो-हड्डी IK। अभी नहीं: पूरा ऑपरेटर निर्भरता ग्राफ़, रिग निर्माण।

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>संपादन</b></summary>

क्लिक से चयन, मूव/रोटेट मैनिपुलेटर, किसी भी एट्रिब्यूट का इंस्पेक्टर, कर्सर पर की, अन्डू/रीडू, बाइट-सटीक सेव। अभी नहीं: ग्राफ़ एडिटर।

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>मोशन एडिटर</b></summary>

रूलर पर होल्ड और फ़ॉलऑफ़ के साथ समय चयन; संपादन SFM की तरह उस पर फैलता है। अभी नहीं: प्रीसेट, लेयर।

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>पैनल डॉकिंग</b></summary>

UE5 और Visual Studio की तरह, पूर्वावलोकन के साथ लक्ष्यों के कम्पास पर पैनल खींचें। अभी नहीं: सहेजे लेआउट, थीम।

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source शेडिंग</b></summary>

केवल टेक्सचर और साधारण रोशनी। अभी नहीं: phong, rim, lightwarp, दृश्य की रोशनी, छायाएँ।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>मैप — `.bsp`</b></summary>

शुरू नहीं हुआ।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>छवि और वीडियो में रेंडर</b></summary>

शुरू नहीं हुआ।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>प्लगइन `.c2plg`</b></summary>

शुरू नहीं हुआ।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>थीम और वर्कस्पेस</b></summary>

जानबूझकर बाद में: एक ही रूप, जब तक एडिटर में सजाने लायक कुछ न हो।

</details>

**रिलीज़ के लिए तैयार नहीं।** नींव — SFM का हर फ़ाइल फ़ॉर्मैट, सही पढ़ा और पूरे इंस्टॉलेशन पर जाँचा — मौजूद और परीक्षित है; सेशन खोला, चलाया, बदला और सहेजा जा सकता है। कमी है काम की *सुविधा* की: ग्राफ़ एडिटर, Source शेडिंग, मैप, एक्सपोर्ट। जब तक कोई एनिमेटर इसमें एक दिन का काम न कर सके, कोई संस्करण संख्या नहीं।

## इसे अलग क्या बनाता है

- **पोर्टेबल।** एप्लिकेशन फ़ोल्डर के बाहर कुछ नहीं लिखा जाता: सेटिंग `App/User` में, कैश `App/Cache` में, अस्थायी `App/Temporary` में। फ़ोल्डर मिटाएँ और कोई निशान नहीं।
- **SFM कभी नहीं चलाता।** चलाने के लिए कोई प्रोसेस नहीं, हथियाने के लिए कोई विंडो नहीं। इंस्टॉलेशन कंटेंट पैक की तरह पढ़ा जाता है।
- **फ़ॉर्मैट सत्यापित, माने हुए नहीं।** हर रीडर असली इंस्टॉलेशन से जाँचा गया; जहाँ फ़ॉर्मैट कुछ अप्रत्याशित करता है, कोड बताता है।
- **सेव सटीक है।** बिना बदले पढ़ा और लिखा सेशन वही फ़ाइल है।
- **इंजन की कोई निर्भरता नहीं।** `Core/` और पूरा टेस्ट सूट शुद्ध Python पर चलता है; केवल विंडो को Qt और OpenGL चाहिए।

## चलाना

Windows, Python 3.13 और Source Filmmaker इंस्टॉलेशन आवश्यक।

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

पहली बार यह Steam से SFM खोजता है; न मिले तो पूछता है। <kbd>Ctrl</kbd>+<kbd>O</kbd> सेशन खोलता है, <kbd>Space</kbd> प्ले, <kbd>C</kbd> शॉट कैमरा, <kbd>T</kbd>/<kbd>R</kbd> मूव/रोटेट, <kbd>M</kbd> मोशन एडिटर, <kbd>Ctrl</kbd>+<kbd>Z</kbd> अन्डू, <kbd>Ctrl</kbd>+<kbd>S</kbd> सेव। पैनल शीर्षक से खींचे जाते हैं। परीक्षणों को कुछ नहीं चाहिए:

```bash
python Testing/run.py
```

## संरचना

```
C2UI_SDK/
├── c2ui.py            लॉन्चर
├── Core/              इंजन: फ़ॉर्मैट, वर्चुअल फ़ाइल सिस्टम, इंडेक्स, ब्रिज
├── App/               एडिटर: कंटेंट लाइब्रेरी, रेंडरर, विंडो
├── Tools/             स्थानीयकरण, UI टूल, प्लगइन (बाद में)
├── Testing/           परीक्षण, बाइट-सटीक फ़िक्सचर, एक रनर
└── GIT&DOCK/README/   यह README अन्य भाषाओं में
```

## रोडमैप

1. **ग्राफ़ एडिटर** — कर्व और की, आँखों के सामने।
2. **Source शेडिंग** — VertexLitGeneric जैसे SFM बनाता है: phong, rim, lightwarp, दृश्य की रोशनी।
3. **मैप** — पृष्ठभूमि के लिए `.bsp`।
4. **आउटपुट** — छवि और वीडियो एक्सपोर्ट।
5. **प्लगइन** — `.c2plg` फ़ॉर्मैट; फिर थीम और वर्कस्पेस।

## लाइसेंस और आभार

Source Filmmaker, Team Fortress 2 और Source इंजन Valve के हैं। यह प्रोजेक्ट उनके फ़ाइल फ़ॉर्मैट पढ़ता है, उनकी कोई फ़ाइल शामिल नहीं करता, और केवल Steam से आपकी अपनी SFM प्रति के साथ काम करता है।

C2UI के अपने कोड का लाइसेंस अभी चुना नहीं गया — तब तक सर्वाधिकार सुरक्षित। Issues और pull requests का फिर भी स्वागत है।

<p align="center"><img src="../../.github/assets/models.png" alt="इंस्टॉलेशन से सीधे रेंडर किए 64 मॉडल" width="60%"><br><sub>इंस्टॉलेशन से यादृच्छिक चुने चौंसठ मॉडल, C2UI के अपने रेंडरर से बनाए गए।</sub></p>
