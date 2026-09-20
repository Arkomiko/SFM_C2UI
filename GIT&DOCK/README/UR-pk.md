<p align="center"><img src="../assets/UR-pk/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <b>🇵🇰 اردو</b> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%D8%AD%D8%A7%D9%84%D8%AA-%D9%BE%D8%B1%DB%8C--%D8%A7%D9%84%D9%81%D8%A7-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%D9%B9%DB%8C%D8%B3%D9%B9-340-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — جدید خول میں Source Filmmaker کا ایڈیٹر: وہی مواد، وہی سیشن فارمیٹ، وہی ڈیٹا ماڈل، اور Steam لائبریری و Unreal Engine 5 ایڈیٹر کے انداز کا انٹرفیس۔</p>

---

## خیال

Source Filmmaker ایک مضبوط ٹول ہے جس کا انٹرفیس 2012 میں رہ گیا۔ C2UI اسے بدلتا یا دوبارہ نہیں بناتا: مقصد بس SFM کو تھوڑا جدید اور آسان بنانا ہے۔

ایڈیٹر انسٹال شدہ SFM کو ڈھونڈتا ہے، اسے مواد کی لائبریری کے طور پر جوڑتا ہے — ماڈل، میٹیریل، ٹیکسچر، سیشن — اور انہی فائلوں کے ساتھ اسی فارمیٹ میں کام کرتا ہے۔ SFM میں بنی ہر چیز C2UI میں کھلتی ہے، اور اس کے برعکس بھی۔

پہلا مقصد ہڈیوں اور رگز سمیت SFM کے ساتھ مکمل مطابقت ہے۔ اس کے بعد — جو SFM میں کم تھا۔

