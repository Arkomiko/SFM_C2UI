# Gotowość C2UI — szczegółowo

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <b>🇵🇱 Polski</b> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Gotowość" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Ogólna gotowość do wydania: 41%</b></p>

Każdy obszar można rozwinąć: co już działa, a czego jeszcze nie ma. Procenty to ocena względem możliwości SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Znajdowanie i montowanie SFM

Rejestr Steam → `libraryfolders.vdf` → ścieżki z `gameinfo.txt` w kolejności silnika. Sześć montowań na standardowej instalacji. Nic nie jest zapisywane poza folderem programu.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Indeks zawartości

70 199 plików w 1,1 s na zimno / 0,02 s z pamięci podręcznej; nadpisania między montowaniami rozwiązywane jak w silniku.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modele — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Wersje 44, 48, 49. Szkielet, siatki, wszystkie poziomy szczegółów, grupy ciała. 1 500 modeli wczytanych, 0 błędów.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Materiały — <code>.vmt</code>

Wszystkie 19 554 materiały z instalacji się wczytują; `patch`, bloki DX, proxy.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Tekstury — <code>.vtf</code>

Wersje 7.0–7.5, DXT1/3/5 i wszystkie formaty nieskompresowane, cubemapy, mipmapy. DXT trafia do GPU bez dekodowania.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sesje — <code>.dmx</code>

Binary 1–5 i KeyValues2. Każda sesja i plik cząsteczek z instalacji zapisuje się z powrotem **bajt w bajt**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Sesja na ekranie

Ujęcia i ścieżki dźwięku na osi czasu, drzewo elementów, scena ujęcia przez jego kamerę. Brak: map, cząsteczek, dźwięku.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animacja

Kanały i logi obliczane na kursorze; przewijanie i odtwarzanie. Kości, kamery i widoczność podążają za sesją.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Twarze

Kontrolery flex, skompilowane reguły i animacja wierzchołków — postacie mówią i wyrażają emocje. Brak: map zmarszczek.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rigi

Wyrażenia, ograniczenia point/orient/parent/aim, IK dwukostny. Brak: pełnego grafu zależności operatorów, tworzenia rigów.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Edycja

Wybór kliknięciem, manipulator przesuwania/obrotu, inspektor dowolnego atrybutu, klucz na kursorze, cofnij/ponów, zapis bajt w bajt.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Zaznaczenie czasu z hold i falloff na linijce; edycja rozkłada się na zaznaczenie jak w SFM. Brak: presetów, warstw.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Edytor wykresów

Krzywe każdego logu wybranego elementu: X/Y/Z, pitch/yaw/roll, skalary. Klucze przeciąga się w czasie i wartości z podglądem na żywo, dwuklik wstawia, Delete usuwa; oś czasu wspólna z osią czasu. Brak: stycznych i typów krzywych, skalowania grupy kluczy.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Dokowanie paneli

Przeciąganie paneli na kompas celów z podglądem, jak w UE5 i Visual Studio. Brak: zapisanych układów, motywów.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Cieniowanie Source

Tylko tekstura i proste światło. Brak: phong, rim, lightwarp, świateł sceny, cieni.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Mapy — <code>.bsp</code>

Nie rozpoczęte.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Render do obrazu i wideo

Nie rozpoczęte.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Wtyczki <code>.c2plg</code>

Nie rozpoczęte.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Motywy i przestrzenie robocze

Celowo później: jeden wygląd, dopóki edytor nie ma czego stylizować.

**Nie jest gotowy do wydania.** Fundament — każdy format SFM, poprawnie odczytany i sprawdzony na całej instalacji — jest na miejscu i przetestowany; sesję można otworzyć, odtworzyć, zmienić i zapisać. Brakuje *wygody* pracy: edytora wykresów, cieniowania Source, map, eksportu. Numer wersji pojawi się, gdy animator będzie mógł przepracować w nim dzień.

<p align="center"><a href="../../README/PL-pl.md"><img alt="← Wróć do README" src="https://img.shields.io/badge/%E2%86%90_Wr%C3%B3%C4%87_do_README-1b2838?style=for-the-badge"></a></p>
