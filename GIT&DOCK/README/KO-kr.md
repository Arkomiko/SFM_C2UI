<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <b>🇰🇷 한국어</b> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%EC%83%81%ED%83%9C-%ED%94%84%EB%A6%AC--%EC%95%8C%ED%8C%8C-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%ED%85%8C%EC%8A%A4%ED%8A%B8-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — 는 Source Filmmaker 편집기를 제가 다시 만든 것입니다. 같은 콘텐츠, 같은 세션 형식, 같은 데이터 모델을 Steam 라이브러리의 외관과 Unreal Engine 5 편집기의 레이아웃을 빌린 셸 안에 담았습니다.</p>

---

## 아이디어

Source Filmmaker는 2012년 인터페이스를 입은 훌륭한 도구입니다. `sfm.exe` 위에 스킨을 씌우고 싶지도, 창을 하나씩 가로채고 싶지도 않습니다. 원하는 것은 **SFM이 어디에 설치되어 있는지 묻고**, Garry's Mod가 Counter-Strike를 마운트하듯 그 설치를 마운트하고, 그 파일들 위에서 모델·머티리얼·텍스처·세션·애니메이션을 모두 스스로 처리하면서 SFM을 한 번도 실행하지 않는 편집기입니다.

목표는 **SFM과 일대일 기능 동등성**(본과 리그 포함), 그다음은 SFM이 결코 갖지 못했던 것들입니다.

