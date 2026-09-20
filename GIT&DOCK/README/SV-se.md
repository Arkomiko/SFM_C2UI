<p align="center"><img src="../assets/SV-se/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <b>🇸🇪 Svenska</b> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/tester-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — Source Filmmakers redigerare i ett modernt skal: samma innehåll, samma sessionsformat, samma datamodell, ett gränssnitt i Steam-bibliotekets och Unreal Engine 5-redigerarens anda.</p>

---

## Mognad

<p align="center"><img src="../assets/SV-se/sidebar.svg" alt="Mognad" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Total mognad för release: 41%</b></p>

<p align="center"><a href="../assets/SV-se/sidebar.md"><img alt="Mognad i detalj" src="https://img.shields.io/badge/Mognad_i_detalj-66c0f4?style=for-the-badge"></a></p>

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
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Vid första start söks SFM via Steam; hittas det inte frågar programmet. <kbd>Ctrl</kbd>+<kbd>O</kbd> öppnar en session, <kbd>Mellanslag</kbd> spelar, <kbd>C</kbd> tittar genom shotkameran, <kbd>T</kbd>/<kbd>R</kbd> flytta/rotera, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> ångrar, <kbd>Ctrl</kbd>+<kbd>S</kbd> sparar. Paneler dras i sin titel. Testerna behöver ingenting alls:

```bash
python Testing/run.py
```

## Struktur

```
C2UI_SDK/
├── README.md
├── Core/              motor: format, virtuellt filsystem, index, bryggor
├── App/               redigeraren: innehållsbibliotek, renderare, fönster
├── Tools/             lokalisering, UI-verktyg, insticksprogram (senare)
│   └── Launcher/      startaren
├── Testing/           tester, byteexakta fixturer, en körare
└── GIT&DOCK/          denna README på andra språk
```

## Färdplan

1. **Source-skuggning** — VertexLitGeneric som SFM ritar det: phong, rim, lightwarp, scenljus.
2. **Kartor** — `.bsp` för bakgrunder.
3. **Utdata** — bild- och videoexport.
4. **Insticksprogram** — formatet `.c2plg`; sedan teman och arbetsytor.

## Licens och tack

C2UI:s egen kod är under **C2UI-licensen**: fri för personligt och icke-kommersiellt bruk; kommersiellt bruk endast med upphovspersonens skriftliga medgivande; ändrade versioner måste ange originalprojektet och dess upphovsperson Arkomiko. Insticksprogram och tillägg är under licensen **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 och Source-motorn tillhör Valve; projektet läser deras format, innehåller inga av deras filer och fungerar bara med din egen kopia av SFM från Steam.

<p align="center"><a href="../LICENSE/SV-se.md"><img alt="Licenstext" src="https://img.shields.io/badge/Licenstext-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 modeller renderade direkt från installationen" width="60%"><br><sub>Sextiofyra slumpvis valda modeller från installationen, ritade av C2UI:s egen renderare.</sub></p>
