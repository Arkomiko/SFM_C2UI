<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <b>🇮🇳 മലയാളം</b> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E0%B4%A8%E0%B4%BF%E0%B4%B2-%E0%B4%AA%E0%B5%8D%E0%B4%B0%E0%B5%80--%E0%B4%86%E0%B5%BD%E0%B4%AB-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E0%B4%9F%E0%B5%86%E0%B4%B8%E0%B5%8D%E0%B4%B1%E0%B5%8D%E0%B4%B1%E0%B5%81%E0%B4%95%E0%B5%BE-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — Source Filmmaker എഡിറ്ററിന്റെ എന്റെ പുനർനിർമ്മാണമാണ്: അതേ ഉള്ളടക്കം, അതേ സെഷൻ ഫോർമാറ്റ്, അതേ ഡേറ്റാ മോഡൽ — Steam ലൈബ്രറിയിൽ നിന്ന് രൂപവും Unreal Engine 5 എഡിറ്ററിൽ നിന്ന് ലേഔട്ടും കടമെടുത്ത ഒരു ഷെല്ലിനുള്ളിൽ.</p>

---

## ആശയം

Source Filmmaker 2012-ലെ ഇന്റർഫേസുള്ള മികച്ച ഉപകരണമാണ്. `sfm.exe`-ന് മുകളിൽ ഒരു സ്കിൻ ഇടാൻ എനിക്ക് താൽപ്പര്യമില്ല, അതിന്റെ വിൻഡോകൾ ഒന്നൊന്നായി പിടിച്ചെടുക്കാനും താൽപ്പര്യമില്ല. **SFM എവിടെ ഇൻസ്റ്റാൾ ചെയ്തിട്ടുണ്ടെന്ന് ചോദിക്കുന്ന**, Garry's Mod Counter-Strike മൗണ്ട് ചെയ്യുന്നതുപോലെ ആ ഇൻസ്റ്റാളേഷൻ മൗണ്ട് ചെയ്യുന്ന, ആ ഫയലുകൾക്ക് മുകളിൽ എല്ലാം സ്വയം ചെയ്യുന്ന — മോഡലുകൾ, മെറ്റീരിയലുകൾ, ടെക്സ്ചറുകൾ, സെഷനുകൾ, ആനിമേഷൻ — SFM ഒരിക്കലും തുറക്കാത്ത ഒരു എഡിറ്റർ എനിക്ക് വേണം.

ലക്ഷ്യം **SFM-മായി ഒന്നിനൊന്ന് ഫീച്ചർ തുല്യത** (എല്ലുകളും റിഗുകളും ഉൾപ്പെടെ), പിന്നെ SFM-ന് ഒരിക്കലും ലഭിക്കാത്തവ.

