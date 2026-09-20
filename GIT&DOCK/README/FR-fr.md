<p align="center"><img src="../assets/FR-fr/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <b>🇫🇷 Français</b> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%C3%A9tat-pr%C3%A9--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/tests-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — l'éditeur de Source Filmmaker dans une coque moderne : le même contenu, le même format de session, le même modèle de données, avec une interface dans l'esprit de la bibliothèque Steam et de l'éditeur d'Unreal Engine 5.</p>

---

## L'idée

Source Filmmaker est un outil solide dont l'interface est restée en 2012. C2UI ne le remplace pas et ne le refait pas : le but est simplement de rendre SFM un peu plus moderne et plus confortable.

L'éditeur trouve le SFM installé, le rattache comme bibliothèque de contenu — modèles, matériaux, textures, sessions — et travaille avec les mêmes fichiers au même format. Tout ce qui a été fait dans SFM s'ouvre dans C2UI, et inversement.

Le premier objectif est la compatibilité complète avec SFM, os et rigs compris. Ensuite, ce qui manquait à SFM.

```
  ┌──────────────┐    "où est SFM ?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI propre   │ ◀─────   monté   ───────│    tf/  hl2/  tf_movies/ …   │
  │  rendu propre │      lecture seule      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Avancement

<img align="right" src="../assets/FR-fr/sidebar.svg" alt="Avancement" width="300">

<img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Avancement global vers la sortie : 41%</b>

Chaque domaine se déplie : ce qui fonctionne déjà et ce qui n'existe pas encore. Les pourcentages sont une estimation par rapport à ce que sait faire SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Trouver et monter SFM</b></summary>

Registre Steam → `libraryfolders.vdf` → les chemins de recherche de `gameinfo.txt`, dans l'ordre du moteur. Six montages sur une installation standard. Rien n'est écrit hors du dossier de l'application.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Index du contenu</b></summary>

70 199 fichiers en 1,1 s à froid / 0,02 s à chaud ; les surcharges entre montages sont résolues exactement comme le moteur.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modèles — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

Versions 44, 48, 49. Squelette, maillages, tous les niveaux de détail, groupes de corps. 1 500 modèles chargés, 0 échec.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Matériaux — <code>.vmt</code></b></summary>

Les 19 554 matériaux fournis se lisent ; `patch`, blocs DX, proxies.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Textures — <code>.vtf</code></b></summary>

Versions 7.0–7.5, DXT1/3/5 et tous les formats non compressés, cubemaps, mips. Le DXT part au GPU sans décodage.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Sessions — <code>.dmx</code></b></summary>

Binaire 1–5 et KeyValues2. Chaque session et fichier de particules de l'installation se réécrit **octet pour octet**.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Session à l'écran</b></summary>

Plans et pistes son sur une timeline, l'arbre des éléments, la scène de chaque plan par sa caméra. Pas encore : cartes, particules, son.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animation</b></summary>

Canaux et logs évalués au curseur ; scrub et lecture. Os, caméras et visibilité suivent la session.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Visages</b></summary>

Contrôleurs flex, règles compilées et animation de sommets — les personnages parlent et expriment. Pas encore : cartes de rides.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Rigs</b></summary>

Expressions, contraintes point/orient/parent/aim, IK à deux os. Pas encore : le graphe complet de dépendances des opérateurs, la création de rigs.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Édition</b></summary>

Clic pour sélectionner, manipulateur de déplacement/rotation, inspecteur de tout attribut, clé au curseur, annuler/rétablir, sauvegarde exacte à l'octet.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Sélection temporelle avec hold et falloff sur la règle ; une édition se répand dessus comme dans SFM. Pas encore : presets, calques.

</details>
<details><summary><img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> <b>Éditeur de courbes</b></summary>

Courbes de chaque log pilotant l'élément sélectionné : X/Y/Z, pitch/yaw/roll, scalaires. Les clés se déplacent en temps et en valeur avec aperçu en direct, double-clic insère, Suppr efface ; l'axe du temps est celui de la timeline. Pas encore : tangentes et types de courbe, mise à l'échelle d'un groupe de clés.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Ancrage des panneaux</b></summary>

Glissez les panneaux sur une boussole de cibles avec aperçu, comme dans UE5 et Visual Studio. Pas encore : dispositions enregistrées, thèmes.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Ombrage Source</b></summary>

Texture et lumière simple seulement. Pas encore : phong, rim, lightwarp, lumières de scène, ombres.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Cartes — <code>.bsp</code></b></summary>

Pas commencé.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Rendu en image et vidéo</b></summary>

Pas commencé.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Plugins <code>.c2plg</code></b></summary>

Pas commencé.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Thèmes et espaces de travail</b></summary>

Volontairement plus tard : une seule apparence tant que l'éditeur n'a rien qui mérite un thème.

</details>

**Pas prêt pour une sortie.** Les fondations — chaque format de fichier utilisé par SFM, lu correctement et vérifié sur toute l'installation — sont là et testées ; une session s'ouvre, se lit, se modifie et se sauvegarde. Ce qui manque, c'est le *confort* de travail : l'éditeur de courbes, l'ombrage Source, les cartes, l'export. Pas de numéro de version tant qu'un animateur ne peut pas y faire une journée de travail.

<br clear="all">

<p align="center"><img src="../assets/editor.png" alt="L'éditeur avec Meet the Heavy ouvert" width="100%"><br><sub>L'éditeur aujourd'hui, avec Meet the Heavy de Valve ouvert : plans et son sur la timeline, l'arbre de session, le premier plan vu par sa propre caméra, personnages posés et avec les visages que dicte la session.</sub></p>

## Ce qui le distingue

- **Portable.** Rien n'est écrit hors du dossier de l'application : réglages dans `App/User`, caches dans `App/Cache`, temporaires dans `App/Temporary`. Supprimez le dossier et il ne reste rien.
- **Ne lance jamais SFM.** Aucun processus à piloter, aucune fenêtre à détourner. L'installation est lue comme un pack de contenu.
- **Formats vérifiés, pas supposés.** Chaque lecteur a été confronté à la vraie installation ; là où un format fait quelque chose de surprenant, le code le dit.
- **La sauvegarde est exacte.** Une session lue puis écrite sans modification est le même fichier.
- **Le moteur n'a aucune dépendance.** `Core/` et toute la suite de tests tournent sur un Python nu ; seule la fenêtre a besoin de Qt et OpenGL.

## Lancer

Nécessite Windows, Python 3.13 et une installation de Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Au premier lancement, SFM est cherché via Steam ; s'il n'est pas trouvé, le programme demande. <kbd>Ctrl</kbd>+<kbd>O</kbd> ouvre une session, <kbd>Espace</kbd> lit, <kbd>C</kbd> regarde par la caméra du plan, <kbd>T</kbd>/<kbd>R</kbd> déplacer/tourner, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> annule, <kbd>Ctrl</kbd>+<kbd>S</kbd> sauvegarde. Les panneaux se déplacent par leur titre. Les tests n'ont besoin de rien :

```bash
python Testing/run.py
```

## Structure

```
C2UI_SDK/
├── c2ui.py            le lanceur
├── Core/              moteur : formats, système de fichiers virtuel, index, ponts
├── App/               l'éditeur : bibliothèque de contenu, moteur de rendu, fenêtre
├── Tools/             localisation, outils UI, plugins (plus tard)
├── Testing/           tests, fixtures exactes à l'octet, un seul runner
└── GIT&DOCK/README/   ce README dans d'autres langues
```

## Feuille de route

1. **Ombrage Source** — VertexLitGeneric tel que SFM le dessine : phong, rim, lightwarp, lumières de scène.
2. **Cartes** — `.bsp` pour les décors.
3. **Sortie** — export image et vidéo.
4. **Plugins** — le format `.c2plg` ; puis thèmes et espaces de travail.

## Licence et crédits

Source Filmmaker, Team Fortress 2 et le moteur Source appartiennent à Valve. Ce projet lit leurs formats de fichiers, n'inclut aucun de leurs fichiers et ne fonctionne qu'avec la copie de SFM que vous avez déjà via Steam.

La licence du code propre de C2UI n'est pas encore choisie — d'ici là, tous droits réservés. Issues et pull requests restent les bienvenus.

<p align="center"><img src="../assets/models.png" alt="64 modèles rendus directement depuis l'installation" width="60%"><br><sub>Soixante-quatre modèles tirés au hasard de l'installation, dessinés par le moteur de rendu de C2UI.</sub></p>
