<p align="center"><img src="../assets/UK-ua/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <b>🇺🇦 Українська</b> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81-%D0%BF%D1%80%D0%B5--%D0%B0%D0%BB%D1%8C%D1%84%D0%B0-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%D1%82%D0%B5%D1%81%D1%82%D1%96%D0%B2-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — редактор Source Filmmaker у сучасній оболонці: той самий контент, той самий формат сесій, та сама модель даних, інтерфейс у дусі бібліотеки Steam і редактора Unreal Engine 5.</p>

---

## Готовність

<p align="center"><img src="../assets/UK-ua/sidebar.svg" alt="Готовність" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Загальна готовність до релізу: 41%</b></p>

<p align="center"><a href="../assets/UK-ua/sidebar.md"><img alt="Готовність докладно" src="https://img.shields.io/badge/%D0%93%D0%BE%D1%82%D0%BE%D0%B2%D0%BD%D1%96%D1%81%D1%82%D1%8C_%D0%B4%D0%BE%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%BE-66c0f4?style=for-the-badge"></a></p>

## Ідея

Source Filmmaker — сильний інструмент, інтерфейс якого лишився у 2012 році. C2UI не замінює його і не переробляє: завдання — зробити SFM трохи сучаснішим і зручнішим.

Редактор знаходить встановлений SFM, підключає його як бібліотеку контенту — моделі, матеріали, текстури, сесії — і працює з тими самими файлами в тому самому форматі. Усе, що зроблено в SFM, відкривається в C2UI, і навпаки.

Перша мета — повна сумісність із SFM, включно з кістками та ригами. Далі — те, чого в SFM бракувало.

```
  ┌──────────────┐    "де SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  свій UI     │ ◀─────  монтує   ───────│    tf/  hl2/  tf_movies/ …   │
  │  свій рендер │      лише читання      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Редактор з відкритою сесією Meet the Heavy" width="100%"><br><sub>Редактор сьогодні: відкрита сесія Valve «Meet the Heavy» — шоти і звук на таймлайні, дерево сесії, перший шот через його власну камеру, персонажі в позах і з обличчями із сесії.</sub></p>

## Чим відрізняється

- **Переносний.** Нічого не пишеться поза текою програми: налаштування в `App/User`, кеш у `App/Cache`, тимчасове в `App/Temporary`. Видалили теку — сліду не лишилось.
- **Не запускає SFM.** Немає процесу, яким треба керувати, немає вікон, які треба перехоплювати. Інсталяція читається як пакет контенту.
- **Формати перевірені, а не припущені.** Кожна читалка звірена зі справжньою інсталяцією; там, де формат робить щось неочевидне, код про це каже.
- **Збереження точне.** Сесія, прочитана і записана без змін, — той самий файл.
- **Ядро без залежностей.** `Core/` і всі тести працюють на голому Python; Qt і OpenGL потрібні лише вікну.

## Запуск

Потрібні Windows, Python 3.13 і встановлений Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

При першому запуску SFM шукається через Steam; якщо не знайшовся — програма спитає. <kbd>Ctrl</kbd>+<kbd>O</kbd> відкриває сесію, <kbd>Space</kbd> — відтворення, <kbd>C</kbd> — камера шота, <kbd>T</kbd>/<kbd>R</kbd> — переміщення/поворот, <kbd>M</kbd> — motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> — скасування, <kbd>Ctrl</kbd>+<kbd>S</kbd> — зберегти. Панелі перетягуються за заголовок. Тести не потребують нічого:

```bash
python Testing/run.py
```

## Структура

```
C2UI_SDK/
├── README.md
├── Core/              ядро: формати, віртуальна ФС, індекс, мости до інсталяцій
├── App/               редактор: бібліотека контенту, рендер, вікно
├── Tools/             локалізація, інструменти UI, плагіни (пізніше)
│   └── Launcher/      лаунчер
├── Testing/           тести, побайтові фікстури, один ранер
└── GIT&DOCK/          цей README іншими мовами
```

## Дорожня карта

1. **Шейдинг Source** — VertexLitGeneric як малює SFM: phong, rim, lightwarp, освітлення сцени.
2. **Карти** — `.bsp` для фону.
3. **Експорт** — зображення і відео.
4. **Плагіни** — формат `.c2plg`; потім теми і робочі простори.

## Ліцензія і подяки

Власний код C2UI поширюється за **ліцензією C2UI**: вільно для особистих і некомерційних потреб; комерційне використання — лише за письмовою згодою автора; змінені версії мають посилатися на оригінальний проєкт і його автора Arkomiko. Плагіни й аддони — за ліцензією **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 і рушій Source належать Valve; проєкт читає їхні формати, не містить їхніх файлів і працює лише з вашою копією SFM зі Steam.

<p align="center"><a href="../LICENSE/UK-ua.md"><img alt="Текст ліцензії" src="https://img.shields.io/badge/%D0%A2%D0%B5%D0%BA%D1%81%D1%82_%D0%BB%D1%96%D1%86%D0%B5%D0%BD%D0%B7%D1%96%D1%97-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 моделі, відрендерені прямо з інсталяції" width="60%"><br><sub>Шістдесят чотири випадкові моделі з інсталяції, намальовані власним рендерером C2UI.</sub></p>
