# C2UI 启动器

<details align="center"><summary>&nbsp;🌐 <b>🇨🇳 中文</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><b>🇨🇳<br>中文</b></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` 是启动项目的地方：一个深色小窗口，含标题、一行说明和三个按钮。它可以打包成单个可执行文件，无需安装 Python；它会自己找到项目——从所在位置向上查找，直到看到 `App`、`Core` 和 `Launcher` 并存。

<p align="center"><img src="../assets/launcher.png" alt="C2UI 启动器" width="562"><br><sub>启动器窗口：“Dev-mode”标题、说明行和三个按钮。</sub></p>

> [!NOTE]
> **启动器界面目前只有俄语——这是临时方案。** 标题、说明和按钮文字写死在代码里；翻译会随编辑器本地化（`Tools/Localization`）一起到来，届时启动器会针对完成后的 App 重写。项目的其余文档已有 32 种语言。

## 三个按钮

| | |
|---|---|
| <code>Запустить Core</code> | 启动编辑器——带视口、时间线和面板的 C2UI 窗口。 |
| <code>Запустить App</code> | 灰显：尚无独立的 App。 |
| <code>Выйти</code> | 关闭启动器。 |

## 从源码运行

需要 Windows、Python 3.13 和已安装的 Source Filmmaker。

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

构建单文件 `Launcher/Launcher-C2UI.exe`（不入 git——从源码重新构建）：

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## 不带编辑器的引擎

`Launcher/core.py` 单独启动 `Core`：挂载安装目录、建立索引，并提供一个引擎之上的小型命令行——模型、材质、贴图、地图、会话及其求值。同样是临时的：等 App 能无窗口运行，编辑器就成为唯一入口。

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## 以后会怎样

- App 出现时重写窗口，连同外观与翻译。
- “Запустить App”按钮开始可用。
- 编辑器能无窗口启动后，`core.py` 即被移除。
- 构建好的 `.exe` 会随 GitHub 发行版一同提供。

<p align="center"><a href="../README/ZH-cn.md"><img alt="← 返回 README" src="https://img.shields.io/badge/%E2%86%90_%E8%BF%94%E5%9B%9E_README-1b2838?style=for-the-badge"></a></p>
