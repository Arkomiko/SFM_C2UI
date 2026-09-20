<p align="center"><img src="../assets/BN-bd/banner.png" alt="C2UI" width="100%"></p>

<p align="center"><a href="../../README.md">🇷🇺 Русский</a> · <a href="EN-en.md">🇬🇧 English</a> · <a href="PL-pl.md">🇵🇱 Polski</a> · <a href="UK-ua.md">🇺🇦 Українська</a> · <a href="DE-de.md">🇩🇪 Deutsch</a> · <a href="RO-md.md">🇲🇩 Moldovenească</a> · <a href="SL-si.md">🇸🇮 Slovenščina</a> · <a href="BE-by.md">🇧🇾 Беларуская</a> · <a href="KK-kz.md">🇰🇿 Қазақша</a> · <a href="JA-jp.md">🇯🇵 日本語</a> · <a href="ZH-cn.md">🇨🇳 中文</a> · <a href="SV-se.md">🇸🇪 Svenska</a> · <a href="ES-es.md">🇪🇸 Español</a> · <a href="HI-in.md">🇮🇳 हिन्दी</a> · <a href="PT-pt.md">🇵🇹 Português</a> · <b>🇧🇩 বাংলা</b> · <a href="FR-fr.md">🇫🇷 Français</a> · <a href="TE-in.md">🇮🇳 తెలుగు</a> · <a href="MR-in.md">🇮🇳 मराठी</a> · <a href="TA-in.md">🇮🇳 தமிழ்</a> · <a href="TR-tr.md">🇹🇷 Türkçe</a> · <a href="UR-pk.md">🇵🇰 اردو</a> · <a href="VI-vn.md">🇻🇳 Tiếng Việt</a> · <a href="GU-in.md">🇮🇳 ગુજરાતી</a> · <a href="IT-it.md">🇮🇹 Italiano</a> · <a href="KO-kr.md">🇰🇷 한국어</a> · <a href="AR-sa.md">🇸🇦 العربية</a> · <a href="JV-id.md">🇮🇩 Basa Jawa</a> · <a href="ML-in.md">🇮🇳 മലയാളം</a> · <a href="NE-np.md">🇳🇵 नेपाली</a> · <a href="UZ-uz.md">🇺🇿 Oʻzbekcha</a> · <a href="OR-in.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/%E0%A6%85%E0%A6%AC%E0%A6%B8%E0%A7%8D%E0%A6%A5%E0%A6%BE-%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%BF--%E0%A6%86%E0%A6%B2%E0%A6%AB%E0%A6%BE-e07b39?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/python-3.13-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="qt" src="https://img.shields.io/badge/Qt-6%20%2F%20PySide6-41cd52?style=flat-square&logo=qt&logoColor=white">
  <img alt="opengl" src="https://img.shields.io/badge/OpenGL-3.3%20core-5586a4?style=flat-square&logo=opengl&logoColor=white">
  <a href="../../Testing"><img alt="tests" src="https://img.shields.io/badge/%E0%A6%AA%E0%A6%B0%E0%A7%80%E0%A6%95%E0%A7%8D%E0%A6%B7%E0%A6%BE-351-66c0f4?style=flat-square"></a>
  <img alt="platform" src="https://img.shields.io/badge/Windows-1b2838?style=flat-square&logo=windows&logoColor=white">
</p>

<p align="center"><b>C2UI</b> — <i>Custom to User Interface</i> — — আধুনিক খোলসে Source Filmmaker-এর এডিটর: একই কনটেন্ট, একই সেশন ফরম্যাট, একই ডেটা মডেল, আর Steam লাইব্রেরি ও Unreal Engine 5 এডিটরের ধাঁচের ইন্টারফেস।</p>

---

## ধারণা

Source Filmmaker একটি শক্তিশালী টুল, যার ইন্টারফেস ২০১২ সালেই রয়ে গেছে। C2UI তাকে প্রতিস্থাপন বা নতুন করে বানায় না: লক্ষ্য কেবল SFM-কে একটু আধুনিক ও সুবিধাজনক করা।

