# Il launcher di C2UI

<details align="center"><summary>&nbsp;🌐 <b>🇮🇹 Italiano</b> &nbsp;·&nbsp; <sub>Language · Язык · 語言 · Idioma · Sprache · भाषा · لغة</sub></summary>

<table align="center">
<tr><td align="center"><a href="RU-ru.md">🇷🇺<br>Русский</a></td><td align="center"><a href="EN-en.md">🇬🇧<br>English</a></td><td align="center"><a href="PL-pl.md">🇵🇱<br>Polski</a></td><td align="center"><a href="UK-ua.md">🇺🇦<br>Українська</a></td><td align="center"><a href="DE-de.md">🇩🇪<br>Deutsch</a></td><td align="center"><a href="RO-md.md">🇲🇩<br>Moldovenească</a></td><td align="center"><a href="SL-si.md">🇸🇮<br>Slovenščina</a></td><td align="center"><a href="BE-by.md">🇧🇾<br>Беларуская</a></td></tr>
<tr><td align="center"><a href="KK-kz.md">🇰🇿<br>Қазақша</a></td><td align="center"><a href="JA-jp.md">🇯🇵<br>日本語</a></td><td align="center"><a href="ZH-cn.md">🇨🇳<br>中文</a></td><td align="center"><a href="SV-se.md">🇸🇪<br>Svenska</a></td><td align="center"><a href="ES-es.md">🇪🇸<br>Español</a></td><td align="center"><a href="HI-in.md">🇮🇳<br>हिन्दी</a></td><td align="center"><a href="PT-pt.md">🇵🇹<br>Português</a></td><td align="center"><a href="BN-bd.md">🇧🇩<br>বাংলা</a></td></tr>
<tr><td align="center"><a href="FR-fr.md">🇫🇷<br>Français</a></td><td align="center"><a href="TE-in.md">🇮🇳<br>తెలుగు</a></td><td align="center"><a href="MR-in.md">🇮🇳<br>मराठी</a></td><td align="center"><a href="TA-in.md">🇮🇳<br>தமிழ்</a></td><td align="center"><a href="TR-tr.md">🇹🇷<br>Türkçe</a></td><td align="center"><a href="UR-pk.md">🇵🇰<br>اردو</a></td><td align="center"><a href="VI-vn.md">🇻🇳<br>Tiếng Việt</a></td><td align="center"><a href="GU-in.md">🇮🇳<br>ગુજરાતી</a></td></tr>
<tr><td align="center"><b>🇮🇹<br>Italiano</b></td><td align="center"><a href="KO-kr.md">🇰🇷<br>한국어</a></td><td align="center"><a href="AR-sa.md">🇸🇦<br>العربية</a></td><td align="center"><a href="JV-id.md">🇮🇩<br>Basa Jawa</a></td><td align="center"><a href="ML-in.md">🇮🇳<br>മലയാളം</a></td><td align="center"><a href="NE-np.md">🇳🇵<br>नेपाली</a></td><td align="center"><a href="UZ-uz.md">🇺🇿<br>Oʻzbekcha</a></td><td align="center"><a href="OR-in.md">🇮🇳<br>ଓଡ଼ିଆ</a></td></tr>
</table>

</details>

`Launcher/` è da dove parte il progetto: una piccola finestra scura con un titolo, una riga di descrizione e tre pulsanti. Si compila in un unico eseguibile che non richiede Python installato e trova il progetto da solo — risale da dove si trova finché non vede insieme `App`, `Core` e `Launcher`.

<p align="center"><img src="../assets/launcher.png" alt="Il launcher di C2UI" width="562"><br><sub>La finestra del launcher: il titolo «Dev-mode», la riga di descrizione e tre pulsanti.</sub></p>

> [!NOTE]
> **L'interfaccia del launcher è per ora solo in russo: è una soluzione provvisoria.** Titolo, descrizione e scritte dei pulsanti sono scritti nel codice; le traduzioni arriveranno con la localizzazione dell'editor (`Tools/Localization`), quando il launcher sarà riscritto per un App finito. Il resto della documentazione del progetto è già in 32 lingue.

## I tre pulsanti

| | |
|---|---|
| <code>Запустить Core</code> | Avvia l'editor — la finestra di C2UI con viewport, timeline e pannelli. |
| <code>Запустить App</code> | Disattivato: un App separato non c'è ancora. |
| <code>Выйти</code> | Chiude il launcher. |

## Avvio dai sorgenti

Servono Windows, Python 3.13 e un'installazione di Source Filmmaker.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r Launcher/requirements.txt
.venv/Scripts/python.exe Launcher/launcher.py
```

Costruzione del file unico `Launcher/Launcher-C2UI.exe` (non tenuto in git: viene ricostruito dai sorgenti):

```bash
.venv/Scripts/python.exe -m pip install pyinstaller
.venv/Scripts/python.exe Launcher/build_exe.py
```

## Il motore senza l'editor

`Launcher/core.py` avvia `Core` da solo: monta un'installazione, la indicizza e offre una piccola shell sul motore — modelli, materiali, texture, mappe, sessioni e la loro valutazione. Anche questo è provvisorio: quando App potrà girare senza finestra, l'editor diventerà l'unico punto d'ingresso.

```bash
python Launcher/core.py
python Launcher/core.py model models/player/hwm/heavy.mdl
python Launcher/core.py map afd_warehouse
python Launcher/core.py eval <session.dmx> 6.0
```

## Cosa cambierà

- La finestra sarà riscritta con App, aspetto e traduzioni compresi.
- Il pulsante «Запустить App» comincerà a funzionare.
- `core.py` sparirà quando l'editor potrà partire senza finestra.
- L'`.exe` compilato accompagnerà le release su GitHub.

<p align="center"><a href="../README/IT-it.md"><img alt="← Torna al README" src="https://img.shields.io/badge/%E2%86%90_Torna_al_README-1b2838?style=for-the-badge"></a></p>
