# C2UI の完成度 — 詳細

<details align="center"><summary>&nbsp;🌐 <b>🇯🇵 日本語</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><b>🇯🇵<br>日本語</b></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/JA-jp.svg" alt="完成度" width="100%"></p>

<p align="center"><img alt="51%" src="https://img.shields.io/badge/51%25-e0a800?style=flat-square"> <b>リリースへの全体的な完成度: 51%</b></p>

各領域を開くと、すでに動くものとまだないものが分かります。パーセントは SFM の機能に対する目安です。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> SFM の検出とマウント

Steam レジストリ → `libraryfolders.vdf` → `gameinfo.txt` の検索パスをエンジンと同じ順序で。標準インストールで 6 つのマウント。アプリケーションフォルダの外には何も書き込みません。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> コンテンツインデックス

70 199 ファイルをコールド 1.1 秒 / キャッシュ 0.02 秒で。マウント間の上書きはエンジンと同じように解決。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> モデル — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

バージョン 44、48、49。スケルトン、メッシュ、全 LOD、ボディグループ。1 500 モデルを読み込み、失敗 0。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> マテリアル — <code>.vmt</code>

同梱の 19 554 マテリアルすべてを解析。`patch`、DX ブロック、プロキシ。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> テクスチャ — <code>.vtf</code>

バージョン 7.0–7.5、DXT1/3/5 とすべての非圧縮形式、キューブマップ、ミップ。DXT はデコードせずに GPU へ。

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> セッション — <code>.dmx</code>

バイナリ 1–5 と KeyValues2。インストール内のすべてのセッションとパーティクルファイルが **バイト単位で同一** に書き戻されます。

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> 画面上のセッション

タイムラインのショットと音声トラック、要素ツリー、各ショットのシーンをそのカメラから。未対応: マップ、パーティクル、音声。

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> アニメーション

チャンネルとログをカーソル位置で評価。スクラブと再生。ボーン、カメラ、可視性はセッションに従います。

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> 表情

Flex コントローラ、コンパイル済みルール、頂点アニメーション — キャラクターが話し、表情を作ります。未対応: しわマップ。

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> リグ

式、point/orient/parent/aim コンストレイント、2 ボーン IK。未対応: 完全なオペレータ依存グラフ、リグ作成。

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> 編集

クリックで選択、移動/回転マニピュレータ、任意の属性のインスペクタ、カーソル位置のキー、元に戻す/やり直し、バイト単位で正確な保存。

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> モーションエディタ

ルーラー上のホールドとフォールオフ付き時間選択。編集は SFM と同じように選択範囲に広がります。未対応: プリセット、レイヤー。

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> グラフエディタ

選択要素を駆動するすべてのログの曲線: X/Y/Z、pitch/yaw/roll、スカラー。キーはライブプレビュー付きで時間と値にドラッグ、ダブルクリックで挿入、Delete で削除。時間軸はタイムラインと共有。未対応: タンジェントとカーブタイプ、キー群のスケーリング。

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> パネルのドッキング

UE5 や Visual Studio のように、プレビュー付きのターゲットコンパスにパネルをドラッグ。未対応: レイアウト保存、テーマ。

### <img alt="65%" src="https://img.shields.io/badge/65%25-e0a800?style=flat-square"> Source シェーディング

セッションのライト (DmeProjectedLight): 視錐台、Source の減衰、maxDistance へのフェード; ハーフランバート、$lightwarptexture、フォン ($phongexponent/boost/fresnelranges)、$rimlight、$selfillum。マップのワールドはライトマップで。未対応: 影、ゴボテクスチャ、$bumpmap、$envmap、アンビエントキューブ、スカイボックス。

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> マップ — <code>.bsp</code>

バージョン 19–21: ワールド形状、ディスプレイスメント地形、ブラシエンティティ、静的プロップ、マップ内蔵 pak のマテリアル。視錐台カリング。未対応: ライトマップ、スカイボックス、水、prop_dynamic。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 画像・動画への書き出し

未着手。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> プラグイン <code>.c2plg</code>

未着手。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> テーマとワークスペース

意図的に後回し。エディタに飾る価値のあるものができるまで一つの見た目。

**リリースの準備はできていません。** 基盤 — SFM が使うすべてのファイル形式を正しく読み、インストール全体で検証したもの — は整い、テストされています。セッションを開き、再生し、変更し、保存できます。足りないのは作業の *快適さ*: グラフエディタ、Source シェーディング、マップ、書き出し。アニメーターが一日の仕事をこなせるまでバージョン番号は付けません。

<p align="center"><a href="../README/JA-jp.md"><img alt="← README に戻る" src="https://img.shields.io/badge/%E2%86%90_README_%E3%81%AB%E6%88%BB%E3%82%8B-1b2838?style=for-the-badge"></a></p>
