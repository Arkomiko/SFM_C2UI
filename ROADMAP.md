# SFM – C2UI · Карта действий (ROADMAP)

> **C2UI** — *Custom to User Interface*. Современная, гибкая, открытая оболочка над Source Filmmaker.
> Хост: Python 3.10+ / PySide6 (Qt6). Мост: агент на Python 2.7 / PySide 1.2 (Qt4) **внутри** процесса `sfm.exe` + C++ (pybind11) для Win32-интеграции.

Легенда: `[ ]` — не начато · `[~]` — в работе · `[x]` — готово

---

## Этап 0 — Разведка окружения `[x]`
- [x] SFM SDK: `game/sdktools/python/2.7` (Python 2.7 + PySide 1.2 / Qt 4.8), `vs`, `sfm`, `sfmApp`
- [x] Точка внедрения: `game/usermod/scripts/sfm/sfm_init.py` (авто-запуск при старте SFM)
- [x] Формат нативных лейаутов SFM: `game/platform/tools/layouts/sfm/layout*.ini` (имена панелей: *Primary Viewport, Animation Set Editor, Element Viewer, Timestrip, Console* …)
- [x] Python 3.14 + PySide6 6.11.2 → `C2UI_SDK/.venv`
- [x] Компилятор MSVC отсутствует (есть CMake) → C++ модуль с ctypes-фолбэком

## Этап 1 — Фундамент: скелет, 4 менеджера, UE5-лейаут `[x]`
- [x] Структура каталогов строго по ТЗ
- [x] `main.py` — точка входа, аргументы (`--workspace`, `--theme`, `--lang`, `--safe-mode`)
- [x] `Core/Library/paths.py`, `settings.py`, `events.py` (EventBus), `logging_setup.py`, `localization.py`
- [x] **ThemeManager** — JSON-токены → QSS-шаблон (`Themes/base.qss`), QPalette, hot-reload
- [x] **LayoutManager** — JSON-лейаут → QDockWidget-дерево, сохранение/восстановление состояния
- [x] **ContextManager** — реестр действий, контекст-пресеты (режимы), горячие клавиши, контекстные меню, выделение
- [x] **WorkspaceManager** — обнаружение и активация workspace (тема + лейаут + контексты + меню + тулбар)
- [x] Реестр панелей + встроенные панели UE5-стиля: Viewport, Outliner, Details, Content Browser, Output Log, Timeline (Sequencer)
- [x] `Workspaces/UnrealEditor` — дефолтный workspace; `UWP`, `AAE` — заготовки
- [x] `Themes/ue5_dark.json` (+ `uwp_dark`, `uwp_light`, `aae_dark`), `Themes/base.qss`
- [x] `Locales/en.json`, `Locales/ru.json`
- [x] `Assets/icons/*.svg` (перекрашиваемые через `currentColor`)
- [x] `Core/Scripts` — загрузчик плагинов + пример `example_hello`
- [x] `Core/API` — каркас моста: протокол, лаунчер `sfm.exe`, клиент (offline-режим)
- [x] `setup.bat` / `run.bat`, `requirements.txt`, `README.md`

## Этап 2 — API-мост: агент внутри SFM ↔ хост `[x]`
- [x] `Core/API/agent/c2ui_agent.py` (Py2.7 / PySide 1.2 / Qt 4.8): JSON-RPC сервер на `QtNetwork.QTcpServer` в GUI-потоке SFM; методы `c2ui.*`, `sfm.*`; события `state_changed`; `sfm.exec`/`eval`, интроспекция `api_dir`; горячая перезагрузка
- [x] `install_agent` — безопасный маркированный хук в `usermod/scripts/sfm/sfm_init.py` (+ бэкап `.c2ui.bak`, пункт меню `mainmenu/C2UI/`, `--uninstall`/`--status`)
- [x] `bridge.py` (Py3): асинхронный клиент на `QTcpSocket`, авто-реконнект, `call`/`call_sync`, события SFM → EventBus; offline-деградация
- [x] `SFMSession` — оркестрация: запуск SFM (+авто-снятие диалога «Missing Mods»), авто-установка агента, connect→handshake→embed/theme
- [x] Встраивание нативного вьюпорта SFM (agent detach HWND → `QWindow.fromWinId` + `createWindowContainer`); guard-таймер геометрии; корректный release
- [x] Перекраска нативных Qt4-виджетов SFM темой C2UI (`Themes/sfm_native.qss`, hot-sync при смене темы)
- [x] `Core/API/native` — pybind11-модуль `c2ui_native.cpp` + CMake/`build.bat`; **ctypes-фолбэк `win32.py`** активен (компилятор не требуется)
- [x] Транспорт из хоста → SFM (play/pause/stop/step/jump), эвристика «playing», живой playhead и статус-бар
- [x] Проверено вживую: запуск sfm.exe, загрузка сессии, встраивание вьюпорта, воспроизведение, синхронизация темы
- [x] **C2UI автономен от SFM**: путь к SFM задаётся в настройках (`sfm.root`), автопоиск по Steam-библиотекам (реестр + `libraryfolders.vdf`), валидация папки, запуск без SFM без единой ошибки
- [x] Диалог **Настройки** (SFM / Внешний вид / Дополнительно) с выбором папки SFM, кнопкой «Найти» и живой проверкой
- [x] Ненавязчивый баннер «укажите путь к SFM» + пустые состояния в Браузере контента и вьюпорте; SFM-действия отключаются с подсказкой-причиной
- [x] Оптимизация и исправление ошибок (см. раздел ниже)

