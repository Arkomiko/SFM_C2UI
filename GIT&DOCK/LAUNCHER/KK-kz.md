# C2UI лаунчері

<details align="center"><summary>&nbsp;🌐 <b>🇰🇿 Қазақша</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><b>🇰🇿<br>Қазақша</b></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` — жобаны іске қосатын нәрсе: атауы, бір жол сипаттамасы және үш түймесі бар шағын қара терезе. Ол Python орнатуды қажет етпейтін бір орындалатын файлға жиналады және жобаны өзі табады — `App`, `Core` және `Launcher` қатар тұрғанын көргенше өз орнынан жоғары қарай жүреді.

<p align="center"><img src="../assets/launcher.png" alt="C2UI лаунчері" width="562"><br><sub>Лаунчер терезесі: «Dev-mode» тақырыбы, сипаттама жолы және үш түйме.</sub></p>

> [!NOTE]
> **Лаунчер интерфейсі әзірге тек орысша — бұл уақытша шешім.** Тақырып, сипаттама және түйме жазулары кодқа енгізілген; аудармалар редактор локализациясымен бірге (`Tools/Localization`), лаунчер дайын App үшін қайта жазылғанда келеді. Жобаның қалған құжаттамасы қазірдің өзінде 32 тілде.

## Үш түйме

| | |
|---|---|
| <code>Запустить Core</code> | Редакторды іске қосады — вьюпорты, таймлайны және панельдері бар C2UI терезесі. |
| <code>Запустить App</code> | Әзірге белсенді емес: бөлек App әлі жоқ. |
| <code>Выйти</code> | Лаунчерді жабады. |

## Бастапқы кодтан іске қосу

Windows, Python 3.13 және орнатылған Source Filmmaker қажет.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Бір `Launcher/Launcher-C2UI.exe` файлын құрастыру (git-те сақталмайды — бастапқы кодтан қайта жиналады):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Редакторсыз қозғалтқыш

`Launcher/core.py` `Core`-ды жеке іске қосады: орнатуды монттайды, индекстейді және қозғалтқыш үстінде шағын қабық береді — модельдер, материалдар, текстуралар, карталар, сессиялар және оларды есептеу. Бұл да уақытша: App терезесіз жұмыс істей бастағанда, жалғыз кіру нүктесі редактор болады.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Әрі қарай не болады

- App пайда болғанда терезе қайта жазылады — безендіру мен аудармалармен бірге.
- «Запустить App» түймесі жұмыс істей бастайды.
- Редакторды терезесіз іске қосуға болатын болса, `core.py` кетеді.
- Дайын `.exe` GitHub релиздеріне қосылады.

<p align="center"><a href="../README/KK-kz.md"><img alt="← README-ге қайту" src="https://img.shields.io/badge/%E2%86%90_README-%D0%B3%D0%B5_%D2%9B%D0%B0%D0%B9%D1%82%D1%83-1b2838?style=for-the-badge"></a></p>
