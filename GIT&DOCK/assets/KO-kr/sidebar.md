# C2UI 완성도 — 상세

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <b>🇰🇷 한국어</b> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="완성도" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>릴리스 전체 준비도: 41%</b></p>

각 영역을 펼치면 이미 동작하는 것과 아직 없는 것이 보입니다. 백분율은 SFM의 기능 대비 추정치입니다.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> SFM 찾기와 마운트

Steam 레지스트리 → `libraryfolders.vdf` → `gameinfo.txt`의 검색 경로를 엔진 순서대로. 기본 설치에서 6개 마운트. 애플리케이션 폴더 밖에는 아무것도 쓰지 않습니다.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 콘텐츠 인덱스

70 199개 파일을 콜드 1.1초 / 캐시 0.02초에; 마운트 간 재정의는 엔진과 똑같이 해결.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 모델 — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

버전 44, 48, 49. 스켈레톤, 메시, 모든 LOD, 바디 그룹. 1 500개 모델 로드, 실패 0.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 머티리얼 — <code>.vmt</code>

포함된 19 554개 머티리얼 전부 파싱; `patch`, DX 블록, 프록시.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 텍스처 — <code>.vtf</code>

버전 7.0–7.5, DXT1/3/5와 모든 비압축 형식, 큐브맵, 밉. DXT는 디코딩 없이 GPU로.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> 세션 — <code>.dmx</code>

바이너리 1–5와 KeyValues2. 설치의 모든 세션과 파티클 파일이 **바이트 단위로 동일하게** 다시 기록됩니다.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> 화면 위의 세션

타임라인의 샷과 사운드 트랙, 요소 트리, 각 샷의 장면을 그 카메라로. 아직 없음: 맵, 파티클, 사운드.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> 애니메이션

채널과 로그를 커서에서 평가; 스크럽과 재생. 본, 카메라, 가시성이 세션을 따릅니다.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> 얼굴

Flex 컨트롤러, 컴파일된 규칙, 정점 애니메이션 — 캐릭터가 말하고 표정을 짓습니다. 아직 없음: 주름 맵.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> 리그

표현식, point/orient/parent/aim 제약, 2본 IK. 아직 없음: 전체 연산자 의존 그래프, 리그 생성.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> 편집

클릭 선택, 이동/회전 매니퓰레이터, 모든 속성의 인스펙터, 커서 위치 키, 실행 취소/다시 실행, 바이트 정확 저장.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> 모션 편집기

룰러의 홀드·폴오프 시간 선택; 편집이 SFM처럼 선택 범위로 퍼집니다. 아직 없음: 프리셋, 레이어.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> 그래프 편집기

선택한 요소를 구동하는 모든 로그의 커브: X/Y/Z, pitch/yaw/roll, 스칼라. 키는 실시간 미리보기와 함께 시간·값으로 드래그, 더블클릭으로 삽입, Delete로 삭제; 시간 축은 타임라인과 공유. 아직 없음: 탄젠트와 커브 유형, 키 그룹 스케일링.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> 패널 도킹

UE5와 Visual Studio처럼 미리보기가 있는 대상 컴퍼스로 패널을 끌어다 놓기. 아직 없음: 저장된 레이아웃, 테마.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source 셰이딩

텍스처와 단순 조명만. 아직 없음: phong, rim, lightwarp, 씬 라이트, 그림자.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 맵 — <code>.bsp</code>

시작 안 함.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 이미지·비디오 렌더

시작 안 함.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 플러그인 <code>.c2plg</code>

시작 안 함.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> 테마와 워크스페이스

의도적으로 나중에: 편집기에 꾸밀 가치가 있는 것이 생길 때까지 하나의 외관.

**릴리스 준비가 되지 않았습니다.** 기반 — SFM이 쓰는 모든 파일 형식을 올바르게 읽고 설치 전체에서 검증한 것 — 은 갖춰져 있고 테스트되었습니다. 세션을 열고, 재생하고, 수정하고, 저장할 수 있습니다. 부족한 것은 작업의 *편안함*: 그래프 편집기, Source 셰이딩, 맵, 내보내기. 애니메이터가 하루 일을 해낼 수 있을 때까지 버전 번호는 없습니다.

<p align="center"><a href="../../README/KO-kr.md"><img alt="← README로 돌아가기" src="https://img.shields.io/badge/%E2%86%90_README%EB%A1%9C_%EB%8F%8C%EC%95%84%EA%B0%80%EA%B8%B0-1b2838?style=for-the-badge"></a></p>
