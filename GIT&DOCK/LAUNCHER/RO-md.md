# Launcher-ul C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇲🇩 Moldovenească</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><b>🇲🇩<br>Moldovenească</b></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` este de unde pornește proiectul: o fereastră mică și întunecată cu un titlu, o linie de descriere și trei butoane. Se construiește într-un singur executabil care nu are nevoie de Python instalat și găsește singur proiectul — urcă din locul în care se află până vede `App`, `Core` și `Launcher` împreună.

<p align="center"><img src="../assets/launcher.png" alt="Launcher-ul C2UI" width="562"><br><sub>Fereastra launcher-ului: titlul „Dev-mode”, linia de descriere și trei butoane.</sub></p>

> [!NOTE]
> **Interfața launcher-ului este deocamdată doar în rusă — o soluție temporară.** Titlul, descrierea și textele butoanelor sunt scrise în cod; traducerile vin odată cu localizarea editorului (`Tools/Localization`), când launcher-ul va fi rescris pentru un App gata. Restul documentației proiectului există deja în 32 de limbi.

## Cele trei butoane

| | |
|---|---|
| <code>Запустить Core</code> | Pornește editorul — fereastra C2UI cu viewport, cronologie și panouri. |
| <code>Запустить App</code> | Dezactivat: nu există încă un App separat. |
| <code>Выйти</code> | Închide launcher-ul. |

## Pornire din surse

Sunt necesare Windows, Python 3.13 și o instalare de Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Construirea fișierului unic `Launcher/Launcher-C2UI.exe` (nu se ține în git — se reconstruiește din surse):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Motorul fără editor

`Launcher/core.py` pornește `Core` singur: montează o instalare, o indexează și oferă o mică consolă peste motor — modele, materiale, texturi, hărți, sesiuni și evaluarea lor. Tot temporar: când App va rula fără fereastră, editorul devine unicul punct de intrare.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Ce urmează

- Fereastra va fi rescrisă odată cu App — cu aspect și traduceri.
- Butonul „Запустить App” va începe să funcționeze.
- `core.py` dispare când editorul poate fi pornit fără fereastră.
- Executabilul construit va însoți lansările de pe GitHub.

<p align="center"><a href="../README/RO-md.md"><img alt="← Înapoi la README" src="https://img.shields.io/badge/%E2%86%90_%C3%8Enapoi_la_README-1b2838?style=for-the-badge"></a></p>
