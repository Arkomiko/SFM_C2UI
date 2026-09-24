# C2UI ランチャー

<details align="center"><summary>&nbsp;🌐 <b>🇯🇵 日本語</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><b>🇯🇵<br>日本語</b></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` はプロジェクトを起動する場所です。タイトル、一行の説明、三つのボタンを持つ小さな暗いウィンドウで、Python のインストールを必要としない単一の実行ファイルにまとめられます。プロジェクトは自分で見つけます — 置かれた場所から上へたどり、`App`・`Core`・`Launcher` が揃っているところまで進みます。

<p align="center"><img src="../assets/launcher.png" alt="C2UI ランチャー" width="562"><br><sub>ランチャーのウィンドウ：「Dev-mode」のタイトル、説明行、三つのボタン。</sub></p>

> [!NOTE]
> **ランチャーの表示は今のところロシア語だけです — 暫定的な措置です。** タイトル、説明、ボタンの文字はコードに直接書かれており、翻訳はエディターのローカライズ（`Tools/Localization`）と同時に、App の完成に合わせてランチャーを書き直すときに入ります。プロジェクトのそれ以外の文書はすでに 32 言語で読めます。

## 三つのボタン

| | |
|---|---|
| <code>Запустить Core</code> | エディターを起動します — ビューポート、タイムライン、パネルを備えた C2UI のウィンドウ。 |
| <code>Запустить App</code> | 無効：独立した App はまだありません。 |
| <code>Выйти</code> | ランチャーを閉じます。 |

## ソースから起動する

Windows、Python 3.13、インストール済みの Source Filmmaker が必要です。

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

単一ファイル `Launcher/Launcher-C2UI.exe` のビルド（git には入れず、ソースから作り直します）：

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## エディターなしのエンジン

`Launcher/core.py` は `Core` だけを起動します。インストールをマウントし、索引を作り、エンジンの上に小さなシェルを与えます — モデル、マテリアル、テクスチャ、マップ、セッションとその評価。これも暫定で、App がウィンドウなしで動くようになればエディターが唯一の入口になります。

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## この先どうなるか

- App の完成に合わせてウィンドウを書き直します（見た目と翻訳も）。
- 「Запустить App」ボタンが動くようになります。
- エディターをウィンドウなしで起動できるようになれば `core.py` はなくなります。
- ビルドした `.exe` を GitHub のリリースに添付します。

<p align="center"><a href="../README/JA-jp.md"><img alt="← README に戻る" src="https://img.shields.io/badge/%E2%86%90_README_%E3%81%AB%E6%88%BB%E3%82%8B-1b2838?style=for-the-badge"></a></p>
