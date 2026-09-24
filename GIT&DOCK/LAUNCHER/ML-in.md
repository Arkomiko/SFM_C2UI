# C2UI ലോഞ്ചർ

<details align="center"><summary>&nbsp;🌐 <b>🇮🇳 മലയാളം</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><b>🇮🇳<br>മലയാളം</b></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` ആണ് പദ്ധതി ആരംഭിക്കുന്ന ഇടം: തലക്കെട്ട്, ഒരു വരി വിവരണം, മൂന്ന് ബട്ടണുകൾ എന്നിവയുള്ള ചെറിയ ഇരുണ്ട ജാലകം. Python ഇൻസ്റ്റാൾ ചെയ്യേണ്ടാത്ത ഒറ്റ എക്സിക്യൂട്ടബിളായി ഇത് നിർമ്മിക്കപ്പെടുന്നു; പദ്ധതി സ്വയം കണ്ടെത്തുന്നു — `App`, `Core`, `Launcher` ഒരുമിച്ച് കാണുന്നത് വരെ സ്വന്തം സ്ഥാനത്ത് നിന്ന് മുകളിലേക്ക് പോകുന്നു.

<p align="center"><img src="../assets/launcher.png" alt="C2UI ലോഞ്ചർ" width="562"><br><sub>ലോഞ്ചർ ജാലകം: «Dev-mode» തലക്കെട്ട്, വിവരണ വരി, മൂന്ന് ബട്ടണുകൾ.</sub></p>

> [!NOTE]
> **ലോഞ്ചറിന്റെ ഇന്റർഫേസ് ഇപ്പോൾ റഷ്യൻ ഭാഷയിൽ മാത്രമാണ് — ഇത് താൽക്കാലിക പരിഹാരമാണ്.** തലക്കെട്ടും വിവരണവും ബട്ടൺ എഴുത്തുകളും കോഡിൽ തന്നെയുണ്ട്; പൂർത്തിയായ App-നായി ലോഞ്ചർ വീണ്ടും എഴുതുമ്പോൾ എഡിറ്ററിന്റെ പ്രാദേശികവൽക്കരണത്തോടൊപ്പം (`Tools/Localization`) വിവർത്തനങ്ങൾ വരും. പദ്ധതിയുടെ മറ്റ് രേഖകൾ ഇപ്പോൾ തന്നെ 32 ഭാഷകളിലുണ്ട്.

## മൂന്ന് ബട്ടണുകൾ

| | |
|---|---|
| <code>Запустить Core</code> | എഡിറ്റർ തുറക്കുന്നു — വ്യൂപോർട്ട്, ടൈംലൈൻ, പാനലുകൾ ഉള്ള C2UI ജാലകം. |
| <code>Запустить App</code> | നിഷ്ക്രിയം: വേറിട്ട App ഇതുവരെ ഇല്ല. |
| <code>Выйти</code> | ലോഞ്ചർ അടയ്ക്കുന്നു. |

## സോഴ്സിൽ നിന്ന് പ്രവർത്തിപ്പിക്കൽ

Windows, Python 3.13, ഇൻസ്റ്റാൾ ചെയ്ത Source Filmmaker വേണം.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

ഒറ്റ ഫയൽ `Launcher/Launcher-C2UI.exe` നിർമ്മാണം (git-ൽ സൂക്ഷിക്കുന്നില്ല — സോഴ്സിൽ നിന്ന് വീണ്ടും നിർമ്മിക്കുന്നു):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## എഡിറ്റർ ഇല്ലാത്ത എഞ്ചിൻ

`Launcher/core.py` `Core` മാത്രം പ്രവർത്തിപ്പിക്കുന്നു: ഒരു ഇൻസ്റ്റാളേഷൻ മൗണ്ട് ചെയ്ത്, സൂചിക ഉണ്ടാക്കി, എഞ്ചിനു മുകളിൽ ഒരു ചെറിയ ഷെൽ നൽകുന്നു — മോഡലുകൾ, മെറ്റീരിയലുകൾ, ടെക്സ്ചറുകൾ, മാപ്പുകൾ, സെഷനുകൾ, അവയുടെ കണക്കുകൂട്ടൽ. ഇതും താൽക്കാലികം: App ജാലകമില്ലാതെ പ്രവർത്തിക്കുമ്പോൾ എഡിറ്ററായിരിക്കും ഏക പ്രവേശന കവാടം.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## പിന്നീട് എന്ത് മാറും

- App വരുമ്പോൾ ജാലകം വീണ്ടും എഴുതും — രൂപവും വിവർത്തനങ്ങളും ഉൾപ്പെടെ.
- «Запустить App» ബട്ടൺ പ്രവർത്തിക്കാൻ തുടങ്ങും.
- എഡിറ്റർ ജാലകമില്ലാതെ തുറക്കാനായാൽ `core.py` ഒഴിവാകും.
- നിർമ്മിച്ച `.exe` GitHub റിലീസുകൾക്കൊപ്പം നൽകും.

<p align="center"><a href="../README/ML-in.md"><img alt="← README-ലേക്ക് മടങ്ങുക" src="https://img.shields.io/badge/%E2%86%90_README-%E0%B4%B2%E0%B5%87%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%8D_%E0%B4%AE%E0%B4%9F%E0%B4%99%E0%B5%8D%E0%B4%99%E0%B5%81%E0%B4%95-1b2838?style=for-the-badge"></a></p>
