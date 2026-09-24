# C2UI ଲଞ୍ଚର

<details align="center"><summary>&nbsp;🌐 <b>🇮🇳 ଓଡ଼ିଆ</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><b>🇮🇳<br>ଓଡ଼ିଆ</b></td></tr>
</table>

</details>

`Launcher/` ହିଁ ପ୍ରକଳ୍ପ ଆରମ୍ଭ ହେବା ସ୍ଥାନ: ଶିରୋନାମା, ଗୋଟିଏ ଧାଡ଼ି ବର୍ଣ୍ଣନା ଓ ତିନୋଟି ବଟନ୍ ଥିବା ଛୋଟ ଗାଢ଼ ୱିଣ୍ଡୋ। ଏହା Python ଇନ୍‌ଷ୍ଟଲ୍ ନଥିଲେ ମଧ୍ୟ ଚାଲୁଥିବା ଗୋଟିଏ ଏକଜିକ୍ୟୁଟେବଲ୍‌ରେ ତିଆରି ହୁଏ ଏବଂ ପ୍ରକଳ୍ପ ନିଜେ ଖୋଜିନିଏ — ନିଜ ସ୍ଥାନରୁ ଉପରକୁ ଯାଇ `App`, `Core` ଓ `Launcher` ଏକାଠି ଦେଖିବା ପର୍ଯ୍ୟନ୍ତ।

<p align="center"><img src="../assets/launcher.png" alt="C2UI ଲଞ୍ଚର" width="562"><br><sub>ଲଞ୍ଚର ୱିଣ୍ଡୋ: «Dev-mode» ଶିରୋନାମା, ବର୍ଣ୍ଣନା ଧାଡ଼ି ଓ ତିନୋଟି ବଟନ୍।</sub></p>

> [!NOTE]
> **ଲଞ୍ଚରର ଇଣ୍ଟରଫେସ୍ ଏବେ କେବଳ ରୁଷୀ ଭାଷାରେ — ଏହା ଅସ୍ଥାୟୀ ସମାଧାନ।** ଶିରୋନାମା, ବର୍ଣ୍ଣନା ଓ ବଟନ୍ ଲେଖା କୋଡ୍‌ରେ ଲେଖାଯାଇଛି; ଅନୁବାଦ ଏଡିଟର୍ ସ୍ଥାନୀୟକରଣ (`Tools/Localization`) ସହ ସେତେବେଳେ ଆସିବ, ଯେତେବେଳେ ପ୍ରସ୍ତୁତ App ପାଇଁ ଲଞ୍ଚର ପୁଣି ଲେଖାଯିବ। ପ୍ରକଳ୍ପର ବାକି ଦଲିଲ ଏବେ ହିଁ 32 ଭାଷାରେ ଅଛି।

## ତିନୋଟି ବଟନ୍

| | |
|---|---|
| <code>Запустить Core</code> | ଏଡିଟର୍ ଆରମ୍ଭ କରେ — ଭ୍ୟୁପୋର୍ଟ, ଟାଇମ୍‌ଲାଇନ୍ ଓ ପ୍ୟାନେଲ୍ ଥିବା C2UI ୱିଣ୍ଡୋ। |
| <code>Запустить App</code> | ନିଷ୍କ୍ରିୟ: ଅଲଗା App ଏବେ ନାହିଁ। |
| <code>Выйти</code> | ଲଞ୍ଚର ବନ୍ଦ କରେ। |

## ସୋର୍ସରୁ ଚଳାଇବା

Windows, Python 3.13 ଓ ଇନ୍‌ଷ୍ଟଲ୍ ହୋଇଥିବା Source Filmmaker ଦରକାର।

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

ଗୋଟିଏ ଫାଇଲ୍ `Launcher/Launcher-C2UI.exe` ନିର୍ମାଣ (git ରେ ରଖାଯାଏ ନାହିଁ — ସୋର୍ସରୁ ପୁଣି ତିଆରି ହୁଏ):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## ଏଡିଟର୍ ବିନା ଇଞ୍ଜିନ୍

`Launcher/core.py` କେବଳ `Core` ଚଳାଏ: ଇନ୍‌ଷ୍ଟଲେସନ୍ ମାଉଣ୍ଟ କରେ, ସୂଚକାଙ୍କ ଗଢ଼େ ଓ ଇଞ୍ଜିନ୍ ଉପରେ ଏକ ଛୋଟ ସେଲ୍ ଦିଏ — ମଡେଲ୍, ମ୍ୟାଟେରିଆଲ୍, ଟେକ୍ସଚର୍, ମ୍ୟାପ୍, ସେସନ୍ ଓ ସେମାନଙ୍କ ଗଣନା। ଏହା ମଧ୍ୟ ଅସ୍ଥାୟୀ: App ୱିଣ୍ଡୋ ବିନା ଚାଲିଲେ ଏଡିଟର୍ ହିଁ ଏକମାତ୍ର ପ୍ରବେଶ ପଥ ହେବ।

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## ପରେ କଣ ବଦଳିବ

- App ଆସିଲେ ୱିଣ୍ଡୋ ପୁଣି ଲେଖାଯିବ — ରୂପ ଓ ଅନୁବାଦ ସହ।
- «Запустить App» ବଟନ୍ କାମ କରିବ।
- ଏଡିଟର୍ ୱିଣ୍ଡୋ ବିନା ଆରମ୍ଭ ହେଲେ `core.py` ଯିବ।
- ତିଆରି `.exe` GitHub ରିଲିଜ୍ ସହ ଦିଆଯିବ।

<p align="center"><a href="../README/OR-in.md"><img alt="← README କୁ ଫେରନ୍ତୁ" src="https://img.shields.io/badge/%E2%86%90_README_%E0%AC%95%E0%AD%81_%E0%AC%AB%E0%AD%87%E0%AC%B0%E0%AC%A8%E0%AD%8D%E0%AC%A4%E0%AD%81-1b2838?style=for-the-badge"></a></p>
