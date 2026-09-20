<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <b>🇰🇿 Қазақша</b> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%D0%BA%D2%AF%D0%B9%D1%96-%D0%BF%D1%80%D0%B5--%D0%B0%D0%BB%D1%8C%D1%84%D0%B0-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%D1%82%D0%B5%D1%81%D1%82-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — бұл менің Source Filmmaker редакторын қайта құруым: сол контент, сол сессия форматы, сол деректер моделі — сыртқы түрін Steam кітапханасынан, орналасуын Unreal Engine 5 редакторынан алған қабықта.</p>

---

## Идея

Source Filmmaker — 2012 жылғы интерфейстегі тамаша құрал. Мен `sfm.exe`-ге скин кигізгім келмейді және оның терезелерін бір-бірлеп ұстағым келмейді. Маған **SFM қайда орнатылғанын сұрайтын**, сол орнатуды Garry's Mod Counter-Strike-ты жалғағандай жалғайтын және сол файлдардың үстінде бәрін өзі істейтін — модельдер, материалдар, текстуралар, сессиялар, анимация — SFM-ді ешқашан іске қоспайтын редактор керек.

Мақсат — **SFM функционалдығы бірге бір** (сүйектер мен ригтерді қоса), одан кейін SFM-де ешқашан болмағандар.