```
  ┌──────────────┐    "SFM은 어디?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  자체 UI     │ ◀─────  마운트   ───────│    tf/  hl2/  tf_movies/ …   │
  │  자체 렌더   │       읽기 전용       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## 완성도

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>릴리스 전체 준비도: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy를 연 편집기" width="100%"><br><sub>오늘의 편집기, Valve의 Meet the Heavy를 연 모습: 타임라인의 샷과 사운드, 세션 트리, 자체 카메라로 본 첫 샷, 세션대로 포즈와 표정을 취한 캐릭터.</sub></p>

영역을 펼치면 정확히 무엇이 되었고 무엇이 안 되었는지 볼 수 있습니다. 백분율은 SFM이 할 수 있는 것에 대한 저의 정직한 추정입니다.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM 찾기와 마운트</b></summary>

Steam 레지스트리 → `libraryfolders.vdf` → `gameinfo.txt`의 검색 경로를 엔진 순서대로. 기본 설치에서 6개 마운트. 애플리케이션 폴더 밖에는 아무것도 쓰지 않습니다.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>콘텐츠 인덱스</b></summary>

70 199개 파일을 콜드 1.1초 / 캐시 0.02초에; 마운트 간 재정의는 엔진과 똑같이 해결.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>모델 — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

버전 44, 48, 49. 스켈레톤, 메시, 모든 LOD, 바디 그룹. 1 500개 모델 로드, 실패 0.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>머티리얼 — <code>.vmt</code></b></summary>

포함된 19 554개 머티리얼 전부 파싱; `patch`, DX 블록, 프록시.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>텍스처 — <code>.vtf</code></b></summary>

버전 7.0–7.5, DXT1/3/5와 모든 비압축 형식, 큐브맵, 밉. DXT는 디코딩 없이 GPU로.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>세션 — <code>.dmx</code></b></summary>

바이너리 1–5와 KeyValues2. 설치의 모든 세션과 파티클 파일이 **바이트 단위로 동일하게** 다시 기록됩니다.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>화면 위의 세션</b></summary>

타임라인의 샷과 사운드 트랙, 요소 트리, 각 샷의 장면을 그 카메라로. 아직 없음: 맵, 파티클, 사운드.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>애니메이션</b></summary>

채널과 로그를 커서에서 평가; 스크럽과 재생. 본, 카메라, 가시성이 세션을 따릅니다.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>얼굴</b></summary>

Flex 컨트롤러, 컴파일된 규칙, 정점 애니메이션 — 캐릭터가 말하고 표정을 짓습니다. 아직 없음: 주름 맵.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>리그</b></summary>

표현식, point/orient/parent/aim 제약, 2본 IK. 아직 없음: 전체 연산자 의존 그래프, 리그 생성.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>편집</b></summary>

클릭 선택, 이동/회전 매니퓰레이터, 모든 속성의 인스펙터, 커서 위치 키, 실행 취소/다시 실행, 바이트 정확 저장. 아직 없음: 그래프 편집기.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>모션 편집기</b></summary>

룰러의 홀드·폴오프 시간 선택; 편집이 SFM처럼 선택 범위로 퍼집니다. 아직 없음: 프리셋, 레이어.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>패널 도킹</b></summary>

UE5와 Visual Studio처럼 미리보기가 있는 대상 컴퍼스로 패널을 끌어다 놓기. 아직 없음: 저장된 레이아웃, 테마.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source 셰이딩</b></summary>

텍스처와 단순 조명만. 아직 없음: phong, rim, lightwarp, 씬 라이트, 그림자.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>맵 — <code>.bsp</code></b></summary>

시작 안 함.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>이미지·비디오 렌더</b></summary>

시작 안 함.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>플러그인 <code>.c2plg</code></b></summary>

시작 안 함.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>테마와 워크스페이스</b></summary>

의도적으로 나중에: 편집기에 꾸밀 가치가 있는 것이 생길 때까지 하나의 외관.

</details>

**릴리스 준비가 되지 않았습니다.** 기반 — SFM이 쓰는 모든 파일 형식을 올바르게 읽고 설치 전체에서 검증한 것 — 은 갖춰져 있고 테스트되었습니다. 세션을 열고, 재생하고, 수정하고, 저장할 수 있습니다. 부족한 것은 작업의 *편안함*: 그래프 편집기, Source 셰이딩, 맵, 내보내기. 애니메이터가 하루 일을 해낼 수 있을 때까지 버전 번호는 없습니다.

## 무엇이 다른가

- **포터블.** 애플리케이션 폴더 밖에는 아무것도 쓰지 않습니다: 설정은 `App/User`, 캐시는 `App/Cache`, 임시는 `App/Temporary`. 폴더를 지우면 흔적이 없습니다.
- **SFM을 절대 실행하지 않음.** 조종할 프로세스도, 가로챌 창도 없습니다. 설치는 콘텐츠 팩처럼 읽힙니다.
- **형식은 검증됨, 가정 아님.** 모든 리더를 실제 설치와 대조했습니다. 형식이 의외의 동작을 하는 곳은 코드가 그렇게 말합니다.
- **저장은 정확함.** 변경 없이 읽고 쓴 세션은 같은 파일입니다.
- **엔진에 의존성 없음.** `Core/`와 전체 테스트는 순수 Python에서 돌아갑니다. 창만 Qt와 OpenGL이 필요합니다.

## 실행

Windows, Python 3.13, Source Filmmaker 설치가 필요합니다.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

첫 실행 시 Steam을 통해 SFM을 찾습니다. 못 찾으면 묻습니다. <kbd>Ctrl</kbd>+<kbd>O</kbd> 세션 열기, <kbd>Space</kbd> 재생, <kbd>C</kbd> 샷 카메라, <kbd>T</kbd>/<kbd>R</kbd> 이동/회전, <kbd>M</kbd> 모션 편집기, <kbd>Ctrl</kbd>+<kbd>Z</kbd> 실행 취소, <kbd>Ctrl</kbd>+<kbd>S</kbd> 저장. 패널은 제목을 잡아 끕니다. 테스트에는 아무것도 필요 없습니다:

```bash
python Testing/run.py
```

## 구조

```
C2UI_SDK/
├── c2ui.py            런처
├── Core/              엔진: 형식, 가상 파일 시스템, 인덱스, 브리지
├── App/               편집기: 콘텐츠 라이브러리, 렌더러, 창
├── Tools/             현지화, UI 도구, 플러그인 (나중에)
├── Testing/           테스트, 바이트 정확 픽스처, 단일 러너
└── GIT&DOCK/README/   이 README의 다른 언어 버전
```

## 로드맵

1. **그래프 편집기** — 커브와 키를 눈으로.
2. **Source 셰이딩** — SFM이 그리는 VertexLitGeneric: phong, rim, lightwarp, 씬 라이트.
3. **맵** — 배경용 `.bsp`.
4. **출력** — 이미지와 비디오 내보내기.
5. **플러그인** — `.c2plg` 형식; 그다음 테마와 워크스페이스.

## 라이선스와 크레딧

Source Filmmaker, Team Fortress 2, Source 엔진은 Valve의 것입니다. 이 프로젝트는 그 파일 형식을 읽기만 하고, 그 파일을 전혀 포함하지 않으며, Steam으로 이미 보유한 SFM 사본과만 작동합니다.

C2UI 자체 코드의 라이선스는 아직 정하지 않았습니다 — 그때까지 모든 권리 보유. 이슈와 풀 리퀘스트는 환영합니다.

<p align="center"><img src="../../.github/assets/models.png" alt="설치에서 바로 렌더링한 64개 모델" width="60%"><br><sub>설치에서 무작위로 고른 64개 모델을 C2UI 자체 렌더러로 그린 것.</sub></p>
