# Лаунчер C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇷🇺 Русский</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><b>🇷🇺<br>Русский</b></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` — то, с чего запускается проект: маленькое тёмное окно с названием, строкой описания и тремя кнопками. Оно собирается в один исполняемый файл, которому не нужен установленный Python, и находит проект само — идёт вверх от своего места, пока не увидит рядом `App`, `Core` и `Launcher`.

<p align="center"><img src="../assets/launcher.png" alt="Лаунчер C2UI" width="562"><br><sub>Окно лаунчера: заголовок «Dev-mode», строка описания и три кнопки.</sub></p>

> [!NOTE]
> **Интерфейс лаунчера пока только на русском — это временное решение.** Заголовок, описание и подписи кнопок зашиты в код; локализация появится вместе с локализацией редактора (`Tools/Localization`), когда лаунчер будет переписан под готовый App. Остальная документация проекта уже доступна на 32 языках.

## Три кнопки

| | |
|---|---|
| <code>Запустить Core</code> | Запускает редактор — окно C2UI с вьюпортом, таймлайном и панелями. |
| <code>Запустить App</code> | Пока неактивна: отдельного приложения App ещё нет. |
| <code>Выйти</code> | Закрывает лаунчер. |

## Запуск из исходников

Нужны Windows, Python 3.13 и установленный Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Сборка в один файл `Launcher/Launcher-C2UI.exe` (в git не хранится — пересобирается из исходников):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Движок без редактора

`Launcher/core.py` запускает `Core` отдельно: монтирует установку, индексирует её и даёт небольшую оболочку над движком — модели, материалы, текстуры, карты, сессии и их вычисление. Тоже временно: когда App научится работать без окна, единой точкой входа станет редактор.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Что будет дальше

- Окно перепишут, когда появится App, — вместе с оформлением и локализацией.
- Кнопка «Запустить App» станет рабочей.
- `core.py` уйдёт, как только редактор можно будет запускать без окна.
- Готовый `.exe` будет прикладываться к релизам на GitHub.

<p align="center"><a href="../../README.md"><img alt="← Назад к README" src="https://img.shields.io/badge/%E2%86%90_%D0%9D%D0%B0%D0%B7%D0%B0%D0%B4_%D0%BA_README-1b2838?style=for-the-badge"></a></p>
