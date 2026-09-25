# C2UI ની તૈયારી — વિગતવાર

<details align="center"><summary>&nbsp;🌐 <b>🇮🇳 ગુજરાતી</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><b>🇮🇳<br>ગુજરાતી</b></td></tr>
<tr><td align="center"><a href="IT-it.md">🇮🇹<br>Italiano</a></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

<p align="center"><img src="../assets/readiness/areas/GU-in.svg" alt="તૈયારી" width="100%"></p>

<p align="center"><img alt="15%" src="https://img.shields.io/badge/15%25-e07b39?style=flat-square"> <b>રિલીઝ માટે એકંદર તૈયારી: 15%</b></p>

> [!IMPORTANT]
> **વિકાસ હાલ અટકાવાયો છે.** રિપોઝિટરી ખુલ્લી રહે છે: કોડ, દસ્તાવેજો અને ઇતિહાસ બધું અહીં જ છે, અને નીચે વર્ણવેલું બધું વર્ણવ્યા પ્રમાણે ચાલે છે. તૈયારીના આંકડા, issues અને રોડમેપ વિરામની ક્ષણની સ્થિતિ બતાવે છે.

દરેક ક્ષેત્ર ખુલે છે: શું પહેલેથી કામ કરે છે અને શું હજુ નથી. ટકાવારી SFM ની ક્ષમતાઓની સાપેક્ષ અંદાજ છે.

દરેક ટકાવારી **તે ક્ષેત્રમાં SFM શું કરે છે તેની સામે તે ક્ષેત્રને** માપે છે, યોજનાની સામે નહીં. કુલ આંકડો આખા ઉત્પાદનને SFM ની બાજુમાં માપે છે, તેથી ઘણો ઓછો છે: ફોર્મેટ સંપૂર્ણ વંચાય છે, પણ Source Filmmaker હોવું એટલે આશરે 350 `Dme*` એલિમેન્ટ પ્રકારો, જેમાંથી એન્જિન 23 જાણે છે.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> SFM શોધવું અને માઉન્ટ કરવું

Steam રજિસ્ટ્રી → `libraryfolders.vdf` → `gameinfo.txt` ના સર્ચ પાથ, એન્જિનના ક્રમમાં. માનક ઇન્સ્ટોલ પર છ માઉન્ટ. એપ્લિકેશન ફોલ્ડર બહાર કંઈ લખાતું નથી.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> કન્ટેન્ટ ઇન્ડેક્સ

70 199 ફાઇલો 1.1 સે ઠંડું / 0.02 સે કેશમાંથી; માઉન્ટ વચ્ચેના ઓવરરાઇડ એન્જિન જેમ જ ઉકેલાય છે.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> મોડેલ — <code>.mdl</code> <code>.vvd</code> <code>.vtx</code>

વર્ઝન 44, 48, 49. હાડપિંજર, મેશ, બધા વિગત સ્તર, બોડી ગ્રુપ. 1 500 મોડેલ લોડ, 0 નિષ્ફળતા.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> મટીરિયલ — <code>.vmt</code>

બધા 19 554 મટીરિયલ વંચાય છે; `patch`, DX બ્લોક, પ્રોક્સી.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> ટેક્સચર — <code>.vtf</code>

વર્ઝન 7.0–7.5, DXT1/3/5 અને બધા અસંકુચિત ફોર્મેટ, ક્યુબમેપ, મિપ. DXT ડીકોડ વિના GPU માં જાય છે.

### <img alt="100%" src="https://img.shields.io/badge/100%25-66c0f4?style=flat-square"> સેશન — <code>.dmx</code>

બાઇનરી 1–5 અને KeyValues2. ઇન્સ્ટોલની દરેક સેશન અને પાર્ટિકલ ફાઇલ **બાઇટ બાય બાઇટ** પાછી લખાય છે.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> સ્ક્રીન પર સેશન

ટાઇમલાઇન પર શોટ અને સાઉન્ડ ટ્રેક, તત્વ વૃક્ષ, દરેક શોટનું દૃશ્ય તેના કેમેરાથી, શોટનો નકશો. હજી નહીં: પાર્ટિકલ, અવાજ.

### <img alt="85%" src="https://img.shields.io/badge/85%25-3b9c5b?style=flat-square"> એનિમેશન

કર્સર પર ચેનલ અને લોગ મૂલ્યાંકિત; સ્ક્રબ અને પ્લે. હાડકાં, કેમેરા અને દૃશ્યતા સેશનને અનુસરે છે.

### <img alt="90%" src="https://img.shields.io/badge/90%25-3b9c5b?style=flat-square"> ચહેરા

Flex કંટ્રોલર, કમ્પાઇલ કરેલા નિયમો અને વર્ટેક્સ એનિમેશન — પાત્રો બોલે છે અને ભાવ બતાવે છે. હજુ નહીં: કરચલી નકશા.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> રિગ

