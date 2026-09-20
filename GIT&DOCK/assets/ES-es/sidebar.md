# Estado de C2UI en detalle

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <b>🇪🇸 Español</b> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Estado" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Preparación general para el lanzamiento: 41%</b></p>

Cada área se despliega: qué funciona ya y qué no existe todavía. Los porcentajes son una estimación frente a lo que puede hacer SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Encontrar y montar SFM

Registro de Steam → `libraryfolders.vdf` → las rutas de búsqueda de `gameinfo.txt`, en el orden del motor. Seis montajes en una instalación estándar. No se escribe nada fuera de la carpeta de la aplicación.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Índice de contenido

70 199 archivos en 1,1 s en frío / 0,02 s en caliente; las sobrescrituras entre montajes se resuelven exactamente como el motor.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modelos — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Versiones 44, 48, 49. Esqueleto, mallas, todos los niveles de detalle, grupos de cuerpo. 1 500 modelos cargados, 0 fallos.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Materiales — <code>.vmt</code>

Los 19 554 materiales incluidos se leen; `patch`, bloques DX, proxies.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Texturas — <code>.vtf</code>

Versiones 7.0–7.5, DXT1/3/5 y todos los formatos sin comprimir, cubemaps, mips. DXT va a la GPU sin decodificar.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sesiones — <code>.dmx</code>

Binario 1–5 y KeyValues2. Cada sesión y archivo de partículas de la instalación se reescribe **byte a byte**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Sesión en pantalla

Planos y pistas de sonido en una línea de tiempo, el árbol de elementos, la escena de cada plano por su cámara. Aún no: mapas, partículas, sonido.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animación

Canales y logs evaluados en el cursor; scrub y reproducción. Huesos, cámaras y visibilidad siguen la sesión.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Caras

Controladores flex, las reglas compiladas y animación de vértices — los personajes hablan y gesticulan. Aún no: mapas de arrugas.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rigs

Expresiones, restricciones point/orient/parent/aim, IK de dos huesos. Aún no: el grafo completo de dependencias de operadores, creación de rigs.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Edición

Clic para seleccionar, manipulador de mover/rotar, inspector de cualquier atributo, clave en el cursor, deshacer/rehacer, guardado exacto al byte.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Selección de tiempo con hold y falloff en la regla; una edición se extiende sobre ella como en SFM. Aún no: presets, capas.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Editor de gráficas

Curvas de cada log que mueve el elemento seleccionado: X/Y/Z, pitch/yaw/roll, escalares. Las claves se arrastran en tiempo y valor con vista previa en vivo, doble clic inserta, Supr borra; el eje de tiempo es el de la línea de tiempo. Aún no: tangentes y tipos de curva, escalar un grupo de claves.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Acoplamiento de paneles

Arrastra paneles a una brújula de destinos con vista previa, como en UE5 y Visual Studio. Aún no: diseños guardados, temas.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Sombreado Source

Solo textura y una luz simple. Aún no: phong, rim, lightwarp, luces de escena, sombras.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Mapas — <code>.bsp</code>

No iniciado.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Render a imagen y vídeo

No iniciado.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugins <code>.c2plg</code>

No iniciado.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Temas y espacios de trabajo

Deliberadamente después: un solo aspecto hasta que el editor tenga algo que merezca tematizarse.

**No está listo para el lanzamiento.** La base — cada formato de archivo que usa SFM, leído correctamente y verificado contra toda la instalación — está y está probada; una sesión se puede abrir, reproducir, cambiar y guardar. Lo que falta es la *comodidad* del trabajo: el editor de gráficas, el sombreado Source, mapas, exportación. Sin número de versión hasta que un animador pueda hacer un día de trabajo en él.

<p align="center"><a href="../../README/ES-es.md"><img alt="← Volver al README" src="https://img.shields.io/badge/%E2%86%90_Volver_al_README-1b2838?style=for-the-badge"></a></p>
