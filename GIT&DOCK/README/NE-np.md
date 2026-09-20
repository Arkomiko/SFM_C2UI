<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <b>🇳🇵 नेपाली</b> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BF%E0%A4%A4%E0%A4%BF-%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A5%80--%E0%A4%85%E0%A4%B2%E0%A5%8D%E0%A4%AB%E0%A4%BE-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E0%A4%AA%E0%A4%B0%E0%A5%80%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A4%A3-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — Source Filmmaker को सम्पादकको मेरो पुनर्निर्माण हो: उही सामग्री, उही सेसन ढाँचा, उही डेटा मोडेल — Steam पुस्तकालयबाट रूप र Unreal Engine 5 सम्पादकबाट लेआउट लिएको खोलभित्र।</p>

---

## विचार

Source Filmmaker २०१२ को इन्टरफेसमा रहेको उत्कृष्ट उपकरण हो। म `sfm.exe` माथि स्किन लगाउन चाहन्न, र यसका विन्डोहरू एक-एक गरी कब्जा गर्न पनि चाहन्न। मलाई त्यस्तो सम्पादक चाहिन्छ जसले **SFM कहाँ स्थापित छ भनेर सोध्छ**, त्यो स्थापनालाई Garry's Mod ले Counter-Strike माउन्ट गरेजस्तै माउन्ट गर्छ, र ती फाइलहरूमाथि सबै आफैँ गर्छ — मोडेल, सामग्री, टेक्सचर, सेसन, एनिमेसन — SFM कहिल्यै नखोलेर।

लक्ष्य **SFM सँग एक-एक सुविधा समानता** (हड्डी र रिगसहित), त्यसपछि SFM ले कहिल्यै नपाएका कुराहरू।

