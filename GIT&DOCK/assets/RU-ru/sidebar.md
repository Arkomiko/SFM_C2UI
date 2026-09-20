# Готовность C2UI — подробно

<p align="center"><b>🇷🇺 Русский</b> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Готовность" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Общая готовность к релизу: 41%</b></p>

Каждая область раскрывается: что уже работает и чего пока нет. Проценты — оценка относительно возможностей SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Поиск и монтирование SFM

Реестр Steam → `libraryfolders.vdf` → пути из `gameinfo.txt` в порядке движка. Шесть монтирований на стандартной установке. Ничего не пишется вне папки программы.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Индекс контента

70 199 файлов за 1,1 с холодно / 0,02 с из кэша; переопределения между монтированиями разрешаются как в движке.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Модели — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Версии 44, 48, 49. Скелет, меши, все уровни детализации, body-группы. 1 500 моделей загружено, 0 сбоев.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Материалы — <code>.vmt</code>

Все 19 554 материала установки читаются; `patch`, DX-блоки, прокси.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Текстуры — <code>.vtf</code>

Версии 7.0–7.5, DXT1/3/5 и все несжатые форматы, кубмапы, mip-уровни. DXT уходит в GPU без распаковки.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Сессии — <code>.dmx</code>

Binary 1–5 и KeyValues2. Каждая сессия и файл частиц установки записываются обратно **побайтово идентично**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Сессия на экране

Шоты и звуковые дорожки на таймлайне, дерево элементов, сцена шота через его камеру. Нет: карт, частиц, звука.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Анимация

Каналы и логи вычисляются на курсоре; скраббинг и воспроизведение. Кости, камеры, видимость следуют сессии.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Лица

Flex-контроллеры, скомпилированные правила и вершинные дельты — персонажи говорят и гримасничают. Нет: wrinkle-карт.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Риги

Выражения, point/orient/parent/aim-констрейнты, двухзвенный IK. Нет: полного графа зависимостей операторов и создания ригов.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Редактирование

Выбор кликом, манипулятор перемещения/поворота, инспектор любого атрибута, ключ на курсоре, отмена/повтор, сохранение побайтово точно.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Выделение времени с hold и falloff на линейке, правка растекается по выделению, как в SFM. Нет: пресетов и слоёв.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Graph editor

Кривые каждого лога выбранного элемента: X/Y/Z, pitch/yaw/roll, скаляры. Ключи двигаются мышью по времени и значению с живым предпросмотром, вставляются двойным щелчком, удаляются; ось времени общая с таймлайном. Нет: касательных и типов кривых, масштабирования группы ключей.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Докинг панелей

Перетаскивание панелей с крестовиной целей и предпросмотром, как в UE5 и Visual Studio. Нет: сохранённых раскладок и тем.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Шейдинг Source

Пока только текстура и простой свет. Нет: phong, rim, lightwarp, освещения сцены, теней.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Карты — <code>.bsp</code>

Не начато.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Рендер в изображение и видео

Не начато.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Плагины <code>.c2plg</code>

Не начато.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Темы и рабочие пространства

Сознательно отложено: одна тема, пока редактору нечего оформлять.

**К релизу не готов.** Фундамент — каждый формат SFM, прочитанный верно и проверенный на всей установке, — есть и покрыт тестами; сессию можно открыть, проиграть, изменить и сохранить. Не хватает *удобства* работы: graph editor, шейдинг Source, карты, экспорт. Номер версии появится, когда аниматор сможет отработать в нём день.

<p align="center"><a href="../../../README.md"><img alt="← Назад к README" src="https://img.shields.io/badge/%E2%86%90_%D0%9D%D0%B0%D0%B7%D0%B0%D0%B4_%D0%BA_README-1b2838?style=for-the-badge"></a></p>
