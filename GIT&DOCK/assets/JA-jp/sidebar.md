# C2UI の完成度 — 詳細

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <b>🇯🇵 日本語</b> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="完成度" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>リリースへの全体的な完成度: 41%</b></p>

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

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source シェーディング

テクスチャと単純なライトのみ。未対応: phong、rim、lightwarp、シーンライト、影。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> マップ — <code>.bsp</code>

未着手。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 画像・動画への書き出し

未着手。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> プラグイン <code>.c2plg</code>

未着手。

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> テーマとワークスペース

意図的に後回し。エディタに飾る価値のあるものができるまで一つの見た目。

**リリースの準備はできていません。** 基盤 — SFM が使うすべてのファイル形式を正しく読み、インストール全体で検証したもの — は整い、テストされています。セッションを開き、再生し、変更し、保存できます。足りないのは作業の *快適さ*: グラフエディタ、Source シェーディング、マップ、書き出し。アニメーターが一日の仕事をこなせるまでバージョン番号は付けません。

<p align="center"><a href="../../README/JA-jp.md"><img alt="← README に戻る" src="https://img.shields.io/badge/%E2%86%90_README_%E3%81%AB%E6%88%BB%E3%82%8B-1b2838?style=for-the-badge"></a></p>
