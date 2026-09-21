<details align="center"><summary>&nbsp;🌐 <b>🇫🇷 Français</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../../README.md">🇷🇺<br>Русский</a></td><td align="center"><a href="../README/EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="../README/PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="../README/UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="../README/DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="../README/RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="../README/SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="../README/BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="../README/KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="../README/JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="../README/ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="../README/SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="../README/ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="../README/HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="../README/PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="../README/BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><b>🇫🇷<br>Français</b></td><td align="center"><a href="../README/TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="../README/MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="../README/TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="../README/TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="../README/UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="../README/VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="../README/GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="../README/IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="../README/KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="../README/AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="../README/JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="../README/ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="../README/NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="../README/UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="../README/OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/banner/FR-fr.png" alt="C2UI" width="100%"></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%C3%A9tat-pr%C3%A9--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/tests-363-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
  <a href="../LICENSE/FR-fr.md"><img alt="licence" src="https://img.shields.io/badge/licence-C2UI-2a475e?style=flat-square"></a>
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — l'éditeur de Source Filmmaker dans une coque moderne : le même contenu, le même format de session, le même modèle de données, avec une interface dans l'esprit de la bibliothèque Steam et de l'éditeur d'Unreal Engine 5.</p>

---

## Avancement

<p align="center"><img src="../assets/readiness/FR-fr.svg" alt="Avancement" width="100%"></p>

<p align="center"><a href="../READINESS/FR-fr.md"><img alt="Avancement en détail" src="https://img.shields.io/badge/Avancement_en_d%C3%A9tail-66c0f4?style=for-the-badge"></a></p>

## L'idée

Source Filmmaker est un outil solide dont l'interface est restée en 2012. C2UI ne le remplace pas et ne le refait pas : le but est simplement de rendre SFM un peu plus moderne et plus confortable.

L'éditeur trouve le SFM installé, le rattache comme bibliothèque de contenu — modèles, matériaux, textures, sessions — et travaille avec les mêmes fichiers au même format. Tout ce qui a été fait dans SFM s'ouvre dans C2UI, et inversement.

Le premier objectif est la compatibilité complète avec SFM, os et rigs compris. Ensuite, ce qui manquait à SFM.

```
  ┌───────────────┐                          ┌──────────────────────────────┐
  │   C2UI        │ ──── "où est SFM ?" ────▶│  SourceFilmmaker/game/       │
  │               │                          │    usermod/gameinfo.txt      │
  │  UI propre    │ ◀──────── monté ─────────│    tf/  hl2/  tf_movies/ …   │
  │  rendu propre │      lecture seule       │    models/ materials/ dmx    │
  └───────────────┘                          └──────────────────────────────┘
```

- **Portable.** Rien n'est écrit hors du dossier de l'application : réglages dans `App/User`, caches dans `App/Cache`, temporaires dans `App/Temporary`. Supprimez le dossier et il ne reste rien.
- **Ne lance jamais SFM.** Aucun processus à piloter, aucune fenêtre à détourner. L'installation est lue comme un pack de contenu.
- **Formats vérifiés, pas supposés.** Chaque lecteur a été confronté à la vraie installation ; là où un format fait quelque chose de surprenant, le code le dit.
- **La sauvegarde est exacte.** Une session lue puis écrite sans modification est le même fichier.
- **Le moteur n'a aucune dépendance.** `Core/` et toute la suite de tests tournent sur un Python nu ; seule la fenêtre a besoin de Qt et OpenGL.

<p align="center"><img src="../assets/editor.png" alt="L'éditeur avec Meet the Heavy ouvert" width="100%"><br><sub>L'éditeur aujourd'hui, avec Meet the Heavy de Valve ouvert : plans et son sur la timeline, l'arbre de session, le premier plan vu par sa propre caméra, personnages posés et avec les visages que dicte la session.</sub></p>

## Structure

```
C2UI_SDK/
├── README.md
├── Core/               moteur : formats, système de fichiers virtuel, index, ponts
│   ├── API/            le contrat pour l'éditeur, les outils et les plugins
│   ├── Code/           moteur : animation, opérateurs, visages, édition
│   │   └── formats/    lecteurs Valve : mdl vvd vtx vmt vtf dmx bsp
│   └── dev-kit/        emplacements SDK (vides) et ponts vers les installations
├── App/                l'éditeur : bibliothèque de contenu, moteur de rendu, fenêtre
│   ├── Code/           bibliothèque de contenu, fenêtre, réglages
│   │   ├── render/     scène, moteur de rendu OpenGL, shaders, caméra
│   │   └── ui/         timeline, arbre de session, inspecteur, graph editor, ancrage
│   ├── Data/           ressources du programme, lecture seule
│   ├── User/           données de l'utilisateur — jamais supprimées
│   └── Cache/          index de contenu, shaders, vignettes
├── Tools/              localisation, outils UI, plugins (plus tard)
│   ├── Launcher/       le lanceur
│   ├── Market Load/    client du marketplace de plugins (plus tard)
│   ├── Localization/   création de traductions
│   ├── NewPlugins/     création de plugins
│   └── UI/             thèmes et espaces de travail
├── Testing/            tests, fixtures exactes à l'octet, un seul runner
│   ├── core/           le moteur
│   ├── app/            l'éditeur
│   └── fixtures/       fausse installation, modèles, textures
└── GIT&DOCK/           README, avancement et licence en 32 langues
```

