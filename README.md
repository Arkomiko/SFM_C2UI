<p align="center"><img src="GIT%26DOCK/assets/RU-ru/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><b>🇷🇺 Русский</b> · <a href="GIT%26DOCK/README/EN-en.md">🇬🇧 English</a> · <a href="GIT%26DOCK/README/PL-pl.md">🇵🇱 Polski</a> · <a href="GIT%26DOCK/README/UK-ua.md">🇺🇦 Українська</a> · <a href="GIT%26DOCK/README/DE-de.md">🇩🇪 Deutsch</a> · <a href="GIT%26DOCK/README/RO-md.md">🇲🇩 Moldovenească</a> · <a href="GIT%26DOCK/README/SL-si.md">🇸🇮 Slovenščina</a> · <a href="GIT%26DOCK/README/BE-by.md">🇧🇾 Беларуская</a> · <a href="GIT%26DOCK/README/KK-kz.md">🇰🇿 Қазақша</a> · <a href="GIT%26DOCK/README/JA-jp.md">🇯🇵 日本語</a> · <a href="GIT%26DOCK/README/ZH-cn.md">🇨🇳 中文</a> · <a href="GIT%26DOCK/README/SV-se.md">🇸🇪 Svenska</a> · <a href="GIT%26DOCK/README/ES-es.md">🇪🇸 Español</a> · <a href="GIT%26DOCK/README/HI-in.md">🇮🇳 हिन्दी</a> · <a href="GIT%26DOCK/README/PT-pt.md">🇵🇹 Português</a> · <a href="GIT%26DOCK/README/BN-bd.md">🇧🇩 বাংলা</a> · <a href="GIT%26DOCK/README/FR-fr.md">🇫🇷 Français</a> · <a href="GIT%26DOCK/README/TE-in.md">🇮🇳 తెలుగు</a> · <a href="GIT%26DOCK/README/MR-in.md">🇮🇳 मराठी</a> · <a href="GIT%26DOCK/README/TA-in.md">🇮🇳 தமிழ்</a> · <a href="GIT%26DOCK/README/TR-tr.md">🇹🇷 Türkçe</a> · <a href="GIT%26DOCK/README/UR-pk.md">🇵🇰 اردو</a> · <a href="GIT%26DOCK/README/VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GIT%26DOCK/README/GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="GIT%26DOCK/README/IT-it.md">🇮🇹 Italiano</a> · <a href="GIT%26DOCK/README/KO-kr.md">🇰🇷 한국어</a> · <a href="GIT%26DOCK/README/AR-sa.md">🇸🇦 العربية</a> · <a href="GIT%26DOCK/README/JV-id.md">🇮🇩 Basa Jawa</a> · <a href="GIT%26DOCK/README/ML-in.md">🇮🇳 മലയാളം</a> · <a href="GIT%26DOCK/README/NE-np.md">🇳🇵 नेपाली</a> · <a href="GIT%26DOCK/README/UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="GIT%26DOCK/README/OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81-%D0%BF%D1%80%D0%B5--%D0%B0%D0%BB%D1%8C%D1%84%D0%B0-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="Testing"><img alt="tests" src="https://img.shields.io/badge/%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — редактор Source Filmmaker в современной оболочке: тот же контент, тот же формат сессий, та же модель данных, интерфейс в духе библиотеки Steam и редактора Unreal Engine 5.</p>

---

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

## Готовность

<img align="right" src="GIT%26DOCK/assets/RU-ru/sidebar.svg" alt="Готовность" width="300">

<img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Общая готовность к релизу: 38%</b>

Каждая область раскрывается: что уже работает и чего пока нет. Проценты — оценка относительно возможностей SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Поиск и монтирование SFM</b></summary>

Реестр Steam → `libraryfolders.vdf` → пути из `gameinfo.txt` в порядке движка. Шесть монтирований на стандартной установке. Ничего не пишется вне папки программы.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Индекс контента</b></summary>

70 199 файлов за 1,1 с холодно / 0,02 с из кэша; переопределения между монтированиями разрешаются как в движке.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Модели — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

Версии 44, 48, 49. Скелет, меши, все уровни детализации, body-группы. 1 500 моделей загружено, 0 сбоев.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Материалы — <code>.vmt</code></b></summary>

Все 19 554 материала установки читаются; `patch`, DX-блоки, прокси.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Текстуры — <code>.vtf</code></b></summary>

Версии 7.0–7.5, DXT1/3/5 и все несжатые форматы, кубмапы, mip-уровни. DXT уходит в GPU без распаковки.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Сессии — <code>.dmx</code></b></summary>