```
  ┌──────────────┐    "SFM എവിടെ?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  സ്വന്തം UI    │ ◀─────   മൗണ്ട്    ───────│    tf/  hl2/  tf_movies/ …   │
  │  സ്വന്തം റെൻഡർ │      വായന മാത്രം       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## തയ്യാറെടുപ്പ്

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>റിലീസിനുള്ള മൊത്തം തയ്യാറെടുപ്പ്: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy തുറന്ന എഡിറ്റർ" width="100%"><br><sub>ഇന്നത്തെ എഡിറ്റർ, Valve-ന്റെ Meet the Heavy തുറന്ന്: ടൈംലൈനിൽ ഷോട്ടുകളും ശബ്ദവും, സെഷൻ ട്രീ, സ്വന്തം കാമറയിലൂടെ ആദ്യ ഷോട്ട്, സെഷൻ പറയുന്നതുപോലെ പോസും മുഖഭാവവുമുള്ള കഥാപാത്രങ്ങൾ.</sub></p>

എന്താണ് ചെയ്തത്, എന്താണ് ചെയ്യാത്തത് എന്ന് കാണാൻ ഒരു മേഖല വികസിപ്പിക്കുക. ശതമാനങ്ങൾ SFM-ന് ചെയ്യാനാവുന്നതിനെതിരെ എന്റെ സത്യസന്ധമായ കണക്കാണ്.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM കണ്ടെത്തലും മൗണ്ടിംഗും</b></summary>

Steam രജിസ്ട്രി → `libraryfolders.vdf` → `gameinfo.txt`-ന്റെ തിരയൽ പാതകൾ, എഞ്ചിന്റെ ക്രമത്തിൽ. സാധാരണ ഇൻസ്റ്റാളിൽ ആറ് മൗണ്ടുകൾ. ആപ്ലിക്കേഷൻ ഫോൾഡറിന് പുറത്ത് ഒന്നും എഴുതുന്നില്ല.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>ഉള്ളടക്ക സൂചിക</b></summary>

70 199 ഫയലുകൾ 1.1 സെ തണുത്ത / 0.02 സെ കാഷിൽ നിന്ന്; മൗണ്ടുകൾക്കിടയിലെ ഓവർറൈഡുകൾ എഞ്ചിൻ പോലെ തന്നെ പരിഹരിക്കുന്നു.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>മോഡലുകൾ — `.mdl` `.vvd` `.vtx`</b></summary>

പതിപ്പുകൾ 44, 48, 49. അസ്ഥികൂടം, മെഷുകൾ, എല്ലാ വിശദാംശ തലങ്ങളും, ബോഡി ഗ്രൂപ്പുകൾ. 1 500 മോഡലുകൾ ലോഡ്, 0 പരാജയങ്ങൾ.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>മെറ്റീരിയലുകൾ — `.vmt`</b></summary>

എല്ലാ 19 554 മെറ്റീരിയലുകളും വായിക്കുന്നു; `patch`, DX ബ്ലോക്കുകൾ, പ്രോക്സികൾ.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>ടെക്സ്ചറുകൾ — `.vtf`</b></summary>

പതിപ്പുകൾ 7.0–7.5, DXT1/3/5 ഉം എല്ലാ കംപ്രസ് ചെയ്യാത്ത ഫോർമാറ്റുകളും, ക്യൂബ്മാപ്പുകൾ, മിപ്പുകൾ. DXT ഡീകോഡ് ചെയ്യാതെ GPU-ലേക്ക്.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>സെഷനുകൾ — `.dmx`</b></summary>

ബൈനറി 1–5 ഉം KeyValues2 ഉം. ഇൻസ്റ്റാളിലെ ഓരോ സെഷനും പാർട്ടിക്കിൽ ഫയലും **ബൈറ്റ് ബൈ ബൈറ്റ്** തിരികെ എഴുതുന്നു.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>സ്ക്രീനിലെ സെഷൻ</b></summary>

ടൈംലൈനിൽ ഷോട്ടുകളും സൗണ്ട് ട്രാക്കുകളും, എലമെന്റ് ട്രീ, ഓരോ ഷോട്ടിന്റെ രംഗം അതിന്റെ കാമറയിലൂടെ. ഇതുവരെ ഇല്ല: മാപ്പുകൾ, പാർട്ടിക്കിളുകൾ, ശബ്ദം.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>ആനിമേഷൻ</b></summary>

കഴ്‌സറിൽ ചാനലുകളും ലോഗുകളും വിലയിരുത്തുന്നു; സ്ക്രബും പ്ലേയും. എല്ലുകൾ, കാമറകൾ, ദൃശ്യത സെഷനെ പിന്തുടരുന്നു.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>മുഖങ്ങൾ</b></summary>

Flex കൺട്രോളറുകൾ, കംപൈൽ ചെയ്ത നിയമങ്ങൾ, വെർട്ടക്സ് ആനിമേഷൻ — കഥാപാത്രങ്ങൾ സംസാരിക്കുന്നു, ഭാവങ്ങൾ കാണിക്കുന്നു. ഇതുവരെ ഇല്ല: ചുളിവ് മാപ്പുകൾ.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>റിഗുകൾ</b></summary>

എക്സ്പ്രഷനുകൾ, point/orient/parent/aim കൺസ്ട്രെയിന്റുകൾ, രണ്ട്-എല്ല് IK. ഇതുവരെ ഇല്ല: പൂർണ്ണ ഓപ്പറേറ്റർ ആശ്രിതത്വ ഗ്രാഫ്, റിഗ് നിർമ്മാണം.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>എഡിറ്റിംഗ്</b></summary>

ക്ലിക്ക് ചെയ്ത് തിരഞ്ഞെടുക്കൽ, മൂവ്/റൊട്ടേറ്റ് മാനിപ്പുലേറ്റർ, ഏത് ആട്രിബ്യൂട്ടിനും ഇൻസ്പെക്ടർ, കഴ്‌സറിൽ കീ, അൻഡു/റീഡു, ബൈറ്റ്-കൃത്യമായ സേവ്. ഇതുവരെ ഇല്ല: ഗ്രാഫ് എഡിറ്റർ.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>മോഷൻ എഡിറ്റർ</b></summary>

റൂളറിൽ ഹോൾഡും ഫോൾഓഫുമുള്ള സമയ തിരഞ്ഞെടുപ്പ്; എഡിറ്റ് SFM പോലെ അതിൽ പരക്കുന്നു. ഇതുവരെ ഇല്ല: പ്രീസെറ്റുകൾ, ലെയറുകൾ.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>പാനൽ ഡോക്കിംഗ്</b></summary>

UE5-ലും Visual Studio-യിലും പോലെ, പ്രിവ്യൂവുള്ള ലക്ഷ്യ കോമ്പസിലേക്ക് പാനലുകൾ വലിച്ചിടുക. ഇതുവരെ ഇല്ല: സേവ് ചെയ്ത ലേഔട്ടുകൾ, തീമുകൾ.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source ഷേഡിംഗ്</b></summary>

ടെക്സ്ചറും ലളിതമായ വെളിച്ചവും മാത്രം. ഇതുവരെ ഇല്ല: phong, rim, lightwarp, രംഗ വെളിച്ചങ്ങൾ, നിഴലുകൾ.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>മാപ്പുകൾ — `.bsp`</b></summary>

തുടങ്ങിയിട്ടില്ല.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>ചിത്രത്തിലേക്കും വീഡിയോയിലേക്കും റെൻഡർ</b></summary>

തുടങ്ങിയിട്ടില്ല.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>പ്ലഗിനുകൾ `.c2plg`</b></summary>

തുടങ്ങിയിട്ടില്ല.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>തീമുകളും വർക്ക്‌സ്‌പേസുകളും</b></summary>

മനഃപൂർവ്വം പിന്നീട്: എഡിറ്ററിൽ അലങ്കരിക്കാൻ യോഗ്യമായത് വരുന്നതുവരെ ഒരു രൂപം.

</details>

**റിലീസിന് തയ്യാറല്ല.** അടിത്തറ — SFM ഉപയോഗിക്കുന്ന ഓരോ ഫയൽ ഫോർമാറ്റും, ശരിയായി വായിച്ച് മുഴുവൻ ഇൻസ്റ്റാളേഷനിലും പരിശോധിച്ചത് — ഉണ്ട്, ടെസ്റ്റ് ചെയ്തിട്ടുണ്ട്; ഒരു സെഷൻ തുറക്കാം, പ്ലേ ചെയ്യാം, മാറ്റാം, സേവ് ചെയ്യാം. ഇല്ലാത്തത് ജോലിയുടെ *സൗകര്യം*: ഗ്രാഫ് എഡിറ്റർ, Source ഷേഡിംഗ്, മാപ്പുകൾ, എക്സ്പോർട്ട്. ഒരു ആനിമേറ്റർ ഇതിൽ ഒരു ദിവസത്തെ ജോലി ചെയ്യാനാവുന്നതുവരെ വേർഷൻ നമ്പർ ഇല്ല.

## വ്യത്യാസം എന്ത്

- **പോർട്ടബിൾ.** ആപ്ലിക്കേഷൻ ഫോൾഡറിന് പുറത്ത് ഒന്നും എഴുതുന്നില്ല: സെറ്റിംഗുകൾ `App/User`, കാഷ് `App/Cache`, താൽക്കാലികം `App/Temporary`. ഫോൾഡർ ഇല്ലാതാക്കൂ, ഒരു അടയാളവുമില്ല.
- **SFM ഒരിക്കലും പ്രവർത്തിപ്പിക്കുന്നില്ല.** നിയന്ത്രിക്കാൻ പ്രോസസ്സില്ല, പിടിച്ചെടുക്കാൻ വിൻഡോകളില്ല. ഇൻസ്റ്റാളേഷൻ ഒരു ഉള്ളടക്ക പാക്ക് പോലെ വായിക്കുന്നു.
- **ഫോർമാറ്റുകൾ പരിശോധിച്ചത്, ഊഹിച്ചതല്ല.** ഓരോ റീഡറും യഥാർത്ഥ ഇൻസ്റ്റാളേഷനുമായി ഒത്തുനോക്കി; ഫോർമാറ്റ് അപ്രതീക്ഷിതമായത് ചെയ്യുന്നിടത്ത് കോഡ് പറയുന്നു.
- **സേവ് കൃത്യമാണ്.** മാറ്റമില്ലാതെ വായിച്ച് എഴുതിയ സെഷൻ അതേ ഫയലാണ്.
- **എഞ്ചിന് ആശ്രിതത്വങ്ങളില്ല.** `Core/` ഉം മുഴുവൻ ടെസ്റ്റ് സ്യൂട്ടും ശുദ്ധ Python-ൽ ഓടുന്നു; വിൻഡോയ്ക്ക് മാത്രം Qt ഉം OpenGL ഉം വേണം.

## പ്രവർത്തിപ്പിക്കൽ

Windows, Python 3.13, Source Filmmaker ഇൻസ്റ്റാളേഷൻ ആവശ്യമാണ്.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

ആദ്യ തുടക്കത്തിൽ Steam വഴി SFM തിരയുന്നു; കിട്ടിയില്ലെങ്കിൽ ചോദിക്കുന്നു. <kbd>Ctrl</kbd>+<kbd>O</kbd> സെഷൻ തുറക്കുന്നു, <kbd>Space</kbd> പ്ലേ, <kbd>C</kbd> ഷോട്ട് കാമറ, <kbd>T</kbd>/<kbd>R</kbd> മൂവ്/റൊട്ടേറ്റ്, <kbd>M</kbd> മോഷൻ എഡിറ്റർ, <kbd>Ctrl</kbd>+<kbd>Z</kbd> അൻഡു, <kbd>Ctrl</kbd>+<kbd>S</kbd> സേവ്. പാനലുകൾ തലക്കെട്ടിൽ പിടിച്ച് വലിക്കുന്നു. ടെസ്റ്റുകൾക്ക് ഒന്നും വേണ്ട:

```bash
python Testing/run.py
```

## ഘടന

```
C2UI_SDK/
├── c2ui.py            ലോഞ്ചർ
├── Core/              എഞ്ചിൻ: ഫോർമാറ്റുകൾ, വെർച്വൽ ഫയൽ സിസ്റ്റം, സൂചിക, പാലങ്ങൾ
├── App/               എഡിറ്റർ: ഉള്ളടക്ക ലൈബ്രറി, റെൻഡറർ, വിൻഡോ
├── Tools/             പ്രാദേശികവൽക്കരണം, UI ഉപകരണങ്ങൾ, പ്ലഗിനുകൾ (പിന്നീട്)
├── Testing/           ടെസ്റ്റുകൾ, ബൈറ്റ്-കൃത്യ ഫിക്സ്ചറുകൾ, ഒരു റണ്ണർ
└── GIT&DOCK/README/   ഈ README മറ്റ് ഭാഷകളിൽ
```

## റോഡ്‌മാപ്പ്

1. **ഗ്രാഫ് എഡിറ്റർ** — വളവുകളും കീകളും, കണ്ണിന് മുന്നിൽ.
2. **Source ഷേഡിംഗ്** — SFM വരയ്ക്കുന്നതുപോലെ VertexLitGeneric: phong, rim, lightwarp, രംഗ വെളിച്ചങ്ങൾ.
3. **മാപ്പുകൾ** — പശ്ചാത്തലത്തിന് `.bsp`.
4. **ഔട്ട്‌പുട്ട്** — ചിത്രവും വീഡിയോയും എക്സ്പോർട്ട്.
5. **പ്ലഗിനുകൾ** — `.c2plg` ഫോർമാറ്റ്; പിന്നെ തീമുകളും വർക്ക്‌സ്‌പേസുകളും.

## ലൈസൻസും കടപ്പാടും

Source Filmmaker, Team Fortress 2, Source എഞ്ചിൻ Valve-ന്റേതാണ്. ഈ പ്രോജക്റ്റ് അവരുടെ ഫയൽ ഫോർമാറ്റുകൾ വായിക്കുന്നു, അവരുടെ ഒരു ഫയലും ഉൾപ്പെടുത്തുന്നില്ല, Steam വഴി നിങ്ങൾക്ക് ഇതിനകം ഉള്ള SFM പകർപ്പുമായി മാത്രം പ്രവർത്തിക്കുന്നു.

C2UI-യുടെ സ്വന്തം കോഡിന്റെ ലൈസൻസ് ഇതുവരെ തിരഞ്ഞെടുത്തിട്ടില്ല — അതുവരെ എല്ലാ അവകാശങ്ങളും നിക്ഷിപ്തം. Issues ഉം pull requests ഉം സ്വാഗതം.

<p align="center"><img src="../../.github/assets/models.png" alt="ഇൻസ്റ്റാളേഷനിൽ നിന്ന് നേരിട്ട് റെൻഡർ ചെയ്ത 64 മോഡലുകൾ" width="60%"><br><sub>ഇൻസ്റ്റാളേഷനിൽ നിന്ന് ക്രമരഹിതമായി തിരഞ്ഞെടുത്ത അറുപത്തിനാല് മോഡലുകൾ, C2UI-യുടെ സ്വന്തം റെൻഡറർ വരച്ചത്.</sub></p>