### Comment ça marche

Le chemin de « où est Source Filmmaker ? » jusqu'à une image à l'écran traverse cinq couches ; chacune ne connaît que celle du dessous.

1. **Le pont** (`Core/dev-kit/bridge_sfm`) trouve l'installation via Steam, lit `gameinfo.txt` et renvoie les chemins de contenu dans l'ordre du moteur. `sfm.exe` n'est jamais lancé.
2. **Le système de fichiers virtuel et l'index** (`Core/Code/vfs.py`, `content_index.py`) superposent ces chemins comme le fait Source : le premier fichier trouvé l'emporte. L'index est un seul fichier SQLite dans `App/Cache`, le parcours de 70 000 fichiers n'est donc payé qu'une fois.
3. **Les formats** (`Core/Code/formats`) lisent les fichiers de Valve sans bibliothèque tierce : `.mdl` `.vvd` `.vtx` forment un modèle, `.vmt` `.vtf` un matériau et sa texture, `.dmx` une session, `.bsp` une carte. Chaque lecteur est vérifié sur toute l'installation ; une session est réécrite octet pour octet.
4. **La session** est un graphe d'éléments DMX. `animation.py` évalue les canaux à un instant donné, `operators.py` exécute les expressions et les contraintes de rig, `flex.py` anime les visages, `pose.py` construit les matrices d'os. Chaque modification passe par `editing.py` sous forme de commande annulable.
5. **L'éditeur** (`App/Code`) en fait une scène (`render/scene.py`) et la dessine avec son propre moteur de rendu OpenGL 3.3 (`renderer.py`, `shaders.py`) : lumières de session, lightmaps et éclairage de la carte tels que SFM les affiche. Les panneaux (`ui/`) sont la timeline, l'arbre de session, l'inspecteur, le graph editor et l'ancrage façon UE5.

Tout ce que le programme écrit reste dans son dossier : `App/User` pour les réglages, `App/Cache` pour l'index et les caches, `App/Temporary` pour le journal. `Core/` n'écrit rien et ne dépend pas de Qt : le moteur et les tests tournent sur Python nu ; Qt et OpenGL ne servent qu'à la fenêtre. Les utilitaires de `Tools/` sont bâtis strictement sur `Core/API` — c'est ainsi que l'on vérifie que l'API suffit aussi aux plugins tiers.

<p align="center"><img src="../assets/models.png" alt="64 modèles rendus directement depuis l'installation" width="60%"><br><sub>Soixante-quatre modèles tirés au hasard de l'installation, dessinés par le moteur de rendu de C2UI.</sub></p>

### Lancer

Nécessite Windows, Python 3.13 et une installation de Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Au premier lancement, SFM est cherché via Steam ; s'il n'est pas trouvé, le programme demande. <kbd>Ctrl</kbd>+<kbd>O</kbd> ouvre une session, <kbd>Espace</kbd> lit, <kbd>C</kbd> regarde par la caméra du plan, <kbd>T</kbd>/<kbd>R</kbd> déplacer/tourner, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> annule, <kbd>Ctrl</kbd>+<kbd>S</kbd> sauvegarde. Les panneaux se déplacent par leur titre. Les tests n'ont besoin de rien :

```bash
python Testing/run.py
```

### Prévu

**Ensuite**
- L'aspect de la carte : skybox, eau, prop_dynamic, textures gobo des lumières, `$bumpmap` et `$envmap`, ombres des lumières de session.
- Export : séquences d'images et vidéo.
- Plugins `.c2plg` et le client du marketplace dans `Tools/Market Load` ; puis thèmes et espaces de travail.
- Son sur la timeline, particules, wrinkle maps, presets et calques du motion editor, tangentes dans le graph editor.

**Plus tard**
- Performance sur les cartes complètes : props statiques instanciés, poses en cache.
- Refonte du moteur : nouveaux paramètres de compilation des cartes pour un meilleur éclairage et de meilleures ombres, limite de carte à 120 000 unités.
- Un lanceur empaqueté avec son propre Python et sa mise à jour automatique ; localisation de l'éditeur.

## Licence et crédits

Le code propre de C2UI est sous **licence C2UI** : libre pour un usage personnel et non commercial ; usage commercial uniquement avec l'accord écrit de l'auteur ; les versions modifiées doivent citer le projet d'origine et son auteur, Arkomiko. Les plugins et addons sont sous licence **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 et le moteur Source appartiennent à Valve ; le projet lit leurs formats, n'inclut aucun de leurs fichiers et ne fonctionne qu'avec votre propre copie de SFM via Steam.

<p align="center"><a href="../LICENSE/FR-fr.md"><img alt="Texte de la licence" src="https://img.shields.io/badge/Texte_de_la_licence-66c0f4?style=for-the-badge"></a></p>
