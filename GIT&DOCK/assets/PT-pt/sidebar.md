# Estado do C2UI em detalhe

<details align="center"><summary>&nbsp;🌐 <b>🇵🇹 Português</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../RU-ru/sidebar.md">🇷🇺<br>Русский</a></td><td align="center"><a href="../EN-en/sidebar.md">🇬🇧<br>English</a></td><td align="center"><a href="../PL-pl/sidebar.md">🇵🇱<br>Polski</a></td><td align="center"><a href="../UK-ua/sidebar.md">🇺🇦<br>Українська</a></td><td align="center"><a href="../DE-de/sidebar.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="../RO-md/sidebar.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="../SL-si/sidebar.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="../BE-by/sidebar.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="../KK-kz/sidebar.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="../JA-jp/sidebar.md">🇯🇵<br>日本語</a></td><td align="center"><a href="../ZH-cn/sidebar.md">🇨🇳<br>中文</a></td><td align="center"><a href="../SV-se/sidebar.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="../ES-es/sidebar.md">🇪🇸<br>Español</a></td><td align="center"><a href="../HI-in/sidebar.md">🇮🇳<br>हिन्दी</a></td><td align="center"><b>🇵🇹<br>Português</b></td><td align="center"><a href="../BN-bd/sidebar.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="../FR-fr/sidebar.md">🇫🇷<br>Français</a></td><td align="center"><a href="../TE-in/sidebar.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="../MR-in/sidebar.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="../TA-in/sidebar.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="../TR-tr/sidebar.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="../UR-pk/sidebar.md">🇵🇰<br>اردو</a></td><td align="center"><a href="../VI-vn/sidebar.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="../GU-in/sidebar.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="../IT-it/sidebar.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="../KO-kr/sidebar.md">🇰🇷<br>한국어</a></td><td align="center"><a href="../AR-sa/sidebar.md">🇸🇦<br>العربية</a></td><td align="center"><a href="../JV-id/sidebar.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="../ML-in/sidebar.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="../NE-np/sidebar.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="../UZ-uz/sidebar.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="../OR-in/sidebar.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

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
