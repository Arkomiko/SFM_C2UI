# C2UI-এর প্রস্তুতি — বিস্তারিত

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <b>🇧🇩 বাংলা</b> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <a href="../TR-tr/sidebar.md">🇹🇷 Türkçe</a> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="প্রস্তুতি" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>রিলিজের জন্য সামগ্রিক প্রস্তুতি: 41%</b></p>

প্রতিটি ক্ষেত্র খোলা যায়: কী ইতিমধ্যে কাজ করে আর কী এখনো নেই। শতাংশ SFM-এর সক্ষমতার তুলনায় একটি অনুমান।

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> SFM খোঁজা ও মাউন্ট করা

Steam রেজিস্ট্রি → `libraryfolders.vdf` → `gameinfo.txt`-এর সার্চ পাথ, ইঞ্জিনের ক্রমে। স্ট্যান্ডার্ড ইনস্টলে ছয়টি মাউন্ট। অ্যাপ্লিকেশন ফোল্ডারের বাইরে কিছু লেখা হয় না।

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> কনটেন্ট ইনডেক্স

৭০ ১৯৯ ফাইল ১.১ সেকেন্ডে ঠান্ডা / ০.০২ সেকেন্ডে ক্যাশ থেকে; মাউন্টের মধ্যে ওভাররাইড ঠিক ইঞ্জিনের মতো সমাধান হয়।

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> মডেল — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

সংস্করণ ৪৪, ৪৮, ৪৯। কঙ্কাল, মেশ, সব ডিটেইল লেভেল, বডি গ্রুপ। ১ ৫০০ মডেল লোড, ০ ব্যর্থতা।

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> ম্যাটেরিয়াল — <code>.vmt</code>

সব ১৯ ৫৫৪টি ম্যাটেরিয়াল পড়া যায়; `patch`, DX ব্লক, প্রক্সি।

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> টেক্সচার — <code>.vtf</code>

সংস্করণ ৭.০–৭.৫, DXT1/3/5 ও সব অসংকুচিত ফরম্যাট, কিউবম্যাপ, মিপ। DXT ডিকোড ছাড়াই GPU-তে যায়।

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> সেশন — <code>.dmx</code>

বাইনারি ১–৫ ও KeyValues2। ইনস্টলেশনের প্রতিটি সেশন ও পার্টিকল ফাইল **বাইটে বাইটে** ফিরে লেখা হয়।

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> পর্দায় সেশন

টাইমলাইনে শট ও সাউন্ড ট্র্যাক, এলিমেন্ট ট্রি, প্রতিটি শটের দৃশ্য তার ক্যামেরায়। এখনো নয়: ম্যাপ, পার্টিকল, শব্দ।

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> অ্যানিমেশন

কার্সরে চ্যানেল ও লগ মূল্যায়ন; স্ক্রাব ও প্লে। হাড়, ক্যামেরা ও দৃশ্যমানতা সেশন অনুসরণ করে।

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> মুখ

Flex কন্ট্রোলার, কম্পাইল করা নিয়ম ও ভার্টেক্স অ্যানিমেশন — চরিত্ররা কথা বলে ও অভিব্যক্তি দেখায়। এখনো নয়: রিঙ্কল ম্যাপ।

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> রিগ

এক্সপ্রেশন, point/orient/parent/aim কনস্ট্রেইন্ট, দুই-হাড় IK। এখনো নয়: পূর্ণ অপারেটর নির্ভরতা গ্রাফ, রিগ তৈরি।

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> সম্পাদনা

ক্লিকে নির্বাচন, মুভ/রোটেট ম্যানিপুলেটর, যেকোনো অ্যাট্রিবিউটের ইন্সপেক্টর, কার্সরে কী, আনডু/রিডু, বাইট-নিখুঁত সেভ।

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> মোশন এডিটর

রুলারে হোল্ড ও ফলঅফ সহ সময় নির্বাচন; সম্পাদনা SFM-এর মতো তার উপর ছড়ায়। এখনো নয়: প্রিসেট, লেয়ার।

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> গ্রাফ এডিটর

নির্বাচিত এলিমেন্ট চালানো প্রতিটি লগের কার্ভ: X/Y/Z, pitch/yaw/roll, স্কেলার। কী লাইভ প্রিভিউ সহ সময় ও মানে টানা যায়, ডাবল-ক্লিকে যোগ, Delete-এ মুছে; সময় অক্ষ টাইমলাইনের। এখনো নয়: ট্যানজেন্ট ও কার্ভ টাইপ, কী গ্রুপ স্কেলিং।

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> প্যানেল ডকিং

UE5 ও Visual Studio-র মতো, প্রিভিউ সহ লক্ষ্যের কম্পাসে প্যানেল টানুন। এখনো নয়: সংরক্ষিত লেআউট, থিম।

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source শেডিং

শুধু টেক্সচার আর সাধারণ আলো। এখনো নয়: phong, rim, lightwarp, দৃশ্যের আলো, ছায়া।

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> ম্যাপ — <code>.bsp</code>

শুরু হয়নি।

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> ছবি ও ভিডিওতে রেন্ডার

শুরু হয়নি।

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> প্লাগইন <code>.c2plg</code>

শুরু হয়নি।

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> থিম ও ওয়ার্কস্পেস

ইচ্ছাকৃতভাবে পরে: এডিটরে সাজানোর মতো কিছু না হওয়া পর্যন্ত একটাই চেহারা।

**রিলিজের জন্য প্রস্তুত নয়।** ভিত্তি — SFM যে প্রতিটি ফাইল ফরম্যাট ব্যবহার করে, সঠিকভাবে পড়া ও পুরো ইনস্টলেশনে যাচাই করা — আছে ও পরীক্ষিত; সেশন খোলা, চালানো, বদলানো ও সেভ করা যায়। যা নেই তা কাজের *স্বাচ্ছন্দ্য*: গ্রাফ এডিটর, Source শেডিং, ম্যাপ, এক্সপোর্ট। একজন অ্যানিমেটর এতে এক দিনের কাজ করতে না পারা পর্যন্ত কোনো সংস্করণ নম্বর নয়।

<p align="center"><a href="../../README/BN-bd.md"><img alt="← README-এ ফিরুন" src="https://img.shields.io/badge/%E2%86%90_README-%E0%A6%8F_%E0%A6%AB%E0%A6%BF%E0%A6%B0%E0%A7%81%E0%A6%A8-1b2838?style=for-the-badge"></a></p>
