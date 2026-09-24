# C2UI-startaren

<details align="center"><summary>&nbsp;🌐 <b>🇸🇪 Svenska</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><b>🇸🇪<br>Svenska</b></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` är det projektet startas från: ett litet mörkt fönster med en titel, en beskrivningsrad och tre knappar. Det byggs till en enda körbar fil som inte behöver installerad Python, och hittar projektet själv — det går uppåt från sin plats tills det ser `App`, `Core` och `Launcher` tillsammans.

<p align="center"><img src="../assets/launcher.png" alt="C2UI-startaren" width="562"><br><sub>Startarens fönster: titeln ”Dev-mode”, beskrivningsraden och tre knappar.</sub></p>

> [!NOTE]
> **Startarens gränssnitt är än så länge bara på ryska — en tillfällig lösning.** Titeln, beskrivningen och knapptexterna står i koden; översättningarna kommer med redigerarens lokalisering (`Tools/Localization`) när startaren skrivs om för ett färdigt App. Projektets övriga dokumentation finns redan på 32 språk.

## De tre knapparna

| | |
|---|---|
| <code>Запустить Core</code> | Startar redigeraren — C2UI-fönstret med vy, tidslinje och paneler. |
| <code>Запустить App</code> | Nedtonad: något separat App finns ännu inte. |
| <code>Выйти</code> | Stänger startaren. |

## Köra från källkoden

Windows, Python 3.13 och en installerad Source Filmmaker behövs.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Bygga den enda filen `Launcher/Launcher-C2UI.exe` (inte i git — den byggs om från källkoden):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Motorn utan redigeraren

`Launcher/core.py` startar `Core` för sig: monterar en installation, indexerar den och ger ett litet skal över motorn — modeller, material, texturer, kartor, sessioner och deras utvärdering. Också tillfälligt: när App kan köras utan fönster blir redigeraren enda ingången.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Vad som händer sedan

- Fönstret skrivs om när App finns — med utseende och översättningar.
- Knappen ”Запустить App” börjar fungera.
- `core.py` försvinner när redigeraren kan startas utan fönster.
- Den byggda `.exe`-filen bifogas GitHub-utgåvorna.

<p align="center"><a href="../README/SV-se.md"><img alt="← Tillbaka till README" src="https://img.shields.io/badge/%E2%86%90_Tillbaka_till_README-1b2838?style=for-the-badge"></a></p>
