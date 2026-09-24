# Zaganjalnik C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇸🇮 Slovenščina</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><b>🇸🇮<br>Slovenščina</b></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` je tisto, iz česar se projekt zažene: majhno temno okno z naslovom, eno vrstico opisa in tremi gumbi. Zgradi se v eno izvršljivo datoteko, ki ne potrebuje nameščenega Pythona, projekt pa najde sam — od svojega mesta gre navzgor, dokler ne vidi `App`, `Core` in `Launcher` skupaj.

<p align="center"><img src="../assets/launcher.png" alt="Zaganjalnik C2UI" width="562"><br><sub>Okno zaganjalnika: naslov »Dev-mode«, vrstica opisa in trije gumbi.</sub></p>

> [!NOTE]
> **Vmesnik zaganjalnika je zaenkrat le v ruščini — začasna rešitev.** Naslov, opis in napisi na gumbih so zapisani v kodi; prevodi pridejo skupaj z lokalizacijo urejevalnika (`Tools/Localization`), ko bo zaganjalnik prepisan za dokončan App. Preostala dokumentacija projekta je že v 32 jezikih.

## Trije gumbi

| | |
|---|---|
| <code>Запустить Core</code> | Zažene urejevalnik — okno C2UI s pogledom, časovnico in ploščami. |
| <code>Запустить App</code> | Onemogočen: samostojnega App še ni. |
| <code>Выйти</code> | Zapre zaganjalnik. |

## Zagon iz izvorne kode

Potrebni so Windows, Python 3.13 in nameščen Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Gradnja ene datoteke `Launcher/Launcher-C2UI.exe` (ni v gitu — zgradi se iz izvorne kode):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Pogon brez urejevalnika

`Launcher/core.py` zažene `Core` sam: namesti namestitev, jo indeksira in ponudi majhno lupino nad pogonom — modele, materiale, teksture, zemljevide, seje in njihov izračun. Prav tako začasno: ko bo App tekel brez okna, bo urejevalnik edina vstopna točka.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Kaj sledi

- Okno bo prepisano skupaj z App — z videzom in prevodi.
- Gumb »Запустить App« bo začel delovati.
- `core.py` izgine, ko bo urejevalnik mogoče zagnati brez okna.
- Zgrajeni `.exe` bo priložen izdajam na GitHubu.

<p align="center"><a href="../README/SL-si.md"><img alt="← Nazaj na README" src="https://img.shields.io/badge/%E2%86%90_Nazaj_na_README-1b2838?style=for-the-badge"></a></p>
