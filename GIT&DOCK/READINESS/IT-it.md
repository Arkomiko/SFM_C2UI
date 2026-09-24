# Avanzamento di C2UI in dettaglio

<details align="center"><summary>&nbsp;🌐 <b>🇮🇹 Italiano</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><b>🇮🇹<br>Italiano</b></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/IT-it.svg" alt="Stato di avanzamento" width="100%"></p>

<p align="center"><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Avanzamento complessivo verso il rilascio: 60%</b></p>

Ogni area si espande: cosa funziona già e cosa non c'è ancora. Le percentuali sono una stima rispetto a ciò che sa fare SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Trovare e montare SFM

Registro di Steam → `libraryfolders.vdf` → i percorsi di ricerca di `gameinfo.txt`, nell'ordine del motore. Sei montaggi su un'installazione standard. Nulla viene scritto fuori dalla cartella dell'applicazione.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Indice dei contenuti

70 199 file in 1,1 s a freddo / 0,02 s dalla cache; le sovrascritture tra montaggi risolte esattamente come fa il motore.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modelli — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Versioni 44, 48, 49. Scheletro, mesh, ogni livello di dettaglio, gruppi del corpo. 1 500 modelli caricati, 0 errori.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Materiali — <code>.vmt</code>

Tutti i 19 554 materiali inclusi si leggono; `patch`, blocchi DX, proxy.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Texture — <code>.vtf</code>

Versioni 7.0–7.5, DXT1/3/5 e tutti i formati non compressi, cubemap, mip. Il DXT va alla GPU senza decodifica.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sessioni — <code>.dmx</code>

Binario 1–5 e KeyValues2. Ogni sessione e file di particelle dell'installazione si riscrive **byte per byte**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Sessione sullo schermo

Inquadrature e tracce audio sulla timeline, l'albero degli elementi, la scena di ogni inquadratura attraverso la sua camera, la mappa dell'inquadratura. Non ancora: particelle, audio.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animazione

Canali e log valutati al cursore; scrub e riproduzione. Ossa, camere e visibilità seguono la sessione.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Volti

Controller flex, regole compilate e animazione dei vertici — i personaggi parlano e fanno espressioni. Non ancora: mappe delle rughe.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rig

Espressioni, vincoli point/orient/parent/aim, IK a due ossa. Non ancora: il grafo completo delle dipendenze degli operatori, la creazione di rig.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Modifica

Clic per selezionare, manipolatore sposta/ruota, inspector per ogni attributo, chiave al cursore, annulla/ripeti, salvataggio esatto al byte.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Selezione temporale con hold e falloff sul righello; una modifica si distribuisce come in SFM. Non ancora: preset, livelli.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Graph editor

Curve di ogni log che muove l'elemento selezionato: X/Y/Z, pitch/yaw/roll, scalari. Le chiavi si trascinano in tempo e valore con anteprima dal vivo, doppio clic inserisce, Canc elimina; l'asse del tempo è quello della timeline. Non ancora: tangenti e tipi di curva, scalatura di un gruppo di chiavi.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Aggancio dei pannelli

Trascina i pannelli su una bussola di destinazioni con anteprima, come in UE5 e Visual Studio. Non ancora: layout salvati, temi.

### <img alt="75%" src="https://img.shields.io/badge/75%25-3b9c5b?style=flat-square"> Shading Source

Luci della sessione (DmeProjectedLight): frustum, attenuazione Source, dissolvenza fino a maxDistance; half-lambert, $lightwarptexture, phong, $rimlight, $selfillum. Il mondo della mappa tramite le lightmap; i modelli illuminati dai cubi ambientali e dalle luci della mappa. Non ancora: ombre, texture gobo, $bumpmap, $envmap.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Mappe — <code>.bsp</code>

Versioni 19–21: geometria del mondo, terreno displacement, brush entity, prop statici, materiali pak della mappa, lightmap, la skybox intorno alla camera. Frustum culling. Non ancora: acqua, prop_dynamic.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Rendering in immagine e video

Sequenze PNG/TGA e filmati AVI/MP4 dalla sessione: tutta la sessione, l'inquadratura corrente o un intervallo; preset; File → Export, Ctrl+E. Non ancora: l'audio nel filmato.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugin <code>.c2plg</code>

Non iniziato.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Temi e spazi di lavoro

Volutamente dopo: un solo aspetto finché l'editor non ha qualcosa che meriti un tema.

**Non pronto per il rilascio.** Le fondamenta — ogni formato di file usato da SFM, letto correttamente e verificato su tutta l'installazione — ci sono e sono testate; una sessione si apre, si riproduce, si modifica e si salva. Manca la *comodità* del lavoro: graph editor, shading Source, mappe, esportazione. Nessun numero di versione finché un animatore non può farci una giornata di lavoro.

<p align="center"><a href="../README/IT-it.md"><img alt="← Torna al README" src="https://img.shields.io/badge/%E2%86%90_Torna_al_README-1b2838?style=for-the-badge"></a></p>
