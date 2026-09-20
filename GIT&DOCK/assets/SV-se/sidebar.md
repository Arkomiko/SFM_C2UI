# C2UI:s mognad i detalj

<details align="center"><summary>&nbsp;🌐 <b>🇸🇪 Svenska</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="../RU-ru/sidebar.md">🇷🇺<br>Русский</a></td><td align="center"><a href="../EN-en/sidebar.md">🇬🇧<br>English</a></td><td align="center"><a href="../PL-pl/sidebar.md">🇵🇱<br>Polski</a></td><td align="center"><a href="../UK-ua/sidebar.md">🇺🇦<br>Українська</a></td><td align="center"><a href="../DE-de/sidebar.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="../RO-md/sidebar.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="../SL-si/sidebar.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="../BE-by/sidebar.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="../KK-kz/sidebar.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="../JA-jp/sidebar.md">🇯🇵<br>日本語</a></td><td align="center"><a href="../ZH-cn/sidebar.md">🇨🇳<br>中文</a></td><td align="center"><b>🇸🇪<br>Svenska</b></td><td align="center"><a href="../ES-es/sidebar.md">🇪🇸<br>Español</a></td><td align="center"><a href="../HI-in/sidebar.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="../PT-pt/sidebar.md">🇵🇹<br>Português</a></td><td align="center"><a href="../BN-bd/sidebar.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="../FR-fr/sidebar.md">🇫🇷<br>Français</a></td><td align="center"><a href="../TE-in/sidebar.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="../MR-in/sidebar.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="../TA-in/sidebar.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="../TR-tr/sidebar.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="../UR-pk/sidebar.md">🇵🇰<br>اردو</a></td><td align="center"><a href="../VI-vn/sidebar.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="../GU-in/sidebar.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><a href="../IT-it/sidebar.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="../KO-kr/sidebar.md">🇰🇷<br>한국어</a></td><td align="center"><a href="../AR-sa/sidebar.md">🇸🇦<br>العربية</a></td><td align="center"><a href="../JV-id/sidebar.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="../ML-in/sidebar.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="../NE-np/sidebar.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="../UZ-uz/sidebar.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="../OR-in/sidebar.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="sidebar.svg" alt="Mognad" width="320"></p>

<p align="center"><img alt="44%" src="https://img.shields.io/badge/44%25-e0a800?style=flat-square"> <b>Total mognad för release: 44%</b></p>

Varje område kan fällas ut: vad som redan fungerar och vad som inte finns än. Procenten är en uppskattning mot vad SFM kan.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Hitta och montera SFM

Steam-registret → `libraryfolders.vdf` → sökvägarna i `gameinfo.txt`, i motorns egen ordning. Sex monteringar på en standardinstallation. Inget skrivs utanför programmappen.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Innehållsindex

70 199 filer på 1,1 s kallt / 0,02 s varmt; överskuggningar mellan monteringar löses exakt som motorn gör.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Modeller — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

Version 44, 48, 49. Skelett, meshar, alla detaljnivåer, kroppsgrupper. 1 500 modeller laddade, 0 fel.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Material — <code>.vmt</code>

Alla 19 554 medföljande material tolkas; `patch`, DX-block, proxyer.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Texturer — <code>.vtf</code>

Version 7.0–7.5, DXT1/3/5 och alla okomprimerade format, kubkartor, mippar. DXT går till GPU:n utan avkodning.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> Sessioner — <code>.dmx</code>

Binär 1–5 och KeyValues2. Varje session och partikelfil i installationen skrivs tillbaka **byte för byte**.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Session på skärmen

Shots och ljudspår på en tidslinje, elementträdet, varje shots scen genom sin kamera. Inte ännu: kartor, partiklar, ljud.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> Animation

Kanaler och loggar utvärderas vid markören; scrubba och spela. Ben, kameror och synlighet följer sessionen.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> Ansikten

Flex-kontroller, de kompilerade reglerna och vertexanimation — karaktärer pratar och visar känslor. Inte ännu: rynkkartor.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Riggar

Uttryck, point/orient/parent/aim-begränsningar, tvåbens-IK. Inte ännu: hela operatorberoendegrafen, riggskapande.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> Redigering

Klicka för att välja, en flytta/rotera-manipulator, en inspektör för alla attribut, en nyckel vid markören, ångra/gör om, byteexakt sparning.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> Motion editor

Ett tidsurval med hold och falloff på linjalen; en ändring sprids över det som i SFM. Inte ännu: förinställningar, lager.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> Grafredigerare

Kurvor för varje logg som styr det valda elementet: X/Y/Z, pitch/yaw/roll, skalärer. Nycklar dras i tid och värde med förhandsvisning, dubbelklick lägger till, Delete tar bort; tidsaxeln är tidslinjens. Inte ännu: tangenter och kurvtyper, skalning av en grupp nycklar.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> Paneldockning

Dra paneler till en kompass av mål med förhandsvisning, som i UE5 och Visual Studio. Inte ännu: sparade layouter, teman.

### <img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> Source-skuggning

Bara textur och ett enkelt ljus. Inte ännu: phong, rim, lightwarp, scenljus, skuggor.

### <img alt="45%" src="https://img.shields.io/badge/45%25-e0a800?style=flat-square"> Kartor — <code>.bsp</code>

Version 19–21: världsgeometri, displacement-terräng, brush-entiteter, statiska props, kartans egna pak-material. Frustum-culling. Inte ännu: lightmaps, skybox, vatten, prop_dynamic.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Rendering till bild och video

Inte påbörjat.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Insticksprogram <code>.c2plg</code>

Inte påbörjat.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> Teman och arbetsytor

Medvetet senare: ett utseende tills redigeraren har något värt att tema.

**Inte redo för release.** Grunden — varje filformat SFM använder, korrekt läst och verifierat mot hela installationen — finns och är testad; en session kan öppnas, spelas, ändras och sparas. Det som saknas är *bekvämligheten* i arbetet: grafredigeraren, Source-skuggning, kartor, export. Inget versionsnummer förrän en animatör kan göra en dags arbete i den.

<p align="center"><a href="../../README/SV-se.md"><img alt="← Tillbaka till README" src="https://img.shields.io/badge/%E2%86%90_Tillbaka_till_README-1b2838?style=for-the-badge"></a></p>
