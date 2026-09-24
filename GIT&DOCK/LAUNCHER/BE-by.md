# Лаўнчар C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇧🇾 Беларуская</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><b>🇧🇾<br>Беларуская</b></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` — тое, з чаго запускаецца праект: маленькае цёмнае акно з назвай, радком апісання і трыма кнопкамі. Яно збіраецца ў адзін выканальны файл, якому не патрэбны ўсталяваны Python, і знаходзіць праект само — ідзе ўверх ад свайго месца, пакуль не ўбачыць побач `App`, `Core` і `Launcher`.

<p align="center"><img src="../assets/launcher.png" alt="Лаўнчар C2UI" width="562"><br><sub>Акно лаўнчара: загаловак «Dev-mode», радок апісання і тры кнопкі.</sub></p>

> [!NOTE]
> **Інтэрфейс лаўнчара пакуль толькі па-руску — гэта часовае рашэнне.** Загаловак, апісанне і подпісы кнопак зашытыя ў код; пераклады з'явяцца разам з лакалізацыяй рэдактара (`Tools/Localization`), калі лаўнчар перапішуць пад гатовы App. Астатняя дакументацыя праекта ўжо даступная на 32 мовах.

## Тры кнопкі

| | |
|---|---|
| <code>Запустить Core</code> | Запускае рэдактар — акно C2UI з в'юпартам, таймлайнам і панэлямі. |
| <code>Запустить App</code> | Пакуль неактыўная: асобнай праграмы App яшчэ няма. |
| <code>Выйти</code> | Зачыняе лаўнчар. |

## Запуск з зыходнікаў

Патрэбныя Windows, Python 3.13 і ўсталяваны Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Зборка ў адзін файл `Launcher/Launcher-C2UI.exe` (у git не захоўваецца — перазбіраецца з зыходнікаў):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Рухавік без рэдактара

`Launcher/core.py` запускае `Core` асобна: манціруе ўсталёўку, індэксуе яе і дае невялікую абалонку над рухавіком — мадэлі, матэрыялы, тэкстуры, карты, сесіі і іх вылічэнне. Таксама часова: калі App будзе працаваць без акна, адзінай кропкай уваходу стане рэдактар.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Што будзе далей

- Акно перапішуць, калі з'явіцца App, — разам з афармленнем і перакладамі.
- Кнопка «Запустить App» запрацуе.
- `core.py` пойдзе, як толькі рэдактар можна будзе запускаць без акна.
- Гатовы `.exe` будуць дадаваць да рэлізаў на GitHub.

<p align="center"><a href="../README/BE-by.md"><img alt="← Назад да README" src="https://img.shields.io/badge/%E2%86%90_%D0%9D%D0%B0%D0%B7%D0%B0%D0%B4_%D0%B4%D0%B0_README-1b2838?style=for-the-badge"></a></p>
