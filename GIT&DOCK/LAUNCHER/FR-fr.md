# Le lanceur de C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇫🇷 Français</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><b>🇫🇷<br>Français</b></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` est ce par quoi le projet démarre : une petite fenêtre sombre avec un titre, une ligne de description et trois boutons. Elle se compile en un seul exécutable qui n'a besoin d'aucun Python installé, et trouve le projet toute seule — elle remonte depuis l'endroit où elle se trouve jusqu'à voir `App`, `Core` et `Launcher` réunis.

<p align="center"><img src="../assets/launcher.png" alt="Le lanceur de C2UI" width="562"><br><sub>La fenêtre du lanceur : le titre « Dev-mode », la ligne de description et trois boutons.</sub></p>

> [!NOTE]
> **L'interface du lanceur n'est pour l'instant qu'en russe — c'est une solution provisoire.** Le titre, la description et les libellés des boutons sont écrits en dur ; les traductions viendront avec la localisation de l'éditeur (`Tools/Localization`), quand le lanceur sera réécrit pour un App abouti. Le reste de la documentation du projet est déjà en 32 langues.

## Les trois boutons

| | |
|---|---|
| <code>Запустить Core</code> | Lance l'éditeur — la fenêtre C2UI avec sa vue, sa timeline et ses panneaux. |
| <code>Запустить App</code> | Grisé : il n'y a pas encore d'App séparé. |
| <code>Выйти</code> | Ferme le lanceur. |

## Lancer depuis les sources

Il faut Windows, Python 3.13 et une installation de Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Construire le fichier unique `Launcher/Launcher-C2UI.exe` (non conservé dans git — il est reconstruit depuis les sources) :

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Le moteur sans l'éditeur

`Launcher/core.py` démarre `Core` seul : il monte une installation, l'indexe et donne un petit shell au-dessus du moteur — modèles, matériaux, textures, cartes, sessions et leur évaluation. Provisoire également : dès qu'App pourra tourner sans fenêtre, l'éditeur deviendra le seul point d'entrée.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Ce qui changera

- La fenêtre sera réécrite avec App — mise en forme et traductions comprises.
- Le bouton « Запустить App » se mettra à fonctionner.
- `core.py` disparaîtra dès que l'éditeur pourra démarrer sans fenêtre.
- L'exécutable construit accompagnera les versions publiées sur GitHub.

<p align="center"><a href="../README/FR-fr.md"><img alt="← Retour au README" src="https://img.shields.io/badge/%E2%86%90_Retour_au_README-1b2838?style=for-the-badge"></a></p>
