<p align="center"><img src="../assets/JV-id/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <b>🇮🇩 Basa Jawa</b> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pra--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/tes-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — editor Source Filmmaker ing cangkang modern: isi sing padha, format sesi sing padha, model data sing padha, antarmuka kanthi semangat pustaka Steam lan editor Unreal Engine 5.</p>

---

## Kesiapan

<p align="center"><img src="../assets/JV-id/sidebar.svg" alt="Kesiapan" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Kesiapan sakabèhé kanggo rilis: 41%</b></p>

<p align="center"><a href="../assets/JV-id/sidebar.md"><img alt="Kesiapan rinci" src="https://img.shields.io/badge/Kesiapan_rinci-66c0f4?style=for-the-badge"></a></p>

## Gagasan

Source Filmmaker iku piranti kuwat sing antarmukané kandheg ing taun 2012. C2UI ora ngganti lan ora mbangun ulang: tujuané mung nggawé SFM luwih modern lan luwih kepenak sithik.

Editor nemokake SFM sing wis dipasang, nyambungake minangka pustaka isi — model, materi, tekstur, sesi — lan nyambut gawe karo file sing padha ing format sing padha. Kabeh sing digawé ing SFM bisa dibukak ing C2UI, lan sewaliké.

Tujuan pisanan yaiku kompatibilitas lengkap karo SFM, kalebu balung lan rig. Sabanjuré, apa sing kurang ing SFM.

```
  ┌──────────────┐    "SFM ing endi?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  UI dhewe    │ ◀───── dipasang  ───────│    tf/  hl2/  tf_movies/ …   │
  │  render dhewe │       mung waca       │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Editor karo Meet the Heavy dibukak" width="100%"><br><sub>Editor saiki, karo Meet the Heavy saka Valve dibukak: shot lan swara ing garis wektu, wit sesi, shot pisanan liwat kamerané dhewe, karakter mapan lan raine kaya sing diomongake sesi.</sub></p>

## Apa bedané

- **Portabel.** Ora ana sing ditulis ing njaba folder aplikasi: setelan ing `App/User`, cache ing `App/Cache`, sauntara ing `App/Temporary`. Busak folderé lan ora ana tilas.
- **Ora tau mbukak SFM.** Ora ana proses sing dikendhaleni, ora ana jendhela sing direbut. Instalasi diwaca kaya paket isi.
- **Format diverifikasi, ora diandhakake.** Saben pamaca dipriksa karo instalasi nyata; yen format nindakake sing nggumunake, kodené ngomong.
- **Nyimpen presisi.** Sesi sing diwaca lan ditulis tanpa owah iku file sing padha.
- **Mesin ora duwe ketergantungan.** `Core/` lan kabeh tes mlaku ing Python murni; mung jendhela sing butuh Qt lan OpenGL.

## Mbukak

Mbutuhake Windows, Python 3.13 lan instalasi Source Filmmaker.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Nalika pisanan mbukak, SFM digoleki liwat Steam; yen ora ketemu, program takon. <kbd>Ctrl</kbd>+<kbd>O</kbd> mbukak sesi, <kbd>Space</kbd> muter, <kbd>C</kbd> kamera shot, <kbd>T</kbd>/<kbd>R</kbd> pindhah/puter, <kbd>M</kbd> motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> batal, <kbd>Ctrl</kbd>+<kbd>S</kbd> simpen. Panel diseret saka judhulé. Tes ora butuh apa-apa:

```bash
python Testing/run.py
```

## Struktur

```
C2UI_SDK/
├── README.md
├── Core/              mesin: format, sistem file virtual, indeks, jembatan
├── App/               editor: pustaka isi, renderer, jendhela
├── Tools/             lokalisasi, piranti UI, plugin (mengko)
│   └── Launcher/      peluncur
├── Testing/           tes, fixture presisi bait, siji runner
└── GIT&DOCK/          README iki ing basa liya
```

## Peta dalan

1. **Shading Source** — VertexLitGeneric kaya sing digambar SFM: phong, rim, lightwarp, cahya adegan.
2. **Peta** — `.bsp` kanggo latar.
3. **Output** — ekspor gambar lan video.
4. **Plugin** — format `.c2plg`; banjur tema lan ruang kerja.

## Lisensi lan panuwun

Kode dhewe C2UI ana ing **lisensi C2UI**: bebas kanggo panggunaan pribadi lan non-komersial; panggunaan komersial mung kanthi persetujuan tinulis saka penulis; versi sing diowahi kudu nyebutake proyek asli lan penulisé, Arkomiko. Plugin lan addon ana ing lisensi **C2UI — Plugins & Addons (C2UI‑Pl&AD)**.

Source Filmmaker, Team Fortress 2 lan mesin Source iku duweké Valve; proyek maca formaté, ora nyertakake file apa wae saka dheweke, lan mung bisa karo salinan SFM sampeyan dhewe saka Steam.

<p align="center"><a href="../LICENSE/JV-id.md"><img alt="Teks lisensi" src="https://img.shields.io/badge/Teks_lisensi-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="64 model dirender langsung saka instalasi" width="60%"><br><sub>Sewidak papat model dipilih acak saka instalasi, digambar dening renderer C2UI dhewe.</sub></p>
