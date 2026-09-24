# Launcher C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇮🇩 Basa Jawa</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><b>🇮🇩<br>Basa Jawa</b></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` yaiku papan proyek diwiwiti: jendhela peteng cilik kanthi irah-irahan, sakbaris katrangan lan telung tombol. Iki dibangun dadi siji berkas eksekutabel sing ora butuh Python diinstal, lan nemokake proyek dhewe — munggah saka panggonane nganti weruh `App`, `Core` lan `Launcher` bareng.

<p align="center"><img src="../assets/launcher.png" alt="Launcher C2UI" width="562"><br><sub>Jendhela launcher: irah-irahan «Dev-mode», baris katrangan lan telung tombol.</sub></p>

> [!NOTE]
> **Tampilan launcher saiki mung basa Rusia — iki solusi sauntara.** Irah-irahan, katrangan lan tulisan tombol ditulis ing kode; terjemahan bakal teka bareng lokalisasi editor (`Tools/Localization`), nalika launcher ditulis maneh kanggo App sing wis rampung. Dokumentasi liyane wis ana ing 32 basa.

## Telung tombol

| | |
|---|---|
| <code>Запустить Core</code> | Miwiti editor — jendhela C2UI kanthi viewport, garis wektu lan panel. |
| <code>Запустить App</code> | Ora aktif: App kapisah durung ana. |
| <code>Выйти</code> | Nutup launcher. |

## Mlaku saka sumber

Butuh Windows, Python 3.13 lan Source Filmmaker sing wis diinstal.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Mbangun siji berkas `Launcher/Launcher-C2UI.exe` (ora disimpen ing git — dibangun maneh saka sumber):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Mesin tanpa editor

`Launcher/core.py` miwiti `Core` dhewe: masang instalasi, nggawe indeks lan menehi cangkang cilik ing ndhuwur mesin — model, material, tekstur, peta, sesi lan etungane. Iki uga sauntara: yen App bisa mlaku tanpa jendhela, editor dadi siji-sijine lawang mlebu.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Sing bakal owah

- Jendhela ditulis maneh bareng App — kalebu rupa lan terjemahan.
- Tombol «Запустить App» wiwit mlaku.
- `core.py` ilang yen editor bisa diwiwiti tanpa jendhela.
- Berkas `.exe` sing wis dibangun bakal melu rilis ing GitHub.

<p align="center"><a href="../README/JV-id.md"><img alt="← Bali menyang README" src="https://img.shields.io/badge/%E2%86%90_Bali_menyang_README-1b2838?style=for-the-badge"></a></p>
