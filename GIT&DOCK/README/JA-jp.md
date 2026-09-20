<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <b>🇯🇵 日本語</b> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E7%8A%B6%E6%85%8B-%E3%83%97%E3%83%AC--%E3%82%A2%E3%83%AB%E3%83%95%E3%82%A1-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E3%83%86%E3%82%B9%E3%83%88-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — は Source Filmmaker のエディタを私が作り直したものです。同じコンテンツ、同じセッション形式、同じデータモデルを、Steam ライブラリの見た目と Unreal Engine 5 エディタのレイアウトを借りたシェルの中に収めました。</p>

---

## アイデア

Source Filmmaker は 2012 年のインターフェースをまとった優れたツールです。`sfm.exe` にスキンを被せたくはないし、そのウィンドウを一つずつ乗っ取りたくもありません。欲しいのは、**SFM がどこにインストールされているかを尋ね**、Garry's Mod が Counter-Strike をマウントするようにそのインストールをマウントし、モデル・マテリアル・テクスチャ・セッション・アニメーションのすべてをそのファイルの上で自力で行い、SFM を一度も起動しないエディタです。

目標は **SFM と一対一の機能同等性**（ボーンとリグを含む）、その先に SFM が持たなかったものです。

```
  ┌──────────────┐    "SFM はどこ?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  独自 UI     │ ◀───── マウント  ───────│    tf/  hl2/  tf_movies/ …   │
  │  独自描画    │      読み取り専用      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## 完成度

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>リリースへの全体的な完成度: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy を開いたエディタ" width="100%"><br><sub>現在のエディタ。Valve の「Meet the Heavy」を開いた状態: タイムラインにショットと音声、セッションツリー、最初のショットを自身のカメラから、セッション通りのポーズと表情のキャラクター。</sub></p>

領域を開くと、何ができていて何ができていないかが分かります。パーセントは SFM の能力に対する私の正直な見積もりです。

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM の検出とマウント</b></summary>

Steam レジストリ → `libraryfolders.vdf` → `gameinfo.txt` の検索パスをエンジンと同じ順序で。標準インストールで 6 つのマウント。アプリケーションフォルダの外には何も書き込みません。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>コンテンツインデックス</b></summary>

70 199 ファイルをコールド 1.1 秒 / キャッシュ 0.02 秒で。マウント間の上書きはエンジンと同じように解決。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>モデル — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

バージョン 44、48、49。スケルトン、メッシュ、全 LOD、ボディグループ。1 500 モデルを読み込み、失敗 0。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>マテリアル — <code>.vmt</code></b></summary>

同梱の 19 554 マテリアルすべてを解析。`patch`、DX ブロック、プロキシ。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>テクスチャ — <code>.vtf</code></b></summary>

バージョン 7.0–7.5、DXT1/3/5 とすべての非圧縮形式、キューブマップ、ミップ。DXT はデコードせずに GPU へ。

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>セッション — <code>.dmx</code></b></summary>

バイナリ 1–5 と KeyValues2。インストール内のすべてのセッションとパーティクルファイルが **バイト単位で同一** に書き戻されます。

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>画面上のセッション</b></summary>

タイムラインのショットと音声トラック、要素ツリー、各ショットのシーンをそのカメラから。未対応: マップ、パーティクル、音声。

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>アニメーション</b></summary>

チャンネルとログをカーソル位置で評価。スクラブと再生。ボーン、カメラ、可視性はセッションに従います。

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>表情</b></summary>

Flex コントローラ、コンパイル済みルール、頂点アニメーション — キャラクターが話し、表情を作ります。未対応: しわマップ。

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>リグ</b></summary>

式、point/orient/parent/aim コンストレイント、2 ボーン IK。未対応: 完全なオペレータ依存グラフ、リグ作成。

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>編集</b></summary>

クリックで選択、移動/回転マニピュレータ、任意の属性のインスペクタ、カーソル位置のキー、元に戻す/やり直し、バイト単位で正確な保存。未対応: グラフエディタ。

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>モーションエディタ</b></summary>

ルーラー上のホールドとフォールオフ付き時間選択。編集は SFM と同じように選択範囲に広がります。未対応: プリセット、レイヤー。

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>パネルのドッキング</b></summary>

UE5 や Visual Studio のように、プレビュー付きのターゲットコンパスにパネルをドラッグ。未対応: レイアウト保存、テーマ。

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source シェーディング</b></summary>

テクスチャと単純なライトのみ。未対応: phong、rim、lightwarp、シーンライト、影。

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>マップ — <code>.bsp</code></b></summary>

未着手。

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>画像・動画への書き出し</b></summary>

未着手。

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>プラグイン <code>.c2plg</code></b></summary>

未着手。

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>テーマとワークスペース</b></summary>

意図的に後回し。エディタに飾る価値のあるものができるまで一つの見た目。

</details>

**リリースの準備はできていません。** 基盤 — SFM が使うすべてのファイル形式を正しく読み、インストール全体で検証したもの — は整い、テストされています。セッションを開き、再生し、変更し、保存できます。足りないのは作業の *快適さ*: グラフエディタ、Source シェーディング、マップ、書き出し。アニメーターが一日の仕事をこなせるまでバージョン番号は付けません。

## 何が違うのか

- **ポータブル。** アプリケーションフォルダの外には何も書きません: 設定は `App/User`、キャッシュは `App/Cache`、一時ファイルは `App/Temporary`。フォルダを消せば跡形もありません。
- **SFM を起動しない。** 操作するプロセスも乗っ取るウィンドウもありません。インストールはコンテンツパックとして読まれます。
- **形式は検証済み、推測ではない。** すべてのリーダーを実際のインストールと照合しました。形式が意外なことをする箇所はコードがそう述べています。
- **保存は正確。** 変更せずに読んで書いたセッションは同じファイルです。
- **エンジンに依存関係なし。** `Core/` とテスト全体は素の Python で動きます。Qt と OpenGL が必要なのはウィンドウだけです。

## 実行

Windows、Python 3.13、Source Filmmaker のインストールが必要です。

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

初回起動時に Steam 経由で SFM を探します。見つからなければ尋ねます。<kbd>Ctrl</kbd>+<kbd>O</kbd> でセッションを開く、<kbd>Space</kbd> で再生、<kbd>C</kbd> でショットカメラ、<kbd>T</kbd>/<kbd>R</kbd> で移動/回転、<kbd>M</kbd> でモーションエディタ、<kbd>Ctrl</kbd>+<kbd>Z</kbd> で元に戻す、<kbd>Ctrl</kbd>+<kbd>S</kbd> で保存。パネルはタイトルをドラッグします。テストには何も必要ありません:

```bash
python Testing/run.py
```

## 構成

```
C2UI_SDK/
├── c2ui.py            ランチャー
├── Core/              エンジン: 形式、仮想ファイルシステム、インデックス、ブリッジ
├── App/               エディタ: コンテンツライブラリ、レンダラ、ウィンドウ
├── Tools/             ローカライズ、UI ツール、プラグイン (後日)
├── Testing/           テスト、バイト単位のフィクスチャ、単一ランナー
└── GIT&DOCK/README/   この README の他言語版
```

## ロードマップ

1. **グラフエディタ** — カーブとキーを目で見る。
2. **Source シェーディング** — SFM が描く VertexLitGeneric: phong、rim、lightwarp、シーンライト。
3. **マップ** — 背景用の `.bsp`。
4. **出力** — 画像と動画の書き出し。
5. **プラグイン** — `.c2plg` 形式。その後テーマとワークスペース。

## ライセンスとクレジット

Source Filmmaker、Team Fortress 2、Source エンジンは Valve のものです。このプロジェクトはそれらのファイル形式を読むだけで、ファイルは一切同梱せず、Steam で既にお持ちの SFM でのみ動作します。

C2UI 自身のコードのライセンスはまだ決めていません — それまでは全著作権を留保します。Issue と Pull Request は歓迎します。

<p align="center"><img src="../../.github/assets/models.png" alt="インストールから直接描画した 64 モデル" width="60%"><br><sub>インストールから無作為に選んだ 64 のモデルを C2UI 独自のレンダラで描画。</sub></p>
