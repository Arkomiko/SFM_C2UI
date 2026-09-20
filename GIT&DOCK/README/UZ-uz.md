<p align="center"><img src="../../.github/assets/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <a href="BN-bd.md">🇧🇩 বাংলা</a> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <b>🇺🇿 Oʻzbekcha</b> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/holat-pre--alfa-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/test-339-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — Source Filmmaker muharririning men tomonimdan qayta qurilgani: xuddi shu kontent, xuddi shu sessiya formati, xuddi shu maʼlumotlar modeli — koʻrinishini Steam kutubxonasidan, joylashuvini Unreal Engine 5 muharriridan olgan qobiq ichida.</p>

---

## Gʻoya

Source Filmmaker — 2012 yil interfeysidagi ajoyib vosita. Men `sfm.exe` ustiga skin qoplamoqchi emasman, uning oynalarini birma-bir egallab olmoqchi ham emasman. Menga **SFM qayerda oʻrnatilganini soʻraydigan**, oʻsha oʻrnatmani Garry's Mod Counter-Strike ni ulagandek ulaydigan va oʻsha fayllar ustida hamma narsani oʻzi qiladigan — modellar, materiallar, teksturalar, sessiyalar, animatsiya — SFM ni hech qachon ishga tushirmaydigan muharrir kerak.

Maqsad — **SFM bilan birga-bir funksional tenglik** (suyaklar va riglar bilan), keyin SFM da hech qachon boʻlmaganlar.

