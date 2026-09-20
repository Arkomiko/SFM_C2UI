# C2UI 完成度 — 详情

<details align="center"><summary>&nbsp;🌐 <b>🇨🇳 中文</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../RU-ru/sidebar.md">🇷🇺<br>Русский</a></td><td align="center"><a href="../EN-en/sidebar.md">🇬🇧<br>English</a></td><td align="center"><a href="../PL-pl/sidebar.md">🇵🇱<br>Polski</a></td><td align="center"><a href="../UK-ua/sidebar.md">🇺🇦<br>Українська</a></td><td align="center"><a href="../DE-de/sidebar.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="../RO-md/sidebar.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="../SL-si/sidebar.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="../BE-by/sidebar.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="../KK-kz/sidebar.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="../JA-jp/sidebar.md">🇯🇵<br>日本語</a></td><td align="center"><b>🇨🇳<br>中文</b></td><td align="center"><a href="../SV-se/sidebar.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="../ES-es/sidebar.md">🇪🇸<br>Español</a></td><td align="center"><a href="../HI-in/sidebar.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="../PT-pt/sidebar.md">🇵🇹<br>Português</a></td><td align="center"><a href="../BN-bd/sidebar.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="../FR-fr/sidebar.md">🇫🇷<br>Français</a></td><td align="center"><a href="../TE-in/sidebar.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="../MR-in/sidebar.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="../TA-in/sidebar.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="../TR-tr/sidebar.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="../UR-pk/sidebar.md">🇵🇰<br>اردو</a></td><td align="center"><a href="../VI-vn/sidebar.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="../GU-in/sidebar.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="../IT-it/sidebar.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="../KO-kr/sidebar.md">🇰🇷<br>한국어</a></td><td align="center"><a href="../AR-sa/sidebar.md">🇸🇦<br>العربية</a></td><td align="center"><a href="../JV-id/sidebar.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="../ML-in/sidebar.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="../NE-np/sidebar.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="../UZ-uz/sidebar.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="../OR-in/sidebar.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="sidebar.svg" alt="完成度" width="320"></p>

<p align="center"><img alt="44%" src="https://img.shields.io/badge/44%25-e0a800?style=flat-square"> <b>整体发布就绪度：44%</b></p>

每个领域都可以展开：已经能用的和暂时还没有的。百分比是相对于 SFM 能力的估计。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 查找并挂载 SFM

Steam 注册表 → `libraryfolders.vdf` → `gameinfo.txt` 的搜索路径，按引擎自身顺序。标准安装下六个挂载点。应用程序文件夹之外不写入任何内容。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 内容索引

70 199 个文件冷启动 1.1 秒 / 缓存 0.02 秒；挂载间的覆盖完全按引擎方式解析。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 模型 — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

版本 44、48、49。骨架、网格、所有细节层级、身体组。已加载 1 500 个模型，0 失败。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 材质 — <code>.vmt</code>

全部 19 554 个自带材质均可解析；`patch`、DX 级别块、代理。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 纹理 — <code>.vtf</code>

版本 7.0–7.5，DXT1/3/5 和所有未压缩格式、立方体贴图、mip。DXT 无需解码直接进 GPU。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 会话 — <code>.dmx</code>

二进制 1–5 和 KeyValues2。安装中的每个会话和粒子文件都能**逐字节**写回。

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> 屏幕上的会话

时间线上的镜头和音轨、元素树、每个镜头通过其相机的场景。尚无：地图、粒子、声音。

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> 动画

在光标处求值通道和日志；拖动和播放。骨骼、相机和可见性跟随会话。

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> 面部

Flex 控制器、编译后的规则和顶点动画——角色会说话和做表情。尚无：皱纹贴图。

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> 绑定

表达式、point/orient/parent/aim 约束、双骨 IK。尚无：完整的操作符依赖图、绑定创建。

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> 编辑

点击选择、移动/旋转操纵器、任意属性的检查器、光标处打关键帧、撤销/重做、逐字节精确保存。

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> 运动编辑器

标尺上带保持和衰减的时间选择；编辑像 SFM 一样扩散到选区。尚无：预设、图层。

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> 曲线编辑器

驱动所选元素的每个日志的曲线：X/Y/Z、pitch/yaw/roll、标量。关键帧可在时间和值上拖动并实时预览，双击插入，Delete 删除；时间轴与时间线共享。尚无：切线和曲线类型、成组缩放关键帧。

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> 面板停靠

像 UE5 和 Visual Studio 一样，把面板拖到带预览的目标罗盘上。尚无：保存布局、主题。

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source 着色

仅纹理和简单光照。尚无：phong、rim、lightwarp、场景灯光、阴影。

### <img alt="45%" src="https://img.shields.io/badge/45%25-e0a800?style=flat-square"> 地图 — <code>.bsp</code>

版本 19–21：世界几何、置换地形、笔刷实体、静态道具、地图自带 pak 材质。视锥剔除。尚无：光照贴图、天空盒、水、prop_dynamic。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 渲染为图像和视频

未开始。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 插件 <code>.c2plg</code>

未开始。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 主题和工作区

有意推后：在编辑器有值得美化的东西之前只用一种外观。

**尚未准备好发布。** 基础——SFM 使用的每种文件格式，正确读取并对整个安装验证——已经就位并通过测试；会话可以打开、播放、修改和保存。缺少的是工作的*舒适度*：曲线编辑器、Source 着色、地图、导出。在动画师能在其中工作一整天之前不会有版本号。

<p align="center"><a href="../../README/ZH-cn.md"><img alt="← 返回 README" src="https://img.shields.io/badge/%E2%86%90_%E8%BF%94%E5%9B%9E_README-1b2838?style=for-the-badge"></a></p>