Binary 1–5 и KeyValues2. Каждая сессия и файл частиц установки записываются обратно **побайтово идентично**.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Сессия на экране</b></summary>

Шоты и звуковые дорожки на таймлайне, дерево элементов, сцена шота через его камеру. Нет: карт, частиц, звука.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Анимация</b></summary>

Каналы и логи вычисляются на курсоре; скраббинг и воспроизведение. Кости, камеры, видимость следуют сессии.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Лица</b></summary>

Flex-контроллеры, скомпилированные правила и вершинные дельты — персонажи говорят и гримасничают. Нет: wrinkle-карт.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Риги</b></summary>

Выражения, point/orient/parent/aim-констрейнты, двухзвенный IK. Нет: полного графа зависимостей операторов и создания ригов.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Редактирование</b></summary>

Выбор кликом, манипулятор перемещения/поворота, инспектор любого атрибута, ключ на курсоре, отмена/повтор, сохранение побайтово точно. Нет: graph editor.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Выделение времени с hold и falloff на линейке, правка растекается по выделению, как в SFM. Нет: пресетов и слоёв.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Докинг панелей</b></summary>

Перетаскивание панелей с крестовиной целей и предпросмотром, как в UE5 и Visual Studio. Нет: сохранённых раскладок и тем.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Шейдинг Source</b></summary>

Пока только текстура и простой свет. Нет: phong, rim, lightwarp, освещения сцены, теней.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Карты — <code>.bsp</code></b></summary>

Не начато.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Рендер в изображение и видео</b></summary>

Не начато.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Плагины <code>.c2plg</code></b></summary>

Не начато.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Темы и рабочие пространства</b></summary>

Сознательно отложено: одна тема, пока редактору нечего оформлять.

</details>

**К релизу не готов.** Фундамент — каждый формат SFM, прочитанный верно и проверенный на всей установке, — есть и покрыт тестами; сессию можно открыть, проиграть, изменить и сохранить. Не хватает *удобства* работы: graph editor, шейдинг Source, карты, экспорт. Номер версии появится, когда аниматор сможет отработать в нём день.

<br clear="all">

<p align="center"><img src="GIT%26DOCK/assets/editor.png" alt="Редактор с открытой сессией Meet the Heavy" width="100%"><br><sub>Редактор сегодня: открыта сессия Valve «Meet the Heavy» — шоты и звук на таймлайне, дерево сессии, первый шот через его собственную камеру, персонажи в позах и с лицами из сессии.</sub></p>

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
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

При первом запуске SFM ищется через Steam; если не нашёлся — программа спросит. <kbd>Ctrl</kbd>+<kbd>O</kbd> открывает сессию, <kbd>Space</kbd> — воспроизведение, <kbd>C</kbd> — камера шота, <kbd>T</kbd>/<kbd>R</kbd> — перемещение/поворот, <kbd>M</kbd> — motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> — отмена, <kbd>Ctrl</kbd>+<kbd>S</kbd> — сохранить. Панели перетаскиваются за заголовок. Тесты не требуют ничего:

```bash
python Testing/run.py
```

## Структура

```
C2UI_SDK/
├── c2ui.py            лаунчер
├── Core/              ядро: форматы, виртуальная ФС, индекс, мосты к установкам
├── App/               редактор: библиотека контента, рендер, окно
├── Tools/             локализация, инструменты UI, плагины (позже)
├── Testing/           тесты, побайтовые фикстуры, один раннер
└── GIT&DOCK/README/   этот README на других языках
```

## Дорожная карта

1. **Graph editor** — кривые и ключи глазами.
2. **Шейдинг Source** — VertexLitGeneric как рисует SFM: phong, rim, lightwarp, освещение сцены.
3. **Карты** — `.bsp` для фона.
4. **Экспорт** — изображение и видео.
5. **Плагины** — формат `.c2plg`; затем темы и рабочие пространства.

## Лицензия и благодарности

Source Filmmaker, Team Fortress 2 и движок Source принадлежат Valve. Проект читает их форматы, не содержит их файлов и работает только с вашей копией SFM из Steam.

Лицензия собственного кода C2UI ещё не выбрана — до тех пор все права защищены. Issues и pull requests приветствуются.

<p align="center"><img src="GIT%26DOCK/assets/models.png" alt="64 модели, отрендеренные прямо из установки" width="60%"><br><sub>Шестьдесят четыре случайные модели из установки, нарисованные собственным рендерером C2UI.</sub></p>