```
  ┌──────────────┐    "SFM qayerda?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  oʻz UI      │ ◀─────  ulangan  ───────│    tf/  hl2/  tf_movies/ …   │
  │  oʻz render  │      faqat oʻqish      │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## Tayyorlik

<p align="center"><img alt="38%" src="https://img.shields.io/badge/38%25-e07b39?style=flat-square"> <b>Relizga umumiy tayyorlik: 38%</b></p>

<p align="center"><img src="../../.github/assets/editor.png" alt="Meet the Heavy ochilgan muharrir" width="100%"><br><sub>Bugungi muharrir, Valve ning Meet the Heavy sessiyasi ochiq: taymlaynda shotlar va ovoz, sessiya daraxti, birinchi shot oʻz kamerasi orqali, sessiyadagi holat va yuz ifodalari bilan personajlar.</sub></p>

Nima tayyor va nima tayyor emasligini koʻrish uchun sohani oching. Foizlar — SFM qila oladigan narsalarga nisbatan mening halol bahom.

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM ni topish va ulash</b></summary>

Steam reyestri → `libraryfolders.vdf` → `gameinfo.txt` qidiruv yoʻllari, dvigatel tartibida. Standart oʻrnatmada oltita ulanish. Ilova papkasidan tashqarida hech narsa yozilmaydi.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Kontent indeksi</b></summary>

70 199 fayl 1,1 s sovuq / 0,02 s keshdan; ulanishlar orasidagi qayta belgilashlar dvigateldagidek hal qilinadi.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Modellar — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

Versiyalar 44, 48, 49. Skelet, meshlar, barcha detal darajalari, body-guruhlar. 1 500 model yuklandi, 0 xato.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Materiallar — <code>.vmt</code></b></summary>

Barcha 19 554 material oʻqiladi; `patch`, DX bloklari, proksilar.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Teksturalar — <code>.vtf</code></b></summary>

Versiyalar 7.0–7.5, DXT1/3/5 va barcha siqilmagan formatlar, kubmaplar, miplar. DXT dekodlanmasdan GPU ga boradi.

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>Sessiyalar — <code>.dmx</code></b></summary>

Binary 1–5 va KeyValues2. Oʻrnatmadagi har bir sessiya va zarralar fayli **baytma-bayt** qayta yoziladi.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Ekrandagi sessiya</b></summary>

Taymlaynda shotlar va ovoz yoʻlaklari, elementlar daraxti, har bir shot sahnasi oʻz kamerasi orqali. Hali yoʻq: xaritalar, zarralar, ovoz.

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>Animatsiya</b></summary>

Kanallar va loglar kursorda hisoblanadi; skrabbing va ijro. Suyaklar, kameralar va koʻrinish sessiyaga ergashadi.

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>Yuzlar</b></summary>

Flex kontrollerlar, kompilyatsiya qilingan qoidalar va vertex animatsiya — personajlar gapiradi va ifoda koʻrsatadi. Hali yoʻq: ajin xaritalari.

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>Riglar</b></summary>

Ifodalar, point/orient/parent/aim cheklovlari, ikki suyakli IK. Hali yoʻq: toʻliq operator bogʻliqlik grafi, rig yaratish.

</details>
<details><summary><img alt="55%" src="https://img.shields.io/badge/55%25-e0a800?style=flat-square"> <b>Tahrirlash</b></summary>

Bosib tanlash, koʻchirish/aylantirish manipulyatori, istalgan atribut uchun inspektor, kursorda kalit, bekor qilish/qaytarish, baytgacha aniq saqlash. Hali yoʻq: graf muharriri.

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>Motion editor</b></summary>

Chizgʻichda hold va falloff bilan vaqt tanlovi; tahrir SFM dagidek unga yoyiladi. Hali yoʻq: presetlar, qatlamlar.

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>Panellarni ulash</b></summary>

UE5 va Visual Studio dagidek, panellarni oldindan koʻrish bilan maqsadlar kompasiga torting. Hali yoʻq: saqlangan joylashuvlar, mavzular.

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source sheyding</b></summary>

Faqat tekstura va oddiy yorugʻlik. Hali yoʻq: phong, rim, lightwarp, sahna yorugʻliklari, soyalar.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Xaritalar — <code>.bsp</code></b></summary>

Boshlanmagan.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Rasm va videoga render</b></summary>

Boshlanmagan.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Plaginlar <code>.c2plg</code></b></summary>

Boshlanmagan.

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>Mavzular va ish maydonlari</b></summary>

Ataylab keyinga: muharrirda bezashga arzigulik narsa boʻlmaguncha bitta koʻrinish.

</details>

**Relizga tayyor emas.** Asos — SFM ishlatadigan har bir fayl formati, toʻgʻri oʻqilgan va butun oʻrnatmada tekshirilgan — mavjud va testlangan; sessiyani ochish, ijro etish, oʻzgartirish va saqlash mumkin. Yetishmayotgani — ish *qulayligi*: graf muharriri, Source sheyding, xaritalar, eksport. Animator unda bir kunlik ish qila olmaguncha versiya raqami boʻlmaydi.

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
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

Birinchi ishga tushirishda SFM Steam orqali qidiriladi; topilmasa — dastur soʻraydi. <kbd>Ctrl</kbd>+<kbd>O</kbd> sessiyani ochadi, <kbd>Space</kbd> — ijro, <kbd>C</kbd> — shot kamerasi, <kbd>T</kbd>/<kbd>R</kbd> — koʻchirish/aylantirish, <kbd>M</kbd> — motion editor, <kbd>Ctrl</kbd>+<kbd>Z</kbd> — bekor qilish, <kbd>Ctrl</kbd>+<kbd>S</kbd> — saqlash. Panellar sarlavhasidan tortiladi. Testlarga hech narsa kerak emas:

```bash
python Testing/run.py
```

## Tuzilma

```
C2UI_SDK/
├── c2ui.py            ishga tushirgich
├── Core/              dvigatel: formatlar, virtual fayl tizimi, indeks, koʻpriklar
├── App/               muharrir: kontent kutubxonasi, renderer, oyna
├── Tools/             lokalizatsiya, UI vositalari, plaginlar (keyinroq)
├── Testing/           testlar, baytgacha aniq fiksturalar, bitta runner
└── GIT&DOCK/README/   bu README boshqa tillarda
```

## Yoʻl xaritasi

1. **Graf muharriri** — egri chiziqlar va kalitlar koʻz oldida.
2. **Source sheyding** — SFM chizganidek VertexLitGeneric: phong, rim, lightwarp, sahna yorugʻliklari.
3. **Xaritalar** — fon uchun `.bsp`.
4. **Eksport** — rasm va video.
5. **Plaginlar** — `.c2plg` formati; keyin mavzular va ish maydonlari.

## Litsenziya va minnatdorchilik

Source Filmmaker, Team Fortress 2 va Source dvigateli Valve ga tegishli. Loyiha ularning formatlarini oʻqiydi, fayllarini oʻz ichiga olmaydi va faqat Steam dagi oʻz SFM nusxangiz bilan ishlaydi.

C2UI oʻz kodining litsenziyasi hali tanlanmagan — ungacha barcha huquqlar himoyalangan. Issues va pull requestlar xush kelibsiz.

<p align="center"><img src="../../.github/assets/models.png" alt="Oʻrnatmadan toʻgʻridan-toʻgʻri renderlangan 64 model" width="60%"><br><sub>Oʻrnatmadan tasodifiy tanlangan oltmish toʻrt model, C2UI ning oʻz rendereri bilan chizilgan.</sub></p>
