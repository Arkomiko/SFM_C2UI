# مشغّل C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇸🇦 العربية</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><b>🇸🇦<br>العربية</b></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` هو ما يبدأ منه المشروع: نافذة داكنة صغيرة فيها عنوان وسطر وصف وثلاثة أزرار. تُبنى في ملف تنفيذي واحد لا يحتاج إلى Python مثبَّت، وتجد المشروع بنفسها — تصعد من موضعها حتى ترى `App` و`Core` و`Launcher` معًا.

<p align="center"><img src="../assets/launcher.png" alt="مشغّل C2UI" width="562"><br><sub>نافذة المشغّل: عنوان «Dev-mode» وسطر الوصف وثلاثة أزرار.</sub></p>

> [!NOTE]
> **واجهة المشغّل بالروسية فقط حتى الآن — وهو حل مؤقت.** العنوان والوصف ونصوص الأزرار مكتوبة في الشيفرة؛ وستأتي الترجمات مع توطين المحرّر (`Tools/Localization`) حين يُعاد كتابة المشغّل من أجل App مكتمل. أمّا بقية وثائق المشروع فمتاحة بالفعل بـ 32 لغة.

## الأزرار الثلاثة

| | |
|---|---|
| <code>Запустить Core</code> | يشغّل المحرّر — نافذة C2UI بمنظورها وخطها الزمني ولوحاتها. |
| <code>Запустить App</code> | معطّل: لا يوجد App منفصل بعد. |
| <code>Выйти</code> | يغلق المشغّل. |

## التشغيل من المصدر

يلزم Windows وPython 3.13 ونسخة مثبَّتة من Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

بناء الملف الواحد `Launcher/Launcher-C2UI.exe` (لا يُحفظ في git — يُعاد بناؤه من المصدر):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## المحرّك بلا محرّر

يشغّل `Launcher/core.py` المحرّك `Core` وحده: يركّب تثبيتًا ويفهرسه ويمنح صدفة صغيرة فوق المحرّك — النماذج والخامات والأنسجة والخرائط والجلسات وتقييمها. وهو مؤقت أيضًا: متى عمل App بلا نافذة صار المحرّر نقطة الدخول الوحيدة.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## ما سيتغيّر لاحقًا

- ستُعاد كتابة النافذة مع App — بالمظهر والترجمات.
- سيبدأ زر «Запустить App» بالعمل.
- يزول `core.py` حين يمكن تشغيل المحرّر بلا نافذة.
- سيرافق الملف التنفيذي المبني إصدارات GitHub.

<p align="center"><a href="../README/AR-sa.md"><img alt="← العودة إلى README" src="https://img.shields.io/badge/%E2%86%90_%D8%A7%D9%84%D8%B9%D9%88%D8%AF%D8%A9_%D8%A5%D9%84%D9%89_README-1b2838?style=for-the-badge"></a></p>
