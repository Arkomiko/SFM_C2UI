<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <b>🇵🇱 Polski</b> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/test%C3%B3w-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — to moja przebudowa edytora Source Filmmaker: ta sama zawartość, ten sam format sesji, ten sam model danych — w powłoce, która wygląd zapożycza z biblioteki Steam, a układ z edytora Unreal Engine 5.</p>

---

## Idea

Source Filmmaker to świetne narzędzie w interfejsie z 2012 roku. Nie chcę nakładać skórki na `sfm.exe` ani przechwytywać jego okien po kolei. Chcę edytora, który **pyta, gdzie jest zainstalowany SFM**, montuje tę instalację tak, jak Garry's Mod montuje Counter-Strike'a, i wszystko robi sam na tych plikach — modele, materiały, tekstury, sesje, animację — nigdy nie uruchamiając SFM.

Cel to **funkcjonalność SFM jeden do jednego** (łącznie z kośćmi i rigami), a potem to, czego SFM nigdy nie miał.

```
  ┌──────────────┐    "gdzie jest SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  własne UI   │ ◀─────  montuje  ───────│    tf/  hl2/  tf_movies/ …   │
  │  własny render │      tylko odczyt      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Gotowość

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Ogólna gotowość do wydania: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Edytor z otwartą sesją Meet the Heavy" width="100%"><br><sub>Edytor dzisiaj: otwarta sesja Valve „Meet the Heavy” — ujęcia i dźwięk na osi czasu, drzewo sesji, pierwsze ujęcie przez jego własną kamerę, postacie w pozach i z twarzami z sesji.</sub></p>

Rozwiń obszar, aby zobaczyć, co dokładnie jest gotowe, a co nie. Procenty to moja uczciwa ocena względem możliwości SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Znajdowanie i montowanie SFM</b></summary>

Rejestr Steam → `libraryfolders.vdf` → ścieżki z `gameinfo.txt` w kolejności silnika. Sześć montowań na standardowej instalacji. Nic nie jest zapisywane poza folderem programu.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Indeks zawartości</b></summary>

70 199 plików w 1,1 s na zimno / 0,02 s z pamięci podręcznej; nadpisania między montowaniami rozwiązywane jak w silniku.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modele — `.mdl` `.vvd` `.vtx`</b></summary>

Wersje 44, 48, 49. Szkielet, siatki, wszystkie poziomy szczegółów, grupy ciała. 1 500 modeli wczytanych, 0 błędów.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Materiały — `.vmt`</b></summary>

Wszystkie 19 554 materiały z instalacji się wczytują; `patch`, bloki DX, proxy.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Tekstury — `.vtf`</b></summary>

Wersje 7.0–7.5, DXT1/3/5 i wszystkie formaty nieskompresowane, cubemapy, mipmapy. DXT trafia do GPU bez dekodowania.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Sesje — `.dmx`</b></summary>

Binary 1–5 i KeyValues2. Każda sesja i plik cząsteczek z instalacji zapisuje się z powrotem **bajt w bajt**.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Sesja na ekranie</b></summary>

Ujęcia i ścieżki dźwięku na osi czasu, drzewo elementów, scena ujęcia przez jego kamerę. Brak: map, cząsteczek, dźwięku.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animacja</b></summary>

Kanały i logi obliczane na kursorze; przewijanie i odtwarzanie. Kości, kamery i widoczność podążają za sesją.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Twarze</b></summary>

Kontrolery flex, skompilowane reguły i animacja wierzchołków — postacie mówią i wyrażają emocje. Brak: map zmarszczek.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Rigi</b></summary>

Wyrażenia, ograniczenia point/orient/parent/aim, IK dwukostny. Brak: pełnego grafu zależności operatorów, tworzenia rigów.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Edycja</b></summary>

Wybór kliknięciem, manipulator przesuwania/obrotu, inspektor dowolnego atrybutu, klucz na kursorze, cofnij/ponów, zapis bajt w bajt. Brak: edytora wykresów.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Zaznaczenie czasu z hold i falloff na linijce; edycja rozkłada się na zaznaczenie jak w SFM. Brak: presetów, warstw.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Dokowanie paneli</b></summary>

Przeciąganie paneli na kompas celów z podglądem, jak w UE5 i Visual Studio. Brak: zapisanych układów, motywów.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Cieniowanie Source</b></summary>

Tylko tekstura i proste światło. Brak: phong, rim, lightwarp, świateł sceny, cieni.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Mapy — `.bsp`</b></summary>

Nie rozpoczęte.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Render do obrazu i wideo</b></summary>

Nie rozpoczęte.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Wtyczki `.c2plg`</b></summary>

Nie rozpoczęte.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Motywy i przestrzenie robocze</b></summary>

Celowo później: jeden wygląd, dopóki edytor nie ma czego stylizować.

</details>

**Nie jest gotowy do wydania.** Fundament — każdy format SFM, poprawnie odczytany i sprawdzony na całej instalacji — jest na miejscu i przetestowany; sesję można otworzyć, odtworzyć, zmienić i zapisać. Brakuje *wygody* pracy: edytora wykresów, cieniowania Source, map, eksportu. Numer wersji pojawi się, gdy animator będzie mógł przepracować w nim dzień.

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
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Przy pierwszym uruchomieniu SFM jest szukany przez Steam; jeśli go nie znajdzie — zapyta. <kbd>Ctrl</kbd>+<kbd>O</kbd> otwiera sesję, <kbd>Space</kbd> odtwarza, <kbd>C</kbd> patrzy przez kamerę ujęcia, <kbd>T</kbd>/<kbd>R</kbd> przesuwa/obraca, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> cofa, <kbd>Ctrl</kbd>+<kbd>S</kbd> zapisuje. Panele przeciąga się za tytuł. Testy nie wymagają niczego:

```bash
python Testing/run.py
```

## Struktura

```
C2UI_SDK/
├── c2ui.py            program uruchamiający
├── Core/              silnik: formaty, wirtualny system plików, indeks, mosty
├── App/               edytor: biblioteka zawartości, renderer, okno
├── Tools/             lokalizacja, narzędzia UI, wtyczki (później)
├── Testing/           testy, fixtury bajt w bajt, jeden runner
└── GIT&DOCK/README/   ten README w innych językach
```

## Plan

1. **Edytor wykresów** — krzywe i klucze na oczach.
2. **Cieniowanie Source** — VertexLitGeneric tak, jak rysuje SFM: phong, rim, lightwarp, światła sceny.
3. **Mapy** — `.bsp` jako tło.
4. **Eksport** — obraz i wideo.
5. **Wtyczki** — format `.c2plg`; potem motywy i przestrzenie robocze.

## Licencja i podziękowania

Source Filmmaker, Team Fortress 2 i silnik Source należą do Valve. Projekt czyta ich formaty plików, nie zawiera ich plików i działa tylko z twoją kopią SFM ze Steam.

Licencja własnego kodu C2UI nie została jeszcze wybrana — do tego czasu wszelkie prawa zastrzeżone. Zgłoszenia i pull requesty są mile widziane.

<p align="center"><img src="../../.github/assets/models.png" alt="64 modele wyrenderowane prosto z instalacji" width="60%"><br><sub>Sześćdziesiąt cztery losowe modele z instalacji, narysowane przez własny renderer C2UI.</sub></p>
