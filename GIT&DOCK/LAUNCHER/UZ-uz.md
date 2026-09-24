# C2UI launcher'i

<details align="center"><summary>&nbsp;🌐 <b>🇺🇿 Oʻzbekcha</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><b>🇺🇿<br>Oʻzbekcha</b></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` — loyiha ishga tushadigan joy: sarlavha, bir qator tavsif va uchta tugmali kichik qorong'i oyna. U o'rnatilgan Python talab qilmaydigan bitta bajariladigan faylga yig'iladi va loyihani o'zi topadi — o'z joyidan yuqoriga yurib, `App`, `Core` va `Launcher` yonma-yon ko'ringunicha.

<p align="center"><img src="../assets/launcher.png" alt="C2UI launcher'i" width="562"><br><sub>Launcher oynasi: «Dev-mode» sarlavhasi, tavsif qatori va uchta tugma.</sub></p>

> [!NOTE]
> **Launcher interfeysi hozircha faqat rus tilida — bu vaqtinchalik yechim.** Sarlavha, tavsif va tugma yozuvlari kodning o'zida; tarjimalar muharrir mahalliylashtirilishi (`Tools/Localization`) bilan birga, launcher tayyor App uchun qayta yozilganda keladi. Loyihaning qolgan hujjatlari allaqachon 32 tilda.

## Uchta tugma

| | |
|---|---|
| <code>Запустить Core</code> | Muharrirni ishga tushiradi — vyuport, taymlayn va panellari bilan C2UI oynasi. |
| <code>Запустить App</code> | Faol emas: alohida App hali yo'q. |
| <code>Выйти</code> | Launcher'ni yopadi. |

## Manbadan ishga tushirish

Windows, Python 3.13 va o'rnatilgan Source Filmmaker kerak.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Bitta `Launcher/Launcher-C2UI.exe` faylini yig'ish (git da saqlanmaydi — manbadan qayta yig'iladi):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Muharrirsiz dvigatel

`Launcher/core.py` `Core`ni yolg'iz ishga tushiradi: o'rnatmani ulaydi, indekslaydi va dvigatel ustida kichik qobiq beradi — modellar, materiallar, teksturalar, xaritalar, seanslar va ularni hisoblash. Bu ham vaqtinchalik: App oynasiz ishlay boshlagach, muharrir yagona kirish nuqtasi bo'ladi.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Keyin nima o'zgaradi

- App paydo bo'lgach oyna qayta yoziladi — ko'rinishi va tarjimalari bilan.
- «Запустить App» tugmasi ishlay boshlaydi.
- Muharrirni oynasiz ishga tushirish mumkin bo'lgach `core.py` ketadi.
- Yig'ilgan `.exe` GitHub relizlariga qo'shiladi.

<p align="center"><a href="../README/UZ-uz.md"><img alt="← README ga qaytish" src="https://img.shields.io/badge/%E2%86%90_README_ga_qaytish-1b2838?style=for-the-badge"></a></p>