```
  ┌──────────────┐    "SFM қайда?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  өз UI       │ ◀───── жалғайды  ───────│    tf/  hl2/  tf_movies/ …   │
  │  өз рендер   │        тек оқу        │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Дайындық

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Релизге жалпы дайындық: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy ашылған редактор" width="100%"><br><sub>Бүгінгі редактор: Valve-тың «Meet the Heavy» сессиясы ашық — таймлайндағы шоттар мен дыбыс, сессия ағашы, өз камерасы арқылы бірінші шот, сессиядағы позалар мен беттердегі кейіпкерлер.</sub></p>

Нақты не дайын, не дайын емес екенін көру үшін аймақты ашыңыз. Пайыздар — SFM мүмкіндіктеріне қатысты менің адал бағам.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM-ді табу және жалғау</b></summary>

Steam реестрі → `libraryfolders.vdf` → `gameinfo.txt` жолдары қозғалтқыш ретімен. Стандартты орнатуда алты жалғау. Бағдарлама папкасынан тыс ештеңе жазылмайды.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Контент индексі</b></summary>

70 199 файл 1,1 с суық / 0,02 с кэштен; жалғаулар арасындағы қайта анықтаулар қозғалтқыштағыдай шешіледі.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Модельдер — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

44, 48, 49 нұсқалары. Қаңқа, мештер, барлық детализация деңгейлері, body-топтар. 1 500 модель жүктелді, 0 сәтсіздік.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Материалдар — <code>.vmt</code></b></summary>

Орнатудағы барлық 19 554 материал оқылады; `patch`, DX-блоктар, прокси.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Текстуралар — <code>.vtf</code></b></summary>

7.0–7.5 нұсқалары, DXT1/3/5 және барлық сығылмаған форматтар, кубмаптар, mip-деңгейлер. DXT GPU-ға ашылмай кетеді.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Сессиялар — <code>.dmx</code></b></summary>

Binary 1–5 және KeyValues2. Орнатудағы әрбір сессия мен бөлшектер файлы **байт-байтымен** бірдей қайта жазылады.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Экрандағы сессия</b></summary>

Таймлайндағы шоттар мен дыбыс жолдары, элементтер ағашы, шот сахнасы оның камерасы арқылы. Жоқ: карталар, бөлшектер, дыбыс.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Анимация</b></summary>

Арналар мен логтар курсорда есептеледі; скраббинг және ойнату. Сүйектер, камералар, көрінуі сессияға ереді.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Беттер</b></summary>

Flex-контроллерлер, компиляцияланған ережелер және төбе дельталары — кейіпкерлер сөйлейді және ым жасайды. Жоқ: wrinkle-карталар.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Ригтер</b></summary>

Өрнектер, point/orient/parent/aim-констрейнттер, екі сүйекті IK. Жоқ: операторлардың толық тәуелділік графы, риг жасау.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Өңдеу</b></summary>

Шертумен таңдау, жылжыту/бұру манипуляторы, кез келген атрибут инспекторы, курсордағы кілт, болдырмау/қайталау, байт-дәлдікпен сақтау. Жоқ: graph editor.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Сызғыштағы hold және falloff бар уақыт бөлектеуі; өзгеріс SFM-дегідей бөлектеуге таралады. Жоқ: пресеттер, қабаттар.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Панельдерді бекіту</b></summary>

UE5 және Visual Studio сияқты, панельдерді алдын ала қараумен мақсаттар крестовинасына сүйреу. Жоқ: сақталған орналасулар, тақырыптар.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source шейдингі</b></summary>

Әзірге тек текстура және қарапайым жарық. Жоқ: phong, rim, lightwarp, сахна жарығы, көлеңкелер.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Карталар — <code>.bsp</code></b></summary>

Басталмаған.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Сурет пен бейнеге рендер</b></summary>

Басталмаған.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Плагиндер <code>.c2plg</code></b></summary>

Басталмаған.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Тақырыптар мен жұмыс кеңістіктері</b></summary>

Әдейі кейінге қалдырылған: редакторда безендіретін нәрсе болғанша бір тақырып.

</details>

**Релизге дайын емес.** Іргетас — SFM қолданатын әрбір файл форматы, дұрыс оқылып, бүкіл орнатуда тексерілген — бар және тесттермен жабылған; сессияны ашуға, ойнатуға, өзгертуге және сақтауға болады. Жұмыстың *ыңғайлылығы* жетіспейді: graph editor, Source шейдингі, карталар, экспорт. Аниматор онда бір күн жұмыс істей алғанша нұсқа нөмірі болмайды.

## Айырмашылығы неде

- **Тасымалы.** Бағдарлама папкасынан тыс ештеңе жазылмайды: параметрлер `App/User`, кэш `App/Cache`, уақытша `App/Temporary`. Папканы өшірсеңіз — із қалмайды.
- **SFM-ді іске қоспайды.** Басқаратын процесс жоқ, ұстайтын терезелер жоқ. Орнату контент пакеті ретінде оқылады.
- **Форматтар тексерілген, болжанбаған.** Әрбір оқығыш нақты орнатумен салыстырылған; формат күтпеген нәрсе істесе, код бұл туралы айтады.
- **Сақтау дәл.** Өзгеріссіз оқылып жазылған сессия — сол файл.
- **Ядро тәуелділіксіз.** `Core/` және барлық тесттер таза Python-да жұмыс істейді; Qt мен OpenGL тек терезеге керек.

## Іске қосу

Windows, Python 3.13 және орнатылған Source Filmmaker қажет.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Алғашқы іске қосуда SFM Steam арқылы ізделеді; табылмаса — бағдарлама сұрайды. <kbd>Ctrl</kbd>+<kbd>O</kbd> сессияны ашады, <kbd>Space</kbd> — ойнату, <kbd>C</kbd> — шот камерасы, <kbd>T</kbd>/<kbd>R</kbd> — жылжыту/бұру, <kbd>M</kbd> — motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> — болдырмау, <kbd>Ctrl</kbd>+<kbd>S</kbd> — сақтау. Панельдер тақырыбынан сүйреледі. Тесттерге ештеңе керек емес:

```bash
python Testing/run.py
```

## Құрылымы

```
C2UI_SDK/
├── c2ui.py            іске қосқыш
├── Core/              ядро: форматтар, виртуалды ФЖ, индекс, көпірлер
├── App/               редактор: контент кітапханасы, рендер, терезе
├── Tools/             локализация, UI құралдары, плагиндер (кейін)
├── Testing/           тесттер, байт-дәл фикстуралар, бір раннер
└── GIT&DOCK/README/   осы README басқа тілдерде
```

## Жол картасы

1. **Graph editor** — қисықтар мен кілттер көз алдында.
2. **Source шейдингі** — VertexLitGeneric SFM салғандай: phong, rim, lightwarp, сахна жарығы.
3. **Карталар** — фон үшін `.bsp`.
4. **Экспорт** — сурет және бейне.
5. **Плагиндер** — `.c2plg` форматы; содан кейін тақырыптар мен жұмыс кеңістіктері.

## Лицензия және алғыс

Source Filmmaker, Team Fortress 2 және Source қозғалтқышы Valve-қа тиесілі. Жоба олардың форматтарын оқиды, файлдарын қамтымайды және тек Steam-дегі өз SFM көшірмеңізбен жұмыс істейді.

C2UI өз кодының лицензиясы әлі таңдалмаған — оған дейін барлық құқықтар қорғалған. Issues мен pull request-тер қош келеді.

<p align="center"><img src="../../.github/assets/models.png" alt="Орнатудан тікелей рендерленген 64 модель" width="60%"><br><sub>Орнатудан кездейсоқ алынған алпыс төрт модель, C2UI-дің өз рендерерімен салынған.</sub></p>
