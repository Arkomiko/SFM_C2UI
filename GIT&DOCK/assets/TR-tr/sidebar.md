# C2UI hazırlığı — ayrıntılı

<p align="center"><a href="../RU-ru/sidebar.md">🇷🇺 Русский</a> · <a href="../EN-en/sidebar.md">🇬🇧 English</a> · <a href="../PL-pl/sidebar.md">🇵🇱 Polski</a> · <a href="../UK-ua/sidebar.md">🇺🇦 Українська</a> · <a href="../DE-de/sidebar.md">🇩🇪 Deutsch</a> · <a href="../RO-md/sidebar.md">🇲🇩 Moldovenească</a> · <a href="../SL-si/sidebar.md">🇸🇮 Slovenščina</a> · <a href="../BE-by/sidebar.md">🇧🇾 Беларуская</a> · <a href="../KK-kz/sidebar.md">🇰🇿 Қазақша</a> · <a href="../JA-jp/sidebar.md">🇯🇵 日本語</a> · <a href="../ZH-cn/sidebar.md">🇨🇳 中文</a> · <a href="../SV-se/sidebar.md">🇸🇪 Svenska</a> · <a href="../ES-es/sidebar.md">🇪🇸 Español</a> · <a href="../HI-in/sidebar.md">🇮🇳 हिन्दी</a> · <a href="../PT-pt/sidebar.md">🇵🇹 Português</a> · <a href="../BN-bd/sidebar.md">🇧🇩 বাংলা</a> · <a href="../FR-fr/sidebar.md">🇫🇷 Français</a> · <a href="../TE-in/sidebar.md">🇮🇳 తెలుగు</a> · <a href="../MR-in/sidebar.md">🇮🇳 मराठी</a> · <a href="../TA-in/sidebar.md">🇮🇳 தமிழ்</a> · <b>🇹🇷 Türkçe</b> · <a href="../UR-pk/sidebar.md">🇵🇰 اردو</a> · <a href="../VI-vn/sidebar.md">🇻🇳 Tiếng Việt</a> · <a href="../GU-in/sidebar.md">🇮🇳 ગુજરાતી</a> · <a href="../IT-it/sidebar.md">🇮🇹 Italiano</a> · <a href="../KO-kr/sidebar.md">🇰🇷 한국어</a> · <a href="../AR-sa/sidebar.md">🇸🇦 العربية</a> · <a href="../JV-id/sidebar.md">🇮🇩 Basa Jawa</a> · <a href="../ML-in/sidebar.md">🇮🇳 മലയാളം</a> · <a href="../NE-np/sidebar.md">🇳🇵 नेपाली</a> · <a href="../UZ-uz/sidebar.md">🇺🇿 Oʻzbekcha</a> · <a href="../OR-in/sidebar.md">🇮🇳 ଓଡ଼ିଆ</a></p>

<p align="center"><img src="sidebar.svg" alt="Hazırlık" width="320"></p>

<p align="center"><img alt="41%" src="https://img.shields.io/badge/41%25-e0a800?style=flat-square"> <b>Yayın için genel hazırlık: 41%</b></p>

Her alan açılabilir: neyin zaten çalıştığı ve neyin henüz olmadığı. Yüzdeler, SFM'nin yapabildiklerine göre bir tahmindir.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> SFM'yi bulma ve bağlama

Steam kayıt defteri → `libraryfolders.vdf` → `gameinfo.txt` arama yolları, motorun kendi sırasıyla. Standart kurulumda altı bağlama. Uygulama klasörü dışına hiçbir şey yazılmaz.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> İçerik dizini

70 199 dosya 1,1 s soğuk / 0,02 s önbellekten; bağlamalar arası geçersiz kılmalar tam motor gibi çözülür.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modeller — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Sürüm 44, 48, 49. İskelet, mesh'ler, tüm ayrıntı seviyeleri, gövde grupları. 1 500 model yüklendi, 0 hata.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Malzemeler — <code>.vmt</code>

Gelen 19 554 malzemenin tümü okunur; `patch`, DX blokları, proxy'ler.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Dokular — <code>.vtf</code>

Sürüm 7.0–7.5, DXT1/3/5 ve tüm sıkıştırılmamış biçimler, cubemap'ler, mip'ler. DXT kod çözme olmadan GPU'ya gider.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Oturumlar — <code>.dmx</code>

İkili 1–5 ve KeyValues2. Kurulumdaki her oturum ve parçacık dosyası **bayt bayt** geri yazılır.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Ekranda oturum

Zaman çizelgesinde çekimler ve ses parçaları, öğe ağacı, her çekimin sahnesi kendi kamerasından. Henüz yok: haritalar, parçacıklar, ses.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animasyon

Kanallar ve günlükler imleçte değerlendirilir; kaydırma ve oynatma. Kemikler, kameralar ve görünürlük oturumu izler.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Yüzler

Flex denetleyicileri, derlenmiş kurallar ve köşe animasyonu — karakterler konuşur ve ifade gösterir. Henüz yok: kırışıklık haritaları.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Rig'ler

İfadeler, point/orient/parent/aim kısıtları, iki kemikli IK. Henüz yok: tam operatör bağımlılık grafiği, rig oluşturma.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Düzenleme

Tıklayarak seçim, taşı/döndür manipülatörü, her öznitelik için denetçi, imleçte anahtar, geri al/yinele, bayt düzeyinde kayıt.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Cetvelde hold ve falloff ile zaman seçimi; düzenleme SFM'deki gibi üzerine yayılır. Henüz yok: ön ayarlar, katmanlar.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Grafik düzenleyici

Seçili öğeyi süren her logun eğrileri: X/Y/Z, pitch/yaw/roll, skalerler. Anahtarlar canlı önizlemeyle zaman ve değerde sürüklenir, çift tık ekler, Delete siler; zaman ekseni zaman çizelgesinindir. Henüz yok: teğetler ve eğri türleri, anahtar grubunu ölçekleme.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Panel yerleştirme

UE5 ve Visual Studio'daki gibi panelleri önizlemeli hedef pusulasına sürükleyin. Henüz yok: kayıtlı yerleşimler, temalar.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source gölgelendirme

Sadece doku ve basit ışık. Henüz yok: phong, rim, lightwarp, sahne ışıkları, gölgeler.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Haritalar — <code>.bsp</code>

Başlanmadı.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Görüntü ve videoya render

Başlanmadı.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Eklentiler <code>.c2plg</code>

Başlanmadı.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Temalar ve çalışma alanları

Bilerek sonra: düzenleyicide temalanmaya değer bir şey olana dek tek görünüm.

**Yayına hazır değil.** Temel — SFM'nin kullandığı her dosya biçimi, doğru okunmuş ve tüm kurulumda doğrulanmış — yerinde ve test edilmiş; bir oturum açılabilir, oynatılabilir, değiştirilebilir ve kaydedilebilir. Eksik olan çalışmanın *rahatlığı*: grafik düzenleyici, Source gölgelendirme, haritalar, dışa aktarma. Bir animatör içinde bir günlük iş yapabilene dek sürüm numarası yok.

<p align="center"><a href="../../README/TR-tr.md"><img alt="← README'ye dön" src="https://img.shields.io/badge/%E2%86%90_README%27ye_d%C3%B6n-1b2838?style=for-the-badge"></a></p>
