<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <b>🇻🇳 Tiếng Việt</b> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/tr%E1%BA%A1ng_th%C3%A1i-ti%E1%BB%81n--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/ki%E1%BB%83m_th%E1%BB%AD-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — là bản dựng lại trình biên tập Source Filmmaker của tôi: cùng nội dung, cùng định dạng phiên, cùng mô hình dữ liệu — trong một lớp vỏ mượn giao diện từ thư viện Steam và bố cục từ trình biên tập Unreal Engine 5.</p>

---

## Ý tưởng

Source Filmmaker là một công cụ tuyệt vời khoác giao diện năm 2012. Tôi không muốn một lớp da phủ lên `sfm.exe`, cũng không muốn chiếm từng cửa sổ của nó. Tôi muốn một trình biên tập **hỏi SFM được cài ở đâu**, gắn kết bản cài đó như Garry's Mod gắn kết Counter-Strike, và tự làm mọi thứ trên những tập tin đó — mô hình, vật liệu, kết cấu, phiên, hoạt ảnh — mà không bao giờ khởi chạy SFM.

Mục tiêu là **tương đương tính năng với SFM, một đối một** (kể cả xương và rig), rồi đến những gì SFM chưa từng có.

```
  ┌──────────────┐    "SFM ở đâu?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI riêng    │ ◀─────  gắn kết  ───────│    tf/  hl2/  tf_movies/ …   │
  │  render riêng │        chỉ đọc        │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Mức sẵn sàng

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Mức sẵn sàng phát hành tổng thể: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Trình biên tập đang mở Meet the Heavy" width="100%"><br><sub>Trình biên tập hôm nay, mở Meet the Heavy của Valve: các cảnh và âm thanh trên dòng thời gian, cây phiên, cảnh đầu nhìn qua camera riêng của nó, nhân vật tạo dáng và biểu cảm đúng như phiên.</sub></p>

Mở một mảng để xem chính xác cái gì đã xong và cái gì chưa. Phần trăm là ước lượng trung thực của tôi so với những gì SFM làm được.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Tìm và gắn kết SFM</b></summary>

Registry Steam → `libraryfolders.vdf` → đường dẫn tìm kiếm của `gameinfo.txt`, theo đúng thứ tự engine. Sáu điểm gắn kết trên bản cài chuẩn. Không ghi gì ngoài thư mục ứng dụng.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Chỉ mục nội dung</b></summary>

70 199 tập tin trong 1,1 s lạnh / 0,02 s từ cache; ghi đè giữa các điểm gắn kết được giải quyết đúng như engine.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Mô hình — `.mdl` `.vvd` `.vtx`</b></summary>

Phiên bản 44, 48, 49. Bộ xương, lưới, mọi mức chi tiết, nhóm thân. 1 500 mô hình đã tải, 0 lỗi.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Vật liệu — `.vmt`</b></summary>

Toàn bộ 19 554 vật liệu kèm theo đều đọc được; `patch`, khối DX, proxy.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Kết cấu — `.vtf`</b></summary>

Phiên bản 7.0–7.5, DXT1/3/5 và mọi định dạng không nén, cubemap, mip. DXT lên GPU không cần giải mã.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Phiên — `.dmx`</b></summary>

Nhị phân 1–5 và KeyValues2. Mọi phiên và tập tin hạt trong bản cài ghi lại **từng byte** giống hệt.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Phiên trên màn hình</b></summary>

Cảnh và rãnh âm thanh trên dòng thời gian, cây phần tử, khung cảnh mỗi cảnh qua camera của nó. Chưa có: bản đồ, hạt, âm thanh.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Hoạt ảnh</b></summary>

Kênh và log được tính tại con trỏ; kéo và phát. Xương, camera và hiển thị theo phiên.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Khuôn mặt</b></summary>

Bộ điều khiển flex, quy tắc biên dịch và hoạt ảnh đỉnh — nhân vật nói và biểu cảm. Chưa có: bản đồ nếp nhăn.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Rig</b></summary>

Biểu thức, ràng buộc point/orient/parent/aim, IK hai xương. Chưa có: đồ thị phụ thuộc toán tử đầy đủ, tạo rig.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Chỉnh sửa</b></summary>

Nhấp để chọn, bộ thao tác di chuyển/xoay, trình kiểm tra mọi thuộc tính, khóa tại con trỏ, hoàn tác/làm lại, lưu chính xác từng byte. Chưa có: trình biên tập đồ thị.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Chọn thời gian với hold và falloff trên thước; chỉnh sửa lan ra như trong SFM. Chưa có: preset, lớp.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Gắn bảng</b></summary>

Kéo bảng lên la bàn mục tiêu có xem trước, như UE5 và Visual Studio. Chưa có: bố cục đã lưu, chủ đề.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Tô bóng Source</b></summary>

Chỉ kết cấu và ánh sáng đơn giản. Chưa có: phong, rim, lightwarp, đèn cảnh, bóng.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Bản đồ — `.bsp`</b></summary>

Chưa bắt đầu.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Kết xuất ảnh và video</b></summary>

Chưa bắt đầu.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Plugin `.c2plg`</b></summary>

Chưa bắt đầu.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Chủ đề và không gian làm việc</b></summary>

Cố ý để sau: một giao diện cho đến khi trình biên tập có gì đáng trang trí.

</details>

**Chưa sẵn sàng phát hành.** Nền tảng — mọi định dạng tập tin SFM dùng, đọc đúng và kiểm chứng trên toàn bản cài — đã có và được kiểm thử; có thể mở, phát, sửa và lưu một phiên. Thiếu là *sự thoải mái* khi làm việc: trình biên tập đồ thị, tô bóng Source, bản đồ, xuất. Không có số phiên bản cho đến khi một nhà hoạt hình làm được một ngày việc trong đó.

## Điểm khác biệt

- **Di động.** Không ghi gì ngoài thư mục ứng dụng: thiết lập trong `App/User`, cache trong `App/Cache`, tạm trong `App/Temporary`. Xóa thư mục là hết dấu vết.
- **Không bao giờ chạy SFM.** Không tiến trình để điều khiển, không cửa sổ để chiếm. Bản cài được đọc như một gói nội dung.
- **Định dạng được kiểm chứng, không giả định.** Mọi trình đọc được đối chiếu với bản cài thật; nơi định dạng làm điều bất ngờ, mã nói rõ.
- **Lưu chính xác.** Phiên đọc rồi ghi không đổi là cùng một tập tin.
- **Engine không phụ thuộc.** `Core/` và toàn bộ kiểm thử chạy trên Python thuần; chỉ cửa sổ cần Qt và OpenGL.

## Chạy

Cần Windows, Python 3.13 và một bản cài Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Lần đầu chạy sẽ tìm SFM qua Steam; không thấy thì hỏi. <kbd>Ctrl</kbd>+<kbd>O</kbd> mở phiên, <kbd>Space</kbd> phát, <kbd>C</kbd> camera cảnh, <kbd>T</kbd>/<kbd>R</kbd> di chuyển/xoay, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> hoàn tác, <kbd>Ctrl</kbd>+<kbd>S</kbd> lưu. Bảng kéo bằng tiêu đề. Kiểm thử không cần gì:

```bash
python Testing/run.py
```

## Cấu trúc

```
C2UI_SDK/
├── c2ui.py            trình khởi chạy
├── Core/              engine: định dạng, hệ tập tin ảo, chỉ mục, cầu nối
├── App/               trình biên tập: thư viện nội dung, renderer, cửa sổ
├── Tools/             bản địa hóa, công cụ UI, plugin (sau)
├── Testing/           kiểm thử, fixture chính xác từng byte, một runner
└── GIT&DOCK/README/   README này bằng ngôn ngữ khác
```

## Lộ trình

1. **Trình biên tập đồ thị** — đường cong và khóa, nhìn thấy được.
2. **Tô bóng Source** — VertexLitGeneric như SFM vẽ: phong, rim, lightwarp, đèn cảnh.
3. **Bản đồ** — `.bsp` làm nền.
4. **Đầu ra** — xuất ảnh và video.
5. **Plugin** — định dạng `.c2plg`; rồi chủ đề và không gian làm việc.

## Giấy phép và ghi công

Source Filmmaker, Team Fortress 2 và engine Source thuộc Valve. Dự án này đọc định dạng tập tin của họ, không kèm tập tin nào của họ, và chỉ hoạt động với bản SFM bạn đã có qua Steam.

Giấy phép cho mã riêng của C2UI chưa được chọn — cho đến lúc đó, bảo lưu mọi quyền. Vẫn hoan nghênh issue và pull request.

<p align="center"><img src="../../.github/assets/models.png" alt="64 mô hình kết xuất trực tiếp từ bản cài" width="60%"><br><sub>Sáu mươi bốn mô hình chọn ngẫu nhiên từ bản cài, vẽ bằng renderer riêng của C2UI.</sub></p>
