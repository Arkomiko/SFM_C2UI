<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <b>🇮🇹 Italiano</b> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/stato-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/test-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — è la mia ricostruzione dell'editor di Source Filmmaker: lo stesso contenuto, lo stesso formato di sessione, lo stesso modello di dati, dentro un guscio che prende l'aspetto dalla libreria di Steam e la disposizione dall'editor di Unreal Engine 5.</p>

---

## L'idea

Source Filmmaker è uno strumento eccellente con un'interfaccia del 2012. Non voglio una skin sopra `sfm.exe`, né voglio dirottarne le finestre una alla volta. Voglio un editor che **chieda dove è installato SFM**, monti quell'installazione come Garry's Mod monta Counter-Strike, e faccia tutto da sé su quei file — modelli, materiali, texture, sessioni, animazione — senza mai avviare SFM.

L'obiettivo è la **parità di funzioni con SFM, uno a uno** (ossa e rig compresi), poi ciò che SFM non ha mai avuto.

```
  ┌──────────────┐    "dov'è SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI propria  │ ◀─────  montato  ───────│    tf/  hl2/  tf_movies/ …   │
  │  render proprio │      sola lettura      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Stato di avanzamento

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Avanzamento complessivo verso il rilascio: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="L'editor con Meet the Heavy aperto" width="100%"><br><sub>L'editor oggi, con Meet the Heavy di Valve aperto: inquadrature e audio sulla timeline, l'albero della sessione, la prima inquadratura vista dalla sua camera, personaggi in posa e con le espressioni dettate dalla sessione.</sub></p>

Espandi un'area per vedere esattamente cosa è fatto e cosa no. Le percentuali sono la mia stima onesta rispetto a ciò che sa fare SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Trovare e montare SFM</b></summary>

Registro di Steam → `libraryfolders.vdf` → i percorsi di ricerca di `gameinfo.txt`, nell'ordine del motore. Sei montaggi su un'installazione standard. Nulla viene scritto fuori dalla cartella dell'applicazione.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Indice dei contenuti</b></summary>

70 199 file in 1,1 s a freddo / 0,02 s dalla cache; le sovrascritture tra montaggi risolte esattamente come fa il motore.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modelli — `.mdl` `.vvd` `.vtx`</b></summary>

Versioni 44, 48, 49. Scheletro, mesh, ogni livello di dettaglio, gruppi del corpo. 1 500 modelli caricati, 0 errori.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Materiali — `.vmt`</b></summary>

Tutti i 19 554 materiali inclusi si leggono; `patch`, blocchi DX, proxy.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Texture — `.vtf`</b></summary>

Versioni 7.0–7.5, DXT1/3/5 e tutti i formati non compressi, cubemap, mip. Il DXT va alla GPU senza decodifica.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Sessioni — `.dmx`</b></summary>

Binario 1–5 e KeyValues2. Ogni sessione e file di particelle dell'installazione si riscrive **byte per byte**.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Sessione a schermo</b></summary>

Inquadrature e tracce audio sulla timeline, l'albero degli elementi, la scena di ogni inquadratura dalla sua camera. Non ancora: mappe, particelle, audio.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animazione</b></summary>

Canali e log valutati al cursore; scrub e riproduzione. Ossa, camere e visibilità seguono la sessione.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Volti</b></summary>

Controller flex, regole compilate e animazione dei vertici — i personaggi parlano e fanno espressioni. Non ancora: mappe delle rughe.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Rig</b></summary>

Espressioni, vincoli point/orient/parent/aim, IK a due ossa. Non ancora: il grafo completo delle dipendenze degli operatori, la creazione di rig.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Modifica</b></summary>

Clic per selezionare, manipolatore sposta/ruota, inspector per ogni attributo, chiave al cursore, annulla/ripeti, salvataggio esatto al byte. Non ancora: il graph editor.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Selezione temporale con hold e falloff sul righello; una modifica si distribuisce come in SFM. Non ancora: preset, livelli.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Aggancio dei pannelli</b></summary>

Trascina i pannelli su una bussola di destinazioni con anteprima, come in UE5 e Visual Studio. Non ancora: layout salvati, temi.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Shading Source</b></summary>

Solo texture e una luce semplice. Non ancora: phong, rim, lightwarp, luci di scena, ombre.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Mappe — `.bsp`</b></summary>

Non iniziato.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Render in immagine e video</b></summary>

Non iniziato.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Plugin `.c2plg`</b></summary>

Non iniziato.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Temi e spazi di lavoro</b></summary>

Volutamente dopo: un solo aspetto finché l'editor non ha qualcosa che meriti un tema.

</details>

**Non pronto per il rilascio.** Le fondamenta — ogni formato di file usato da SFM, letto correttamente e verificato su tutta l'installazione — ci sono e sono testate; una sessione si apre, si riproduce, si modifica e si salva. Manca la *comodità* del lavoro: graph editor, shading Source, mappe, esportazione. Nessun numero di versione finché un animatore non può farci una giornata di lavoro.

## Cosa lo rende diverso

- **Portatile.** Nulla viene scritto fuori dalla cartella dell'applicazione: impostazioni in `App/User`, cache in `App/Cache`, temporanei in `App/Temporary`. Elimina la cartella e non resta nulla.
- **Non avvia mai SFM.** Nessun processo da pilotare, nessuna finestra da dirottare. L'installazione è letta come un pacchetto di contenuti.
- **Formati verificati, non presunti.** Ogni lettore è stato confrontato con l'installazione reale; dove un formato fa qualcosa di sorprendente, il codice lo dice.
- **Il salvataggio è esatto.** Una sessione letta e scritta senza modifiche è lo stesso file.
- **Il motore non ha dipendenze.** `Core/` e l'intera suite di test girano su Python puro; solo la finestra richiede Qt e OpenGL.

## Avvio

Richiede Windows, Python 3.13 e un'installazione di Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Al primo avvio SFM viene cercato tramite Steam; se non lo trova, il programma chiede. <kbd>Ctrl</kbd>+<kbd>O</kbd> apre una sessione, <kbd>Spazio</kbd> riproduce, <kbd>C</kbd> guarda dalla camera dell'inquadratura, <kbd>T</kbd>/<kbd>R</kbd> sposta/ruota, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> annulla, <kbd>Ctrl</kbd>+<kbd>S</kbd> salva. I pannelli si trascinano dal titolo. I test non richiedono nulla:

```bash
python Testing/run.py
```

## Struttura

```
C2UI_SDK/
├── c2ui.py            il launcher
├── Core/              motore: formati, file system virtuale, indice, ponti
├── App/               l'editor: libreria dei contenuti, renderer, finestra
├── Tools/             localizzazione, strumenti UI, plugin (più avanti)
├── Testing/           test, fixture esatte al byte, un solo runner
└── GIT&DOCK/README/   questo README in altre lingue
```

## Roadmap

1. **Graph editor** — curve e chiavi, visibili.
2. **Shading Source** — VertexLitGeneric come lo disegna SFM: phong, rim, lightwarp, luci di scena.
3. **Mappe** — `.bsp` per gli sfondi.
4. **Output** — esportazione immagine e video.
5. **Plugin** — il formato `.c2plg`; poi temi e spazi di lavoro.

## Licenza e crediti

Source Filmmaker, Team Fortress 2 e il motore Source appartengono a Valve. Questo progetto legge i loro formati di file, non include alcun loro file e funziona solo con la copia di SFM che già possiedi tramite Steam.

La licenza del codice proprio di C2UI non è ancora stata scelta — fino ad allora, tutti i diritti riservati. Issue e pull request sono comunque benvenuti.

<p align="center"><img src="../../.github/assets/models.png" alt="64 modelli renderizzati direttamente dall'installazione" width="60%"><br><sub>Sessantaquattro modelli scelti a caso dall'installazione, disegnati dal renderer di C2UI.</sub></p>
