<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <b>🇪🇸 Español</b> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/estado-pre--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/pruebas-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — es mi reconstrucción del editor de Source Filmmaker: el mismo contenido, el mismo formato de sesión, el mismo modelo de datos, dentro de una interfaz que toma su aspecto de la biblioteca de Steam y su disposición del editor de Unreal Engine 5.</p>

---

## La idea

Source Filmmaker es una gran herramienta con una interfaz de 2012. No quiero una piel sobre `sfm.exe`, ni quiero secuestrar sus ventanas una a una. Quiero un editor que **pregunte dónde está instalado SFM**, monte esa instalación como Garry's Mod monta Counter-Strike, y lo haga todo por sí mismo sobre esos archivos — modelos, materiales, texturas, sesiones, animación — sin lanzar nunca SFM.

El objetivo es **paridad de funciones con SFM, uno a uno** (incluidos huesos y rigs), y después lo que SFM nunca tuvo.

```
  ┌──────────────┐    "¿dónde está SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI propia   │ ◀─────  montado  ───────│    tf/  hl2/  tf_movies/ …   │
  │  render propio │      solo lectura      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Estado

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Preparación general para el lanzamiento: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="El editor con Meet the Heavy abierto" width="100%"><br><sub>El editor hoy, con Meet the Heavy de Valve abierto: planos y sonido en la línea de tiempo, el árbol de la sesión, el primer plano visto por su propia cámara, personajes posados y con las caras que dice la sesión.</sub></p>

Despliega un área para ver exactamente qué está hecho y qué no. Los porcentajes son mi estimación honesta frente a lo que puede hacer SFM.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Encontrar y montar SFM</b></summary>

Registro de Steam → `libraryfolders.vdf` → las rutas de búsqueda de `gameinfo.txt`, en el orden del motor. Seis montajes en una instalación estándar. No se escribe nada fuera de la carpeta de la aplicación.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Índice de contenido</b></summary>

70 199 archivos en 1,1 s en frío / 0,02 s en caliente; las sobrescrituras entre montajes se resuelven exactamente como el motor.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modelos — <code></code> <code></code> <code></code></b></summary>

Versiones 44, 48, 49. Esqueleto, mallas, todos los niveles de detalle, grupos de cuerpo. 1 500 modelos cargados, 0 fallos.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Materiales — <code></code></b></summary>

Los 19 554 materiales incluidos se leen; `patch`, bloques DX, proxies.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Texturas — <code></code></b></summary>

Versiones 7.0–7.5, DXT1/3/5 y todos los formatos sin comprimir, cubemaps, mips. DXT va a la GPU sin decodificar.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Sesiones — <code></code></b></summary>

Binario 1–5 y KeyValues2. Cada sesión y archivo de partículas de la instalación se reescribe **byte a byte**.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Sesión en pantalla</b></summary>

Planos y pistas de sonido en una línea de tiempo, el árbol de elementos, la escena de cada plano por su cámara. Aún no: mapas, partículas, sonido.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animación</b></summary>

Canales y logs evaluados en el cursor; scrub y reproducción. Huesos, cámaras y visibilidad siguen la sesión.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Caras</b></summary>

Controladores flex, las reglas compiladas y animación de vértices — los personajes hablan y gesticulan. Aún no: mapas de arrugas.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Rigs</b></summary>

Expresiones, restricciones point/orient/parent/aim, IK de dos huesos. Aún no: el grafo completo de dependencias de operadores, creación de rigs.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Edición</b></summary>

Clic para seleccionar, manipulador de mover/rotar, inspector de cualquier atributo, clave en el cursor, deshacer/rehacer, guardado exacto al byte. Aún no: el editor de gráficas.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Selección de tiempo con hold y falloff en la regla; una edición se extiende sobre ella como en SFM. Aún no: presets, capas.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Acoplamiento de paneles</b></summary>

Arrastra paneles a una brújula de destinos con vista previa, como en UE5 y Visual Studio. Aún no: diseños guardados, temas.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Sombreado Source</b></summary>

Solo textura y una luz simple. Aún no: phong, rim, lightwarp, luces de escena, sombras.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Mapas — <code></code></b></summary>

No iniciado.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Render a imagen y vídeo</b></summary>

No iniciado.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Plugins <code></code></b></summary>

No iniciado.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Temas y espacios de trabajo</b></summary>

Deliberadamente después: un solo aspecto hasta que el editor tenga algo que merezca tematizarse.

</details>

**No está listo para el lanzamiento.** La base — cada formato de archivo que usa SFM, leído correctamente y verificado contra toda la instalación — está y está probada; una sesión se puede abrir, reproducir, cambiar y guardar. Lo que falta es la *comodidad* del trabajo: el editor de gráficas, el sombreado Source, mapas, exportación. Sin número de versión hasta que un animador pueda hacer un día de trabajo en él.

## Qué lo hace diferente

- **Portátil.** No se escribe nada fuera de la carpeta de la aplicación: ajustes en `App/User`, cachés en `App/Cache`, temporales en `App/Temporary`. Borra la carpeta y desaparece.
- **Nunca ejecuta SFM.** No hay proceso que controlar ni ventanas que secuestrar. La instalación se lee como un paquete de contenido.
- **Formatos verificados, no supuestos.** Cada lector se comprobó contra la instalación real; donde un formato hace algo sorprendente, el código lo dice.
- **El guardado es exacto.** Una sesión leída y escrita sin cambios es el mismo archivo.
- **El motor no tiene dependencias.** `Core/` y toda la suite de pruebas corren en Python puro; solo la ventana necesita Qt y OpenGL.

## Ejecutar

Requiere Windows, Python 3.13 y una instalación de Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Al primer arranque busca SFM a través de Steam; si no lo encuentra, pregunta. <kbd>Ctrl</kbd>+<kbd>O</kbd> abre una sesión, <kbd>Espacio</kbd> reproduce, <kbd>C</kbd> mira por la cámara del plano, <kbd>T</kbd>/<kbd>R</kbd> mover/rotar, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> deshace, <kbd>Ctrl</kbd>+<kbd>S</kbd> guarda. Los paneles se arrastran por su título. Las pruebas no necesitan nada:

```bash
python Testing/run.py
```

## Estructura

```
C2UI_SDK/
├── c2ui.py            el lanzador
├── Core/              motor: formatos, sistema de archivos virtual, índice, puentes
├── App/               el editor: biblioteca de contenido, renderizador, ventana
├── Tools/             localización, herramientas de UI, plugins (más adelante)
├── Testing/           pruebas, fixtures exactos al byte, un runner
└── GIT&DOCK/README/   este README en otros idiomas
```

## Hoja de ruta

1. **Editor de gráficas** — curvas y claves, a la vista.
2. **Sombreado Source** — VertexLitGeneric como lo dibuja SFM: phong, rim, lightwarp, luces de escena.
3. **Mapas** — `.bsp` para fondos.
4. **Salida** — exportación a imagen y vídeo.
5. **Plugins** — el formato `.c2plg`; después temas y espacios de trabajo.

## Licencia y créditos

Source Filmmaker, Team Fortress 2 y el motor Source son de Valve. Este proyecto lee sus formatos de archivo, no incluye ninguno de sus archivos y solo funciona con la copia de SFM que ya tienes en Steam.

La licencia del código propio de C2UI aún no está elegida — hasta entonces, todos los derechos reservados. Los issues y pull requests son bienvenidos igualmente.

<p align="center"><img src="../../.github/assets/models.png" alt="64 modelos renderizados directamente desde la instalación" width="60%"><br><sub>Sesenta y cuatro modelos elegidos al azar de la instalación, dibujados por el renderizador propio de C2UI.</sub></p>
