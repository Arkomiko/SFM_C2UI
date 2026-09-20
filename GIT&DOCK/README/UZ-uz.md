<p align="center"><img src="../assets/UZ-uz/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <b>🇺🇿 Oʻzbekcha</b> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/holat-pre--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/test-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — zamonaviy qobiqdagi Source Filmmaker muharriri: xuddi shu kontent, xuddi shu sessiya formati, xuddi shu maʼlumotlar modeli, Steam kutubxonasi va Unreal Engine 5 muharriri ruhidagi interfeys.</p>

---

## Tayyorlik

<p align="center"><img src="../assets/UZ-uz/sidebar.svg" alt="Tayyorlik" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Relizga umumiy tayyorlik: 41%</b></p>

<p align="center"><a href="../assets/UZ-uz/sidebar.md"><img alt="Tayyorlik batafsil" src="https://img.shields.io/badge/Tayyorlik_batafsil-66c0f4?style=for-the-badge"></a></p>

## Gʻoya

Source Filmmaker — interfeysi 2012 yilda qolib ketgan kuchli vosita. C2UI uni almashtirmaydi va qayta yasamaydi: maqsad — SFM ni biroz zamonaviyroq va qulayroq qilish.

Muharrir oʻrnatilgan SFM ni topadi, uni kontent kutubxonasi sifatida ulaydi — modellar, materiallar, teksturalar, sessiyalar — va xuddi shu fayllar bilan xuddi shu formatda ishlaydi. SFM da qilingan hamma narsa C2UI da ochiladi, aksincha ham.

Birinchi maqsad — suyaklar va riglar bilan birga SFM bilan toʻliq moslik. Keyin — SFM da yetishmagan narsalar.

```
  ┌──────────────┐    "SFM qayerda?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  oʻz UI      │ ◀─────  ulangan  ───────│    tf/  hl2/  tf_movies/ …   │
  │  oʻz render  │      faqat oʻqish      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

<p align="center"><img src="../assets/editor.png" alt="Meet the Heavy ochilgan muharrir" width="100%"><br><sub>Bugungi muharrir, Valve ning Meet the Heavy sessiyasi ochiq: taymlaynda shotlar va ovoz, sessiya daraxti, birinchi shot oʻz kamerasi orqali, sessiyadagi holat va yuz ifodalari bilan personajlar.</sub></p>

## Nimasi bilan farq qiladi

- **Koʻchma.** Ilova papkasidan tashqarida hech narsa yozilmaydi: sozlamalar `App/User`, kesh `App/Cache`, vaqtinchalik `App/Temporary`. Papkani oʻchirsangiz — iz qolmaydi.
- **SFM ni hech qachon ishga tushirmaydi.** Boshqariladigan jarayon yoʻq, egallanadigan oynalar yoʻq. Oʻrnatma kontent paketi kabi oʻqiladi.
- **Formatlar tekshirilgan, taxmin qilinmagan.** Har bir oʻquvchi haqiqiy oʻrnatma bilan solishtirilgan; format kutilmagan narsa qilsa, kod bu haqda aytadi.
- **Saqlash aniq.** Oʻzgarishsiz oʻqilgan va yozilgan sessiya — xuddi shu fayl.
- **Dvigatelda bogʻliqliklar yoʻq.** `Core/` va barcha testlar sof Python da ishlaydi; Qt va OpenGL faqat oynaga kerak.

## Ishga tushirish

Windows, Python 3.13 va oʻrnatilgan Source Filmmaker kerak.

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Tools/Launcher/requirements.txt
.venv/Scripts/python.exe Tools/Launcher/c2ui.py
```

Birinchi ishga tushirishda SFM Steam orqali qidiriladi; topilmasa — dastur soʻraydi. <kbd>Ctrl</kbd>+<kbd>O</kbd> sessiyani ochadi, <kbd>Space</kbd> — ijro, <kbd>C</kbd> — shot kamerasi, <kbd>T</kbd>/<kbd>R</kbd> — koʻchirish/aylantirish, <kbd>M</kbd> — motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> — bekor qilish, <kbd>Ctrl</kbd>+<kbd>S</kbd> — saqlash. Panellar sarlavhasidan tortiladi. Testlarga hech narsa kerak emas:

```bash
python Testing/run.py
```

## Tuzilma

```
C2UI_SDK/
├── README.md
├── Core/              dvigatel: formatlar, virtual fayl tizimi, indeks, koʻpriklar
├── App/               muharrir: kontent kutubxonasi, renderer, oyna
├── Tools/             lokalizatsiya, UI vositalari, plaginlar (keyinroq)
│   └── Launcher/      ishga tushirgich
├── Testing/           testlar, baytgacha aniq fiksturalar, bitta runner
└── GIT&DOCK/          bu README boshqa tillarda
```

## Yoʻl xaritasi

1. **Source sheyding** — SFM chizganidek VertexLitGeneric: phong, rim, lightwarp, sahna yorugʻliklari.
2. **Xaritalar** — fon uchun `.bsp`.
3. **Eksport** — rasm va video.
4. **Plaginlar** — `.c2plg` formati; keyin mavzular va ish maydonlari.

## Litsenziya va minnatdorchilik

C2UI ning oʻz kodi **C2UI litsenziyasi** ostida: shaxsiy va notijorat maqsadlarda erkin; tijorat maqsadida faqat muallifning yozma roziligi bilan; oʻzgartirilgan versiyalar asl loyiha va uning muallifi Arkomiko ni koʻrsatishi shart. Plaginlar va addonlar **C2UI — Plugins & Addons (C2UI‑Pl&AD)** litsenziyasi ostida.

Source Filmmaker, Team Fortress 2 va Source dvigateli Valve ga tegishli; loyiha ularning formatlarini oʻqiydi, fayllarini oʻz ichiga olmaydi va faqat Steam dagi oʻz SFM nusxangiz bilan ishlaydi.

<p align="center"><a href="../LICENSE/UZ-uz.md"><img alt="Litsenziya matni" src="https://img.shields.io/badge/Litsenziya_matni-66c0f4?style=for-the-badge"></a></p>

<p align="center"><img src="../assets/models.png" alt="Oʻrnatmadan toʻgʻridan-toʻgʻri renderlangan 64 model" width="60%"><br><sub>Oʻrnatmadan tasodifiy tanlangan oltmish toʻrt model, C2UI ning oʻz rendereri bilan chizilgan.</sub></p>
