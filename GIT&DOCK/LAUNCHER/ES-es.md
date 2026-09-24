# El lanzador de C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇪🇸 Español</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><b>🇪🇸<br>Español</b></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` es desde donde se arranca el proyecto: una ventana oscura y pequeña con un título, una línea de descripción y tres botones. Se compila en un único ejecutable que no necesita Python instalado y encuentra el proyecto por sí mismo: sube desde donde esté hasta ver juntos `App`, `Core` y `Launcher`.

<p align="center"><img src="../assets/launcher.png" alt="El lanzador de C2UI" width="562"><br><sub>La ventana del lanzador: el título «Dev-mode», la línea de descripción y tres botones.</sub></p>

> [!NOTE]
> **La interfaz del lanzador está de momento solo en ruso: es una solución provisional.** El título, la descripción y los textos de los botones están escritos en el código; las traducciones llegarán junto con la localización del editor (`Tools/Localization`), cuando el lanzador se reescriba para un App terminado. El resto de la documentación del proyecto ya está en 32 idiomas.

## Los tres botones

| | |
|---|---|
| <code>Запустить Core</code> | Arranca el editor: la ventana de C2UI con su visor, su línea de tiempo y sus paneles. |
| <code>Запустить App</code> | Desactivado: todavía no hay un App aparte. |
| <code>Выйти</code> | Cierra el lanzador. |

## Ejecutar desde el código

Hacen falta Windows, Python 3.13 y una instalación de Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Compilar el archivo único `Launcher/Launcher-C2UI.exe` (no se guarda en git: se reconstruye desde el código):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## El motor sin el editor

`Launcher/core.py` arranca `Core` por su cuenta: monta una instalación, la indexa y ofrece una pequeña consola sobre el motor — modelos, materiales, texturas, mapas, sesiones y su evaluación. También provisional: cuando App pueda funcionar sin ventana, el editor será el único punto de entrada.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Qué cambiará

- La ventana se reescribirá con App, con su diseño y sus traducciones.
- El botón «Запустить App» empezará a funcionar.
- `core.py` desaparecerá cuando el editor pueda arrancarse sin ventana.
- El `.exe` compilado acompañará a las publicaciones en GitHub.

<p align="center"><a href="../README/ES-es.md"><img alt="← Volver al README" src="https://img.shields.io/badge/%E2%86%90_Volver_al_README-1b2838?style=for-the-badge"></a></p>
