# C2UI લૉન્ચર

<details align="center"><summary>&nbsp;🌐 <b>🇮🇳 ગુજરાતી</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><b>🇮🇳<br>ગુજરાતી</b></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` એ જ છે જ્યાંથી પ્રોજેક્ટ શરૂ થાય છે: શીર્ષક, એક લીટીનું વર્ણન અને ત્રણ બટનવાળી નાની ઘેરી વિન્ડો. તે એક જ એક્ઝિક્યુટેબલમાં બને છે જેને Python ઇન્સ્ટોલ કરવાની જરૂર નથી, અને પ્રોજેક્ટ જાતે શોધી લે છે — પોતાના સ્થાનથી ઉપર જતાં જ્યાં સુધી `App`, `Core` અને `Launcher` સાથે ન દેખાય.

<p align="center"><img src="../assets/launcher.png" alt="C2UI લૉન્ચર" width="562"><br><sub>લૉન્ચરની વિન્ડો: «Dev-mode» શીર્ષક, વર્ણનની લીટી અને ત્રણ બટન.</sub></p>

> [!NOTE]
> **લૉન્ચરનું ઇન્ટરફેસ હાલ ફક્ત રશિયનમાં છે — આ કામચલાઉ ઉકેલ છે.** શીર્ષક, વર્ણન અને બટનોના શબ્દો કોડમાં લખેલા છે; અનુવાદ એડિટરના સ્થાનિકીકરણ (`Tools/Localization`) સાથે ત્યારે આવશે જ્યારે તૈયાર App માટે લૉન્ચર ફરી લખાશે. પ્રોજેક્ટના બાકીના દસ્તાવેજો પહેલેથી 32 ભાષાઓમાં છે.

## ત્રણ બટન

| | |
|---|---|
| <code>Запустить Core</code> | એડિટર શરૂ કરે છે — વ્યૂપોર્ટ, ટાઇમલાઇન અને પેનલવાળી C2UI વિન્ડો. |
| <code>Запустить App</code> | નિષ્ક્રિય: અલગ App હજી નથી. |
| <code>Выйти</code> | લૉન્ચર બંધ કરે છે. |

## સ્રોતમાંથી ચલાવવું

Windows, Python 3.13 અને ઇન્સ્ટોલ કરેલ Source Filmmaker જોઈએ.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

એક જ ફાઇલ `Launcher/Launcher-C2UI.exe` બનાવવી (git માં રાખવામાં આવતી નથી — સ્રોતમાંથી ફરી બને છે):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## એડિટર વગરનું એન્જિન

`Launcher/core.py` માત્ર `Core` ચલાવે છે: ઇન્સ્ટોલેશન માઉન્ટ કરે છે, ઇન્ડેક્સ બનાવે છે અને એન્જિન પર નાનું શેલ આપે છે — મોડેલ, મટીરિયલ, ટેક્સચર, નકશા, સેશન અને તેમની ગણતરી. આ પણ કામચલાઉ: App વિન્ડો વગર ચાલવા લાગે ત્યારે એડિટર જ એકમાત્ર પ્રવેશદ્વાર રહેશે.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## આગળ શું બદલાશે

- App આવતાં વિન્ડો ફરી લખાશે — દેખાવ અને અનુવાદ સાથે.
- «Запустить App» બટન કામ કરવા લાગશે.
- એડિટર વિન્ડો વગર શરૂ થઈ શકે ત્યારે `core.py` જશે.
- બનેલી `.exe` GitHub પ્રકાશનો સાથે અપાશે.

<p align="center"><a href="../README/GU-in.md"><img alt="← README પર પાછા" src="https://img.shields.io/badge/%E2%86%90_README_%E0%AA%AA%E0%AA%B0_%E0%AA%AA%E0%AA%BE%E0%AA%9B%E0%AA%BE-1b2838?style=for-the-badge"></a></p>