## Этап 3 — Живые панели `[~]`
- [ ] Outliner ← Animation Sets / DAG (через мост)
- [ ] Details ← атрибуты выбранного элемента (Element Viewer)
- [~] Timeline ← playhead и транспорт готовы; осталось: реальные shots / film clips / треки из сессии
- [x] Output Log ← ввод команд в SFM (`sfm.exec`, stdout захватывается); осталось: зеркалирование консоли SFM
- [ ] Content Browser ← `usermod`, VPK-браузер, drag&drop моделей в сцену

## Этап 4 — Workspaces & кастомизация `[ ]`
- [ ] `UWP` (Windows 11 Fluent) и `AAE` (After Effects) — полноценные лейауты/темы
- [ ] Редактор тем (live-редактирование токенов), импорт/экспорт
- [ ] Пользовательские лейауты: сохранение/переключение/сброс; per-workspace
- [ ] DaVinci Resolve workspace

## Этап 5 — Скрипты, плагины, макросы `[ ]`
- [ ] Стабильный Plugin API (`c2ui.api`): панели, действия, меню, хуки событий
- [ ] Командная палитра (Ctrl+Shift+P), редактор горячих клавиш
- [ ] Макро-рекордер (запись действий → Python-скрипт), выполнение в SFM

## Этап 6 — Сборка и дистрибуция `[ ]`
- [ ] Сборка C++ модуля (MSVC / clang-cl), CI
- [ ] PyInstaller-пакет, инсталлятор, автообновление
- [ ] Документация, вики, шаблон плагина

---

## Найденные и исправленные ошибки (ревизия структуры)

| # | Где | Проблема | Исправление |
|---|-----|----------|-------------|
| 1 | `Core/Library/paths.py` | Пути к SFM были константами уровня модуля — при отсутствии SFM приложение работало на мусорных путях, а сменить путь в рантайме было невозможно | Пути стали функциями (`sfm_root()`, `sfm_exe()`…) с валидацией, автопоиском и `None` при отсутствии; старые константы сохранены через `__getattr__` |
| 2 | `Core/API/agent/c2ui_agent.py` | `_poll_state` был **удалён** ошибочной заменой диапазона → таймер бил в несуществующий метод, события `state_changed` не приходили | Метод восстановлен; поллинг дополнительно перезапускается при подключении клиента |
| 3 | `Core/Library/app.py`, `timeline.py` | Обработчики событий читали кадр из `payload`, а приходило `{"state":…, "changed":…}` → playhead не двигался | Распаковка `payload["state"]` |
| 4 | `Core/Library/layout_manager.py` | При закрытии окна `visibilityChanged` дока стрелял в уже удалённый C++ QTimer → `RuntimeError` в консоль | Флаг `_closing` + защищённый `_schedule_title_refresh()` |
| 5 | `Core/Library/events.py` | `_dispatch` итерировал живой словарь подписок — подписка из обработчика роняла шину | Итерация по снимку `list(...)` |
| 6 | `Core/Library/icons.py` | Прозрачность иконок писалась в SVG как `#AARRGGBB` — вне стандарта SVG, риск чёрных иконок | Переведено на `rgba(r,g,b,a)` |
| 7 | `output_log.py` + `logging_setup.py` | Маркер «очищено» хранил длину **ограниченной** очереди → после 2000 строк журнал обрезался неверно | Абсолютный счётчик `sink.total` и пересчёт смещения |
| 8 | `Core/API/session.py` | Автозакрытие стартового диалога SFM двигало **физическую мышь** пользователя | `BM_CLICK` напрямую в кнопку через `EnumChildWindows` |
| 9 | `Core/Library/panels/*` | Подписки на EventBus жили дольше панели → обращение к удалённому виджету | `C2UIPanel.subscribe()` с авто-отпиской по `destroyed` |
| 10 | `Core/Library/ui/banner.py`, `context_manager.py` | `signal.disconnect()` без подключения → `RuntimeWarning` от PySide | Отслеживание факта подключения |
| 11 | `main_window.py`, `app.py` | Обращение к приватным `layout._central_id`, `window._toolbar_spec` из других модулей | Публичные свойства `central_id`, `toolbar_spec`, `menu_spec` |
| 12 | `Core/API/agent/` | Отсутствовал `__init__.py` (работало только через namespace-пакеты) | Файл добавлен |
| 13 | `install_agent.py` | Падал с `AttributeError`, если SFM не настроен | `SFMNotFound`, безопасные `Optional[Path]`, флаг `--path` |
| 14 | `settings.py` | Запись на диск при каждом изменении; при сбое — обрезанный JSON | Debounce 400 мс + атомарная запись через временный файл |
| 15 | `theme_manager.py` | 73 SVG перезаписывались при каждой смене темы | Пропуск, если цвет тинта не изменился |
| 16 | `app.py` | Смена темы полностью пересобирала тулбары | `context.refresh_icons()` + `window.retheme()` — виджеты остаются |
| 17 | `localization.py` | Список локалей перечитывался с диска при каждом открытии меню | Кэш с явным `refresh=True` |
| 18 | Агент | `playing` мог быть `true` без загруженной сессии | Привязано к `has_document` |
| 19 | по проекту | Мёртвые импорты (pyflakes) | Удалены |
