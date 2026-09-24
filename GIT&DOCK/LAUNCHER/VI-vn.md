# Trình khởi chạy C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇻🇳 Tiếng Việt</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><b>🇻🇳<br>Tiếng Việt</b></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` là nơi dự án được khởi chạy: một cửa sổ tối nhỏ với tiêu đề, một dòng mô tả và ba nút. Nó được đóng gói thành một tệp thực thi duy nhất không cần cài Python, và tự tìm ra dự án — đi ngược lên từ vị trí của mình cho đến khi thấy `App`, `Core` và `Launcher` cùng nhau.

<p align="center"><img src="../assets/launcher.png" alt="Trình khởi chạy C2UI" width="562"><br><sub>Cửa sổ trình khởi chạy: tiêu đề «Dev-mode», dòng mô tả và ba nút.</sub></p>

> [!NOTE]
> **Giao diện trình khởi chạy hiện chỉ có tiếng Nga — đây là giải pháp tạm thời.** Tiêu đề, mô tả và chữ trên nút được ghi thẳng trong mã; bản dịch sẽ đến cùng việc bản địa hóa trình biên tập (`Tools/Localization`), khi trình khởi chạy được viết lại cho một App hoàn chỉnh. Phần còn lại của tài liệu dự án đã có bằng 32 ngôn ngữ.

## Ba nút

| | |
|---|---|
| <code>Запустить Core</code> | Khởi động trình biên tập — cửa sổ C2UI với khung nhìn, dòng thời gian và các bảng. |
| <code>Запустить App</code> | Bị làm mờ: chưa có App riêng. |
| <code>Выйти</code> | Đóng trình khởi chạy. |

## Chạy từ mã nguồn

Cần Windows, Python 3.13 và một bản cài Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Dựng tệp duy nhất `Launcher/Launcher-C2UI.exe` (không lưu trong git — được dựng lại từ mã nguồn):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Engine không có trình biên tập

`Launcher/core.py` khởi động riêng `Core`: gắn một bản cài, lập chỉ mục và cho một shell nhỏ trên engine — mô hình, vật liệu, texture, bản đồ, phiên và việc tính toán chúng. Cũng là tạm thời: khi App chạy được không cần cửa sổ, trình biên tập sẽ là lối vào duy nhất.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Sau này sẽ thay đổi gì

- Cửa sổ được viết lại khi có App — cùng diện mạo và bản dịch.
- Nút «Запустить App» bắt đầu hoạt động.
- `core.py` biến mất khi trình biên tập khởi động được không cần cửa sổ.
- Tệp `.exe` đã dựng sẽ đi kèm các bản phát hành trên GitHub.

<p align="center"><a href="../README/VI-vn.md"><img alt="← Quay lại README" src="https://img.shields.io/badge/%E2%86%90_Quay_l%E1%BA%A1i_README-1b2838?style=for-the-badge"></a></p>
