# O lançador do C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇵🇹 Português</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><b>🇵🇹<br>Português</b></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` é de onde o projeto arranca: uma pequena janela escura com um título, uma linha de descrição e três botões. Compila-se num único executável que não precisa de Python instalado e encontra o projeto sozinho — sobe a partir de onde está até ver `App`, `Core` e `Launcher` juntos.

<p align="center"><img src="../assets/launcher.png" alt="O lançador do C2UI" width="562"><br><sub>A janela do lançador: o título «Dev-mode», a linha de descrição e três botões.</sub></p>

> [!NOTE]
> **A interface do lançador está por agora só em russo — é uma solução provisória.** O título, a descrição e os textos dos botões estão escritos no código; as traduções chegam com a localização do editor (`Tools/Localization`), quando o lançador for reescrito para um App terminado. A restante documentação do projeto já existe em 32 línguas.

## Os três botões

| | |
|---|---|
| <code>Запустить Core</code> | Arranca o editor — a janela do C2UI com o visor, a linha de tempo e os painéis. |
| <code>Запустить App</code> | Desativado: ainda não há um App separado. |
| <code>Выйти</code> | Fecha o lançador. |

## Correr a partir do código

São precisos Windows, Python 3.13 e uma instalação do Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Construir o ficheiro único `Launcher/Launcher-C2UI.exe` (não fica no git — é reconstruído a partir do código):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## O motor sem o editor

`Launcher/core.py` arranca o `Core` por si: monta uma instalação, indexa-a e dá uma pequena consola sobre o motor — modelos, materiais, texturas, mapas, sessões e a sua avaliação. Também provisório: quando o App correr sem janela, o editor passa a ser o único ponto de entrada.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## O que muda depois

- A janela será reescrita com o App — com aspeto e traduções.
- O botão «Запустить App» passará a funcionar.
- `core.py` sai quando o editor puder arrancar sem janela.
- O `.exe` construído acompanhará os lançamentos no GitHub.

<p align="center"><a href="../README/PT-pt.md"><img alt="← Voltar ao README" src="https://img.shields.io/badge/%E2%86%90_Voltar_ao_README-1b2838?style=for-the-badge"></a></p>