এডিটর ইনস্টল করা SFM খুঁজে নেয়, তাকে কনটেন্ট লাইব্রেরি হিসেবে যুক্ত করে — মডেল, ম্যাটেরিয়াল, টেক্সচার, সেশন — আর একই ফাইল একই ফরম্যাটে নিয়ে কাজ করে। SFM-এ যা বানানো হয়েছে সবই C2UI-তে খোলে, উল্টোটাও।

প্রথম লক্ষ্য হাড় ও রিগ সহ SFM-এর সাথে পূর্ণ সামঞ্জস্য। তারপর — SFM-এ যা ছিল না।

```
  ┌──────────────┐    "SFM কোথায়?"    ┌──────────────────────────────┐
  │   C2UI       │ ─────────────────────▶│  SourceFilmmaker/game/       │
  │              │                       │    usermod/gameinfo.txt      │
  │  নিজস্ব UI    │ ◀─────   মাউন্ট   ───────│    tf/  hl2/  tf_movies/ …   │
  │  নিজস্ব রেন্ডার │       শুধু পড়া        │    models/ materials/ dmx    │
  └──────────────┘                       └──────────────────────────────┘
```

## প্রস্তুতি

<img align="right" src="../assets/BN-bd/sidebar.svg" alt="প্রস্তুতি" width="300">

<img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>রিলিজের জন্য সামগ্রিক প্রস্তুতি: 41%</b>

প্রতিটি ক্ষেত্র খোলা যায়: কী ইতিমধ্যে কাজ করে আর কী এখনো নেই। শতাংশ SFM-এর সক্ষমতার তুলনায় একটি অনুমান।

<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>SFM খোঁজা ও মাউন্ট করা</b></summary>

Steam রেজিস্ট্রি → `libraryfolders.vdf` → `gameinfo.txt`-এর সার্চ পাথ, ইঞ্জিনের ক্রমে। স্ট্যান্ডার্ড ইনস্টলে ছয়টি মাউন্ট। অ্যাপ্লিকেশন ফোল্ডারের বাইরে কিছু লেখা হয় না।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>কনটেন্ট ইনডেক্স</b></summary>

৭০ ১৯৯ ফাইল ১.১ সেকেন্ডে ঠান্ডা / ০.০২ সেকেন্ডে ক্যাশ থেকে; মাউন্টের মধ্যে ওভাররাইড ঠিক ইঞ্জিনের মতো সমাধান হয়।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>মডেল — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code></b></summary>

সংস্করণ ৪৪, ৪৮, ৪৯। কঙ্কাল, মেশ, সব ডিটেইল লেভেল, বডি গ্রুপ। ১ ৫০০ মডেল লোড, ০ ব্যর্থতা।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>ম্যাটেরিয়াল — <code>.vmt</code></b></summary>

সব ১৯ ৫৫৪টি ম্যাটেরিয়াল পড়া যায়; `patch`, DX ব্লক, প্রক্সি।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>টেক্সচার — <code>.vtf</code></b></summary>

সংস্করণ ৭.০–৭.৫, DXT1/3/5 ও সব অসংকুচিত ফরম্যাট, কিউবম্যাপ, মিপ। DXT ডিকোড ছাড়াই GPU-তে যায়।

</details>
<details><summary><img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> <b>সেশন — <code>.dmx</code></b></summary>

বাইনারি ১–৫ ও KeyValues2। ইনস্টলেশনের প্রতিটি সেশন ও পার্টিকল ফাইল **বাইটে বাইটে** ফিরে লেখা হয়।

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>পর্দায় সেশন</b></summary>

টাইমলাইনে শট ও সাউন্ড ট্র্যাক, এলিমেন্ট ট্রি, প্রতিটি শটের দৃশ্য তার ক্যামেরায়। এখনো নয়: ম্যাপ, পার্টিকল, শব্দ।

</details>
<details><summary><img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> <b>অ্যানিমেশন</b></summary>

কার্সরে চ্যানেল ও লগ মূল্যায়ন; স্ক্রাব ও প্লে। হাড়, ক্যামেরা ও দৃশ্যমানতা সেশন অনুসরণ করে।

</details>
<details><summary><img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> <b>মুখ</b></summary>