```
  ┌──────────────┐    "SFM کہاں؟"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  اپنا UI     │ ◀─────   ماؤنٹ   ───────│    tf/  hl2/  tf_movies/ …   │
  │  اپنا رینڈر  │       صرف پڑھنا       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## تیاری

<img align="right" src="../assets/UR-pk/sidebar.svg" alt="تیاری" width="300">

<img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>ریلیز کے لیے مجموعی تیاری: 38%</b>

ہر حصہ کھلتا ہے: کیا پہلے سے کام کرتا ہے اور کیا ابھی نہیں۔ فیصد SFM کی صلاحیتوں کے مقابلے ایک اندازہ ہے۔

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM تلاش کرنا اور ماؤنٹ کرنا</b></summary>

Steam رجسٹری → `libraryfolders.vdf` → `gameinfo.txt` کے سرچ پاتھ، انجن کی ترتیب میں۔ معیاری انسٹال پر چھ ماؤنٹ۔ ایپلیکیشن فولڈر کے باہر کچھ نہیں لکھا جاتا۔

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>مواد کا انڈیکس</b></summary>

70 199 فائلیں 1.1 سیکنڈ ٹھنڈا / 0.02 سیکنڈ کیش سے؛ ماؤنٹس کے درمیان اوور رائیڈ بالکل انجن کی طرح حل ہوتے ہیں۔

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>ماڈل — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

ورژن 44، 48، 49۔ ڈھانچہ، میش، تمام تفصیلی سطحیں، باڈی گروپ۔ 1 500 ماڈل لوڈ، 0 ناکامی۔

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>میٹیریل — <code>.vmt</code></b></summary>

تمام 19 554 میٹیریل پڑھے جاتے ہیں؛ `patch`، DX بلاک، پراکسی۔

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>ٹیکسچر — <code>.vtf</code></b></summary>

ورژن 7.0–7.5، DXT1/3/5 اور تمام غیر کمپریسڈ فارمیٹ، کیوب میپ، مِپ۔ DXT بغیر ڈی کوڈ GPU میں جاتا ہے۔

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>سیشن — <code>.dmx</code></b></summary>

بائنری 1–5 اور KeyValues2۔ انسٹال کا ہر سیشن اور پارٹیکل فائل **بائٹ بہ بائٹ** واپس لکھی جاتی ہے۔

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>اسکرین پر سیشن</b></summary>

ٹائم لائن پر شاٹس اور ساؤنڈ ٹریک، ایلیمنٹ ٹری، ہر شاٹ کا منظر اس کے کیمرے سے۔ ابھی نہیں: نقشے، پارٹیکل، آواز۔

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>اینیمیشن</b></summary>

کرسر پر چینل اور لاگ کا اندازہ؛ اسکرب اور پلے۔ ہڈیاں، کیمرے اور مرئیت سیشن کی پیروی کرتے ہیں۔

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>چہرے</b></summary>

Flex کنٹرولر، کمپائل شدہ قواعد اور ورٹیکس اینیمیشن — کردار بولتے اور تاثرات دکھاتے ہیں۔ ابھی نہیں: جھریوں کے نقشے۔

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>رگز</b></summary>

ایکسپریشن، point/orient/parent/aim کنسٹرینٹ، دو ہڈی IK۔ ابھی نہیں: مکمل آپریٹر انحصار گراف، رگ بنانا۔

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>ایڈیٹنگ</b></summary>

کلک سے انتخاب، موو/روٹیٹ مینیپولیٹر، کسی بھی ایٹریبیوٹ کا انسپکٹر، کرسر پر کی، انڈو/ریڈو، بائٹ درست سیو۔ ابھی نہیں: گراف ایڈیٹر۔

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>موشن ایڈیٹر</b></summary>

رولر پر ہولڈ اور فال آف کے ساتھ وقت کا انتخاب؛ ترمیم SFM کی طرح اس پر پھیلتی ہے۔ ابھی نہیں: پری سیٹ، لیئر۔

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>پینل ڈاکنگ</b></summary>

UE5 اور Visual Studio کی طرح، پیش نظارہ کے ساتھ اہداف کے کمپاس پر پینل گھسیٹیں۔ ابھی نہیں: محفوظ لے آؤٹ، تھیم۔

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source شیڈنگ</b></summary>

صرف ٹیکسچر اور سادہ روشنی۔ ابھی نہیں: phong، rim، lightwarp، منظر کی روشنیاں، سائے۔

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>نقشے — <code>.bsp</code></b></summary>

شروع نہیں ہوا۔

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>تصویر اور ویڈیو میں رینڈر</b></summary>

شروع نہیں ہوا۔

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>پلگ ان <code>.c2plg</code></b></summary>

شروع نہیں ہوا۔

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>تھیم اور ورک اسپیس</b></summary>

جان بوجھ کر بعد میں: ایک ہی شکل جب تک ایڈیٹر میں سجانے کے قابل کچھ نہ ہو۔

</details>

**ریلیز کے لیے تیار نہیں۔** بنیاد — SFM کا ہر فائل فارمیٹ، صحیح پڑھا اور پوری انسٹالیشن پر جانچا گیا — موجود اور ٹیسٹ شدہ ہے؛ سیشن کھولا، چلایا، بدلا اور محفوظ کیا جا سکتا ہے۔ کمی ہے کام کی *سہولت* کی: گراف ایڈیٹر، Source شیڈنگ، نقشے، ایکسپورٹ۔ جب تک کوئی اینیمیٹر اس میں ایک دن کا کام نہ کر سکے، کوئی ورژن نمبر نہیں۔

<br clear="all">

<p align="center"><img src="../assets/editor.png" alt="Meet the Heavy کھلا ہوا ایڈیٹر" width="100%"><br><sub>آج کا ایڈیٹر، Valve کا Meet the Heavy کھلا ہوا: ٹائم لائن پر شاٹس اور آواز، سیشن ٹری، پہلا شاٹ اپنے کیمرے سے، سیشن کے مطابق پوز اور چہروں والے کردار۔</sub></p>

## کیا مختلف ہے

- **پورٹیبل۔** ایپلیکیشن فولڈر کے باہر کچھ نہیں لکھا جاتا: سیٹنگز `App/User` میں، کیش `App/Cache` میں، عارضی `App/Temporary` میں۔ فولڈر حذف کریں اور کوئی نشان نہیں۔
- **SFM کبھی نہیں چلاتا۔** چلانے کا کوئی پروسیس نہیں، قبضے کی کوئی ونڈو نہیں۔ انسٹالیشن مواد کے پیک کی طرح پڑھی جاتی ہے۔
- **فارمیٹ تصدیق شدہ، مفروضہ نہیں۔** ہر ریڈر اصل انسٹالیشن سے جانچا گیا؛ جہاں فارمیٹ کچھ غیر متوقع کرتا ہے، کوڈ بتاتا ہے۔
- **سیو درست ہے۔** بغیر تبدیلی پڑھا اور لکھا سیشن وہی فائل ہے۔
- **انجن کا کوئی انحصار نہیں۔** `Core/` اور پورا ٹیسٹ سوٹ خالص Python پر چلتا ہے؛ صرف ونڈو کو Qt اور OpenGL چاہیے۔

## چلانا

Windows، Python 3.13 اور Source Filmmaker انسٹالیشن درکار۔

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

پہلی بار Steam سے SFM تلاش کرتا ہے؛ نہ ملے تو پوچھتا ہے۔ <kbd>Ctrl</kbd>+<kbd>O</kbd> سیشن کھولتا ہے، <kbd>Space</kbd> پلے، <kbd>C</kbd> شاٹ کیمرہ، <kbd>T</kbd>/<kbd>R</kbd> موو/روٹیٹ، <kbd>M</kbd> موشن ایڈیٹر، <kbd>Ctrl</kbd>+<kbd>Z</kbd> انڈو، <kbd>Ctrl</kbd>+<kbd>S</kbd> سیو۔ پینل عنوان سے گھسیٹے جاتے ہیں۔ ٹیسٹ کو کچھ نہیں چاہیے:

```bash
python Testing/run.py
```

## ساخت

```
C2UI_SDK/
├── c2ui.py            لانچر
├── Core/              انجن: فارمیٹ، ورچوئل فائل سسٹم، انڈیکس، برج
├── App/               ایڈیٹر: مواد لائبریری، رینڈرر، ونڈو
├── Tools/             لوکلائزیشن، UI ٹولز، پلگ ان (بعد میں)
├── Testing/           ٹیسٹ، بائٹ درست فکسچر، ایک رنر
└── GIT&DOCK/README/   یہ README دیگر زبانوں میں
```

## روڈ میپ

1. **گراف ایڈیٹر** — کرو اور کیز، آنکھوں کے سامنے۔
2. **Source شیڈنگ** — VertexLitGeneric جیسے SFM بناتا ہے: phong، rim، lightwarp، منظر کی روشنیاں۔
3. **نقشے** — پس منظر کے لیے `.bsp`۔
4. **آؤٹ پٹ** — تصویر اور ویڈیو ایکسپورٹ۔
5. **پلگ ان** — `.c2plg` فارمیٹ؛ پھر تھیم اور ورک اسپیس۔

## لائسنس اور اعتراف

Source Filmmaker، Team Fortress 2 اور Source انجن Valve کے ہیں۔ یہ پروجیکٹ ان کے فائل فارمیٹ پڑھتا ہے، ان کی کوئی فائل شامل نہیں کرتا، اور صرف Steam سے آپ کی اپنی SFM کاپی کے ساتھ کام کرتا ہے۔

C2UI کے اپنے کوڈ کا لائسنس ابھی منتخب نہیں ہوا — تب تک جملہ حقوق محفوظ۔ Issues اور pull requests پھر بھی خوش آمدید۔

<p align="center"><img src="../assets/models.png" alt="انسٹالیشن سے براہ راست رینڈر کیے 64 ماڈل" width="60%"><br><sub>انسٹالیشن سے بے ترتیب چنے چونسٹھ ماڈل، C2UI کے اپنے رینڈرر سے بنائے گئے۔</sub></p>
