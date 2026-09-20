<p align="center"><img src="../assets/AR-sa/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <b>🇸🇦 العربية</b> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%D8%A7%D9%84%D8%AD%D8%A7%D9%84%D8%A9-%D9%82%D8%A8%D9%84--%D8%A3%D9%84%D9%81%D8%A7-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%D8%A7%D8%AE%D8%AA%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — محرّر Source Filmmaker في غلاف حديث: المحتوى نفسه، صيغة الجلسات نفسها، نموذج البيانات نفسه، وواجهة بروح مكتبة Steam ومحرّر Unreal Engine 5.</p>

---

## الجاهزية

<p align="center"><img src="../assets/AR-sa/sidebar.svg" alt="الجاهزية" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>الجاهزية الإجمالية للإصدار: 41%</b></p>

<p align="center"><a href="../assets/AR-sa/sidebar.md"><img alt="الجاهزية بالتفصيل" src="https://img.shields.io/badge/%D8%A7%D9%84%D8%AC%D8%A7%D9%87%D8%B2%D9%8A%D8%A9_%D8%A8%D8%A7%D9%84%D8%AA%D9%81%D8%B5%D9%8A%D9%84-66c0f4?style=for-the-badge"></a></p>

## الفكرة

Source Filmmaker أداة قوية بقيت واجهتها في عام 2012. لا يستبدله C2UI ولا يعيد صنعه: الهدف ببساطة جعل SFM أكثر حداثة وراحة قليلًا.

يجد المحرّر SFM المثبّت، ويربطه كمكتبة محتوى — النماذج والمواد والقوام والجلسات — ويعمل مع الملفات نفسها بالصيغة نفسها. كل ما صُنع في SFM يُفتح في C2UI، والعكس صحيح.

الهدف الأول هو التوافق الكامل مع SFM بما فيه العظام والريغات. بعد ذلك، ما كان ينقص SFM.

```
  ┌──────────────┐    "أين SFM؟"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  واجهة خاصة  │ ◀─────   محمّل    ───────│    tf/  hl2/  tf_movies/ …   │
  │  عرض خاص     │       قراءة فقط       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="المحرّر وفيه Meet the Heavy مفتوح" width="100%"><br><sub>المحرّر اليوم، وفيه Meet the Heavy من Valve مفتوح: اللقطات والصوت على الخط الزمني، شجرة الجلسة، اللقطة الأولى من كاميرتها، والشخصيات بوضعياتها وتعابيرها كما تقول الجلسة.</sub></p>

## ما الذي يميّزه

- **محمول.** لا يُكتب شيء خارج مجلد التطبيق: الإعدادات في `App/User`، الذاكرة المخبأة في `App/Cache`، المؤقت في `App/Temporary`. احذف المجلد ولا يبقى أثر.
- **لا يشغّل SFM أبدًا.** لا عملية تُقاد ولا نوافذ تُختطف. يُقرأ التثبيت كحزمة محتوى.
- **الصيغ مُتحقَّق منها، لا مُفترَضة.** كل قارئ قُورن بالتثبيت الحقيقي؛ حيث تفعل صيغة شيئًا مفاجئًا يقول الكود ذلك.
- **الحفظ دقيق.** الجلسة المقروءة والمكتوبة دون تغيير هي الملف نفسه.
- **المحرّك بلا اعتماديات.** `Core/` وكل الاختبارات تعمل على Python خام؛ النافذة وحدها تحتاج Qt وOpenGL.

## التشغيل

يتطلب Windows وPython 3.13 وتثبيت Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

عند أول تشغيل يُبحث عن SFM عبر Steam؛ إن لم يُوجد يسأل البرنامج. <kbd>Ctrl</kbd>+<kbd>O</kbd> يفتح جلسة، <kbd>Space</kbd> تشغيل، <kbd>C</kbd> كاميرا اللقطة، <kbd>T</kbd>/<kbd>R</kbd> تحريك/تدوير، <kbd>M</kbd> محرّر الحركة، <kbd>Ctrl</kbd>+<kbd>Z</kbd> تراجع، <kbd>Ctrl</kbd>+<kbd>S</kbd> حفظ. تُسحب اللوحات من عنوانها. الاختبارات لا تحتاج شيئًا:

```bash
python Testing/run.py
```

## البنية

```
C2UI_SDK/
├── README.md
├── Core/              المحرّك: الصيغ، نظام ملفات افتراضي، الفهرس، الجسور
├── App/               المحرّر: مكتبة المحتوى، المُصيِّر، النافذة
├── Tools/             التوطين، أدوات الواجهة، الإضافات (لاحقًا)
│   └── Launcher/      المُشغِّل
├── Testing/           الاختبارات، تجهيزات دقيقة بالبايت، مشغّل واحد
└── GIT&DOCK/          هذا الـ README بلغات أخرى
```

## خارطة الطريق

1. **تظليل Source** — VertexLitGeneric كما يرسمه SFM: phong، rim، lightwarp، أضواء المشهد.
2. **الخرائط** — `.bsp` للخلفيات.
3. **الإخراج** — تصدير صورة وفيديو.
4. **الإضافات** — صيغة `.c2plg`؛ ثم السمات ومساحات العمل.

## الترخيص والشكر

كود C2UI الخاص يخضع **لرخصة C2UI**: حر للاستخدام الشخصي وغير التجاري؛ الاستخدام التجاري فقط بموافقة خطية من المؤلف؛ النسخ المعدّلة يجب أن تنسب إلى المشروع الأصلي ومؤلفه Arkomiko. الإضافات والملحقات تخضع لرخصة **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker وTeam Fortress 2 ومحرّك Source ملك Valve؛ يقرأ المشروع صيغها، ولا يرفق أي ملف منها، ويعمل فقط مع نسختك من SFM عبر Steam.

<p align="center"><a href="../LICENSE/AR-sa.md"><img alt="نص الرخصة" src="https://img.shields.io/badge/%D9%86%D8%B5_%D8%A7%D9%84%D8%B1%D8%AE%D8%B5%D8%A9-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 نموذجًا مُصيَّرة مباشرة من التثبيت" width="60%"><br><sub>أربعة وستون نموذجًا اختيرت عشوائيًا من التثبيت، رسمها مُصيِّر C2UI الخاص.</sub></p>