Flex কন্ট্রোলার, কম্পাইল করা নিয়ম ও ভার্টেক্স অ্যানিমেশন — চরিত্ররা কথা বলে ও অভিব্যক্তি দেখায়। এখনো নয়: রিঙ্কল ম্যাপ।

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>রিগ</b></summary>

এক্সপ্রেশন, point/orient/parent/aim কনস্ট্রেইন্ট, দুই-হাড় IK। এখনো নয়: পূর্ণ অপারেটর নির্ভরতা গ্রাফ, রিগ তৈরি।

</details>
<details><summary><img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> <b>সম্পাদনা</b></summary>

ক্লিকে নির্বাচন, মুভ/রোটেট ম্যানিপুলেটর, যেকোনো অ্যাট্রিবিউটের ইন্সপেক্টর, কার্সরে কী, আনডু/রিডু, বাইট-নিখুঁত সেভ।

</details>
<details><summary><img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> <b>মোশন এডিটর</b></summary>

রুলারে হোল্ড ও ফলঅফ সহ সময় নির্বাচন; সম্পাদনা SFM-এর মতো তার উপর ছড়ায়। এখনো নয়: প্রিসেট, লেয়ার।

</details>
<details><summary><img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> <b>গ্রাফ এডিটর</b></summary>

নির্বাচিত এলিমেন্ট চালানো প্রতিটি লগের কার্ভ: X/Y/Z, pitch/yaw/roll, স্কেলার। কী লাইভ প্রিভিউ সহ সময় ও মানে টানা যায়, ডাবল-ক্লিকে যোগ, Delete-এ মুছে; সময় অক্ষ টাইমলাইনের। এখনো নয়: ট্যানজেন্ট ও কার্ভ টাইপ, কী গ্রুপ স্কেলিং।

</details>
<details><summary><img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> <b>প্যানেল ডকিং</b></summary>

UE5 ও Visual Studio-র মতো, প্রিভিউ সহ লক্ষ্যের কম্পাসে প্যানেল টানুন। এখনো নয়: সংরক্ষিত লেআউট, থিম।

</details>
<details><summary><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Source শেডিং</b></summary>

শুধু টেক্সচার আর সাধারণ আলো। এখনো নয়: phong, rim, lightwarp, দৃশ্যের আলো, ছায়া।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>ম্যাপ — <code>.bsp</code></b></summary>

শুরু হয়নি।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>ছবি ও ভিডিওতে রেন্ডার</b></summary>

শুরু হয়নি।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>প্লাগইন <code>.c2plg</code></b></summary>

শুরু হয়নি।

</details>
<details><summary><img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> <b>থিম ও ওয়ার্কস্পেস</b></summary>

ইচ্ছাকৃতভাবে পরে: এডিটরে সাজানোর মতো কিছু না হওয়া পর্যন্ত একটাই চেহারা।

</details>

**রিলিজের জন্য প্রস্তুত নয়।** ভিত্তি — SFM যে প্রতিটি ফাইল ফরম্যাট ব্যবহার করে, সঠিকভাবে পড়া ও পুরো ইনস্টলেশনে যাচাই করা — আছে ও পরীক্ষিত; সেশন খোলা, চালানো, বদলানো ও সেভ করা যায়। যা নেই তা কাজের *স্বাচ্ছন্দ্য*: গ্রাফ এডিটর, Source শেডিং, ম্যাপ, এক্সপোর্ট। একজন অ্যানিমেটর এতে এক দিনের কাজ করতে না পারা পর্যন্ত কোনো সংস্করণ নম্বর নয়।

<br clear="all">

<p align="center"><img src="../assets/editor.png" alt="Meet the Heavy খোলা অবস্থায় এডিটর" width="100%"><br><sub>আজকের এডিটর, Valve-এর Meet the Heavy খোলা: টাইমলাইনে শট আর শব্দ, সেশন ট্রি, প্রথম শট তার নিজের ক্যামেরায়, সেশন অনুযায়ী ভঙ্গি ও মুখভঙ্গিতে চরিত্ররা।</sub></p>

## কী একে আলাদা করে

