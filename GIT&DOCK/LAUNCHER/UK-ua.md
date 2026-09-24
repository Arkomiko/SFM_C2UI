# Лаунчер C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇺🇦 Українська</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><b>🇺🇦<br>Українська</b></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` — те, з чого запускається проєкт: маленьке темне вікно з назвою, рядком опису та трьома кнопками. Воно збирається в один виконуваний файл, якому не потрібен встановлений Python, і знаходить проєкт саме — йде вгору від свого місця, доки не побачить поруч `App`, `Core` і `Launcher`.

<p align="center"><img src="../assets/launcher.png" alt="Лаунчер C2UI" width="562"><br><sub>Вікно лаунчера: заголовок «Dev-mode», рядок опису та три кнопки.</sub></p>

> [!NOTE]
> **Інтерфейс лаунчера поки лише російською — це тимчасове рішення.** Заголовок, опис і підписи кнопок зашиті в код; переклади з'являться разом із локалізацією редактора (`Tools/Localization`), коли лаунчер перепишуть під готовий App. Решта документації проєкту вже доступна 32 мовами.

## Три кнопки

| | |
|---|---|
| <code>Запустить Core</code> | Запускає редактор — вікно C2UI з в'юпортом, таймлайном і панелями. |
| <code>Запустить App</code> | Поки неактивна: окремого застосунку App ще немає. |
| <code>Выйти</code> | Закриває лаунчер. |

## Запуск із джерел

Потрібні Windows, Python 3.13 та встановлений Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Збірка в один файл `Launcher/Launcher-C2UI.exe` (у git не зберігається — перезбирається з джерел):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Рушій без редактора

`Launcher/core.py` запускає `Core` окремо: монтує установку, індексує її та дає невелику оболонку над рушієм — моделі, матеріали, текстури, карти, сесії та їх обчислення. Теж тимчасово: коли App працюватиме без вікна, єдиною точкою входу стане редактор.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Що буде далі

- Вікно перепишуть, коли з'явиться App, — разом з оформленням і перекладами.
- Кнопка «Запустить App» запрацює.
- `core.py` піде, щойно редактор можна буде запускати без вікна.
- Готовий `.exe` додаватимуть до релізів на GitHub.

<p align="center"><a href="../README/UK-ua.md"><img alt="← Назад до README" src="https://img.shields.io/badge/%E2%86%90_%D0%9D%D0%B0%D0%B7%D0%B0%D0%B4_%D0%B4%D0%BE_README-1b2838?style=for-the-badge"></a></p>
