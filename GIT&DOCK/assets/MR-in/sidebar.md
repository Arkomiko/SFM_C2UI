# C2UI ची तयारी — सविस्तर

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <b>🇮🇳 मराठी</b> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="तयारी" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>रिलीजसाठी एकूण तयारी: 41%</b></p>

प्रत्येक क्षेत्र उघडता येते: काय आधीच काम करते आणि काय अजून नाही. टक्केवारी SFM च्या क्षमतांच्या तुलनेत अंदाज आहे.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> SFM शोधणे आणि माउंट करणे

Steam रजिस्ट्री → `libraryfolders.vdf` → `gameinfo.txt` चे शोध मार्ग, इंजिनच्या क्रमाने. मानक इन्स्टॉलवर सहा माउंट. अॅप्लिकेशन फोल्डरबाहेर काहीही लिहिले जात नाही.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> कंटेंट इंडेक्स

७० १९९ फाइल्स १.१ से थंड / ०.०२ से कॅशमधून; माउंटमधील ओव्हरराइड इंजिनप्रमाणेच सोडवले जातात.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> मॉडेल — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

आवृत्त्या ४४, ४८, ४९. सांगाडा, मेश, सर्व तपशील स्तर, बॉडी ग्रुप. १ ५०० मॉडेल लोड, ० अपयश.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> मटेरियल — <code>.vmt</code>

सर्व १९ ५५४ मटेरियल वाचली जातात; `patch`, DX ब्लॉक, प्रॉक्सी.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> टेक्सचर — <code>.vtf</code>

आवृत्त्या ७.०–७.५, DXT1/3/5 आणि सर्व असंपीडित फॉरमॅट, क्यूबमॅप, मिप. DXT डिकोड न करता GPU कडे जाते.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> सेशन — <code>.dmx</code>

बायनरी १–५ आणि KeyValues2. इन्स्टॉलमधील प्रत्येक सेशन आणि पार्टिकल फाइल **बाइट बाय बाइट** परत लिहिली जाते.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> पडद्यावर सेशन

टाइमलाइनवर शॉट्स आणि साउंड ट्रॅक, एलिमेंट ट्री, प्रत्येक शॉटचे दृश्य त्याच्या कॅमेऱ्यातून. अजून नाही: नकाशे, पार्टिकल, आवाज.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> अॅनिमेशन

कर्सरवर चॅनेल आणि लॉग मूल्यांकित; स्क्रब आणि प्ले. हाडे, कॅमेरे आणि दृश्यमानता सेशनचे अनुसरण करतात.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> चेहरे

Flex कंट्रोलर, संकलित नियम आणि व्हर्टेक्स अॅनिमेशन — पात्रे बोलतात आणि भाव दाखवतात. अजून नाही: सुरकुत्या नकाशे.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> रिग

एक्सप्रेशन, point/orient/parent/aim कन्स्ट्रेंट, दोन-हाडांचा IK. अजून नाही: पूर्ण ऑपरेटर अवलंबित्व आलेख, रिग निर्मिती.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> संपादन

क्लिकने निवड, मूव्ह/रोटेट मॅनिप्युलेटर, कोणत्याही अॅट्रिब्यूटसाठी इन्स्पेक्टर, कर्सरवर की, अनडू/रीडू, बाइट-अचूक सेव्ह.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> मोशन एडिटर

रूलरवर होल्ड आणि फॉलऑफसह वेळ निवड; संपादन SFM प्रमाणे त्यावर पसरते. अजून नाही: प्रीसेट, लेयर.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> ग्राफ एडिटर

निवडलेल्या एलिमेंटला चालवणाऱ्या प्रत्येक लॉगचे वक्र: X/Y/Z, pitch/yaw/roll, स्केलर. की लाइव्ह पूर्वावलोकनासह वेळ आणि मूल्यात ओढता येतात, डबल-क्लिक जोडते, Delete काढते; वेळ अक्ष टाइमलाइनचा. अजून नाही: टँजंट आणि वक्र प्रकार, की गटाचे स्केलिंग.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> पॅनेल डॉकिंग

UE5 आणि Visual Studio प्रमाणे, पूर्वावलोकनासह लक्ष्यांच्या कंपासवर पॅनेल ओढा. अजून नाही: जतन केलेली मांडणी, थीम.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source शेडिंग

फक्त टेक्सचर आणि साधा प्रकाश. अजून नाही: phong, rim, lightwarp, दृश्य प्रकाश, सावल्या.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> नकाशे — <code>.bsp</code>

सुरू केले नाही.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> प्रतिमा आणि व्हिडिओमध्ये रेंडर

सुरू केले नाही.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> प्लगइन <code>.c2plg</code>

सुरू केले नाही.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> थीम आणि वर्कस्पेस

मुद्दाम नंतर: एडिटरमध्ये सजवण्यासारखे काही येईपर्यंत एकच रूप.

**रिलीजसाठी तयार नाही.** पाया — SFM वापरणारा प्रत्येक फाइल फॉरमॅट, योग्य वाचलेला आणि संपूर्ण इन्स्टॉलेशनवर तपासलेला — आहे आणि चाचणी केलेला; सेशन उघडता, चालवता, बदलता आणि जतन करता येते. कमी आहे कामाची *सोय*: ग्राफ एडिटर, Source शेडिंग, नकाशे, निर्यात. अॅनिमेटर यात दिवसभर काम करू शकेपर्यंत आवृत्ती क्रमांक नाही.

<p align="center"><a href="../../README/MR-in.md"><img alt="← README कडे परत" src="https://img.shields.io/badge/%E2%86%90_README_%E0%A4%95%E0%A4%A1%E0%A5%87_%E0%A4%AA%E0%A4%B0%E0%A4%A4-1b2838?style=for-the-badge"></a></p>