- **পোর্টেবল।** অ্যাপ্লিকেশন ফোল্ডারের বাইরে কিছু লেখা হয় না: সেটিংস `App/User`-এ, ক্যাশ `App/Cache`-এ, অস্থায়ী `App/Temporary`-তে। ফোল্ডার মুছুন, কোনো চিহ্ন নেই।
- **SFM কখনো চালায় না।** চালানোর কোনো প্রসেস নেই, দখলের কোনো উইন্ডো নেই। ইনস্টলেশন কনটেন্ট প্যাকের মতো পড়া হয়।
- **ফরম্যাট যাচাই করা, অনুমান নয়।** প্রতিটি রিডার আসল ইনস্টলেশনের সাথে মেলানো; যেখানে ফরম্যাট অপ্রত্যাশিত কিছু করে, কোড তা বলে।
- **সেভ নিখুঁত।** অপরিবর্তিত পড়া ও লেখা সেশন একই ফাইল।
- **ইঞ্জিনের কোনো নির্ভরতা নেই।** `Core/` ও পুরো টেস্ট সুট খাঁটি Python-এ চলে; শুধু উইন্ডোর Qt ও OpenGL লাগে।

## চালানো

Windows, Python 3.13 ও Source Filmmaker ইনস্টলেশন প্রয়োজন।

```bash
git clone https://github.com/Arkomiko/SFM_C2UI.git
cd SFM_C2UI
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe c2ui.py
```

প্রথম চালুতে Steam-এর মাধ্যমে SFM খোঁজে; না পেলে জিজ্ঞেস করে। <kbd>Ctrl</kbd>+<kbd>O</kbd> সেশন খোলে, <kbd>Space</kbd> প্লে, <kbd>C</kbd> শট ক্যামেরা, <kbd>T</kbd>/<kbd>R</kbd> মুভ/রোটেট, <kbd>M</kbd> মোশন এডিটর, <kbd>Ctrl</kbd>+<kbd>Z</kbd> আনডু, <kbd>Ctrl</kbd>+<kbd>S</kbd> সেভ। প্যানেল শিরোনাম ধরে টানা হয়। পরীক্ষার কিছু লাগে না:

```bash
python Testing/run.py
```

## কাঠামো

```
C2UI_SDK/
├── c2ui.py            লঞ্চার
├── Core/              ইঞ্জিন: ফরম্যাট, ভার্চুয়াল ফাইল সিস্টেম, ইনডেক্স, ব্রিজ
├── App/               এডিটর: কনটেন্ট লাইব্রেরি, রেন্ডারার, উইন্ডো
├── Tools/             স্থানীয়করণ, UI টুল, প্লাগইন (পরে)
├── Testing/           পরীক্ষা, বাইট-নিখুঁত ফিক্সচার, এক রানার
└── GIT&DOCK/README/   এই README অন্য ভাষায়
```

## রোডম্যাপ

১. **Source শেডিং** — VertexLitGeneric যেভাবে SFM আঁকে: phong, rim, lightwarp, দৃশ্যের আলো।
২. **ম্যাপ** — পটভূমির জন্য `.bsp`।
৩. **আউটপুট** — ছবি ও ভিডিও এক্সপোর্ট।
৪. **প্লাগইন** — `.c2plg` ফরম্যাট; তারপর থিম ও ওয়ার্কস্পেস।

## লাইসেন্স ও কৃতজ্ঞতা

Source Filmmaker, Team Fortress 2 ও Source ইঞ্জিন Valve-এর। এই প্রকল্প তাদের ফাইল ফরম্যাট পড়ে, তাদের কোনো ফাইল অন্তর্ভুক্ত করে না, আর শুধু Steam-এ আপনার নিজের SFM কপির সাথে কাজ করে।

C2UI-এর নিজস্ব কোডের লাইসেন্স এখনো ঠিক হয়নি — ততক্ষণ সর্বস্বত্ব সংরক্ষিত। Issues ও pull requests তবুও স্বাগত।

<p align="center"><img src="../assets/models.png" alt="ইনস্টলেশন থেকে সরাসরি রেন্ডার করা ৬৪টি মডেল" width="60%"><br><sub>ইনস্টলেশন থেকে এলোমেলোভাবে বাছা চৌষট্টিটি মডেল, C2UI-এর নিজস্ব রেন্ডারারে আঁকা।</sub></p>
