# Готовность C2UI — подробно

<details align="center"><summary>&nbsp;🌐 <b>🇷🇺 Русский</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><b>🇷🇺<br>Русский</b></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/RU-ru.svg" alt="Готовность" width="100%"></p>

<p align="center"><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Общая готовность к релизу: 15%</b></p>

Каждая область раскрывается: что уже работает и чего пока нет. Проценты — оценка относительно возможностей SFM.

Каждый процент — это **область относительно того, что делает SFM в ней**, а не относительно задуманного. Общая цифра измеряет весь продукт целиком рядом с SFM и потому намного ниже: форматы читаются полностью, но быть Source Filmmaker'ом — это ещё около 350 типов элементов `Dme*`, из которых движок знает 23.

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

Шоты и звуковые дорожки на таймлайне, дерево элементов, сцена шота через его камеру, карта шота. Нет: частиц, звука.

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

### <img alt="75%" src="https://img.shields.io/badge/75%25-3b9c5b?style=flat-square"> Шейдинг Source

Свет сессии (DmeProjectedLight): фрустум, затухание Source, спад к maxDistance; half-lambert, $lightwarptexture, phong, $rimlight, $selfillum. Мир карты — по лайтмапам; модели освещают ambient-кубы и world lights карты. Нет: теней, гобо-текстур, $bumpmap, $envmap.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Карты — <code>.bsp</code>

Версии 19–21: геометрия мира, displacement-рельеф, brush-энтити, статичные пропы, материалы из pak-лампа карты, лайтмапы, скайбокс вокруг камеры. Отсекание по пирамиде камеры. Нет: воды, prop_dynamic.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Рендер в изображение и видео

PNG/TGA-последовательности и AVI/MP4 из сессии: вся сессия, текущий шот или диапазон; пресеты; File → Export, Ctrl+E. Нет: звука в видео.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Плагины <code>.c2plg</code>

Не начато.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Темы и рабочие пространства

Сознательно отложено: одна тема, пока редактору нечего оформлять.

**К релизу не готов.** Фундамент — каждый формат SFM, прочитанный верно и проверенный на всей установке, — есть и покрыт тестами; сессию можно открыть, проиграть, изменить и сохранить. Не хватает *удобства* работы: graph editor, шейдинг Source, карты, экспорт. Номер версии появится, когда аниматор сможет отработать в нём день.

<p align="center"><a href="../../README.md"><img alt="← Назад к README" src="https://img.shields.io/badge/%E2%86%90_%D0%9D%D0%B0%D0%B7%D0%B0%D0%B4_%D0%BA_README-1b2838?style=for-the-badge"></a></p>
