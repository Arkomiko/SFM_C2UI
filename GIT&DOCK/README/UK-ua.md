<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <b>🇺🇦 Українська</b> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81-%D0%BF%D1%80%D0%B5--%D0%B0%D0%BB%D1%8C%D1%84%D0%B0-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%D1%82%D0%B5%D1%81%D1%82%D1%96%D0%B2-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — це моя перебудова редактора Source Filmmaker: той самий контент, той самий формат сесій, та сама модель даних — в оболонці, що бере вигляд від бібліотеки Steam, а компонування від редактора Unreal Engine 5.</p>

---

## Ідея

Source Filmmaker — чудовий інструмент в інтерфейсі 2012 року. Я не хочу натягувати скін на `sfm.exe` і не хочу перехоплювати його вікна по одному. Я хочу редактор, який **питає, де встановлено SFM**, монтує цю інсталяцію так, як Garry's Mod монтує Counter-Strike, і все робить сам поверх цих файлів — моделі, матеріали, текстури, сесії, анімацію — ніколи не запускаючи SFM.

Мета — **функціональність SFM один в один** (включно з кістками та ригами), а далі те, чого в SFM ніколи не було.

```
  ┌──────────────┐    "де SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  свій UI     │ ◀─────  монтує   ───────│    tf/  hl2/  tf_movies/ …   │
  │  свій рендер │      лише читання      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Готовність

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Загальна готовність до релізу: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Редактор з відкритою сесією Meet the Heavy" width="100%"><br><sub>Редактор сьогодні: відкрита сесія Valve «Meet the Heavy» — шоти і звук на таймлайні, дерево сесії, перший шот через його власну камеру, персонажі в позах і з обличчями із сесії.</sub></p>

Розгорніть область, щоб побачити, що саме готове, а що ні. Відсотки — моя чесна оцінка відносно можливостей SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Пошук і монтування SFM</b></summary>

Реєстр Steam → `libraryfolders.vdf` → шляхи з `gameinfo.txt` у порядку рушія. Шість монтувань на стандартній інсталяції. Нічого не пишеться поза текою програми.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Індекс контенту</b></summary>

70 199 файлів за 1,1 с холодно / 0,02 с із кешу; перевизначення між монтуваннями розв'язуються як у рушії.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Моделі — <code></code> <code></code> <code></code></b></summary>

Версії 44, 48, 49. Скелет, меші, всі рівні деталізації, body-групи. 1 500 моделей завантажено, 0 збоїв.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Матеріали — <code></code></b></summary>

Усі 19 554 матеріали інсталяції читаються; `patch`, DX-блоки, проксі.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Текстури — <code></code></b></summary>

Версії 7.0–7.5, DXT1/3/5 і всі нестиснені формати, кубмапи, mip-рівні. DXT іде в GPU без розпакування.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Сесії — <code></code></b></summary>

Binary 1–5 і KeyValues2. Кожна сесія і файл частинок інсталяції записуються назад **побайтово ідентично**.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Сесія на екрані</b></summary>

Шоти і звукові доріжки на таймлайні, дерево елементів, сцена шота через його камеру. Немає: карт, частинок, звуку.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Анімація</b></summary>

Канали і логи обчислюються на курсорі; скрабінг і відтворення. Кістки, камери, видимість слідують сесії.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Обличчя</b></summary>

Flex-контролери, скомпільовані правила і вершинні дельти — персонажі говорять і гримасують. Немає: wrinkle-карт.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Риги</b></summary>

Вирази, point/orient/parent/aim-констрейнти, дволанковий IK. Немає: повного графа залежностей операторів, створення ригів.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Редагування</b></summary>

Вибір кліком, маніпулятор переміщення/повороту, інспектор будь-якого атрибута, ключ на курсорі, скасування/повтор, побайтово точне збереження. Немає: graph editor.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Виділення часу з hold і falloff на лінійці; правка розтікається по виділенню, як у SFM. Немає: пресетів, шарів.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Докінг панелей</b></summary>

Перетягування панелей на хрестовину цілей з попереднім переглядом, як в UE5 і Visual Studio. Немає: збережених розкладок, тем.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Шейдинг Source</b></summary>

Поки лише текстура і просте світло. Немає: phong, rim, lightwarp, освітлення сцени, тіней.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Карти — <code></code></b></summary>

Не розпочато.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Рендер у зображення і відео</b></summary>

Не розпочато.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Плагіни <code></code></b></summary>

Не розпочато.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Теми і робочі простори</b></summary>

Свідомо відкладено: одна тема, поки редактору нічого оформлювати.

</details>

**До релізу не готовий.** Фундамент — кожен формат SFM, прочитаний вірно і перевірений на всій інсталяції, — є і покритий тестами; сесію можна відкрити, програти, змінити і зберегти. Бракує *зручності* роботи: graph editor, шейдингу Source, карт, експорту. Номер версії з'явиться, коли аніматор зможе відпрацювати в ньому день.

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
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

При першому запуску SFM шукається через Steam; якщо не знайшовся — програма спитає. <kbd>Ctrl</kbd>+<kbd>O</kbd> відкриває сесію, <kbd>Space</kbd> — відтворення, <kbd>C</kbd> — камера шота, <kbd>T</kbd>/<kbd>R</kbd> — переміщення/поворот, <kbd>M</kbd> — motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> — скасування, <kbd>Ctrl</kbd>+<kbd>S</kbd> — зберегти. Панелі перетягуються за заголовок. Тести не потребують нічого:

```bash
python Testing/run.py
```

## Структура

```
C2UI_SDK/
├── c2ui.py            лаунчер
├── Core/              ядро: формати, віртуальна ФС, індекс, мости до інсталяцій
├── App/               редактор: бібліотека контенту, рендер, вікно
├── Tools/             локалізація, інструменти UI, плагіни (пізніше)
├── Testing/           тести, побайтові фікстури, один ранер
└── GIT&DOCK/README/   цей README іншими мовами
```

## Дорожня карта

1. **Graph editor** — криві та ключі на очах.
2. **Шейдинг Source** — VertexLitGeneric як малює SFM: phong, rim, lightwarp, освітлення сцени.
3. **Карти** — `.bsp` для фону.
4. **Експорт** — зображення і відео.
5. **Плагіни** — формат `.c2plg`; потім теми і робочі простори.

## Ліцензія і подяки

Source Filmmaker, Team Fortress 2 і рушій Source належать Valve. Проєкт читає їхні формати, не містить їхніх файлів і працює лише з вашою копією SFM зі Steam.

Ліцензію власного коду C2UI ще не обрано — до того часу всі права захищені. Issues і pull requests вітаються.

<p align="center"><img src="../../.github/assets/models.png" alt="64 моделі, відрендерені прямо з інсталяції" width="60%"><br><sub>Шістдесят чотири випадкові моделі з інсталяції, намальовані власним рендерером C2UI.</sub></p>
