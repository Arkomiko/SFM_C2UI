# Avancement de C2UI en détail

<details align="center"><summary>&nbsp;🌐 <b>🇫🇷 Français</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../RU-ru/sidebar.md">🇷🇺<br>Русский</a></td><td align="center"><a href="../EN-en/sidebar.md">🇬🇧<br>English</a></td><td align="center"><a href="../PL-pl/sidebar.md">🇵🇱<br>Polski</a></td><td align="center"><a href="../UK-ua/sidebar.md">🇺🇦<br>Українська</a></td><td align="center"><a href="../DE-de/sidebar.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="../RO-md/sidebar.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="../SL-si/sidebar.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="../BE-by/sidebar.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="../KK-kz/sidebar.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="../JA-jp/sidebar.md">🇯🇵<br>日本語</a></td><td align="center"><a href="../ZH-cn/sidebar.md">🇨🇳<br>中文</a></td><td align="center"><a href="../SV-se/sidebar.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="../ES-es/sidebar.md">🇪🇸<br>Español</a></td><td align="center"><a href="../HI-in/sidebar.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="../PT-pt/sidebar.md">🇵🇹<br>Português</a></td><td align="center"><a href="../BN-bd/sidebar.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><b>🇫🇷<br>Français</b></td><td align="center"><a href="../TE-in/sidebar.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="../MR-in/sidebar.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="../TA-in/sidebar.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="../TR-tr/sidebar.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="../UR-pk/sidebar.md">🇵🇰<br>اردو</a></td><td align="center"><a href="../VI-vn/sidebar.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="../GU-in/sidebar.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="../IT-it/sidebar.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="../KO-kr/sidebar.md">🇰🇷<br>한국어</a></td><td align="center"><a href="../AR-sa/sidebar.md">🇸🇦<br>العربية</a></td><td align="center"><a href="../JV-id/sidebar.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="../ML-in/sidebar.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="../NE-np/sidebar.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="../UZ-uz/sidebar.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="../OR-in/sidebar.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="sidebar.svg" alt="Avancement" width="320"></p>

<p align="center"><img alt="49%" src="https://img.shields.io/badge/49%25-e0a800?style=flat-square"> <b>Avancement global vers la sortie : 49%</b></p>

Chaque domaine se déplie : ce qui fonctionne déjà et ce qui n'existe pas encore. Les pourcentages sont une estimation par rapport à ce que sait faire SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Trouver et monter SFM

Registre Steam → `libraryfolders.vdf` → les chemins de recherche de `gameinfo.txt`, dans l'ordre du moteur. Six montages sur une installation standard. Rien n'est écrit hors du dossier de l'application.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Index du contenu

70 199 fichiers en 1,1 s à froid / 0,02 s à chaud ; les surcharges entre montages sont résolues exactement comme le moteur.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modèles — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Versions 44, 48, 49. Squelette, maillages, tous les niveaux de détail, groupes de corps. 1 500 modèles chargés, 0 échec.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Matériaux — <code>.vmt</code>

Les 19 554 matériaux fournis se lisent ; `patch`, blocs DX, proxies.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Textures — <code>.vtf</code>

Versions 7.0–7.5, DXT1/3/5 et tous les formats non compressés, cubemaps, mips. Le DXT part au GPU sans décodage.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sessions — <code>.dmx</code>

Binaire 1–5 et KeyValues2. Chaque session et fichier de particules de l'installation se réécrit **octet pour octet**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Session à l'écran

Plans et pistes son sur une timeline, l'arbre des éléments, la scène de chaque plan par sa caméra. Pas encore : cartes, particules, son.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animation

Canaux et logs évalués au curseur ; scrub et lecture. Os, caméras et visibilité suivent la session.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Visages

Contrôleurs flex, règles compilées et animation de sommets — les personnages parlent et expriment. Pas encore : cartes de rides.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rigs

Expressions, contraintes point/orient/parent/aim, IK à deux os. Pas encore : le graphe complet de dépendances des opérateurs, la création de rigs.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Édition

Clic pour sélectionner, manipulateur de déplacement/rotation, inspecteur de tout attribut, clé au curseur, annuler/rétablir, sauvegarde exacte à l'octet.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Sélection temporelle avec hold et falloff sur la règle ; une édition se répand dessus comme dans SFM. Pas encore : presets, calques.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Éditeur de courbes

Courbes de chaque log pilotant l'élément sélectionné : X/Y/Z, pitch/yaw/roll, scalaires. Les clés se déplacent en temps et en valeur avec aperçu en direct, double-clic insère, Suppr efface ; l'axe du temps est celui de la timeline. Pas encore : tangentes et types de courbe, mise à l'échelle d'un groupe de clés.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Ancrage des panneaux

Glissez les panneaux sur une boussole de cibles avec aperçu, comme dans UE5 et Visual Studio. Pas encore : dispositions enregistrées, thèmes.

### <img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> Ombrage Source

Lumières de la session (DmeProjectedLight) : frustum, atténuation Source, fondu jusqu'à maxDistance ; half-lambert, $lightwarptexture, phong ($phongexponent/boost/fresnelranges), $rimlight, $selfillum. Le monde de la carte par ses lightmaps. Pas encore : ombres, textures gobo, $bumpmap, $envmap, cubes d'ambiance, skybox.

### <img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> Cartes — <code>.bsp</code>

Versions 19–21 : géométrie du monde, terrain displacement, entités brush, props statiques, matériaux du pak de la carte. Élimination hors champ. Pas encore : lightmaps, skybox, eau, prop_dynamic.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Rendu en image et vidéo

Pas commencé.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugins <code>.c2plg</code>

Pas commencé.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Thèmes et espaces de travail

Volontairement plus tard : une seule apparence tant que l'éditeur n'a rien qui mérite un thème.

**Pas prêt pour une sortie.** Les fondations — chaque format de fichier utilisé par SFM, lu correctement et vérifié sur toute l'installation — sont là et testées ; une session s'ouvre, se lit, se modifie et se sauvegarde. Ce qui manque, c'est le *confort* de travail : l'éditeur de courbes, l'ombrage Source, les cartes, l'export. Pas de numéro de version tant qu'un animateur ne peut pas y faire une journée de travail.

<p align="center"><a href="../../README/FR-fr.md"><img alt="← Retour au README" src="https://img.shields.io/badge/%E2%86%90_Retour_au_README-1b2838?style=for-the-badge"></a></p>
