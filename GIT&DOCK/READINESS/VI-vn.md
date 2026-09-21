# Mức sẵn sàng của C2UI — chi tiết

<details align="center"><summary>&nbsp;🌐 <b>🇻🇳 Tiếng Việt</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><b>🇻🇳<br>Tiếng Việt</b></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/VI-vn.svg" alt="Mức sẵn sàng" width="100%"></p>

<p align="center"><img alt="51%" src="https://img.shields.io/badge/51%25-e0a800?style=flat-square"> <b>Mức sẵn sàng phát hành tổng thể: 51%</b></p>

Mỗi mảng có thể mở ra: cái gì đã chạy và cái gì chưa có. Phần trăm là ước lượng so với khả năng của SFM.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Tìm và gắn kết SFM

Registry Steam → `libraryfolders.vdf` → đường dẫn tìm kiếm của `gameinfo.txt`, theo đúng thứ tự engine. Sáu điểm gắn kết trên bản cài chuẩn. Không ghi gì ngoài thư mục ứng dụng.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Chỉ mục nội dung

70 199 tập tin trong 1,1 s lạnh / 0,02 s từ cache; ghi đè giữa các điểm gắn kết được giải quyết đúng như engine.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Mô hình — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Phiên bản 44, 48, 49. Bộ xương, lưới, mọi mức chi tiết, nhóm thân. 1 500 mô hình đã tải, 0 lỗi.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Vật liệu — <code>.vmt</code>

Toàn bộ 19 554 vật liệu kèm theo đều đọc được; `patch`, khối DX, proxy.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Kết cấu — <code>.vtf</code>

Phiên bản 7.0–7.5, DXT1/3/5 và mọi định dạng không nén, cubemap, mip. DXT lên GPU không cần giải mã.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Phiên — <code>.dmx</code>

Nhị phân 1–5 và KeyValues2. Mọi phiên và tập tin hạt trong bản cài ghi lại **từng byte** giống hệt.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Phiên trên màn hình

Cảnh và rãnh âm thanh trên dòng thời gian, cây phần tử, khung cảnh mỗi cảnh qua camera của nó. Chưa có: bản đồ, hạt, âm thanh.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Hoạt ảnh

Kênh và log được tính tại con trỏ; kéo và phát. Xương, camera và hiển thị theo phiên.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Khuôn mặt

Bộ điều khiển flex, quy tắc biên dịch và hoạt ảnh đỉnh — nhân vật nói và biểu cảm. Chưa có: bản đồ nếp nhăn.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rig

Biểu thức, ràng buộc point/orient/parent/aim, IK hai xương. Chưa có: đồ thị phụ thuộc toán tử đầy đủ, tạo rig.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Chỉnh sửa

Nhấp để chọn, bộ thao tác di chuyển/xoay, trình kiểm tra mọi thuộc tính, khóa tại con trỏ, hoàn tác/làm lại, lưu chính xác từng byte.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Chọn thời gian với hold và falloff trên thước; chỉnh sửa lan ra như trong SFM. Chưa có: preset, lớp.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Trình biên tập đồ thị

Đường cong của mọi log điều khiển phần tử được chọn: X/Y/Z, pitch/yaw/roll, vô hướng. Khóa kéo theo thời gian và giá trị với xem trước trực tiếp, nhấp đúp chèn, Delete xóa; trục thời gian là của dòng thời gian. Chưa có: tiếp tuyến và kiểu đường cong, co giãn nhóm khóa.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Gắn bảng

Kéo bảng lên la bàn mục tiêu có xem trước, như UE5 và Visual Studio. Chưa có: bố cục đã lưu, chủ đề.

### <img alt="65%" src="https://img.shields.io/badge/65%25-e0a800?style=flat-square"> Tô bóng Source

Đèn của phiên (DmeProjectedLight): khung nhìn, suy giảm kiểu Source, mờ dần tới maxDistance; half-lambert, $lightwarptexture, phong ($phongexponent/boost/fresnelranges), $rimlight, $selfillum. Thế giới bản đồ theo lightmap. Chưa có: bóng đổ, kết cấu gobo, $bumpmap, $envmap, khối ambient, skybox.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Bản đồ — <code>.bsp</code>

Phiên bản 19–21: hình học thế giới, địa hình displacement, thực thể brush, prop tĩnh, vật liệu pak riêng của bản đồ. Loại bỏ ngoài khung nhìn. Chưa có: lightmap, skybox, nước, prop_dynamic.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Kết xuất ảnh và video

Chưa bắt đầu.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Plugin <code>.c2plg</code>

Chưa bắt đầu.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Chủ đề và không gian làm việc

Cố ý để sau: một giao diện cho đến khi trình biên tập có gì đáng trang trí.

**Chưa sẵn sàng phát hành.** Nền tảng — mọi định dạng tập tin SFM dùng, đọc đúng và kiểm chứng trên toàn bản cài — đã có và được kiểm thử; có thể mở, phát, sửa và lưu một phiên. Thiếu là *sự thoải mái* khi làm việc: trình biên tập đồ thị, tô bóng Source, bản đồ, xuất. Không có số phiên bản cho đến khi một nhà hoạt hình làm được một ngày việc trong đó.

<p align="center"><a href="../README/VI-vn.md"><img alt="← Quay lại README" src="https://img.shields.io/badge/%E2%86%90_Quay_l%E1%BA%A1i_README-1b2838?style=for-the-badge"></a></p>
