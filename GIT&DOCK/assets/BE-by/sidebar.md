# Гатоўнасць C2UI — падрабязна

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <b>🇧🇾 Беларуская</b> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Гатоўнасць" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Агульная гатоўнасць да рэлізу: 41%</b></p>

Кожная вобласць разгортваецца: што ўжо працуе і чаго пакуль няма. Працэнты — ацэнка адносна магчымасцей SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Пошук і мантаванне SFM

Рэестр Steam → `libraryfolders.vdf` → шляхі з `gameinfo.txt` у парадку рухавіка. Шэсць мантаванняў на стандартнай устаноўцы. Нічога не пішацца па-за папкай праграмы.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Індэкс кантэнту

70 199 файлаў за 1,1 с холадна / 0,02 с з кэшу; перавызначэнні паміж мантаваннямі вырашаюцца як у рухавіку.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Мадэлі — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Версіі 44, 48, 49. Шкілет, мешы, усе ўзроўні дэталізацыі, body-групы. 1 500 мадэляў загружана, 0 збояў.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Матэрыялы — <code>.vmt</code>

Усе 19 554 матэрыялы ўстаноўкі чытаюцца; `patch`, DX-блокі, проксі.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Тэкстуры — <code>.vtf</code>

Версіі 7.0–7.5, DXT1/3/5 і ўсе несціснутыя фарматы, кубмапы, mip-узроўні. DXT ідзе ў GPU без распакоўкі.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Сесіі — <code>.dmx</code>

Binary 1–5 і KeyValues2. Кожная сесія і файл часціц устаноўкі запісваюцца назад **пабайтава ідэнтычна**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Сесія на экране

Шоты і гукавыя дарожкі на таймлайне, дрэва элементаў, сцэна шота праз яго камеру. Няма: карт, часціц, гуку.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Анімацыя

Каналы і логі вылічаюцца на курсоры; скрабінг і прайграванне. Косткі, камеры, бачнасць ідуць за сесіяй.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Твары

Flex-кантролеры, скампіляваныя правілы і вяршынныя дэльты — персанажы гавораць і грымаснічаюць. Няма: wrinkle-карт.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Рыгі

Выразы, point/orient/parent/aim-канстрэйнты, двухзвённы IK. Няма: поўнага графа залежнасцей аператараў, стварэння рыгаў.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Рэдагаванне

Выбар клікам, маніпулятар перамяшчэння/павароту, інспектар любога атрыбута, ключ на курсоры, адмена/паўтор, пабайтава дакладнае захаванне.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Вылучэнне часу з hold і falloff на лінейцы; праўка расцякаецца па вылучэнні, як у SFM. Няма: прэсэтаў, слаёў.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Graph editor

Крывыя кожнага лога выбранага элемента: X/Y/Z, pitch/yaw/roll, скаляры. Ключы рухаюцца мышшу па часе і значэнні з жывым праглядам, устаўляюцца падвойным клікам, выдаляюцца; вось часу агульная з таймлайнам. Няма: датычных і тыпаў крывых, маштабавання групы ключоў.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Докінг панэляў

Перацягванне панэляў на крыжавіну мэт з папярэднім праглядам, як у UE5 і Visual Studio. Няма: захаваных раскладак, тэм.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Шэйдынг Source

Пакуль толькі тэкстура і простае святло. Няма: phong, rim, lightwarp, асвятлення сцэны, ценяў.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Карты — <code>.bsp</code>

Не пачата.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Рэндар у выяву і відэа

Не пачата.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Плагіны <code>.c2plg</code>

Не пачата.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Тэмы і працоўныя прасторы

Свядома адкладзена: адна тэма, пакуль рэдактару няма чаго афармляць.

**Да рэлізу не гатовы.** Падмурак — кожны фармат SFM, прачытаны правільна і правераны на ўсёй устаноўцы, — ёсць і пакрыты тэстамі; сесію можна адкрыць, прайграць, змяніць і захаваць. Не хапае *зручнасці* працы: graph editor, шэйдынгу Source, карт, экспарту. Нумар версіі з'явіцца, калі аніматар зможа адпрацаваць у ім дзень.

<p align="center"><a href="../../README/BE-by.md"><img alt="← Назад да README" src="https://img.shields.io/badge/%E2%86%90_%D0%9D%D0%B0%D0%B7%D0%B0%D0%B4_%D0%B4%D0%B0_README-1b2838?style=for-the-badge"></a></p>
