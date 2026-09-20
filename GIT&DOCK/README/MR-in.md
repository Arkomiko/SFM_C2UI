<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <b>🇮🇳 मराठी</b> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BF%E0%A4%A4%E0%A5%80-%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A5%80--%E0%A4%85%E0%A4%B2%E0%A5%8D%E0%A4%AB%E0%A4%BE-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E0%A4%9A%E0%A4%BE%E0%A4%9A%E0%A4%A3%E0%A5%8D%E0%A4%AF%E0%A4%BE-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — ही Source Filmmaker च्या एडिटरची माझी पुनर्बांधणी आहे: तोच कंटेंट, तोच सेशन फॉरमॅट, तेच डेटा मॉडेल — Steam लायब्ररीकडून रूप आणि Unreal Engine 5 एडिटरकडून मांडणी घेतलेल्या कवचात.</p>

---

## कल्पना

Source Filmmaker हे २०१२ च्या इंटरफेसमधील उत्तम साधन आहे. मला `sfm.exe` वर स्किन चढवायची नाही, आणि त्याच्या खिडक्या एकेक करून ताब्यात घ्यायच्या नाहीत. मला असा एडिटर हवा जो **SFM कुठे इन्स्टॉल आहे ते विचारतो**, ते इन्स्टॉलेशन Garry's Mod जसे Counter-Strike माउंट करते तसे माउंट करतो, आणि त्या फाइल्सवर सर्व काही स्वतः करतो — मॉडेल, मटेरियल, टेक्सचर, सेशन, अॅनिमेशन — SFM कधीही न चालवता.

लक्ष्य आहे **SFM सोबत एकास एक फीचर समानता** (हाडे आणि रिग्ससह), मग SFM ला कधीच न मिळालेल्या गोष्टी.

