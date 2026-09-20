# C2UI дайындығы — толығырақ

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <b>🇰🇿 Қазақша</b> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Дайындық" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Релизге жалпы дайындық: 41%</b></p>

Әр аймақ ашылады: не жұмыс істейді және не әлі жоқ. Пайыздар — SFM мүмкіндіктеріне қатысты баға.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> SFM-ді табу және жалғау

Steam реестрі → `libraryfolders.vdf` → `gameinfo.txt` жолдары қозғалтқыш ретімен. Стандартты орнатуда алты жалғау. Бағдарлама папкасынан тыс ештеңе жазылмайды.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Контент индексі

70 199 файл 1,1 с суық / 0,02 с кэштен; жалғаулар арасындағы қайта анықтаулар қозғалтқыштағыдай шешіледі.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Модельдер — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

44, 48, 49 нұсқалары. Қаңқа, мештер, барлық детализация деңгейлері, body-топтар. 1 500 модель жүктелді, 0 сәтсіздік.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Материалдар — <code>.vmt</code>

Орнатудағы барлық 19 554 материал оқылады; `patch`, DX-блоктар, прокси.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Текстуралар — <code>.vtf</code>

7.0–7.5 нұсқалары, DXT1/3/5 және барлық сығылмаған форматтар, кубмаптар, mip-деңгейлер. DXT GPU-ға ашылмай кетеді.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Сессиялар — <code>.dmx</code>

Binary 1–5 және KeyValues2. Орнатудағы әрбір сессия мен бөлшектер файлы **байт-байтымен** бірдей қайта жазылады.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Экрандағы сессия

Таймлайндағы шоттар мен дыбыс жолдары, элементтер ағашы, шот сахнасы оның камерасы арқылы. Жоқ: карталар, бөлшектер, дыбыс.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Анимация

Арналар мен логтар курсорда есептеледі; скраббинг және ойнату. Сүйектер, камералар, көрінуі сессияға ереді.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Беттер

Flex-контроллерлер, компиляцияланған ережелер және төбе дельталары — кейіпкерлер сөйлейді және ым жасайды. Жоқ: wrinkle-карталар.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Ригтер

Өрнектер, point/orient/parent/aim-констрейнттер, екі сүйекті IK. Жоқ: операторлардың толық тәуелділік графы, риг жасау.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Өңдеу

Шертумен таңдау, жылжыту/бұру манипуляторы, кез келген атрибут инспекторы, курсордағы кілт, болдырмау/қайталау, байт-дәлдікпен сақтау.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Сызғыштағы hold және falloff бар уақыт бөлектеуі; өзгеріс SFM-дегідей бөлектеуге таралады. Жоқ: пресеттер, қабаттар.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Graph editor

Таңдалған элементтің әр логының қисықтары: X/Y/Z, pitch/yaw/roll, скалярлар. Кілттер уақыт пен мән бойынша тірі алдын ала қараумен сүйреледі, қос шерту кірістіреді, Delete өшіреді; уақыт осі таймлайнмен ортақ. Жоқ: жанамалар мен қисық түрлері, кілттер тобын масштабтау.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Панельдерді бекіту

UE5 және Visual Studio сияқты, панельдерді алдын ала қараумен мақсаттар крестовинасына сүйреу. Жоқ: сақталған орналасулар, тақырыптар.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source шейдингі

Әзірге тек текстура және қарапайым жарық. Жоқ: phong, rim, lightwarp, сахна жарығы, көлеңкелер.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Карталар — <code>.bsp</code>

Басталмаған.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Сурет пен бейнеге рендер

Басталмаған.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Плагиндер <code>.c2plg</code>

Басталмаған.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Тақырыптар мен жұмыс кеңістіктері

Әдейі кейінге қалдырылған: редакторда безендіретін нәрсе болғанша бір тақырып.

**Релизге дайын емес.** Іргетас — SFM қолданатын әрбір файл форматы, дұрыс оқылып, бүкіл орнатуда тексерілген — бар және тесттермен жабылған; сессияны ашуға, ойнатуға, өзгертуге және сақтауға болады. Жұмыстың *ыңғайлылығы* жетіспейді: graph editor, Source шейдингі, карталар, экспорт. Аниматор онда бір күн жұмыс істей алғанша нұсқа нөмірі болмайды.

<p align="center"><a href="../../README/KK-kz.md"><img alt="← README-ге қайту" src="https://img.shields.io/badge/%E2%86%90_README-%D0%B3%D0%B5_%D2%9B%D0%B0%D0%B9%D1%82%D1%83-1b2838?style=for-the-badge"></a></p>
