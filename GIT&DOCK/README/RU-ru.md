<p align="center"><img src="../assets/RU-ru/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><b>🇷🇺 Русский</b> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81-%D0%BF%D1%80%D0%B5--%D0%B0%D0%BB%D1%8C%D1%84%D0%B0-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — редактор Source Filmmaker в современной оболочке: тот же контент, тот же формат сессий, та же модель данных, интерфейс в духе библиотеки Steam и редактора Unreal Engine 5.</p>

---

## Готовность

<p align="center"><img src="../assets/RU-ru/sidebar.svg" alt="Готовность" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Общая готовность к релизу: 41%</b></p>

<p align="center"><a href="../assets/RU-ru/sidebar.md"><img alt="Подробнее о готовности" src="https://img.shields.io/badge/%D0%9F%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D0%B5%D0%B5_%D0%BE_%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%BD%D0%BE%D1%81%D1%82%D0%B8-66c0f4?style=for-the-badge"></a></p>

## Идея

Source Filmmaker — сильный инструмент, интерфейс которого остался в 2012 году. C2UI не заменяет его и не переделывает: задача — сделать SFM немного современнее и удобнее.

Редактор находит установленный SFM, подключает его как библиотеку контента — модели, материалы, текстуры, сессии — и работает с теми же файлами в том же формате. Всё, что сделано в SFM, открывается в C2UI, и наоборот.

Первая цель — полная совместимость с SFM, включая кости и риги. Дальше — то, чего в SFM не хватало.

```
  ┌──────────────┐    "где SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  свой UI     │ ◀───── монтирует ───────│    tf/  hl2/  tf_movies/ …   │
  │  свой рендер │      только чтение      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Редактор с открытой сессией Meet the Heavy" width="100%"><br><sub>Редактор сегодня: открыта сессия Valve «Meet the Heavy» — шоты и звук на таймлайне, дерево сессии, первый шот через его собственную камеру, персонажи в позах и с лицами из сессии.</sub></p>

## Чем отличается

- **Переносимый.** Ничего не пишется вне папки программы: настройки в `App/User`, кэш в `App/Cache`, временное в `App/Temporary`. Удалили папку — не осталось следа.
- **Не запускает SFM.** Нет процесса, которым надо управлять, нет окон, которые надо перехватывать. Установка читается как пакет контента.
- **Форматы проверены, а не предположены.** Каждая читалка сверена с настоящей установкой; там, где формат делает что-то неочевидное, код об этом говорит.
- **Сохранение точное.** Сессия, прочитанная и записанная без изменений, — тот же самый файл.
- **Ядро без зависимостей.** `Core/` и все тесты работают на голом Python; Qt и OpenGL нужны только окну.

## Запуск

Нужны Windows, Python 3.13 и установленный Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

При первом запуске SFM ищется через Steam; если не нашёлся — программа спросит. <kbd>Ctrl</kbd>+<kbd>O</kbd> открывает сессию, <kbd>Space</kbd> — воспроизведение, <kbd>C</kbd> — камера шота, <kbd>T</kbd>/<kbd>R</kbd> — перемещение/поворот, <kbd>M</kbd> — motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> — отмена, <kbd>Ctrl</kbd>+<kbd>S</kbd> — сохранить. Панели перетаскиваются за заголовок. Тесты не требуют ничего:

```bash
python Testing/run.py
```

## Структура

```
C2UI_SDK/
├── README.md
├── Core/              ядро: форматы, виртуальная ФС, индекс, мосты к установкам
├── App/               редактор: библиотека контента, рендер, окно
├── Tools/             локализация, инструменты UI, плагины (позже)
│   └── Launcher/      лаунчер
├── Testing/           тесты, побайтовые фикстуры, один раннер
└── GIT&DOCK/          этот README на других языках
```

## Дорожная карта

1. **Шейдинг Source** — VertexLitGeneric как рисует SFM: phong, rim, lightwarp, освещение сцены.
2. **Карты** — `.bsp` для фона.
3. **Экспорт** — изображение и видео.
4. **Плагины** — формат `.c2plg`; затем темы и рабочие пространства.

## Лицензия и благодарности

Собственный код C2UI распространяется по **лицензии C2UI**: свободно для личных и некоммерческих нужд; коммерческое использование — только по письменному согласию автора; при модификации — ссылка на оригинальный проект и автора Arkomiko. Плагины и аддоны — по лицензии **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 и движок Source принадлежат Valve; проект читает их форматы, не содержит их файлов и работает только с вашей копией SFM из Steam.

<p align="center"><a href="../LICENSE/RU-ru.md"><img alt="Текст лицензии" src="https://img.shields.io/badge/%D0%A2%D0%B5%D0%BA%D1%81%D1%82_%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%B8-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 модели, отрендеренные прямо из установки" width="60%"><br><sub>Шестьдесят четыре случайные модели из установки, нарисованные собственным рендерером C2UI.</sub></p>