```
  ┌──────────────┐    "SFM कुठे?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  स्वतःचा UI   │ ◀─────   माउंट   ───────│    tf/  hl2/  tf_movies/ …   │
  │  स्वतःचा रेंडर │       फक्त वाचन        │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## तयारी

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>रिलीजसाठी एकूण तयारी: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy उघडलेला एडिटर" width="100%"><br><sub>आजचा एडिटर, Valve चे Meet the Heavy उघडलेले: टाइमलाइनवर शॉट्स आणि आवाज, सेशन ट्री, पहिला शॉट त्याच्या स्वतःच्या कॅमेऱ्यातून, सेशनप्रमाणे पोझ आणि चेहऱ्यांसह पात्रे.</sub></p>

नक्की काय झाले आणि काय नाही हे पाहण्यासाठी एखादे क्षेत्र उघडा. टक्केवारी SFM काय करू शकते याच्या तुलनेत माझा प्रामाणिक अंदाज आहे.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM शोधणे आणि माउंट करणे</b></summary>

Steam रजिस्ट्री → `libraryfolders.vdf` → `gameinfo.txt` चे शोध मार्ग, इंजिनच्या क्रमाने. मानक इन्स्टॉलवर सहा माउंट. अॅप्लिकेशन फोल्डरबाहेर काहीही लिहिले जात नाही.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>कंटेंट इंडेक्स</b></summary>

७० १९९ फाइल्स १.१ से थंड / ०.०२ से कॅशमधून; माउंटमधील ओव्हरराइड इंजिनप्रमाणेच सोडवले जातात.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>मॉडेल — <code></code> <code></code> <code></code></b></summary>

आवृत्त्या ४४, ४८, ४९. सांगाडा, मेश, सर्व तपशील स्तर, बॉडी ग्रुप. १ ५०० मॉडेल लोड, ० अपयश.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>मटेरियल — <code></code></b></summary>

सर्व १९ ५५४ मटेरियल वाचली जातात; `patch`, DX ब्लॉक, प्रॉक्सी.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>टेक्सचर — <code></code></b></summary>

आवृत्त्या ७.०–७.५, DXT1/3/5 आणि सर्व असंपीडित फॉरमॅट, क्यूबमॅप, मिप. DXT डिकोड न करता GPU कडे जाते.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>सेशन — <code></code></b></summary>

बायनरी १–५ आणि KeyValues2. इन्स्टॉलमधील प्रत्येक सेशन आणि पार्टिकल फाइल **बाइट बाय बाइट** परत लिहिली जाते.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>पडद्यावर सेशन</b></summary>

टाइमलाइनवर शॉट्स आणि साउंड ट्रॅक, एलिमेंट ट्री, प्रत्येक शॉटचे दृश्य त्याच्या कॅमेऱ्यातून. अजून नाही: नकाशे, पार्टिकल, आवाज.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>अॅनिमेशन</b></summary>

कर्सरवर चॅनेल आणि लॉग मूल्यांकित; स्क्रब आणि प्ले. हाडे, कॅमेरे आणि दृश्यमानता सेशनचे अनुसरण करतात.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>चेहरे</b></summary>

Flex कंट्रोलर, संकलित नियम आणि व्हर्टेक्स अॅनिमेशन — पात्रे बोलतात आणि भाव दाखवतात. अजून नाही: सुरकुत्या नकाशे.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>रिग</b></summary>

एक्सप्रेशन, point/orient/parent/aim कन्स्ट्रेंट, दोन-हाडांचा IK. अजून नाही: पूर्ण ऑपरेटर अवलंबित्व आलेख, रिग निर्मिती.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>संपादन</b></summary>

क्लिकने निवड, मूव्ह/रोटेट मॅनिप्युलेटर, कोणत्याही अॅट्रिब्यूटसाठी इन्स्पेक्टर, कर्सरवर की, अनडू/रीडू, बाइट-अचूक सेव्ह. अजून नाही: ग्राफ एडिटर.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>मोशन एडिटर</b></summary>

रूलरवर होल्ड आणि फॉलऑफसह वेळ निवड; संपादन SFM प्रमाणे त्यावर पसरते. अजून नाही: प्रीसेट, लेयर.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>पॅनेल डॉकिंग</b></summary>

UE5 आणि Visual Studio प्रमाणे, पूर्वावलोकनासह लक्ष्यांच्या कंपासवर पॅनेल ओढा. अजून नाही: जतन केलेली मांडणी, थीम.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source शेडिंग</b></summary>

फक्त टेक्सचर आणि साधा प्रकाश. अजून नाही: phong, rim, lightwarp, दृश्य प्रकाश, सावल्या.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>नकाशे — <code></code></b></summary>

सुरू केले नाही.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>प्रतिमा आणि व्हिडिओमध्ये रेंडर</b></summary>

सुरू केले नाही.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>प्लगइन <code></code></b></summary>

सुरू केले नाही.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>थीम आणि वर्कस्पेस</b></summary>

मुद्दाम नंतर: एडिटरमध्ये सजवण्यासारखे काही येईपर्यंत एकच रूप.

</details>

**रिलीजसाठी तयार नाही.** पाया — SFM वापरणारा प्रत्येक फाइल फॉरमॅट, योग्य वाचलेला आणि संपूर्ण इन्स्टॉलेशनवर तपासलेला — आहे आणि चाचणी केलेला; सेशन उघडता, चालवता, बदलता आणि जतन करता येते. कमी आहे कामाची *सोय*: ग्राफ एडिटर, Source शेडिंग, नकाशे, निर्यात. अॅनिमेटर यात दिवसभर काम करू शकेपर्यंत आवृत्ती क्रमांक नाही.

## काय वेगळे आहे

- **पोर्टेबल.** अॅप्लिकेशन फोल्डरबाहेर काहीही लिहिले जात नाही: सेटिंग्ज `App/User` मध्ये, कॅश `App/Cache` मध्ये, तात्पुरते `App/Temporary` मध्ये. फोल्डर हटवा आणि खूण नाही.
- **SFM कधीही चालवत नाही.** चालवायला प्रोसेस नाही, ताब्यात घ्यायला खिडक्या नाहीत. इन्स्टॉलेशन कंटेंट पॅकसारखे वाचले जाते.
- **फॉरमॅट तपासलेले, गृहीत धरलेले नाही.** प्रत्येक रीडर खऱ्या इन्स्टॉलेशनशी तपासला; जिथे फॉरमॅट अनपेक्षित करतो, कोड सांगतो.
- **सेव्ह अचूक आहे.** न बदलता वाचलेले आणि लिहिलेले सेशन तीच फाइल आहे.
- **इंजिनला अवलंबित्व नाही.** `Core/` आणि संपूर्ण चाचणी संच शुद्ध Python वर चालतो; फक्त खिडकीला Qt आणि OpenGL लागते.

## चालवणे

Windows, Python 3.13 आणि Source Filmmaker इन्स्टॉलेशन आवश्यक.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

पहिल्या सुरुवातीला Steam द्वारे SFM शोधते; न सापडल्यास विचारते. <kbd>Ctrl</kbd>+<kbd>O</kbd> सेशन उघडते, <kbd>Space</kbd> प्ले, <kbd>C</kbd> शॉट कॅमेरा, <kbd>T</kbd>/<kbd>R</kbd> मूव्ह/रोटेट, <kbd>M</kbd> मोशन एडिटर, <kbd>Ctrl</kbd>+<kbd>Z</kbd> अनडू, <kbd>Ctrl</kbd>+<kbd>S</kbd> सेव्ह. पॅनेल शीर्षकाने ओढले जातात. चाचण्यांना काही लागत नाही:

```bash
python Testing/run.py
```

## रचना

```
C2UI_SDK/
├── c2ui.py            लाँचर
├── Core/              इंजिन: फॉरमॅट, व्हर्च्युअल फाइल सिस्टम, इंडेक्स, ब्रिज
├── App/               एडिटर: कंटेंट लायब्ररी, रेंडरर, खिडकी
├── Tools/             स्थानिकीकरण, UI साधने, प्लगइन (नंतर)
├── Testing/           चाचण्या, बाइट-अचूक फिक्स्चर, एक रनर
└── GIT&DOCK/README/   हा README इतर भाषांमध्ये
```

## रोडमॅप

१. **ग्राफ एडिटर** — वक्र आणि की, डोळ्यांसमोर.
२. **Source शेडिंग** — SFM काढते तसे VertexLitGeneric: phong, rim, lightwarp, दृश्य प्रकाश.
३. **नकाशे** — पार्श्वभूमीसाठी `.bsp`.
४. **आउटपुट** — प्रतिमा आणि व्हिडिओ निर्यात.
५. **प्लगइन** — `.c2plg` फॉरमॅट; मग थीम आणि वर्कस्पेस.

## परवाना आणि आभार

Source Filmmaker, Team Fortress 2 आणि Source इंजिन Valve चे आहेत. हा प्रकल्प त्यांचे फाइल फॉरमॅट वाचतो, त्यांची कोणतीही फाइल समाविष्ट करत नाही, आणि फक्त Steam द्वारे तुमच्याकडे असलेल्या SFM प्रतीसह काम करतो.

C2UI च्या स्वतःच्या कोडचा परवाना अजून निवडला नाही — तोपर्यंत सर्व हक्क राखीव. Issues आणि pull requests तरीही स्वागतार्ह.

<p align="center"><img src="../../.github/assets/models.png" alt="इन्स्टॉलेशनमधून थेट रेंडर केलेली ६४ मॉडेल" width="60%"><br><sub>इन्स्टॉलेशनमधून यादृच्छिक निवडलेली चौसष्ट मॉडेल, C2UI च्या स्वतःच्या रेंडररने काढलेली.</sub></p>
