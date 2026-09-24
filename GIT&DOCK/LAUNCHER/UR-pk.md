# C2UI لانچر

<details align="center"><summary>&nbsp;🌐 <b>🇵🇰 اردو</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><b>🇵🇰<br>اردو</b></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` وہی ہے جہاں سے منصوبہ شروع ہوتا ہے: عنوان، ایک سطر کی تفصیل اور تین بٹنوں والی ایک چھوٹی گہری ونڈو۔ یہ ایک ہی قابلِ عمل فائل میں بنتی ہے جسے نصب شدہ Python کی ضرورت نہیں، اور منصوبہ خود ڈھونڈ لیتی ہے — اپنی جگہ سے اوپر جاتے ہوئے جب تک `App`، `Core` اور `Launcher` ساتھ نظر نہ آئیں۔

<p align="center"><img src="../assets/launcher.png" alt="C2UI لانچر" width="562"><br><sub>لانچر کی ونڈو: «Dev-mode» عنوان، تفصیل کی سطر اور تین بٹن۔</sub></p>

> [!NOTE]
> **لانچر کا انٹرفیس فی الحال صرف روسی میں ہے — یہ عارضی حل ہے۔** عنوان، تفصیل اور بٹنوں کے الفاظ کوڈ میں لکھے ہیں؛ ترجمے ایڈیٹر کی لوکلائزیشن (`Tools/Localization`) کے ساتھ تب آئیں گے جب مکمل App کے لیے لانچر دوبارہ لکھا جائے گا۔ منصوبے کی باقی دستاویزات پہلے ہی 32 زبانوں میں ہیں۔

## تین بٹن

| | |
|---|---|
| <code>Запустить Core</code> | ایڈیٹر شروع کرتا ہے — ویو پورٹ، ٹائم لائن اور پینلز والی C2UI ونڈو۔ |
| <code>Запустить App</code> | غیر فعال: الگ App ابھی نہیں ہے۔ |
| <code>Выйти</code> | لانچر بند کرتا ہے۔ |

## سورس سے چلانا

Windows، Python 3.13 اور نصب شدہ Source Filmmaker درکار ہیں۔

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

واحد فائل `Launcher/Launcher-C2UI.exe` بنانا (git میں نہیں رکھی جاتی — سورس سے دوبارہ بنتی ہے):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## ایڈیٹر کے بغیر انجن

`Launcher/core.py` صرف `Core` چلاتا ہے: ایک انسٹالیشن ماؤنٹ کرتا ہے، اس کا اشاریہ بناتا ہے اور انجن پر ایک چھوٹا شیل دیتا ہے — ماڈلز، میٹیریلز، ٹیکسچرز، نقشے، سیشنز اور ان کا حساب۔ یہ بھی عارضی ہے: جب App بغیر ونڈو چل سکے گا تو ایڈیٹر ہی واحد داخلی راستہ رہے گا۔

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## آگے کیا بدلے گا

- App کے ساتھ ونڈو دوبارہ لکھی جائے گی — شکل اور ترجموں سمیت۔
- «Запустить App» بٹن کام کرنے لگے گا۔
- ایڈیٹر بغیر ونڈو چلنے لگا تو `core.py` ختم ہو جائے گا۔
- بنی ہوئی `.exe` GitHub ریلیزز کے ساتھ دی جائے گی۔

<p align="center"><a href="../README/UR-pk.md"><img alt="← README پر واپس" src="https://img.shields.io/badge/%E2%86%90_README_%D9%BE%D8%B1_%D9%88%D8%A7%D9%BE%D8%B3-1b2838?style=for-the-badge"></a></p>
