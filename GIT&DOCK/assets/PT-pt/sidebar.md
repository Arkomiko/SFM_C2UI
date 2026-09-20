# Estado do C2UI em detalhe

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <b>🇵🇹 Português</b> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Estado" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Prontidão geral para lançamento: 41%</b></p>

Cada área expande-se: o que já funciona e o que ainda não existe. As percentagens são uma estimativa face ao que o SFM consegue.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Encontrar e montar o SFM

Registo do Steam → `libraryfolders.vdf` → os caminhos de pesquisa do `gameinfo.txt`, na ordem do motor. Seis montagens numa instalação normal. Nada é escrito fora da pasta da aplicação.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Índice de conteúdo

70 199 ficheiros em 1,1 s a frio / 0,02 s em cache; as sobreposições entre montagens são resolvidas exatamente como o motor faz.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modelos — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Versões 44, 48, 49. Esqueleto, malhas, todos os níveis de detalhe, grupos de corpo. 1 500 modelos carregados, 0 falhas.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Materiais — <code>.vmt</code>

Todos os 19 554 materiais incluídos são lidos; `patch`, blocos DX, proxies.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Texturas — <code>.vtf</code>

Versões 7.0–7.5, DXT1/3/5 e todos os formatos não comprimidos, cubemaps, mips. O DXT vai para a GPU sem descodificação.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sessões — <code>.dmx</code>

Binário 1–5 e KeyValues2. Cada sessão e ficheiro de partículas da instalação é reescrito **byte a byte**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Sessão no ecrã

Planos e faixas de som numa linha temporal, a árvore de elementos, a cena de cada plano pela sua câmara. Ainda não: mapas, partículas, som.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animação

Canais e logs avaliados no cursor; scrub e reprodução. Ossos, câmaras e visibilidade seguem a sessão.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Caras

Controladores flex, as regras compiladas e animação de vértices — as personagens falam e fazem expressões. Ainda não: mapas de rugas.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rigs

Expressões, restrições point/orient/parent/aim, IK de dois ossos. Ainda não: o grafo completo de dependências de operadores, criação de rigs.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Edição

Clique para selecionar, manipulador de mover/rodar, inspetor de qualquer atributo, chave no cursor, anular/refazer, gravação exata ao byte.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Seleção de tempo com hold e falloff na régua; uma edição espalha-se sobre ela como no SFM. Ainda não: presets, camadas.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Editor de gráficos

Curvas de cada log que move o elemento selecionado: X/Y/Z, pitch/yaw/roll, escalares. As chaves arrastam-se em tempo e valor com pré-visualização ao vivo, duplo clique insere, Delete remove; o eixo do tempo é o da linha temporal. Ainda não: tangentes e tipos de curva, escalar um grupo de chaves.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Ancoragem de painéis

Arraste painéis para uma bússola de alvos com pré-visualização, como no UE5 e no Visual Studio. Ainda não: disposições guardadas, temas.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Sombreamento Source

Só textura e uma luz simples. Ainda não: phong, rim, lightwarp, luzes de cena, sombras.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Mapas — <code>.bsp</code>

Não iniciado.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Render para imagem e vídeo

Não iniciado.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugins <code>.c2plg</code>

Não iniciado.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Temas e espaços de trabalho

Deliberadamente mais tarde: um só aspeto até o editor ter algo que valha a pena tematizar.

**Não está pronto para lançamento.** A base — cada formato de ficheiro que o SFM usa, lido corretamente e verificado contra toda a instalação — está feita e testada; uma sessão pode ser aberta, reproduzida, alterada e gravada. O que falta é o *conforto* do trabalho: o editor de gráficos, o sombreamento Source, mapas, exportação. Sem número de versão até um animador conseguir fazer um dia de trabalho nele.

<p align="center"><a href="../../README/PT-pt.md"><img alt="← Voltar ao README" src="https://img.shields.io/badge/%E2%86%90_Voltar_ao_README-1b2838?style=for-the-badge"></a></p>
