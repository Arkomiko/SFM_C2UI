<details align="center"><summary>&nbsp;🌐 <b>🇵🇹 Português</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../../README.md">🇷🇺<br>Русский</a></td><td align="center"><a href="../README/EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="../README/PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="../README/UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="../README/DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="../README/RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="../README/SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="../README/BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="../README/KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="../README/JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="../README/ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="../README/SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="../README/ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="../README/HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><b>🇵🇹<br>Português</b></td><td align="center"><a href="../README/BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="../README/FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="../README/TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="../README/MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="../README/TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="../README/TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="../README/UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="../README/VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="../README/GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="../README/IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="../README/KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="../README/AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="../README/JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="../README/ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="../README/NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="../README/UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="../README/OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/banner/PT-pt.png" alt="C2UI" width="100%"></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/estado-pr%C3%A9--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/testes-363-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
  <a href="../LICENSE/PT-pt.md"><img alt="licence" src="https://img.shields.io/badge/licen%C3%A7a-C2UI-2a475e?style=flat-square"></a>
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — o editor do Source Filmmaker numa interface moderna: o mesmo conteúdo, o mesmo formato de sessão, o mesmo modelo de dados, com um aspeto no espírito da biblioteca do Steam e do editor do Unreal Engine 5.</p>

---

## Estado

<p align="center"><img src="../assets/readiness/PT-pt.svg" alt="Estado" width="100%"></p>

<p align="center"><a href="../READINESS/PT-pt.md"><img alt="Estado em detalhe" src="https://img.shields.io/badge/Estado_em_detalhe-66c0f4?style=for-the-badge"></a></p>

## A ideia

O Source Filmmaker é uma ferramenta forte cuja interface ficou em 2012. O C2UI não o substitui nem o refaz: o objetivo é simplesmente tornar o SFM um pouco mais moderno e confortável.

O editor encontra o SFM instalado, liga-o como biblioteca de conteúdo — modelos, materiais, texturas, sessões — e trabalha com os mesmos ficheiros no mesmo formato. Tudo o que foi feito no SFM abre no C2UI, e vice-versa.

O primeiro objetivo é a compatibilidade total com o SFM, ossos e rigs incluídos. Depois, o que faltava ao SFM.

```
  ┌─────────────────┐                              ┌──────────────────────────────┐
  │   C2UI          │ ──── "onde está o SFM?" ────▶│  SourceFilmmaker/game/       │
  │                 │                              │    usermod/gameinfo.txt      │
  │  UI própria     │ ◀───────── montado ──────────│    tf/  hl2/  tf_movies/ …   │
  │  render próprio │          só leitura          │    models/ materials/ dmx    │
  └─────────────────┘                              └──────────────────────────────┘
```

- **Portátil.** Nada é escrito fora da pasta da aplicação: definições em `App/User`, caches em `App/Cache`, temporários em `App/Temporary`. Apague a pasta e desaparece.
- **Nunca corre o SFM.** Não há processo a controlar nem janelas a sequestrar. A instalação é lida como um pacote de conteúdo.
- **Formatos verificados, não presumidos.** Cada leitor foi comparado com a instalação real; onde um formato faz algo surpreendente, o código diz-o.
- **A gravação é exata.** Uma sessão lida e escrita sem alterações é o mesmo ficheiro.
- **O motor não tem dependências.** `Core/` e toda a suíte de testes correm em Python puro; só a janela precisa de Qt e OpenGL.

<p align="center"><img src="../assets/editor.png" alt="O editor com Meet the Heavy aberto" width="100%"><br><sub>O editor hoje, com o Meet the Heavy da Valve aberto: planos e som na linha temporal, a árvore da sessão, o primeiro plano visto pela sua própria câmara, personagens em pose e com as caras que a sessão dita.</sub></p>

## Estrutura

```
C2UI_SDK/
├── README.md
├── Core/               motor: formatos, sistema de ficheiros virtual, índice, pontes
│   ├── API/            o contrato para o editor, as ferramentas e os plugins
│   ├── Code/           motor: animação, operadores, caras, edição
│   │   └── formats/    leitores Valve: mdl vvd vtx vmt vtf dmx bsp
│   └── dev-kit/        ranhuras SDK (vazias) e pontes para instalações
├── App/                o editor: biblioteca de conteúdo, renderizador, janela
│   ├── Code/           biblioteca de conteúdo, janela, definições
│   │   ├── render/     cena, renderizador OpenGL, shaders, câmara
│   │   └── ui/         linha de tempo, árvore da sessão, inspetor, graph editor, ancoragem
│   ├── Data/           recursos do programa, só de leitura
│   ├── User/           dados do utilizador — nunca apagados
│   └── Cache/          índice de conteúdo, shaders, miniaturas
├── Tools/              localização, ferramentas de UI, plugins (mais tarde)
│   ├── Launcher/       o lançador
│   ├── Market Load/    cliente do marketplace de plugins (mais tarde)
│   ├── Localization/   criar traduções
│   ├── NewPlugins/     criar plugins
│   └── UI/             temas e espaços de trabalho
├── Testing/            testes, fixtures exatas ao byte, um runner
│   ├── core/           o motor
│   ├── app/            o editor
│   └── fixtures/       instalação falsa, modelos, texturas
└── GIT&DOCK/           README, prontidão e licença em 32 línguas
```

