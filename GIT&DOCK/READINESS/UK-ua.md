# Готовність C2UI — докладно

<details align="center"><summary>&nbsp;🌐 <b>🇺🇦 Українська</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><b>🇺🇦<br>Українська</b></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/UK-ua.svg" alt="Готовність" width="100%"></p>

<p align="center"><img alt="51%" src="https://img.shields.io/badge/51%25-e0a800?style=flat-square"> <b>Загальна готовність до релізу: 51%</b></p>

Кожна область розгортається: що вже працює і чого поки немає. Відсотки — оцінка відносно можливостей SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Пошук і монтування SFM

Реєстр Steam → `libraryfolders.vdf` → шляхи з `gameinfo.txt` у порядку рушія. Шість монтувань на стандартній інсталяції. Нічого не пишеться поза текою програми.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Індекс контенту

70 199 файлів за 1,1 с холодно / 0,02 с із кешу; перевизначення між монтуваннями розв'язуються як у рушії.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Моделі — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Версії 44, 48, 49. Скелет, меші, всі рівні деталізації, body-групи. 1 500 моделей завантажено, 0 збоїв.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Матеріали — <code>.vmt</code>

Усі 19 554 матеріали інсталяції читаються; `patch`, DX-блоки, проксі.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Текстури — <code>.vtf</code>

Версії 7.0–7.5, DXT1/3/5 і всі нестиснені формати, кубмапи, mip-рівні. DXT іде в GPU без розпакування.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Сесії — <code>.dmx</code>

Binary 1–5 і KeyValues2. Кожна сесія і файл частинок інсталяції записуються назад **побайтово ідентично**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Сесія на екрані

Шоти і звукові доріжки на таймлайні, дерево елементів, сцена шота через його камеру. Немає: карт, частинок, звуку.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Анімація

Канали і логи обчислюються на курсорі; скрабінг і відтворення. Кістки, камери, видимість слідують сесії.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Обличчя

Flex-контролери, скомпільовані правила і вершинні дельти — персонажі говорять і гримасують. Немає: wrinkle-карт.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Риги

Вирази, point/orient/parent/aim-констрейнти, дволанковий IK. Немає: повного графа залежностей операторів, створення ригів.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Редагування

Вибір кліком, маніпулятор переміщення/повороту, інспектор будь-якого атрибута, ключ на курсорі, скасування/повтор, побайтово точне збереження.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Виділення часу з hold і falloff на лінійці; правка розтікається по виділенню, як у SFM. Немає: пресетів, шарів.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Graph editor

Криві кожного логу вибраного елемента: X/Y/Z, pitch/yaw/roll, скаляри. Ключі рухаються мишею за часом і значенням з живим переглядом, вставляються подвійним кліком, видаляються; вісь часу спільна з таймлайном. Немає: дотичних і типів кривих, масштабування групи ключів.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Докінг панелей

Перетягування панелей на хрестовину цілей з попереднім переглядом, як в UE5 і Visual Studio. Немає: збережених розкладок, тем.

### <img alt="65%" src="https://img.shields.io/badge/65%25-e0a800?style=flat-square"> Шейдинг Source

Світло сесії (DmeProjectedLight): фрустум, згасання Source, спад до maxDistance; half-lambert, $lightwarptexture, phong ($phongexponent/boost/fresnelranges), $rimlight, $selfillum. Світ карти — за лайтмапами. Немає: тіней, гобо-текстур, $bumpmap, $envmap, ambient-кубів, скайбоксу.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Карти — <code>.bsp</code>

Версії 19–21: геометрія світу, displacement-рельєф, brush-ентіті, статичні пропи, матеріали з pak-лампа карти. Відсікання за пірамідою камери. Немає: лайтмап, скайбоксу, води, prop_dynamic.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Рендер у зображення і відео

Не розпочато.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Плагіни <code>.c2plg</code>

Не розпочато.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Теми і робочі простори

Свідомо відкладено: одна тема, поки редактору нічого оформлювати.

**До релізу не готовий.** Фундамент — кожен формат SFM, прочитаний вірно і перевірений на всій інсталяції, — є і покритий тестами; сесію можна відкрити, програти, змінити і зберегти. Бракує *зручності* роботи: graph editor, шейдингу Source, карт, експорту. Номер версії з'явиться, коли аніматор зможе відпрацювати в ньому день.

<p align="center"><a href="../README/UK-ua.md"><img alt="← Назад до README" src="https://img.shields.io/badge/%E2%86%90_%D0%9D%D0%B0%D0%B7%D0%B0%D0%B4_%D0%B4%D0%BE_README-1b2838?style=for-the-badge"></a></p>
