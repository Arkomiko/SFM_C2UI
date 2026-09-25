# C2UI hazırlığı — ayrıntılı

<details align="center"><summary>&nbsp;🌐 <b>🇹🇷 Türkçe</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><b>🇹🇷<br>Türkçe</b></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/TR-tr.svg" alt="Hazırlık" width="100%"></p>

<p align="center"><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>Yayın için genel hazırlık: 15%</b></p>

> [!IMPORTANT]
> **Geliştirme duraklatıldı.** Depo açık kalıyor: kod, belgeler ve geçmiş burada duruyor ve aşağıda anlatılan her şey anlatıldığı gibi çalışıyor. Hazırlık sayıları, konular ve yol haritası duraklama anındaki durumu gösteriyor.

Her alan açılabilir: neyin zaten çalıştığı ve neyin henüz olmadığı. Yüzdeler, SFM'nin yapabildiklerine göre bir tahmindir.

Her yüzde **bir alanı, SFM'nin o alanda yaptığına göre** ölçer; planlanana göre değil. Genel rakam ürünün tamamını SFM'nin yanında ölçer ve çok daha düşüktür: biçimler eksiksiz okunuyor, ama Source Filmmaker olmak yaklaşık 350 `Dme*` öğe türü demek ve motor bunların 23'ünü biliyor.

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

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Ekrandaki oturum

Zaman çizelgesinde çekimler ve ses parçaları, öğe ağacı, her çekimin sahnesi kendi kamerasından, çekimin haritası. Henüz yok: parçacıklar, ses.

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

### <img alt="75%" src="https://img.shields.io/badge/75%25-3b9c5b?style=flat-square"> Source gölgeleme

Oturum ışıkları (DmeProjectedLight): frustum, Source sönümü, maxDistance'a kadar solma; half-lambert, $lightwarptexture, phong, $rimlight, $selfillum. Haritanın dünyası lightmap'lerle; modeller haritanın ambient küpleri ve dünya ışıklarıyla aydınlatılır. Henüz yok: gölgeler, gobo dokuları, $bumpmap, $envmap.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Haritalar — <code>.bsp</code>

Sürüm 19–21: dünya geometrisi, displacement arazi, brush varlıkları, statik prop'lar, haritanın kendi pak malzemeleri, lightmap'ler, kameranın çevresindeki skybox. Frustum ayıklama. Henüz yok: su, prop_dynamic.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Görüntü ve videoya işleme

Oturumdan PNG/TGA dizileri ve AVI/MP4 filmler: tüm oturum, geçerli çekim veya bir aralık; ön ayarlar; File → Export, Ctrl+E. Henüz yok: filmde ses.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Eklentiler <code>.c2plg</code>

Başlanmadı.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Temalar ve çalışma alanları

Bilerek sonra: düzenleyicide temalanmaya değer bir şey olana dek tek görünüm.

**Yayına hazır değil.** Temel — SFM'nin kullandığı her dosya biçimi, doğru okunmuş ve tüm kurulumda doğrulanmış — yerinde ve test edilmiş; bir oturum açılabilir, oynatılabilir, değiştirilebilir ve kaydedilebilir. Eksik olan çalışmanın *rahatlığı*: grafik düzenleyici, Source gölgelendirme, haritalar, dışa aktarma. Bir animatör içinde bir günlük iş yapabilene dek sürüm numarası yok.

<p align="center"><a href="../README/TR-tr.md"><img alt="← README'ye dön" src="https://img.shields.io/badge/%E2%86%90_README%27ye_d%C3%B6n-1b2838?style=for-the-badge"></a></p>