```
  ┌──────────────┐    "SFM कहाँ?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  आफ्नै UI     │ ◀─────   माउन्ट   ───────│    tf/  hl2/  tf_movies/ …   │
  │  आफ्नै रेन्डर  │       पढ्ने मात्र       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## तयारी

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>रिलिजका लागि समग्र तयारी: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy खोलिएको सम्पादक" width="100%"><br><sub>आजको सम्पादक, Valve को Meet the Heavy खोलिएको: टाइमलाइनमा शट र आवाज, सेसन ट्री, पहिलो शट आफ्नै क्यामेराबाट, सेसनअनुसार पोज र अनुहार भएका पात्रहरू।</sub></p>

के भयो र के भएन ठ्याक्कै हेर्न कुनै क्षेत्र खोल्नुहोस्। प्रतिशत SFM ले गर्न सक्ने कुराको तुलनामा मेरो इमानदार अनुमान हो।

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM खोज्ने र माउन्ट गर्ने</b></summary>

Steam रजिस्ट्री → `libraryfolders.vdf` → `gameinfo.txt` का खोज पथ, इन्जिनको क्रममा। मानक स्थापनामा छ माउन्ट। एप्लिकेसन फोल्डरबाहिर केही लेखिँदैन।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>सामग्री सूचकांक</b></summary>

७० १९९ फाइल १.१ से चिसो / ०.०२ से क्यासबाट; माउन्टबीचका ओभरराइड इन्जिनजस्तै समाधान हुन्छन्।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>मोडेल — <code></code> <code></code> <code></code></b></summary>

संस्करण ४४, ४८, ४९। कंकाल, मेश, सबै विवरण स्तर, बडी समूह। १ ५०० मोडेल लोड, ० असफलता।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>सामग्री — <code></code></b></summary>

सबै १९ ५५४ सामग्री पढिन्छन्; `patch`, DX ब्लक, प्रोक्सी।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>टेक्सचर — <code></code></b></summary>

संस्करण ७.०–७.५, DXT1/3/5 र सबै असंकुचित ढाँचा, क्युबम्याप, मिप। DXT डिकोड नगरी GPU मा जान्छ।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>सेसन — <code></code></b></summary>

बाइनरी १–५ र KeyValues2। स्थापनाको हरेक सेसन र पार्टिकल फाइल **बाइट-बाइट** फिर्ता लेखिन्छ।

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>स्क्रिनमा सेसन</b></summary>

टाइमलाइनमा शट र साउन्ड ट्र्याक, एलिमेन्ट ट्री, हरेक शटको दृश्य आफ्नै क्यामेराबाट। अझै छैन: नक्सा, पार्टिकल, आवाज।

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>एनिमेसन</b></summary>

कर्सरमा च्यानल र लग मूल्याङ्कन; स्क्रब र प्ले। हड्डी, क्यामेरा र दृश्यता सेसनलाई पछ्याउँछन्।

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>अनुहार</b></summary>

Flex नियन्त्रक, कम्पाइल गरिएका नियम र भर्टेक्स एनिमेसन — पात्रहरू बोल्छन् र भाव देखाउँछन्। अझै छैन: चाउरी नक्सा।

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>रिग</b></summary>

अभिव्यक्ति, point/orient/parent/aim बाधा, दुई-हड्डी IK। अझै छैन: पूर्ण अपरेटर निर्भरता ग्राफ, रिग निर्माण।

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>सम्पादन</b></summary>

क्लिकबाट चयन, मुभ/रोटेट म्यानिपुलेटर, कुनै पनि एट्रिब्युटको इन्स्पेक्टर, कर्सरमा की, अन्डु/रिडु, बाइट-सटीक सेभ। अझै छैन: ग्राफ सम्पादक।

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>मोशन सम्पादक</b></summary>

रुलरमा होल्ड र फलअफसहित समय चयन; सम्पादन SFM जस्तै त्यसमा फैलिन्छ। अझै छैन: प्रिसेट, तह।

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>प्यानल डकिङ</b></summary>

UE5 र Visual Studio जस्तै, पूर्वावलोकनसहित लक्ष्यहरूको कम्पासमा प्यानल तान्नुहोस्। अझै छैन: सुरक्षित लेआउट, थिम।

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source शेडिङ</b></summary>

टेक्सचर र साधारण प्रकाश मात्र। अझै छैन: phong, rim, lightwarp, दृश्य प्रकाश, छाया।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>नक्सा — <code></code></b></summary>

सुरु भएको छैन।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>तस्बिर र भिडियोमा रेन्डर</b></summary>

सुरु भएको छैन।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>प्लगइन <code></code></b></summary>

सुरु भएको छैन।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>थिम र कार्यस्थान</b></summary>

जानीजानी पछि: सम्पादकमा सजाउन योग्य केही नआउँदासम्म एउटै रूप।

</details>

**रिलिजका लागि तयार छैन।** जग — SFM ले प्रयोग गर्ने हरेक फाइल ढाँचा, सही पढिएको र पूरै स्थापनामा प्रमाणित — छ र परीक्षण गरिएको छ; सेसन खोल्न, चलाउन, बदल्न र सेभ गर्न सकिन्छ। कमी छ कामको *सहजता*: ग्राफ सम्पादक, Source शेडिङ, नक्सा, निर्यात। एनिमेटरले यसमा एक दिनको काम गर्न नसक्दासम्म संस्करण नम्बर छैन।

## के फरक छ

- **पोर्टेबल।** एप्लिकेसन फोल्डरबाहिर केही लेखिँदैन: सेटिङ `App/User` मा, क्यास `App/Cache` मा, अस्थायी `App/Temporary` मा। फोल्डर मेट्नुहोस्, कुनै छाप छैन।
- **SFM कहिल्यै चलाउँदैन।** चलाउने प्रोसेस छैन, कब्जा गर्ने विन्डो छैन। स्थापना सामग्री प्याकजस्तै पढिन्छ।
- **ढाँचा प्रमाणित, अनुमानित होइन।** हरेक रिडर वास्तविक स्थापनासँग जाँचिएको; ढाँचाले अनपेक्षित गर्ने ठाउँमा कोड बताउँछ।
- **सेभ सटीक छ।** नबदलेर पढिएको र लेखिएको सेसन उही फाइल हो।
- **इन्जिनको कुनै निर्भरता छैन।** `Core/` र सम्पूर्ण परीक्षण सुइट शुद्ध Python मा चल्छ; विन्डोलाई मात्र Qt र OpenGL चाहिन्छ।

## चलाउने

Windows, Python 3.13 र Source Filmmaker स्थापना आवश्यक।

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

पहिलो पटक Steam मार्फत SFM खोज्छ; नपाए सोध्छ। <kbd>Ctrl</kbd>+<kbd>O</kbd> सेसन खोल्छ, <kbd>Space</kbd> प्ले, <kbd>C</kbd> शट क्यामेरा, <kbd>T</kbd>/<kbd>R</kbd> मुभ/रोटेट, <kbd>M</kbd> मोशन सम्पादक, <kbd>Ctrl</kbd>+<kbd>Z</kbd> अन्डु, <kbd>Ctrl</kbd>+<kbd>S</kbd> सेभ। प्यानल शीर्षकबाट तानिन्छन्। परीक्षणलाई केही चाहिँदैन:

```bash
python Testing/run.py
```

## संरचना

```
C2UI_SDK/
├── c2ui.py            लन्चर
├── Core/              इन्जिन: ढाँचा, भर्चुअल फाइल प्रणाली, सूचकांक, पुल
├── App/               सम्पादक: सामग्री पुस्तकालय, रेन्डरर, विन्डो
├── Tools/             स्थानीयकरण, UI उपकरण, प्लगइन (पछि)
├── Testing/           परीक्षण, बाइट-सटीक फिक्स्चर, एक रनर
└── GIT&DOCK/README/   यो README अन्य भाषामा
```

## रोडम्याप

१. **ग्राफ सम्पादक** — वक्र र की, आँखा अगाडि।
२. **Source शेडिङ** — SFM ले कोरेजस्तै VertexLitGeneric: phong, rim, lightwarp, दृश्य प्रकाश।
३. **नक्सा** — पृष्ठभूमिका लागि `.bsp`।
४. **आउटपुट** — तस्बिर र भिडियो निर्यात।
५. **प्लगइन** — `.c2plg` ढाँचा; त्यसपछि थिम र कार्यस्थान।

## इजाजतपत्र र आभार

Source Filmmaker, Team Fortress 2 र Source इन्जिन Valve का हुन्। यो परियोजना तिनका फाइल ढाँचा पढ्छ, तिनको कुनै फाइल समावेश गर्दैन, र Steam मार्फत तपाईंसँग भएको SFM प्रतिसँग मात्र काम गर्छ।

C2UI को आफ्नै कोडको इजाजतपत्र अझै छानिएको छैन — त्यसबेलासम्म सर्वाधिकार सुरक्षित। Issues र pull requests स्वागत छ।

<p align="center"><img src="../../.github/assets/models.png" alt="स्थापनाबाट सिधै रेन्डर गरिएका ६४ मोडेल" width="60%"><br><sub>स्थापनाबाट अनियमित छानिएका चौसठ्ठी मोडेल, C2UI को आफ्नै रेन्डररले कोरेका।</sub></p>
