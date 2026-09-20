<p align="center"><img src="../assets/PT-pt/banner.png" alt="C2UI" width="100%"></p>

<details align="center"><summary>&nbsp;🌐 <b>🇵🇹 Português</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../../README.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><b>🇵🇹<br>Português</b></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/estado-pr%C3%A9--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/testes-359-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — o editor do Source Filmmaker numa interface moderna: o mesmo conteúdo, o mesmo formato de sessão, o mesmo modelo de dados, com um aspeto no espírito da biblioteca do Steam e do editor do Unreal Engine 5.</p>

---

## Estado

<p align="center"><img src="../assets/PT-pt/sidebar.svg" alt="Estado" width="320"></p>

<p align="center"><img alt="44%" src="https://img.shields.io/badge/44%25-e0a800?style=flat-square"> <b>Prontidão geral para lançamento: 44%</b></p>

<p align="center"><a href="../assets/PT-pt/sidebar.md"><img alt="Estado em detalhe" src="https://img.shields.io/badge/Estado_em_detalhe-66c0f4?style=for-the-badge"></a></p>

## A ideia

O Source Filmmaker é uma ferramenta forte cuja interface ficou em 2012. O C2UI não o substitui nem o refaz: o objetivo é simplesmente tornar o SFM um pouco mais moderno e confortável.

O editor encontra o SFM instalado, liga-o como biblioteca de conteúdo — modelos, materiais, texturas, sessões — e trabalha com os mesmos ficheiros no mesmo formato. Tudo o que foi feito no SFM abre no C2UI, e vice-versa.

O primeiro objetivo é a compatibilidade total com o SFM, ossos e rigs incluídos. Depois, o que faltava ao SFM.

```
  ┌──────────────┐    "onde está o SFM?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI própria  │ ◀─────  montado  ───────│    tf/  hl2/  tf_movies/ …   │
  │  render próprio │      só leitura       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="O editor com Meet the Heavy aberto" width="100%"><br><sub>O editor hoje, com o Meet the Heavy da Valve aberto: planos e som na linha temporal, a árvore da sessão, o primeiro plano visto pela sua própria câmara, personagens em pose e com as caras que a sessão dita.</sub></p>

## O que o torna diferente

- **Portátil.** Nada é escrito fora da pasta da aplicação: definições em `App/User`, caches em `App/Cache`, temporários em `App/Temporary`. Apague a pasta e desaparece.
- **Nunca corre o SFM.** Não há processo a controlar nem janelas a sequestrar. A instalação é lida como um pacote de conteúdo.
- **Formatos verificados, não presumidos.** Cada leitor foi comparado com a instalação real; onde um formato faz algo surpreendente, o código diz-o.
- **A gravação é exata.** Uma sessão lida e escrita sem alterações é o mesmo ficheiro.
- **O motor não tem dependências.** `Core/` e toda a suíte de testes correm em Python puro; só a janela precisa de Qt e OpenGL.

## Executar

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

## Estrutura

```
C2UI_SDK/
├── README.md
├── Core/              motor: formatos, sistema de ficheiros virtual, índice, pontes
├── App/               o editor: biblioteca de conteúdo, renderizador, janela
├── Tools/             localização, ferramentas de UI, plugins (mais tarde)
│   └── Launcher/      o lançador
├── Testing/           testes, fixtures exatas ao byte, um runner
└── GIT&DOCK/          este README noutras línguas
```

## Plano

1. **Sombreamento Source** — VertexLitGeneric como o SFM o desenha: phong, rim, lightwarp, luzes de cena.
2. **Mapas** — `.bsp` para fundos.
3. **Saída** — exportação de imagem e vídeo.
4. **Plugins** — o formato `.c2plg`; depois temas e espaços de trabalho.

## Licença e créditos

O código próprio do C2UI está sob a **licença C2UI**: livre para uso pessoal e não comercial; uso comercial apenas com o consentimento escrito do autor; as versões modificadas devem indicar o projeto original e o seu autor, Arkomiko. Plugins e addons estão sob a licença **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

O Source Filmmaker, o Team Fortress 2 e o motor Source são da Valve; o projeto lê os seus formatos, não inclui nenhum dos seus ficheiros e só funciona com a sua própria cópia do SFM do Steam.

<p align="center"><a href="../LICENSE/PT-pt.md"><img alt="Texto da licença" src="https://img.shields.io/badge/Texto_da_licen%C3%A7a-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 modelos renderizados diretamente da instalação" width="60%"><br><sub>Sessenta e quatro modelos escolhidos ao acaso da instalação, desenhados pelo renderizador próprio do C2UI.</sub></p>