### Como funciona

O caminho de «onde está o Source Filmmaker?» até um fotograma no ecrã passa por cinco camadas; cada uma conhece apenas a que está por baixo.

1. **A ponte** (`Core/dev-kit/bridge_sfm`) encontra a instalação através do Steam, lê o `gameinfo.txt` e devolve os caminhos de conteúdo pela ordem do motor. O `sfm.exe` nunca é lançado.
2. **O sistema de ficheiros virtual e o índice** (`Core/Code/vfs.py`, `content_index.py`) sobrepõem esses caminhos como o Source faz: o primeiro ficheiro encontrado ganha. O índice é um único ficheiro SQLite em `App/Cache`, por isso a passagem por 70 000 ficheiros é paga uma vez.
3. **Os formatos** (`Core/Code/formats`) leem os ficheiros da Valve sem bibliotecas de terceiros: `.mdl` `.vvd` `.vtx` são um modelo, `.vmt` `.vtf` um material e a sua textura, `.dmx` uma sessão, `.bsp` um mapa. Cada leitor é verificado contra toda a instalação; uma sessão é reescrita byte a byte.
4. **A sessão** é um grafo de elementos DMX. `animation.py` avalia os canais num instante, `operators.py` executa expressões e restrições de rig, `flex.py` move as caras, `pose.py` constrói as matrizes dos ossos. Cada edição passa por `editing.py` como um comando anulável.
5. **O editor** (`App/Code`) transforma isso numa cena (`render/scene.py`) e desenha-a com o seu próprio renderizador OpenGL 3.3 (`renderer.py`, `shaders.py`): luzes da sessão, lightmaps e a iluminação do mapa tal como o SFM as mostra. Os painéis (`ui/`) são a linha de tempo, a árvore da sessão, o inspetor, o graph editor e a ancoragem ao estilo do UE5.

Tudo o que o programa escreve fica na sua pasta: `App/User` para definições, `App/Cache` para o índice e caches, `App/Temporary` para o registo. `Core/` não escreve nada e não depende do Qt, por isso o motor e os testes correm em Python puro; Qt e OpenGL só são precisos pela janela. As utilidades em `Tools/` são construídas estritamente sobre `Core/API` — é assim que se prova que a API chega também para plugins de terceiros.

<p align="center"><img src="../assets/models.png" alt="64 modelos renderizados diretamente da instalação" width="60%"><br><sub>Sessenta e quatro modelos escolhidos ao acaso da instalação, desenhados pelo renderizador próprio do C2UI.</sub></p>

### Executar

Requer Windows, Python 3.13 e uma instalação do Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

No primeiro arranque procura o SFM através do Steam; se não o encontrar, pergunta. <kbd>Ctrl</kbd>+<kbd>O</kbd> abre uma sessão, <kbd>Espaço</kbd> reproduz, <kbd>C</kbd> vê pela câmara do plano, <kbd>T</kbd>/<kbd>R</kbd> mover/rodar, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> anula, <kbd>Ctrl</kbd>+<kbd>S</kbd> grava. Os painéis arrastam-se pelo título. Os testes não precisam de nada:

```bash
python Testing/run.py
```

### Planeado

**A seguir**
- O aspeto do mapa: skybox, água, prop_dynamic, texturas gobo das luzes, `$bumpmap` e `$envmap`, sombras das luzes da sessão.
- Exportação: sequências de imagens e vídeo.
- Plugins `.c2plg` e o cliente do marketplace em `Tools/Market Load`; depois temas e espaços de trabalho.
- Som na linha de tempo, partículas, wrinkle maps, predefinições e camadas do motion editor, tangentes no graph editor.

**Mais tarde**
- Desempenho em mapas completos: props estáticos instanciados, poses em cache.
- Reformulação do motor: novos parâmetros de compilação de mapas para melhor iluminação e sombras, limite de mapa de 120 000 unidades.
- Um lançador empacotado com o seu próprio Python e atualização automática; localização do editor.

## Licença e créditos

O código próprio do C2UI está sob a **licença C2UI**: livre para uso pessoal e não comercial; uso comercial apenas com o consentimento escrito do autor; as versões modificadas devem indicar o projeto original e o seu autor, Arkomiko. Plugins e addons estão sob a licença **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

O Source Filmmaker, o Team Fortress 2 e o motor Source são da Valve; o projeto lê os seus formatos, não inclui nenhum dos seus ficheiros e só funciona com a sua própria cópia do SFM do Steam.

<p align="center"><a href="../LICENSE/PT-pt.md"><img alt="Texto da licença" src="https://img.shields.io/badge/Texto_da_licen%C3%A7a-66c0f4?style=for-the-badge"></a></p>