એક્સપ્રેશન, point/orient/parent/aim કન્સ્ટ્રેન્ટ, બે-હાડકાં IK. હજુ નહીં: સંપૂર્ણ ઓપરેટર નિર્ભરતા ગ્રાફ, રિગ બનાવવું.

### <img alt="60%" src="https://img.shields.io/badge/60%25-e0a800?style=flat-square"> એડિટિંગ

ક્લિકથી પસંદગી, મૂવ/રોટેટ મેનિપ્યુલેટર, કોઈપણ એટ્રિબ્યુટનો ઇન્સ્પેક્ટર, કર્સર પર કી, અનડુ/રીડુ, બાઇટ-ચોક્કસ સેવ.

### <img alt="50%" src="https://img.shields.io/badge/50%25-e0a800?style=flat-square"> મોશન એડિટર

રૂલર પર હોલ્ડ અને ફોલઓફ સાથે સમય પસંદગી; ફેરફાર SFM જેમ તેના પર ફેલાય છે. હજુ નહીં: પ્રીસેટ, લેયર.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> ગ્રાફ એડિટર

પસંદ કરેલા એલિમેન્ટને ચલાવતા દરેક લોગના વળાંક: X/Y/Z, pitch/yaw/roll, સ્કેલર. કી લાઇવ પ્રીવ્યૂ સાથે સમય અને મૂલ્યમાં ખેંચાય છે, ડબલ-ક્લિક ઉમેરે છે, Delete દૂર કરે છે; સમય અક્ષ ટાઇમલાઇનનો. હજુ નહીં: ટેન્જન્ટ અને વળાંક પ્રકાર, કી જૂથનું સ્કેલિંગ.

### <img alt="80%" src="https://img.shields.io/badge/80%25-3b9c5b?style=flat-square"> પેનલ ડોકિંગ

UE5 અને Visual Studio જેમ, પ્રીવ્યૂ સાથે લક્ષ્યોના કંપાસ પર પેનલ ખેંચો. હજુ નહીં: સાચવેલા લેઆઉટ, થીમ.

### <img alt="75%" src="https://img.shields.io/badge/75%25-3b9c5b?style=flat-square"> Source શેડિંગ

સેશન લાઇટો (DmeProjectedLight): ફ્રસ્ટમ, Source ક્ષીણન, maxDistance સુધી ફેડ; half-lambert, $lightwarptexture, phong, $rimlight, $selfillum. નકશાની દુનિયા લાઇટમેપથી; મોડેલ નકશાના એમ્બિયન્ટ ક્યુબ અને વર્લ્ડ લાઇટથી પ્રકાશિત. હજી નહીં: પડછાયા, ગોબો ટેક્સચર, $bumpmap, $envmap.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> નકશા — <code>.bsp</code>

આવૃત્તિઓ 19–21: વર્લ્ડ ભૂમિતિ, ડિસ્પ્લેસમેન્ટ ભૂપ્રદેશ, બ્રશ એન્ટિટી, સ્ટેટિક પ્રોપ્સ, નકશાના પોતાના pak મટીરિયલ, લાઇટમેપ, કેમેરાની આસપાસ સ્કાયબોક્સ. ફ્રસ્ટમ કલિંગ. હજી નહીં: પાણી, prop_dynamic.

### <img alt="70%" src="https://img.shields.io/badge/70%25-3b9c5b?style=flat-square"> છબી અને વિડિઓમાં રેન્ડર

સેશનમાંથી PNG/TGA સિક્વન્સ અને AVI/MP4 ફિલ્મો: આખું સેશન, વર્તમાન શોટ કે રેન્જ; પ્રીસેટ; File → Export, Ctrl+E. હજી નહીં: ફિલ્મમાં અવાજ.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> પ્લગઇન <code>.c2plg</code>

શરૂ થયું નથી.

### <img alt="0%" src="https://img.shields.io/badge/0%25-555555?style=flat-square"> થીમ અને વર્કસ્પેસ

જાણી જોઈને પછી: એડિટરમાં સજાવવા લાયક કંઈ આવે ત્યાં સુધી એક જ દેખાવ.

**રિલીઝ માટે તૈયાર નથી.** પાયો — SFM વાપરે તે દરેક ફાઇલ ફોર્મેટ, યોગ્ય રીતે વાંચેલો અને સંપૂર્ણ ઇન્સ્ટોલેશન પર ચકાસેલો — હાજર અને પરીક્ષિત છે; સેશન ખોલી, ચલાવી, બદલી અને સાચવી શકાય છે. ખૂટે છે કામની *સુવિધા*: ગ્રાફ એડિટર, Source શેડિંગ, નકશા, નિકાસ. એનિમેટર તેમાં એક દિવસનું કામ કરી શકે ત્યાં સુધી કોઈ વર્ઝન નંબર નહીં.

<p align="center"><a href="../README/GU-in.md"><img alt="← README પર પાછા" src="https://img.shields.io/badge/%E2%86%90_README_%E0%AA%AA%E0%AA%B0_%E0%AA%AA%E0%AA%BE%E0%AA%9B%E0%AA%BE-1b2838?style=for-the-badge"></a></p>
