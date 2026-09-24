# C2UI 런처

<details align="center"><summary>&nbsp;🌐 <b>🇰🇷 한국어</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><b>🇰🇷<br>한국어</b></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/`는 프로젝트를 시작하는 곳입니다. 제목, 한 줄 설명, 버튼 세 개가 있는 작은 어두운 창으로, 파이썬 설치가 필요 없는 단일 실행 파일로 빌드됩니다. 프로젝트는 스스로 찾습니다 — 자기 위치에서 위로 올라가며 `App`, `Core`, `Launcher`가 함께 있는 곳까지 갑니다.

<p align="center"><img src="../assets/launcher.png" alt="C2UI 런처" width="562"><br><sub>런처 창: “Dev-mode” 제목, 설명 줄, 버튼 세 개.</sub></p>

> [!NOTE]
> **런처의 화면은 현재 러시아어로만 되어 있습니다 — 임시 조치입니다.** 제목, 설명, 버튼 문구는 코드에 박혀 있으며, 번역은 완성된 App에 맞춰 런처를 다시 작성할 때 에디터 현지화(`Tools/Localization`)와 함께 들어갑니다. 프로젝트의 나머지 문서는 이미 32개 언어로 제공됩니다.

## 세 개의 버튼

| | |
|---|---|
| <code>Запустить Core</code> | 에디터를 시작합니다 — 뷰포트, 타임라인, 패널이 있는 C2UI 창. |
| <code>Запустить App</code> | 비활성: 별도의 App은 아직 없습니다. |
| <code>Выйти</code> | 런처를 닫습니다. |

## 소스에서 실행

Windows, Python 3.13, 설치된 Source Filmmaker가 필요합니다.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

단일 파일 `Launcher/Launcher-C2UI.exe` 빌드(깃에는 두지 않고 소스에서 다시 빌드):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## 에디터 없는 엔진

`Launcher/core.py`는 `Core`만 시작합니다. 설치를 마운트하고 색인을 만들며 엔진 위에 작은 셸을 제공합니다 — 모델, 재질, 텍스처, 맵, 세션과 그 평가. 이것도 임시입니다. App이 창 없이 실행되면 에디터가 유일한 진입점이 됩니다.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## 앞으로 달라질 것

- App이 생기면 창을 다시 작성합니다 — 디자인과 번역까지.
- “Запустить App” 버튼이 동작하기 시작합니다.
- 에디터를 창 없이 시작할 수 있게 되면 `core.py`는 사라집니다.
- 빌드된 `.exe`가 GitHub 릴리스에 첨부됩니다.

<p align="center"><a href="../README/KO-kr.md"><img alt="← README로 돌아가기" src="https://img.shields.io/badge/%E2%86%90_README%EB%A1%9C_%EB%8F%8C%EC%95%84%EA%B0%80%EA%B8%B0-1b2838?style=for-the-badge"></a></p>
