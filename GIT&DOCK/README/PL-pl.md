<p align="center"><img src="../assets/PL-pl/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <b>🇵🇱 Polski</b> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/test%C3%B3w-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — edytor Source Filmmaker w nowoczesnej powłoce: ta sama zawartość, ten sam format sesji, ten sam model danych, interfejs w duchu biblioteki Steam i edytora Unreal Engine 5.</p>

---

## Gotowość

<p align="center"><img src="../assets/PL-pl/sidebar.svg" alt="Gotowość" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Ogólna gotowość do wydania: 41%</b></p>

<p align="center"><a href="../assets/PL-pl/sidebar.md"><img alt="Gotowość szczegółowo" src="https://img.shields.io/badge/Gotowo%C5%9B%C4%87_szczeg%C3%B3%C5%82owo-66c0f4?style=for-the-badge"></a></p>

## Idea

Source Filmmaker to mocne narzędzie, którego interfejs został w 2012 roku. C2UI go nie zastępuje ani nie przerabia: celem jest po prostu uczynić SFM nieco nowocześniejszym i wygodniejszym.

Edytor znajduje zainstalowany SFM, podłącza go jako bibliotekę zawartości — modele, materiały, tekstury, sesje — i pracuje na tych samych plikach w tym samym formacie. Wszystko, co powstało w SFM, otwiera się w C2UI, i odwrotnie.

Pierwszy cel to pełna zgodność z SFM, łącznie z kośćmi i rigami. Potem — to, czego w SFM brakowało.

```
  ┌──────────────┐    "gdzie jest SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  własne UI   │ ◀─────  montuje  ───────│    tf/  hl2/  tf_movies/ …   │
  │  własny render │      tylko odczyt      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Edytor z otwartą sesją Meet the Heavy" width="100%"><br><sub>Edytor dzisiaj: otwarta sesja Valve „Meet the Heavy” — ujęcia i dźwięk na osi czasu, drzewo sesji, pierwsze ujęcie przez jego własną kamerę, postacie w pozach i z twarzami z sesji.</sub></p>

## Czym się różni

- **Przenośny.** Nic nie jest zapisywane poza folderem programu: ustawienia w `App/User`, pamięć podręczna w `App/Cache`, pliki tymczasowe w `App/Temporary`. Usuń folder i nie ma śladu.
- **Nigdy nie uruchamia SFM.** Nie ma procesu do sterowania ani okien do przechwytywania. Instalacja jest czytana jak pakiet zawartości.
- **Formaty sprawdzone, nie założone.** Każdy czytnik porównano z prawdziwą instalacją; gdzie format robi coś zaskakującego, kod o tym mówi.
- **Zapis jest dokładny.** Sesja odczytana i zapisana bez zmian to ten sam plik.
- **Silnik bez zależności.** `Core/` i wszystkie testy działają na czystym Pythonie; tylko okno potrzebuje Qt i OpenGL.

## Uruchamianie

Wymaga Windows, Pythona 3.13 i zainstalowanego Source Filmmakera.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Przy pierwszym uruchomieniu SFM jest szukany przez Steam; jeśli go nie znajdzie — zapyta. <kbd>Ctrl</kbd>+<kbd>O</kbd> otwiera sesję, <kbd>Space</kbd> odtwarza, <kbd>C</kbd> patrzy przez kamerę ujęcia, <kbd>T</kbd>/<kbd>R</kbd> przesuwa/obraca, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> cofa, <kbd>Ctrl</kbd>+<kbd>S</kbd> zapisuje. Panele przeciąga się za tytuł. Testy nie wymagają niczego:

```bash
python Testing/run.py
```

## Struktura

```
C2UI_SDK/
├── README.md
├── Core/              silnik: formaty, wirtualny system plików, indeks, mosty
├── App/               edytor: biblioteka zawartości, renderer, okno
├── Tools/             lokalizacja, narzędzia UI, wtyczki (później)
│   └── Launcher/      program uruchamiający
├── Testing/           testy, fixtury bajt w bajt, jeden runner
└── GIT&DOCK/          ten README w innych językach
```

## Plan

1. **Cieniowanie Source** — VertexLitGeneric tak, jak rysuje SFM: phong, rim, lightwarp, światła sceny.
2. **Mapy** — `.bsp` jako tło.
3. **Eksport** — obraz i wideo.
4. **Wtyczki** — format `.c2plg`; potem motywy i przestrzenie robocze.

## Licencja i podziękowania

Własny kod C2UI jest na **licencji C2UI**: swobodnie do użytku osobistego i niekomercyjnego; użycie komercyjne tylko za pisemną zgodą autora; wersje zmodyfikowane muszą wskazywać oryginalny projekt i jego autora, Arkomiko. Wtyczki i dodatki — na licencji **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 i silnik Source należą do Valve; projekt czyta ich formaty, nie zawiera ich plików i działa tylko z twoją kopią SFM ze Steam.

<p align="center"><a href="../LICENSE/PL-pl.md"><img alt="Tekst licencji" src="https://img.shields.io/badge/Tekst_licencji-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 modele wyrenderowane prosto z instalacji" width="60%"><br><sub>Sześćdziesiąt cztery losowe modele z instalacji, narysowane przez własny renderer C2UI.</sub></p>
