<p align="center"><img src="../assets/VI-vn/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <b>🇻🇳 Tiếng Việt</b> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/tr%E1%BA%A1ng_th%C3%A1i-ti%E1%BB%81n--alpha-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/ki%E1%BB%83m_th%E1%BB%AD-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — trình biên tập Source Filmmaker trong một lớp vỏ hiện đại: cùng nội dung, cùng định dạng phiên, cùng mô hình dữ liệu, giao diện theo tinh thần thư viện Steam và trình biên tập Unreal Engine 5.</p>

---

## Mức sẵn sàng

<p align="center"><img src="../assets/VI-vn/sidebar.svg" alt="Mức sẵn sàng" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Mức sẵn sàng phát hành tổng thể: 41%</b></p>

<p align="center"><a href="../assets/VI-vn/sidebar.md"><img alt="Mức sẵn sàng chi tiết" src="https://img.shields.io/badge/M%E1%BB%A9c_s%E1%BA%B5n_s%C3%A0ng_chi_ti%E1%BA%BFt-66c0f4?style=for-the-badge"></a></p>

## Ý tưởng

Source Filmmaker là một công cụ mạnh nhưng giao diện dừng lại ở năm 2012. C2UI không thay thế hay làm lại nó: mục tiêu chỉ là làm SFM hiện đại và thoải mái hơn một chút.

Trình biên tập tìm SFM đã cài, gắn nó như một thư viện nội dung — mô hình, vật liệu, kết cấu, phiên — và làm việc với cùng những tập tin đó ở cùng định dạng. Mọi thứ làm trong SFM đều mở được trong C2UI, và ngược lại.

Mục tiêu đầu tiên là tương thích hoàn toàn với SFM, kể cả xương và rig. Sau đó là những gì SFM còn thiếu.

```
  ┌──────────────┐    "SFM ở đâu?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI riêng    │ ◀─────  gắn kết  ───────│    tf/  hl2/  tf_movies/ …   │
  │  render riêng │        chỉ đọc        │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Trình biên tập đang mở Meet the Heavy" width="100%"><br><sub>Trình biên tập hôm nay, mở Meet the Heavy của Valve: các cảnh và âm thanh trên dòng thời gian, cây phiên, cảnh đầu nhìn qua camera riêng của nó, nhân vật tạo dáng và biểu cảm đúng như phiên.</sub></p>

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
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Lần đầu chạy sẽ tìm SFM qua Steam; không thấy thì hỏi. <kbd>Ctrl</kbd>+<kbd>O</kbd> mở phiên, <kbd>Space</kbd> phát, <kbd>C</kbd> camera cảnh, <kbd>T</kbd>/<kbd>R</kbd> di chuyển/xoay, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> hoàn tác, <kbd>Ctrl</kbd>+<kbd>S</kbd> lưu. Bảng kéo bằng tiêu đề. Kiểm thử không cần gì:

```bash
python Testing/run.py
```

## Cấu trúc

```
C2UI_SDK/
├── README.md
├── Core/              engine: định dạng, hệ tập tin ảo, chỉ mục, cầu nối
├── App/               trình biên tập: thư viện nội dung, renderer, cửa sổ
├── Tools/             bản địa hóa, công cụ UI, plugin (sau)
│   └── Launcher/      trình khởi chạy
├── Testing/           kiểm thử, fixture chính xác từng byte, một runner
└── GIT&DOCK/          README này bằng ngôn ngữ khác
```

## Lộ trình

1. **Tô bóng Source** — VertexLitGeneric như SFM vẽ: phong, rim, lightwarp, đèn cảnh.
2. **Bản đồ** — `.bsp` làm nền.
3. **Đầu ra** — xuất ảnh và video.
4. **Plugin** — định dạng `.c2plg`; rồi chủ đề và không gian làm việc.

## Giấy phép và ghi công

Mã riêng của C2UI theo **giấy phép C2UI**: tự do cho mục đích cá nhân và phi thương mại; sử dụng thương mại chỉ khi có sự đồng ý bằng văn bản của tác giả; các phiên bản sửa đổi phải ghi nhận dự án gốc và tác giả Arkomiko. Plugin và addon theo giấy phép **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 và engine Source thuộc Valve; dự án đọc định dạng của họ, không kèm tập tin nào của họ và chỉ hoạt động với bản SFM bạn có từ Steam.

<p align="center"><a href="../LICENSE/VI-vn.md"><img alt="Văn bản giấy phép" src="https://img.shields.io/badge/V%C4%83n_b%E1%BA%A3n_gi%E1%BA%A5y_ph%C3%A9p-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 mô hình kết xuất trực tiếp từ bản cài" width="60%"><br><sub>Sáu mươi bốn mô hình chọn ngẫu nhiên từ bản cài, vẽ bằng renderer riêng của C2UI.</sub></p>
