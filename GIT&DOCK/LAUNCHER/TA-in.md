# C2UI துவக்கி

<details align="center"><summary>&nbsp;🌐 <b>🇮🇳 தமிழ்</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><b>🇮🇳<br>தமிழ்</b></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` தான் திட்டம் தொடங்கும் இடம்: தலைப்பு, ஒரு வரி விளக்கம், மூன்று பொத்தான்கள் கொண்ட சிறிய கரும் சாளரம். Python நிறுவப்படாமலே இயங்கும் ஒற்றைச் செயற்கோப்பாக இது கட்டப்படுகிறது; திட்டத்தைத் தானே கண்டறியும் — தான் இருக்கும் இடத்திலிருந்து மேலே சென்று `App`, `Core`, `Launcher` ஒன்றாகத் தெரியும் வரை.

<p align="center"><img src="../assets/launcher.png" alt="C2UI துவக்கி" width="562"><br><sub>துவக்கியின் சாளரம்: «Dev-mode» தலைப்பு, விளக்க வரி, மூன்று பொத்தான்கள்.</sub></p>

> [!NOTE]
> **துவக்கியின் இடைமுகம் தற்போது ரஷ்ய மொழியில் மட்டுமே — இது தற்காலிகத் தீர்வு.** தலைப்பு, விளக்கம், பொத்தான் எழுத்துகள் நிரலிலேயே எழுதப்பட்டுள்ளன; திருத்தியின் மொழிபெயர்ப்புடன் (`Tools/Localization`), முடிந்த App-க்காக துவக்கி மீண்டும் எழுதப்படும்போது மொழிபெயர்ப்புகள் வரும். திட்டத்தின் மற்ற ஆவணங்கள் ஏற்கெனவே 32 மொழிகளில் உள்ளன.

## மூன்று பொத்தான்கள்

| | |
|---|---|
| <code>Запустить Core</code> | திருத்தியைத் தொடங்குகிறது — காட்சிப்பகுதி, காலவரிசை, பலகங்கள் கொண்ட C2UI சாளரம். |
| <code>Запустить App</code> | செயலிழந்தது: தனி App இன்னும் இல்லை. |
| <code>Выйти</code> | துவக்கியை மூடுகிறது. |

## மூலக் குறியீட்டிலிருந்து இயக்குதல்

Windows, Python 3.13 மற்றும் நிறுவப்பட்ட Source Filmmaker தேவை.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

ஒற்றைக் கோப்பு `Launcher/Launcher-C2UI.exe` கட்டுதல் (git-இல் வைக்கப்படுவதில்லை — மூலத்திலிருந்து மீண்டும் கட்டப்படுகிறது):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## திருத்தி இல்லாத எஞ்சின்

`Launcher/core.py` `Core`-ஐ மட்டும் இயக்குகிறது: நிறுவலை ஏற்றி, அட்டவணைப்படுத்தி, எஞ்சின் மீது ஒரு சிறிய ஷெல் தருகிறது — மாதிரிகள், பொருட்கள், அமைப்புகள், வரைபடங்கள், அமர்வுகள், அவற்றின் கணிப்பு. இதுவும் தற்காலிகமே: App சாளரம் இன்றி இயங்கத் தொடங்கியதும் திருத்தியே ஒரே நுழைவாயிலாகும்.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## அடுத்து என்ன மாறும்

- App உருவானதும் சாளரம் மீண்டும் எழுதப்படும் — வடிவமும் மொழிபெயர்ப்பும் சேர்ந்து.
- «Запустить App» பொத்தான் வேலை செய்யத் தொடங்கும்.
- திருத்தியை சாளரம் இன்றி தொடங்க முடிந்ததும் `core.py` நீங்கும்.
- கட்டப்பட்ட `.exe` GitHub வெளியீடுகளுடன் இணைக்கப்படும்.

<p align="center"><a href="../README/TA-in.md"><img alt="← README க்குத் திரும்பு" src="https://img.shields.io/badge/%E2%86%90_README_%E0%AE%95%E0%AF%8D%E0%AE%95%E0%AF%81%E0%AE%A4%E0%AF%8D_%E0%AE%A4%E0%AE%BF%E0%AE%B0%E0%AF%81%E0%AE%AE%E0%AF%8D%E0%AE%AA%E0%AF%81-1b2838?style=for-the-badge"></a></p>
