<p align="center"><img src="../assets/SV-se/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <b>🇸🇪 Svenska</b> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/tester-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — Source Filmmakers redigerare i ett modernt skal: samma innehåll, samma sessionsformat, samma datamodell, ett gränssnitt i Steam-bibliotekets och Unreal Engine 5-redigerarens anda.</p>

---

## Idén

Source Filmmaker är ett starkt verktyg vars gränssnitt stannade i 2012. C2UI ersätter det inte och gör inte om det: målet är helt enkelt att göra SFM lite modernare och bekvämare.

Redigeraren hittar det installerade SFM, kopplar in det som ett innehållsbibliotek — modeller, material, texturer, sessioner — och arbetar med samma filer i samma format. Allt som gjorts i SFM öppnas i C2UI, och tvärtom.

Första målet är full kompatibilitet med SFM, ben och riggar inräknade. Därefter det som SFM saknade.

```
  ┌──────────────┐    "var är SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  eget UI     │ ◀───── monterad  ───────│    tf/  hl2/  tf_movies/ …   │
  │  egen render │      skrivskyddad      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Mognad

<img align="right" src="../assets/SV-se/sidebar.svg" alt="Mognad" width="300">

<img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Total mognad för release: 38%</b>

Varje område kan fällas ut: vad som redan fungerar och vad som inte finns än. Procenten är en uppskattning mot vad SFM kan.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Hitta och montera SFM</b></summary>

Steam-registret → `libraryfolders.vdf` → sökvägarna i `gameinfo.txt`, i motorns egen ordning. Sex monteringar på en standardinstallation. Inget skrivs utanför programmappen.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Innehållsindex</b></summary>

70 199 filer på 1,1 s kallt / 0,02 s varmt; överskuggningar mellan monteringar löses exakt som motorn gör.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modeller — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

Version 44, 48, 49. Skelett, meshar, alla detaljnivåer, kroppsgrupper. 1 500 modeller laddade, 0 fel.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Material — <code>.vmt</code></b></summary>

Alla 19 554 medföljande material tolkas; `patch`, DX-block, proxyer.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Texturer — <code>.vtf</code></b></summary>

Version 7.0–7.5, DXT1/3/5 och alla okomprimerade format, kubkartor, mippar. DXT går till GPU:n utan avkodning.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Sessioner — <code>.dmx</code></b></summary>

Binär 1–5 och KeyValues2. Varje session och partikelfil i installationen skrivs tillbaka **byte för byte**.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Session på skärmen</b></summary>

Shots och ljudspår på en tidslinje, elementträdet, varje shots scen genom sin kamera. Inte ännu: kartor, partiklar, ljud.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animation</b></summary>

Kanaler och loggar utvärderas vid markören; scrubba och spela. Ben, kameror och synlighet följer sessionen.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Ansikten</b></summary>

Flex-kontroller, de kompilerade reglerna och vertexanimation — karaktärer pratar och visar känslor. Inte ännu: rynkkartor.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Riggar</b></summary>

Uttryck, point/orient/parent/aim-begränsningar, tvåbens-IK. Inte ännu: hela operatorberoendegrafen, riggskapande.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Redigering</b></summary>

Klicka för att välja, en flytta/rotera-manipulator, en inspektör för alla attribut, en nyckel vid markören, ångra/gör om, byteexakt sparning. Inte ännu: grafredigeraren.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Ett tidsurval med hold och falloff på linjalen; en ändring sprids över det som i SFM. Inte ännu: förinställningar, lager.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Paneldockning</b></summary>

Dra paneler till en kompass av mål med förhandsvisning, som i UE5 och Visual Studio. Inte ännu: sparade layouter, teman.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source-skuggning</b></summary>

Bara textur och ett enkelt ljus. Inte ännu: phong, rim, lightwarp, scenljus, skuggor.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Kartor — <code>.bsp</code></b></summary>

Inte påbörjat.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Rendering till bild och video</b></summary>

Inte påbörjat.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Insticksprogram <code>.c2plg</code></b></summary>

Inte påbörjat.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Teman och arbetsytor</b></summary>

Medvetet senare: ett utseende tills redigeraren har något värt att tema.

</details>

**Inte redo för release.** Grunden — varje filformat SFM använder, korrekt läst och verifierat mot hela installationen — finns och är testad; en session kan öppnas, spelas, ändras och sparas. Det som saknas är *bekvämligheten* i arbetet: grafredigeraren, Source-skuggning, kartor, export. Inget versionsnummer förrän en animatör kan göra en dags arbete i den.

<br clear="all">

<p align="center"><img src="../assets/editor.png" alt="Redigeraren med Meet the Heavy öppen" width="100%"><br><sub>Redigeraren idag, med Valves Meet the Heavy öppen: shots och ljud på tidslinjen, sessionsträdet, första shoten sedd genom sin egen kamera, karaktärer poserade och med ansikten enligt sessionen.</sub></p>

## Vad som gör den annorlunda

- **Portabel.** Inget skrivs utanför programmappen: inställningar under `App/User`, cache under `App/Cache`, tillfälligt under `App/Temporary`. Ta bort mappen och den är borta.
- **Kör aldrig SFM.** Ingen process att styra, inga fönster att kapa. Installationen läses som ett innehållspaket.
- **Format verifierade, inte antagna.** Varje läsare kontrollerades mot den riktiga installationen; där ett format gör något överraskande säger koden det.
- **Sparningen är exakt.** En session som läses och skrivs oförändrad är samma fil.
- **Motorn har inga beroenden.** `Core/` och hela testsviten körs på ren Python; bara fönstret behöver Qt och OpenGL.

## Köra

Kräver Windows, Python 3.13 och en Source Filmmaker-installation.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Vid första start söks SFM via Steam; hittas det inte frågar programmet. <kbd>Ctrl</kbd>+<kbd>O</kbd> öppnar en session, <kbd>Mellanslag</kbd> spelar, <kbd>C</kbd> tittar genom shotkameran, <kbd>T</kbd>/<kbd>R</kbd> flytta/rotera, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> ångrar, <kbd>Ctrl</kbd>+<kbd>S</kbd> sparar. Paneler dras i sin titel. Testerna behöver ingenting alls:

```bash
python Testing/run.py
```

## Struktur

```
C2UI_SDK/
├── c2ui.py            startaren
├── Core/              motor: format, virtuellt filsystem, index, bryggor
├── App/               redigeraren: innehållsbibliotek, renderare, fönster
├── Tools/             lokalisering, UI-verktyg, insticksprogram (senare)
├── Testing/           tester, byteexakta fixturer, en körare
└── GIT&DOCK/README/   denna README på andra språk
```

## Färdplan

1. **Grafredigerare** — kurvor och nycklar, synliga.
2. **Source-skuggning** — VertexLitGeneric som SFM ritar det: phong, rim, lightwarp, scenljus.
3. **Kartor** — `.bsp` för bakgrunder.
4. **Utdata** — bild- och videoexport.
5. **Insticksprogram** — formatet `.c2plg`; sedan teman och arbetsytor.

## Licens och tack

Source Filmmaker, Team Fortress 2 och Source-motorn tillhör Valve. Projektet läser deras filformat, levererar inga av deras filer och fungerar bara med en kopia av SFM du redan har via Steam.

Licensen för C2UI:s egen kod är inte vald ännu — tills dess, alla rättigheter förbehållna. Issues och pull requests är ändå välkomna.

<p align="center"><img src="../assets/models.png" alt="64 modeller renderade direkt från installationen" width="60%"><br><sub>Sextiofyra slumpvis valda modeller från installationen, ritade av C2UI:s egen renderare.</sub></p>
