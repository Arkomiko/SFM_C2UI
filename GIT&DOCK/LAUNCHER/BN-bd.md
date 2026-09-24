# C2UI লঞ্চার

<details align="center"><summary>&nbsp;🌐 <b>🇧🇩 বাংলা</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><b>🇧🇩<br>বাংলা</b></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` হলো যেখান থেকে প্রকল্প চালু হয়: শিরোনাম, এক লাইনের বিবরণ ও তিনটি বোতামসহ একটি ছোট গাঢ় উইন্ডো। এটি একটিমাত্র এক্সিকিউটেবলে তৈরি হয় যার জন্য Python ইনস্টল থাকার দরকার নেই, এবং প্রকল্প নিজেই খুঁজে নেয় — নিজের জায়গা থেকে উপরে গিয়ে যতক্ষণ না `App`, `Core` ও `Launcher` একসঙ্গে দেখা যায়।

<p align="center"><img src="../assets/launcher.png" alt="C2UI লঞ্চার" width="562"><br><sub>লঞ্চার উইন্ডো: «Dev-mode» শিরোনাম, বিবরণের লাইন ও তিনটি বোতাম।</sub></p>

> [!NOTE]
> **লঞ্চারের ইন্টারফেস এখন কেবল রুশ ভাষায় — এটি সাময়িক সমাধান।** শিরোনাম, বিবরণ ও বোতামের লেখা কোডে বসানো; অনুবাদ আসবে এডিটরের স্থানীয়করণের (`Tools/Localization`) সঙ্গে, যখন প্রস্তুত App-এর জন্য লঞ্চার নতুন করে লেখা হবে। প্রকল্পের বাকি নথিপত্র এখনই ৩২টি ভাষায় আছে।

## তিনটি বোতাম

| | |
|---|---|
| <code>Запустить Core</code> | এডিটর চালু করে — ভিউপোর্ট, টাইমলাইন ও প্যানেলসহ C2UI উইন্ডো। |
| <code>Запустить App</code> | নিষ্ক্রিয়: আলাদা App এখনও নেই। |
| <code>Выйти</code> | লঞ্চার বন্ধ করে। |

## সোর্স থেকে চালানো

দরকার Windows, Python 3.13 এবং ইনস্টল করা Source Filmmaker।

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

একক ফাইল `Launcher/Launcher-C2UI.exe` তৈরি করা (git-এ রাখা হয় না — সোর্স থেকে আবার বানানো হয়):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## এডিটর ছাড়া ইঞ্জিন

`Launcher/core.py` কেবল `Core` চালায়: ইনস্টলেশন মাউন্ট করে, ইনডেক্স বানায় এবং ইঞ্জিনের উপর একটি ছোট শেল দেয় — মডেল, ম্যাটেরিয়াল, টেক্সচার, ম্যাপ, সেশন ও তাদের হিসাব। এটিও সাময়িক: App উইন্ডো ছাড়া চলতে পারলে এডিটরই একমাত্র প্রবেশপথ হবে।

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## পরে কী বদলাবে

- App এলে উইন্ডো নতুন করে লেখা হবে — চেহারা ও অনুবাদসহ।
- «Запустить App» বোতাম কাজ করতে শুরু করবে।
- এডিটর উইন্ডো ছাড়া চালু করা গেলে `core.py` বিদায় নেবে।
- তৈরি `.exe` GitHub রিলিজের সঙ্গে দেওয়া হবে।

<p align="center"><a href="../README/BN-bd.md"><img alt="← README-এ ফিরুন" src="https://img.shields.io/badge/%E2%86%90_README-%E0%A6%8F_%E0%A6%AB%E0%A6%BF%E0%A6%B0%E0%A7%81%E0%A6%A8-1b2838?style=for-the-badge"></a></p>
