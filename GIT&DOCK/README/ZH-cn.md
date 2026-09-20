<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <b>🇨🇳 中文</b> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E7%8A%B6%E6%80%81-%E9%A2%84--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E6%B5%8B%E8%AF%95-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — 是我对 Source Filmmaker 编辑器的重建：同样的内容、同样的会话格式、同样的数据模型，放在一个外观借自 Steam 库、布局借自 Unreal Engine 5 编辑器的外壳里。</p>

---

## 想法

Source Filmmaker 是一款披着 2012 年界面的优秀工具。我不想给 `sfm.exe` 套一层皮肤，也不想逐个劫持它的窗口。我想要一个**询问 SFM 安装在哪里**的编辑器，像 Garry's Mod 挂载 Counter-Strike 那样挂载这份安装，并在这些文件之上自己完成一切——模型、材质、纹理、会话、动画——而从不启动 SFM。

目标是**与 SFM 一比一的功能对等**（包括骨骼和绑定），然后是 SFM 从未有过的东西。

```
  ┌──────────────┐    "SFM 在哪?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  自有 UI     │ ◀─────   挂载    ───────│    tf/  hl2/  tf_movies/ …   │
  │  自有渲染    │         只读          │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## 完成度

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>整体发布就绪度：38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="打开 Meet the Heavy 的编辑器" width="100%"><br><sub>今天的编辑器，打开了 Valve 的《Meet the Heavy》：时间线上的镜头和声音、会话树、通过自身相机看到的第一个镜头、按会话摆好姿势和表情的角色。</sub></p>

展开一个领域即可看到具体完成了什么、没完成什么。百分比是我对照 SFM 能力的诚实估计。

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>查找并挂载 SFM</b></summary>

Steam 注册表 → `libraryfolders.vdf` → `gameinfo.txt` 的搜索路径，按引擎自身顺序。标准安装下六个挂载点。应用程序文件夹之外不写入任何内容。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>内容索引</b></summary>

70 199 个文件冷启动 1.1 秒 / 缓存 0.02 秒；挂载间的覆盖完全按引擎方式解析。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>模型 — `.mdl` `.vvd` `.vtx`</b></summary>

版本 44、48、49。骨架、网格、所有细节层级、身体组。已加载 1 500 个模型，0 失败。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>材质 — `.vmt`</b></summary>

全部 19 554 个自带材质均可解析；`patch`、DX 级别块、代理。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>纹理 — `.vtf`</b></summary>

版本 7.0–7.5，DXT1/3/5 和所有未压缩格式、立方体贴图、mip。DXT 无需解码直接进 GPU。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>会话 — `.dmx`</b></summary>

二进制 1–5 和 KeyValues2。安装中的每个会话和粒子文件都能**逐字节**写回。

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>屏幕上的会话</b></summary>

时间线上的镜头和音轨、元素树、每个镜头通过其相机的场景。尚无：地图、粒子、声音。

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>动画</b></summary>

在光标处求值通道和日志；拖动和播放。骨骼、相机和可见性跟随会话。

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>面部</b></summary>

Flex 控制器、编译后的规则和顶点动画——角色会说话和做表情。尚无：皱纹贴图。

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>绑定</b></summary>

表达式、point/orient/parent/aim 约束、双骨 IK。尚无：完整的操作符依赖图、绑定创建。

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>编辑</b></summary>

点击选择、移动/旋转操纵器、任意属性的检查器、光标处打关键帧、撤销/重做、逐字节精确保存。尚无：曲线编辑器。

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>运动编辑器</b></summary>

标尺上带保持和衰减的时间选择；编辑像 SFM 一样扩散到选区。尚无：预设、图层。

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>面板停靠</b></summary>

像 UE5 和 Visual Studio 一样，把面板拖到带预览的目标罗盘上。尚无：保存布局、主题。

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source 着色</b></summary>

仅纹理和简单光照。尚无：phong、rim、lightwarp、场景灯光、阴影。

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>地图 — `.bsp`</b></summary>

未开始。

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>渲染为图像和视频</b></summary>

未开始。

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>插件 `.c2plg`</b></summary>

未开始。

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>主题和工作区</b></summary>

有意推后：在编辑器有值得美化的东西之前只用一种外观。

</details>

**尚未准备好发布。** 基础——SFM 使用的每种文件格式，正确读取并对整个安装验证——已经就位并通过测试；会话可以打开、播放、修改和保存。缺少的是工作的*舒适度*：曲线编辑器、Source 着色、地图、导出。在动画师能在其中工作一整天之前不会有版本号。

## 有何不同

- **便携。** 应用程序文件夹之外不写入任何内容：设置在 `App/User`，缓存在 `App/Cache`，临时文件在 `App/Temporary`。删掉文件夹就不留痕迹。
- **从不运行 SFM。** 没有要驱动的进程，没有要劫持的窗口。安装被当作内容包读取。
- **格式经过验证，而非假设。** 每个读取器都对照真实安装检查过；格式做了出人意料的事情时，代码会说明。
- **保存精确。** 未经修改读取并写入的会话就是同一个文件。
- **引擎没有依赖。** `Core/` 和整套测试在纯 Python 上运行；只有窗口需要 Qt 和 OpenGL。

## 运行

需要 Windows、Python 3.13 和已安装的 Source Filmmaker。

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

首次启动时通过 Steam 查找 SFM；找不到则询问。<kbd>Ctrl</kbd>+<kbd>O</kbd> 打开会话，<kbd>Space</kbd> 播放，<kbd>C</kbd> 通过镜头相机观看，<kbd>T</kbd>/<kbd>R</kbd> 移动/旋转，<kbd>M</kbd> 运动编辑器，<kbd>Ctrl</kbd>+<kbd>Z</kbd> 撤销，<kbd>Ctrl</kbd>+<kbd>S</kbd> 保存。面板按标题拖动。测试不需要任何东西：

```bash
python Testing/run.py
```

## 结构

```
C2UI_SDK/
├── c2ui.py            启动器
├── Core/              引擎：格式、虚拟文件系统、索引、桥接
├── App/               编辑器：内容库、渲染器、窗口
├── Tools/             本地化、UI 工具、插件（稍后）
├── Testing/           测试、逐字节夹具、单一运行器
└── GIT&DOCK/README/   本 README 的其他语言版本
```

## 路线图

1. **曲线编辑器** — 看得见的曲线和关键帧。
2. **Source 着色** — SFM 绘制的 VertexLitGeneric：phong、rim、lightwarp、场景灯光。
3. **地图** — 用作背景的 `.bsp`。
4. **输出** — 图像和视频导出。
5. **插件** — `.c2plg` 格式；然后是主题和工作区。

## 许可与致谢

Source Filmmaker、Team Fortress 2 和 Source 引擎属于 Valve。本项目读取它们的文件格式，不附带它们的任何文件，只与你已通过 Steam 拥有的 SFM 副本一起工作。

C2UI 自身代码的许可证尚未选定——在此之前保留所有权利。仍然欢迎 Issue 和 Pull Request。

<p align="center"><img src="../../.github/assets/models.png" alt="直接从安装渲染的 64 个模型" width="60%"><br><sub>从安装中随机挑选的六十四个模型，由 C2UI 自己的渲染器绘制。</sub></p>
