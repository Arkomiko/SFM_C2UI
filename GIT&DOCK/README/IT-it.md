<p align="center"><img src="../assets/IT-it/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <b>🇮🇹 Italiano</b> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/stato-pre--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/test-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — l'editor di Source Filmmaker in un guscio moderno: lo stesso contenuto, lo stesso formato di sessione, lo stesso modello di dati, un'interfaccia nello spirito della libreria di Steam e dell'editor di Unreal Engine 5.</p>

---

## Stato di avanzamento

<p align="center"><img src="../assets/IT-it/sidebar.svg" alt="Stato di avanzamento" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Avanzamento complessivo verso il rilascio: 41%</b></p>

<p align="center"><a href="../assets/IT-it/sidebar.md"><img alt="Avanzamento in dettaglio" src="https://img.shields.io/badge/Avanzamento_in_dettaglio-66c0f4?style=for-the-badge"></a></p>

## L'idea

Source Filmmaker è uno strumento solido la cui interfaccia è rimasta al 2012. C2UI non lo sostituisce né lo rifà: l'obiettivo è semplicemente rendere SFM un po' più moderno e comodo.

L'editor trova l'SFM installato, lo collega come libreria di contenuti — modelli, materiali, texture, sessioni — e lavora con gli stessi file nello stesso formato. Tutto ciò che è stato fatto in SFM si apre in C2UI, e viceversa.

Il primo obiettivo è la piena compatibilità con SFM, ossa e rig compresi. Poi, ciò che a SFM mancava.

```
  ┌──────────────┐    "dov'è SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI propria  │ ◀─────  montato  ───────│    tf/  hl2/  tf_movies/ …   │
  │  render proprio │      sola lettura      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="L'editor con Meet the Heavy aperto" width="100%"><br><sub>L'editor oggi, con Meet the Heavy di Valve aperto: inquadrature e audio sulla timeline, l'albero della sessione, la prima inquadratura vista dalla sua camera, personaggi in posa e con le espressioni dettate dalla sessione.</sub></p>

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
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Al primo avvio SFM viene cercato tramite Steam; se non lo trova, il programma chiede. <kbd>Ctrl</kbd>+<kbd>O</kbd> apre una sessione, <kbd>Spazio</kbd> riproduce, <kbd>C</kbd> guarda dalla camera dell'inquadratura, <kbd>T</kbd>/<kbd>R</kbd> sposta/ruota, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> annulla, <kbd>Ctrl</kbd>+<kbd>S</kbd> salva. I pannelli si trascinano dal titolo. I test non richiedono nulla:

```bash
python Testing/run.py
```

## Struttura

```
C2UI_SDK/
├── README.md
├── Core/              motore: formati, file system virtuale, indice, ponti
├── App/               l'editor: libreria dei contenuti, renderer, finestra
├── Tools/             localizzazione, strumenti UI, plugin (più avanti)
│   └── Launcher/      il launcher
├── Testing/           test, fixture esatte al byte, un solo runner
└── GIT&DOCK/          questo README in altre lingue
```

## Roadmap

1. **Shading Source** — VertexLitGeneric come lo disegna SFM: phong, rim, lightwarp, luci di scena.
2. **Mappe** — `.bsp` per gli sfondi.
3. **Output** — esportazione immagine e video.
4. **Plugin** — il formato `.c2plg`; poi temi e spazi di lavoro.

## Licenza e crediti

Il codice proprio di C2UI è sotto la **licenza C2UI**: libero per uso personale e non commerciale; uso commerciale solo con il consenso scritto dell'autore; le versioni modificate devono citare il progetto originale e il suo autore, Arkomiko. Plugin e addon sono sotto la licenza **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 e il motore Source appartengono a Valve; il progetto legge i loro formati, non include alcun loro file e funziona solo con la tua copia di SFM da Steam.

<p align="center"><a href="../LICENSE/IT-it.md"><img alt="Testo della licenza" src="https://img.shields.io/badge/Testo_della_licenza-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 modelli renderizzati direttamente dall'installazione" width="60%"><br><sub>Sessantaquattro modelli scelti a caso dall'installazione, disegnati dal renderer di C2UI.</sub></p>
