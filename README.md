# 🌌 CmdStars (Terminal Constellation Starfield Simulation)

**CmdStars** — это интерактивная консольная 3D-симуляция звездного неба и зодиакальных созвездий на Python. Небосвод медленно вращается вокруг Полярной оси, звезды мягко мерцают, по небу периодически пролетают метеоры, а яркие созвездия соединены пунктирными линиями. Программа поддерживает два режима рендеринга (векторный классический и реалистичный с блочным затенением, ореолами звезд и Млечным Путем), а также интерактивный выбор и подсветку созвездий.

**CmdStars** is an interactive terminal-based 3D starfield and constellation simulation written in Python. The sky rotates around the polar axis, stars twinkle, meteors dash randomly across the viewport, and constellations are linked with dotted guide paths. The project features two rendering pipelines (Classic vector stars and Realistic shaded blocks with glow halos and a rotating Milky Way band) and interactive educational highlight modes.

---

## ✨ Особенности / Features

*   **Суточное вращение небесной сферы / Sky Rotation**: Расчет координат по полярным формулам тригонометрии с автоматическим aspect-коэффициентом (`aspect = 2.0`) для сохранения идеальной круглой формы вращения на консольных шрифтах. Звезды спавнятся в расширенном радиусе `[-1.6, 1.6]`, чтобы плавно появляться в углах экрана при повороте.
*   **Два режима рендеринга / Two Render Modes**:
    *   `Classic` — Звезды отображаются традиционными символами разной величины (`★`, `•`, `*`, `·`, `.`), созвездия — тонкими точками.
    *   `Realistic` — Звезды рисуются символами плотности блоков (`█` → `▓` → `▒` → `░` → `·`). Добавляются **световые ореолы (Halos)** вокруг ярких звезд, **спектральные цвета звезд** (голубые гиганты, желтые и красные звезды) и вращающееся пылевое облако **Млечного Пути**.
*   **Интерактивное изучение созвездий / Constellation Highlight**:
    *   Смена фокуса на клавишу `C`. Выделенное созвездие вспыхивает контрастным цветом, остальные линии затухают, а в верхнем углу появляется образовательная плашка с названием (например, `[ Constellation: Orion (Орион) ]`).
    *   В обычном состоянии оверлей скрыт для сохранения чистой панорамы неба.
*   **Зодиакальный пояс / Ecliptic Belt**: Пунктирная линия эклиптики `.`, плавно соединяющая центры зодиакальных созвездий (Телец, Близнецы, Лев, Скорпион).
*   **Падающие звезды / Shooting Meteors**: Случайные быстрые росчерки по небу с угасающими motion-blur шлейфами (`\` / `/`).

---

## 🚀 Быстрый старт / Quick Start

1.  Убедитесь, что у вас установлен Python 3.
    Ensure you have Python 3 installed.
2.  Запустите программу через файл **`run.bat`** (или выполните команду `python stars.py` в консоли).
    Run the simulation via **`run.bat`** (or execute `python stars.py` in your terminal).
3.  **Клавиши управления / Controls**:
    *   `1` – `5` : Сменить цветовую тему (Switch color theme).
    *   `V` : Переключить режим рендеринга (Toggle Classic / Realistic rendering).
    *   `C` : Циклически переключать фокус на конкретное созвездие (Cycle constellation highlight).
    *   `A` : Включить / выключить линии всех созвездий (Toggle all constellation lines).
    *   `Z` : Включить / выключить зодиакальный пояс и линии эклиптики (Toggle zodiac belt lines).
    *   `+` / `-` : Увеличить / уменьшить скорость вращения неба (Speed up / slow down rotation).
    *   `Пробел / Spacebar` : Пауза / продолжение вращения (Pause / Resume).
    *   `Q` / `ESC` : Выход (Quit).

---

## 🛠️ Настройка / Configuration (`config.txt`)

Настраивайте параметры снегопада в файле `config.txt`:
Configure the snowfall settings in the `config.txt` file:

*   `theme`: Номер стартовой темы (1–5).
*   `render_mode`: Режим рендеринга звездного неба (`classic` или `realistic`).
*   `rotation_speed`: Базовая скорость вращения неба.
*   `twinkle_speed`: Базовая скорость мерцания звезд.
*   `show_all`: Показывать ли все созвездия по умолчанию при старте.
*   `show_zodiac`: Показывать ли зодиакальный пояс по умолчанию.
*   `star_count`: Количество свободно мерцающих фоновых звезд.
*   `aspect`: Коррекция соотношения сторон под ваш шрифт консоли.

---

## 📄 Лицензия / License

Этот проект распространяется под свободной лицензией **MIT License**. Подробнее см. в файле `LICENSE`.
This project is licensed under the **MIT License** - see the `LICENSE` file for details.
