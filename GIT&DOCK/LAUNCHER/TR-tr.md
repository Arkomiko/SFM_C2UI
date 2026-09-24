# C2UI başlatıcısı

<details align="center"><summary>&nbsp;🌐 <b>🇹🇷 Türkçe</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><b>🇹🇷<br>Türkçe</b></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/`, projenin başlatıldığı yerdir: başlık, tek satır açıklama ve üç düğme içeren küçük koyu bir pencere. Kurulu Python gerektirmeyen tek bir çalıştırılabilir dosyaya derlenir ve projeyi kendisi bulur — bulunduğu yerden yukarı çıkar, `App`, `Core` ve `Launcher` bir aradayken durur.

<p align="center"><img src="../assets/launcher.png" alt="C2UI başlatıcısı" width="562"><br><sub>Başlatıcının penceresi: “Dev-mode” başlığı, açıklama satırı ve üç düğme.</sub></p>

> [!NOTE]
> **Başlatıcının arayüzü şimdilik yalnızca Rusça — geçici bir çözüm.** Başlık, açıklama ve düğme yazıları koda gömülüdür; çeviriler, başlatıcı tamamlanmış bir App için yeniden yazıldığında düzenleyicinin yerelleştirmesiyle (`Tools/Localization`) birlikte gelecek. Projenin geri kalan belgeleri şimdiden 32 dilde.

## Üç düğme

| | |
|---|---|
| <code>Запустить Core</code> | Düzenleyiciyi başlatır — görünümü, zaman çizelgesi ve panelleriyle C2UI penceresi. |
| <code>Запустить App</code> | Devre dışı: ayrı bir App henüz yok. |
| <code>Выйти</code> | Başlatıcıyı kapatır. |

## Kaynaktan çalıştırma

Windows, Python 3.13 ve kurulu bir Source Filmmaker gerekir.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Tek dosya `Launcher/Launcher-C2UI.exe` derlemesi (git'te tutulmaz — kaynaktan yeniden derlenir):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Düzenleyicisiz motor

`Launcher/core.py`, `Core`'u tek başına başlatır: bir kurulumu bağlar, dizinler ve motorun üzerinde küçük bir kabuk verir — modeller, malzemeler, dokular, haritalar, oturumlar ve bunların hesaplanması. O da geçici: App penceresiz çalışabildiğinde tek giriş noktası düzenleyici olur.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Sonra ne değişecek

- App ile birlikte pencere yeniden yazılacak — görünümü ve çevirileriyle.
- “Запустить App” düğmesi çalışmaya başlayacak.
- Düzenleyici penceresiz başlatılabildiğinde `core.py` gidecek.
- Derlenen `.exe`, GitHub sürümlerine eklenecek.

<p align="center"><a href="../README/TR-tr.md"><img alt="← README'ye dön" src="https://img.shields.io/badge/%E2%86%90_README%27ye_d%C3%B6n-1b2838?style=for-the-badge"></a></p>
