<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <b>🇧🇾 Беларуская</b> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81-%D0%BF%D1%80%D1%8D--%D0%B0%D0%BB%D1%8C%D1%84%D0%B0-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%D1%82%D1%8D%D1%81%D1%82%D0%B0%D1%9E-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — гэта мая перазборка рэдактара Source Filmmaker: той самы кантэнт, той самы фармат сесій, тая самая мадэль даных — у абалонцы, якая бярэ выгляд ад бібліятэкі Steam, а кампаноўку ад рэдактара Unreal Engine 5.</p>

---

## Ідэя

Source Filmmaker — выдатны інструмент у інтэрфейсе 2012 года. Я не хачу нацягваць скін на `sfm.exe` і не хачу перахапляць яго вокны па адным. Я хачу рэдактар, які **пытаецца, дзе ўсталяваны SFM**, мантуе гэтую ўстаноўку так, як Garry's Mod мантуе Counter-Strike, і ўсё робіць сам паверх гэтых файлаў — мадэлі, матэрыялы, тэкстуры, сесіі, анімацыю — ніколі не запускаючы SFM.

Мэта — **функцыянальнасць SFM адзін у адзін** (уключна з косткамі і рыгамі), а далей тое, чаго ў SFM ніколі не было.

```
  ┌──────────────┐    "дзе SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  свой UI     │ ◀─────  мантуе   ───────│    tf/  hl2/  tf_movies/ …   │
  │  свой рэндар │      толькі чытанне      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Гатоўнасць

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Агульная гатоўнасць да рэлізу: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Рэдактар з адкрытай сесіяй Meet the Heavy" width="100%"><br><sub>Рэдактар сёння: адкрыта сесія Valve «Meet the Heavy» — шоты і гук на таймлайне, дрэва сесіі, першы шот праз яго ўласную камеру, персанажы ў позах і з тварамі з сесіі.</sub></p>

Разгарніце вобласць, каб убачыць, што менавіта гатова, а што не. Працэнты — мая сумленная ацэнка адносна магчымасцей SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Пошук і мантаванне SFM</b></summary>

Рэестр Steam → `libraryfolders.vdf` → шляхі з `gameinfo.txt` у парадку рухавіка. Шэсць мантаванняў на стандартнай устаноўцы. Нічога не пішацца па-за папкай праграмы.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Індэкс кантэнту</b></summary>

70 199 файлаў за 1,1 с холадна / 0,02 с з кэшу; перавызначэнні паміж мантаваннямі вырашаюцца як у рухавіку.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Мадэлі — `.mdl` `.vvd` `.vtx`</b></summary>

Версіі 44, 48, 49. Шкілет, мешы, усе ўзроўні дэталізацыі, body-групы. 1 500 мадэляў загружана, 0 збояў.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Матэрыялы — `.vmt`</b></summary>

Усе 19 554 матэрыялы ўстаноўкі чытаюцца; `patch`, DX-блокі, проксі.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Тэкстуры — `.vtf`</b></summary>

Версіі 7.0–7.5, DXT1/3/5 і ўсе несціснутыя фарматы, кубмапы, mip-узроўні. DXT ідзе ў GPU без распакоўкі.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Сесіі — `.dmx`</b></summary>

Binary 1–5 і KeyValues2. Кожная сесія і файл часціц устаноўкі запісваюцца назад **пабайтава ідэнтычна**.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Сесія на экране</b></summary>

Шоты і гукавыя дарожкі на таймлайне, дрэва элементаў, сцэна шота праз яго камеру. Няма: карт, часціц, гуку.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Анімацыя</b></summary>

Каналы і логі вылічаюцца на курсоры; скрабінг і прайграванне. Косткі, камеры, бачнасць ідуць за сесіяй.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Твары</b></summary>

Flex-кантролеры, скампіляваныя правілы і вяршынныя дэльты — персанажы гавораць і грымаснічаюць. Няма: wrinkle-карт.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Рыгі</b></summary>

Выразы, point/orient/parent/aim-канстрэйнты, двухзвённы IK. Няма: поўнага графа залежнасцей аператараў, стварэння рыгаў.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Рэдагаванне</b></summary>

Выбар клікам, маніпулятар перамяшчэння/павароту, інспектар любога атрыбута, ключ на курсоры, адмена/паўтор, пабайтава дакладнае захаванне. Няма: graph editor.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Вылучэнне часу з hold і falloff на лінейцы; праўка расцякаецца па вылучэнні, як у SFM. Няма: прэсэтаў, слаёў.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Докінг панэляў</b></summary>

Перацягванне панэляў на крыжавіну мэт з папярэднім праглядам, як у UE5 і Visual Studio. Няма: захаваных раскладак, тэм.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Шэйдынг Source</b></summary>

Пакуль толькі тэкстура і простае святло. Няма: phong, rim, lightwarp, асвятлення сцэны, ценяў.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Карты — `.bsp`</b></summary>

Не пачата.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Рэндар у выяву і відэа</b></summary>

Не пачата.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Плагіны `.c2plg`</b></summary>

Не пачата.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Тэмы і працоўныя прасторы</b></summary>

Свядома адкладзена: адна тэма, пакуль рэдактару няма чаго афармляць.

</details>

**Да рэлізу не гатовы.** Падмурак — кожны фармат SFM, прачытаны правільна і правераны на ўсёй устаноўцы, — ёсць і пакрыты тэстамі; сесію можна адкрыць, прайграць, змяніць і захаваць. Не хапае *зручнасці* працы: graph editor, шэйдынгу Source, карт, экспарту. Нумар версіі з'явіцца, калі аніматар зможа адпрацаваць у ім дзень.

## Чым адрозніваецца

- **Пераносны.** Нічога не пішацца па-за папкай праграмы: налады ў `App/User`, кэш у `App/Cache`, часовае ў `App/Temporary`. Выдалілі папку — следу не засталося.
- **Не запускае SFM.** Няма працэсу, якім трэба кіраваць, няма вокнаў, якія трэба перахапляць. Устаноўка чытаецца як пакет кантэнту.
- **Фарматы правераны, а не прадугаданы.** Кожная чыталка звераная з сапраўднай устаноўкай; там, дзе фармат робіць нешта нечаканае, код пра гэта кажа.
- **Захаванне дакладнае.** Сесія, прачытаная і запісаная без змен, — той самы файл.
- **Ядро без залежнасцей.** `Core/` і ўсе тэсты працуюць на голым Python; Qt і OpenGL патрэбныя толькі акну.

## Запуск

Патрэбныя Windows, Python 3.13 і ўсталяваны Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Пры першым запуску SFM шукаецца праз Steam; калі не знайшоўся — праграма спытае. <kbd>Ctrl</kbd>+<kbd>O</kbd> адкрывае сесію, <kbd>Space</kbd> — прайграванне, <kbd>C</kbd> — камера шота, <kbd>T</kbd>/<kbd>R</kbd> — перамяшчэнне/паварот, <kbd>M</kbd> — motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> — адмена, <kbd>Ctrl</kbd>+<kbd>S</kbd> — захаваць. Панэлі перацягваюцца за загаловак. Тэсты не патрабуюць нічога:

```bash
python Testing/run.py
```

## Структура

```
C2UI_SDK/
├── c2ui.py            лаўнчар
├── Core/              ядро: фарматы, віртуальная ФС, індэкс, масты да ўстановак
├── App/               рэдактар: бібліятэка кантэнту, рэндар, акно
├── Tools/             лакалізацыя, інструменты UI, плагіны (пазней)
├── Testing/           тэсты, пабайтавыя фікстуры, адзін ранер
└── GIT&DOCK/README/   гэты README на іншых мовах
```

## Дарожная карта

1. **Graph editor** — крывыя і ключы на вачах.
2. **Шэйдынг Source** — VertexLitGeneric як малюе SFM: phong, rim, lightwarp, асвятленне сцэны.
3. **Карты** — `.bsp` для фону.
4. **Экспарт** — выява і відэа.
5. **Плагіны** — фармат `.c2plg`; затым тэмы і працоўныя прасторы.

## Ліцэнзія і падзякі

Source Filmmaker, Team Fortress 2 і рухавік Source належаць Valve. Праект чытае іх фарматы, не змяшчае іх файлаў і працуе толькі з вашай копіяй SFM са Steam.

Ліцэнзія ўласнага кода C2UI яшчэ не абраная — да таго часу ўсе правы абароненыя. Issues і pull requests вітаюцца.

<p align="center"><img src="../../.github/assets/models.png" alt="64 мадэлі, адрэндараныя проста з устаноўкі" width="60%"><br><sub>Шэсцьдзясят чатыры выпадковыя мадэлі з устаноўкі, намаляваныя ўласным рэндарарам C2UI.</sub></p>
