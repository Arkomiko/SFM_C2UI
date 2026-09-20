<p align="center"><img src="../assets/TR-tr/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <b>🇹🇷 Türkçe</b> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/durum-%C3%B6n--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/test-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — modern bir kabuk içinde Source Filmmaker düzenleyicisi: aynı içerik, aynı oturum biçimi, aynı veri modeli, Steam kitaplığı ve Unreal Engine 5 düzenleyicisi ruhunda bir arayüz.</p>

---

## Hazırlık

<p align="center"><img src="../assets/TR-tr/sidebar.svg" alt="Hazırlık" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Yayın için genel hazırlık: 41%</b></p>

<p align="center"><a href="../assets/TR-tr/sidebar.md"><img alt="Hazırlık ayrıntılı" src="https://img.shields.io/badge/Haz%C4%B1rl%C4%B1k_ayr%C4%B1nt%C4%B1l%C4%B1-66c0f4?style=for-the-badge"></a></p>

## Fikir

Source Filmmaker, arayüzü 2012'de kalmış güçlü bir araçtır. C2UI onun yerini almaz ve onu yeniden yapmaz: amaç yalnızca SFM'yi biraz daha modern ve rahat hale getirmektir.

Düzenleyici kurulu SFM'yi bulur, onu bir içerik kitaplığı olarak bağlar — modeller, malzemeler, dokular, oturumlar — ve aynı dosyalarla aynı biçimde çalışır. SFM'de yapılan her şey C2UI'de açılır, tersi de geçerlidir.

İlk hedef, kemikler ve rig'ler dahil SFM ile tam uyumluluktur. Sonrası, SFM'de eksik olanlar.

```
  ┌──────────────┐    "SFM nerede?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  kendi UI    │ ◀─────   bağlı   ───────│    tf/  hl2/  tf_movies/ …   │
  │  kendi render │      salt okunur      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Meet the Heavy açık düzenleyici" width="100%"><br><sub>Bugünkü düzenleyici, Valve'ın Meet the Heavy'si açık: zaman çizelgesinde çekimler ve ses, oturum ağacı, ilk çekim kendi kamerasından, oturumun dediği gibi pozlanmış ve yüz ifadeli karakterler.</sub></p>

## Onu farklı kılan

- **Taşınabilir.** Uygulama klasörü dışına hiçbir şey yazılmaz: ayarlar `App/User`, önbellek `App/Cache`, geçici `App/Temporary`. Klasörü silin, iz kalmaz.
- **SFM'yi hiç çalıştırmaz.** Yönetilecek süreç yok, ele geçirilecek pencere yok. Kurulum bir içerik paketi gibi okunur.
- **Biçimler doğrulanmış, varsayılmamış.** Her okuyucu gerçek kurulumla karşılaştırıldı; bir biçim şaşırtıcı bir şey yapıyorsa kod bunu söyler.
- **Kayıt tamdır.** Değiştirilmeden okunup yazılan oturum aynı dosyadır.
- **Motorun bağımlılığı yok.** `Core/` ve tüm test paketi çıplak Python'da çalışır; yalnızca pencere Qt ve OpenGL ister.

## Çalıştırma

Windows, Python 3.13 ve bir Source Filmmaker kurulumu gerekir.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

İlk açılışta SFM Steam üzerinden aranır; bulunamazsa program sorar. <kbd>Ctrl</kbd>+<kbd>O</kbd> oturum açar, <kbd>Space</kbd> oynatır, <kbd>C</kbd> çekim kamerasından bakar, <kbd>T</kbd>/<kbd>R</kbd> taşı/döndür, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> geri alır, <kbd>Ctrl</kbd>+<kbd>S</kbd> kaydeder. Paneller başlıklarından sürüklenir. Testler hiçbir şey gerektirmez:

```bash
python Testing/run.py
```

## Yapı

```
C2UI_SDK/
├── README.md
├── Core/              motor: biçimler, sanal dosya sistemi, dizin, köprüler
├── App/               düzenleyici: içerik kitaplığı, renderer, pencere
├── Tools/             yerelleştirme, UI araçları, eklentiler (sonra)
│   └── Launcher/      başlatıcı
├── Testing/           testler, bayt düzeyinde fixture'lar, tek runner
└── GIT&DOCK/          bu README diğer dillerde
```

## Yol haritası

1. **Source gölgelendirme** — SFM'nin çizdiği gibi VertexLitGeneric: phong, rim, lightwarp, sahne ışıkları.
2. **Haritalar** — arka plan için `.bsp`.
3. **Çıktı** — görüntü ve video dışa aktarma.
4. **Eklentiler** — `.c2plg` biçimi; sonra temalar ve çalışma alanları.

## Lisans ve teşekkür

C2UI'nin kendi kodu **C2UI lisansı** altındadır: kişisel ve ticari olmayan kullanım serbest; ticari kullanım yalnızca yazarın yazılı onayıyla; değiştirilmiş sürümler özgün projeyi ve yazarı Arkomiko'yu belirtmelidir. Eklentiler ve ek paketler **C2UI — Plugins & Addons (C2UI‑Pl&AD)** lisansı altındadır.

Source Filmmaker, Team Fortress 2 ve Source motoru Valve'a aittir; proje onların biçimlerini okur, hiçbir dosyalarını içermez ve yalnızca Steam'deki kendi SFM kopyanızla çalışır.

<p align="center"><a href="../LICENSE/TR-tr.md"><img alt="Lisans metni" src="https://img.shields.io/badge/Lisans_metni-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="Kurulumdan doğrudan render edilen 64 model" width="60%"><br><sub>Kurulumdan rastgele seçilen altmış dört model, C2UI'nin kendi renderer'ı ile çizildi.</sub></p>
