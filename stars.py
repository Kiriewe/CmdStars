import os
import sys
import time
import math
import msvcrt
import random

# Включаем поддержку UTF-8 и ANSI цветов / Enable UTF-8 and ANSI escape codes on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
os.system('')

# ANSI коды управления экраном / Console control sequences
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CURSOR_HOME = "\033[H"
CLEAR_SCREEN = "\033[2J"
COLOR_RESET = "\033[0m"

# База данных созвездий (в нормализованных координатах [-0.9, 0.9])
# Constellations coordinates database
CONSTELLATIONS = [
    {
        "name": "Ursa Major",
        "rus_name": "Большая Медведица",
        "stars": [(-0.6, -0.6), (-0.53, -0.48), (-0.45, -0.45), (-0.35, -0.32), (-0.3, -0.1), (-0.05, -0.05), (-0.1, -0.28)],
        "links": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 3)],
        "is_zodiac": False
    },
    {
        "name": "Orion",
        "rus_name": "Орион",
        "stars": [(0.4, -0.5), (0.6, -0.45), (0.46, -0.2), (0.5, -0.2), (0.54, -0.2), (0.42, 0.1), (0.62, 0.15)],
        "links": [(0, 2), (2, 5), (1, 4), (4, 6), (2, 3), (3, 4), (0, 1), (5, 6)],
        "is_zodiac": False
    },
    {
        "name": "Cassiopeia",
        "rus_name": "Кассиопея",
        "stars": [(-0.7, 0.4), (-0.5, 0.52), (-0.35, 0.45), (-0.2, 0.58), (-0.05, 0.5)],
        "links": [(0, 1), (1, 2), (2, 3), (3, 4)],
        "is_zodiac": False
    },
    {
        "name": "Leo",
        "rus_name": "Лев",
        "stars": [(0.1, 0.4), (0.25, 0.35), (0.35, 0.48), (0.25, 0.58), (0.1, 0.6), (0.0, 0.5)],
        "links": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)],
        "is_zodiac": True
    },
    {
        "name": "Scorpius",
        "rus_name": "Скорпион",
        "stars": [(0.5, 0.5), (0.65, 0.45), (0.72, 0.58), (0.65, 0.72), (0.5, 0.8), (0.4, 0.72), (0.35, 0.6)],
        "links": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)],
        "is_zodiac": True
    },
    {
        "name": "Taurus",
        "rus_name": "Телец",
        "stars": [(-0.8, 0.1), (-0.65, 0.05), (-0.55, -0.05), (-0.65, -0.15), (-0.8, -0.2)],
        "links": [(0, 1), (1, 2), (2, 3), (3, 4)],
        "is_zodiac": True
    },
    {
        "name": "Gemini",
        "rus_name": "Близнецы",
        "stars": [(-0.4, -0.6), (-0.3, -0.5), (-0.2, -0.45), (-0.5, -0.55), (-0.4, -0.45), (-0.3, -0.4)],
        "links": [(0, 1), (1, 2), (3, 4), (4, 5), (0, 3)],
        "is_zodiac": True
    }
]

# Цветовые темы / Theme color definitions
THEME_BG = {
    1: (0, 0, 0),        # Classic: черный
    2: (0, 0, 35),       # Deep Sky: темно-синий
    3: (25, 0, 45),      # Nebula: темно-фиолетовый
    4: (20, 10, 0),      # Gold: темно-коричневый
    5: (0, 0, 0)         # Matrix: черный
}

THEME_STARS = {
    1: (255, 255, 255),  # Classic: белые
    2: (160, 220, 255),  # Deep Sky: голубоватые
    3: (255, 140, 90),   # Nebula: оранжево-красные
    4: (255, 215, 0),    # Gold: золотые
    5: (0, 255, 60)      # Matrix: зеленые
}

THEME_LINES = {
    1: (90, 90, 90),     # Classic: серые
    2: (0, 100, 200),    # Deep Sky: синие
    3: (160, 0, 160),    # Nebula: пурпурные
    4: (170, 120, 15),   # Gold: желто-коричневые
    5: (0, 130, 30)      # Matrix: зеленые
}

class Star:
    """Класс звезды с фазой мерцания и цветовой температурой"""
    def __init__(self, x, y, is_constellation=False):
        self.x = x
        self.y = y
        self.is_constellation = is_constellation
        self.base_brightness = random.uniform(0.5, 1.0) if is_constellation else random.uniform(0.15, 0.8)
        self.phase = random.uniform(0, 2 * math.pi)
        
        # Спектральный класс звезд (цветовая температура для realistic-режима)
        # Spectral colors: 60% White, 25% Hot Blue, 15% Cool Red/Orange
        rand = random.random()
        if rand < 0.60:
            self.spectral_color = (255, 255, 240) # White/Ivory
        elif rand < 0.85:
            self.spectral_color = (170, 220, 255) # Blue/Cyan
        else:
            self.spectral_color = (255, 130, 90)  # Orange/Red

def load_config():
    """Загружает конфигурационные параметры из config.txt."""
    cfg = {
        'theme': 1,
        'render_mode': 'classic',
        'rotation_speed': 1.0,
        'twinkle_speed': 1.5,
        'show_all': True,
        'show_zodiac': True,
        'star_count': 250,
        'aspect': 2.0
    }
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.txt")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, val = line.split('=', 1)
                        key = key.strip().lower()
                        val = val.strip()
                        
                        if key == 'theme':
                            cfg['theme'] = max(1, min(5, int(val)))
                        elif key == 'render_mode':
                            cfg['render_mode'] = val.lower() if val.lower() in ('classic', 'realistic') else 'classic'
                        elif key == 'rotation_speed':
                            cfg['rotation_speed'] = float(val)
                        elif key == 'twinkle_speed':
                            cfg['twinkle_speed'] = float(val)
                        elif key == 'show_all':
                            cfg['show_all'] = (val.lower() == 'true')
                        elif key == 'show_zodiac':
                            cfg['show_zodiac'] = (val.lower() == 'true')
                        elif key == 'star_count':
                            cfg['star_count'] = max(50, min(500, int(val)))
                        elif key == 'aspect':
                            cfg['aspect'] = float(val)
        except Exception:
            pass
    return cfg

def draw_dotted_line(x1, y1, x2, y2, char, color, grid, width, height):
    """
    Рисует пунктирную линию методом линейной интерполяции.
    Dotted line rendering using linear interpolation.
    """
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return
        
    for i in range(1, steps):
        t = i / steps
        sx = int(x1 + dx * t)
        sy = int(y1 + dy * t)
        if 0 <= sx < width and 0 <= sy < height:
            # Линии рисуются только на пустых местах, не перебивая звезды
            # Constellation guides should never overwrite bright stars
            if grid[sy][sx][1] == ' ' or grid[sy][sx][1] in ('░', '▒', '·', '.'):
                grid[sy][sx] = (color, char)

def main():
    # Кэшируем тригонометрические функции в локальные для FPS оптимизации
    sin = math.sin
    cos = math.cos
    sqrt = math.sqrt
    
    # Очищаем консоль и скрываем курсор / Clear screen and hide cursor
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()
    
    # Загружаем настройки / Load settings
    cfg = load_config()
    theme_id = cfg['theme']
    last_config_theme = cfg['theme']
    render_mode = cfg['render_mode']
    
    # Режимы отображения созвездий / Display modes
    show_all = cfg['show_all']
    show_zodiac = cfg['show_zodiac']
    highlight_idx = None  # None - все созвездия равны, int - индекс выделенного
    
    # Параметры анимации / Animation variables
    angle = 0.0
    t = 0.0
    prev_width, prev_height = 0, 0
    paused = False
    global_speed = 1.0
    frame_count = 0
    
    # Инициализация звезд созвездий / Instantiate constellation stars
    const_stars_lists = []
    for c in CONSTELLATIONS:
        stars_list = [Star(x, y, is_constellation=True) for x, y in c["stars"]]
        const_stars_lists.append(stars_list)
        
    # Инициализация фоновых звезд / Background random field stars
    bg_stars = [Star(random.uniform(-1.6, 1.6), random.uniform(-1.6, 1.6)) for _ in range(cfg['star_count'])]
    
    # Инициализация частиц Млечного Пути (Nebula dust band)
    # 60 nebula dust particles clustered along rotated diagonal line
    nebula_dust = []
    for _ in range(60):
        nx = random.uniform(-1.5, 1.5)
        ny = nx * 0.55 + random.uniform(-0.28, 0.28)
        nebula_dust.append(Star(nx, ny))
        
    # Метеор (падающая звезда) / Shooting star properties
    meteor_active = False
    meteor_x, meteor_y = 0.0, 0.0
    meteor_vx, meteor_vy = 0.0, 0.0
    meteor_life = 0
    
    try:
        while True:
            # Чтение клавиатуры (неблокирующее) / Non-blocking key poll
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch == b'\x1b' or ch in (b'q', b'Q', b'\x03'): # ESC, q, Ctrl+C
                    break
                elif ch == b' ':
                    paused = not paused
                elif ch in (b'z', b'Z'):
                    show_zodiac = not show_zodiac
                elif ch in (b'a', b'A'):
                    show_all = not show_all
                elif ch in (b'v', b'V'):
                    # Переключение режима рендеринга (Classic vs Realistic)
                    render_mode = 'realistic' if render_mode == 'classic' else 'classic'
                    sys.stdout.write(CLEAR_SCREEN)
                    sys.stdout.flush()
                elif ch in (b'c', b'C'):
                    # Циклическое переключение фокуса созвездий
                    if highlight_idx is None:
                        highlight_idx = 0
                    else:
                        highlight_idx += 1
                        if highlight_idx >= len(CONSTELLATIONS):
                            highlight_idx = None
                elif ch in (b'+', b'='):
                    global_speed = min(4.0, global_speed + 0.2)
                elif ch in (b'-', b'_'):
                    global_speed = max(-4.0, global_speed - 0.2)
                elif ch in (b'1', b'2', b'3', b'4', b'5'):
                    theme_id = int(ch.decode('utf-8'))
                    last_config_theme = theme_id
                    sys.stdout.write(CLEAR_SCREEN)
                    sys.stdout.flush()
                    prev_width = 0
            
            # Читаем конфиг раз в две секунды / Poll config file periodically
            frame_count += 1
            if frame_count % 60 == 0:
                new_cfg = load_config()
                if new_cfg['theme'] != last_config_theme:
                    theme_id = new_cfg['theme']
                    last_config_theme = new_cfg['theme']
                    sys.stdout.write(CLEAR_SCREEN)
                    sys.stdout.flush()
                    prev_width = 0
                    
                # При изменении количества звезд в файле, пересоздаем массив
                if new_cfg['star_count'] != len(bg_stars):
                    bg_stars = [Star(random.uniform(-1.6, 1.6), random.uniform(-1.6, 1.6)) for _ in range(new_cfg['star_count'])]
                    
                cfg = new_cfg
                
            # Размеры терминала / Get current terminal size
            try:
                width, height = os.get_terminal_size()
            except Exception:
                width, height = 80, 25
                
            if width < 5 or height < 5:
                sys.stdout.write(CURSOR_HOME + "Terminal window too small / Окно слишком мало")
                sys.stdout.flush()
                time.sleep(0.1)
                continue
                
            # Очистка экрана при ресайзе консоли
            if width != prev_width or height != prev_height:
                sys.stdout.write(CLEAR_SCREEN)
                sys.stdout.flush()
                prev_width = width
                prev_height = height
                
            # Коэффициент коррекции шрифта и центр
            aspect = cfg.get('aspect', 2.0)
            cx = width / 2.0
            cy = height / 2.0
            
            # Базовые цвета активной темы / Active theme parameters
            rgb_bg = THEME_BG.get(theme_id, (0, 0, 0))
            rgb_star = THEME_STARS.get(theme_id, (255, 255, 255))
            rgb_line = THEME_LINES.get(theme_id, (100, 100, 100))
            bg_ansi = f"\033[48;2;{rgb_bg[0]};{rgb_bg[1]};{rgb_bg[2]}m"
            
            # Вращение звездного неба
            if not paused:
                angle += 0.003 * cfg['rotation_speed'] * global_speed
                t += 0.05 * abs(global_speed)
                
            # --- Логика спавна и движения метеора ---
            if not paused:
                if not meteor_active and random.random() < 0.012:
                    meteor_active = True
                    meteor_x = random.uniform(-1.0, 1.0)
                    meteor_y = random.uniform(-1.0, -0.2)
                    meteor_vx = random.choice([-0.06, 0.06])
                    meteor_vy = random.uniform(0.04, 0.08)
                    meteor_life = random.randint(10, 20)
                elif meteor_active:
                    meteor_x += meteor_vx
                    meteor_y += meteor_vy
                    meteor_life -= 1
                    if meteor_life <= 0:
                        meteor_active = False
            
            # Виртуальный холст для сборки кадра
            grid = [[(None, ' ') for _ in range(width)] for _ in range(height)]
            
            # 1. Отрисовка Млечного Пути / Milky Way Nebula band (Realistic mode only)
            # Renders as a rotating faint dust cloud
            if render_mode == 'realistic':
                # Яркость пылевого облака мягко колышется со временем
                nebula_glow = 0.12 + 0.05 * sin(t * 0.4)
                for d in nebula_dust:
                    rx = d.x * cos(angle) - d.y * sin(angle)
                    ry = d.x * sin(angle) + d.y * cos(angle)
                    
                    sx = int(cx + rx * (height / 2.0) * aspect)
                    sy = int(cy + ry * (height / 2.0))
                    
                    if 0 <= sx < width and 0 <= sy < height:
                        # Пылинки видны только на пустых клетках
                        if grid[sy][sx][1] == ' ':
                            char = random.choice(['░', '·'])
                            # Подмешиваем цвет туманности (из цвета линий темы)
                            r = int(rgb_line[0] * nebula_glow)
                            g = int(rgb_line[1] * nebula_glow)
                            b = int(rgb_line[2] * nebula_glow)
                            grid[sy][sx] = ((r, g, b), char)
            
            # 2. Расчет и прорисовка фоновых звезд / Render background stars
            twinkle_sp = cfg['twinkle_speed']
            for s in bg_stars:
                rx = s.x * cos(angle) - s.y * sin(angle)
                ry = s.x * sin(angle) + s.y * cos(angle)
                
                sx = int(cx + rx * (height / 2.0) * aspect)
                sy = int(cy + ry * (height / 2.0))
                
                if 0 <= sx < width and 0 <= sy < height:
                    brightness = s.base_brightness * (0.6 + 0.4 * sin(t * twinkle_sp + s.phase))
                    brightness = max(0.1, min(1.0, brightness))
                    
                    # Цветовой маппинг
                    if render_mode == 'realistic':
                        # Цветовая температура: горячие/белые/красные оттенки
                        base_col = s.spectral_color
                        # Определение символа в зависимости от плотности блоков
                        if brightness > 0.9:
                            char = '█'
                        elif brightness > 0.7:
                            char = '▓'
                        elif brightness > 0.5:
                            char = '▒'
                        elif brightness > 0.3:
                            char = '░'
                        else:
                            char = '·'
                    else:
                        base_col = rgb_star
                        if brightness > 0.8:
                            char = '★'
                        elif brightness > 0.55:
                            char = '•'
                        elif brightness > 0.38:
                            char = '*'
                        elif brightness > 0.2:
                            char = '·'
                        else:
                            char = '.'
                            
                    r = int(base_col[0] * brightness)
                    g = int(base_col[1] * brightness)
                    b = int(base_col[2] * brightness)
                    
                    # Записываем звезду в буфер
                    grid[sy][sx] = ((r, g, b), char)
                    
                    # Добавляем ореол свечения для ярких звезд в realistic-режиме
                    # Halo glow overlay in realistic mode
                    if render_mode == 'realistic' and brightness > 0.85:
                        halo_col = (int(r * 0.15), int(g * 0.15), int(b * 0.15))
                        for hdx, hdy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            nsx, nsy = sx + hdx, sy + hdy
                            if 0 <= nsx < width and 0 <= nsy < height:
                                if grid[nsy][nsx][1] == ' ':
                                    grid[nsy][nsx] = (halo_col, '░')
                                    
            # 3. Расчет и прорисовка звезд созвездий / Render constellation stars
            screen_coords = [[] for _ in range(len(CONSTELLATIONS))]
            
            for c_idx, c in enumerate(CONSTELLATIONS):
                stars_list = const_stars_lists[c_idx]
                is_focused = (highlight_idx == c_idx)
                
                for s_idx, s in enumerate(stars_list):
                    rx = s.x * cos(angle) - s.y * sin(angle)
                    ry = s.x * sin(angle) + s.y * cos(angle)
                    
                    sx = int(cx + rx * (height / 2.0) * aspect)
                    sy = int(cy + ry * (height / 2.0))
                    
                    screen_coords[c_idx].append((sx, sy))
                    
                    if 0 <= sx < width and 0 <= sy < height:
                        if highlight_idx is not None:
                            brightness = 1.0 if is_focused else 0.25
                        else:
                            brightness = s.base_brightness * (0.7 + 0.3 * sin(t * twinkle_sp + s.phase))
                        
                        brightness = max(0.1, min(1.0, brightness))
                        
                        if render_mode == 'realistic':
                            # Звезды созвездий - чистый яркий белый цвет для выделения
                            base_col = (255, 255, 255) if is_focused or highlight_idx is None else (120, 120, 120)
                            if brightness > 0.9:
                                char = '█'
                            elif brightness > 0.7:
                                char = '▓'
                            elif brightness > 0.5:
                                char = '▒'
                            elif brightness > 0.3:
                                char = '░'
                            else:
                                char = '·'
                        else:
                            base_col = rgb_star
                            if brightness > 0.75:
                                char = '★'
                            elif brightness > 0.5:
                                char = '•'
                            else:
                                char = '*'
                                
                        r = int(base_col[0] * brightness)
                        g = int(base_col[1] * brightness)
                        b = int(base_col[2] * brightness)
                        grid[sy][sx] = ((r, g, b), char)
                        
                        # Ореол для ярких созвездий
                        if render_mode == 'realistic' and brightness > 0.85:
                            halo_col = (int(r * 0.12), int(g * 0.12), int(b * 0.12))
                            for hdx, hdy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                                nsx, nsy = sx + hdx, sy + hdy
                                if 0 <= nsx < width and 0 <= nsy < height:
                                    if grid[nsy][nsx][1] == ' ':
                                        grid[nsy][nsx] = (halo_col, '░')
                                        
            # 4. Отрисовка соединительных линий созвездий / Draw connecting lines
            for c_idx, c in enumerate(CONSTELLATIONS):
                if not show_all:
                    if not (c["is_zodiac"] and show_zodiac):
                        continue
                else:
                    if c["is_zodiac"] and not show_zodiac:
                        continue
                        
                is_focused = (highlight_idx == c_idx)
                
                # Цвет линий / Adjust line intensity
                if highlight_idx is not None:
                    if is_focused:
                        line_color = (255, 255, 255)
                        line_char = '▒' if render_mode == 'realistic' else '•'
                    else:
                        continue
                else:
                    line_color = rgb_line
                    # В реалистичном режиме линии - это размытые тусклые блоки
                    # In realistic mode, lines are faint translucent shaded blocks
                    line_char = '░' if render_mode == 'realistic' else '·'
                    
                # Рисуем все ребра созвездия
                for start_star, end_star in c["links"]:
                    pt1 = screen_coords[c_idx][start_star]
                    pt2 = screen_coords[c_idx][end_star]
                    draw_dotted_line(pt1[0], pt1[1], pt2[0], pt2[1], line_char, line_color, grid, width, height)
                    
            # 5. Прорисовка зодиакального пояса (эклиптики)
            if show_zodiac and highlight_idx is None:
                zodiac_indices = [idx for idx, c in enumerate(CONSTELLATIONS) if c["is_zodiac"]]
                zodiac_centers = []
                for z_idx in zodiac_indices:
                    coords = screen_coords[z_idx]
                    if coords:
                        avg_x = sum(pt[0] for pt in coords) / len(coords)
                        avg_y = sum(pt[1] for pt in coords) / len(coords)
                        zodiac_centers.append((int(avg_x), int(avg_y)))
                        
                if len(zodiac_centers) >= 2:
                    # Пунктирная линия эклиптики
                    ecliptic_color = (int(rgb_line[0] * 0.4), int(rgb_line[1] * 0.4), int(rgb_line[2] * 0.4))
                    ecl_char = '░' if render_mode == 'realistic' else '.'
                    for i in range(len(zodiac_centers)):
                        pt1 = zodiac_centers[i]
                        pt2 = zodiac_centers[(i + 1) % len(zodiac_centers)]
                        draw_dotted_line(pt1[0], pt1[1], pt2[0], pt2[1], ecl_char, ecliptic_color, grid, width, height)
                        
            # 6. Отрисовка падающего метеора
            if meteor_active:
                msx = int(cx + meteor_x * (height / 2.0) * aspect)
                msy = int(cy + meteor_y * (height / 2.0))
                if 0 <= msx < width and 0 <= msy < height:
                    grid[msy][msx] = ((255, 255, 255), '█' if render_mode == 'realistic' else '★')
                    trail_char = '\\' if meteor_vx > 0 else '/'
                    for i in range(1, 4):
                        tsx = int(msx - i * (meteor_vx * 15))
                        tsy = int(msy - i * (meteor_vy * 10))
                        if 0 <= tsx < width and 0 <= tsy < height:
                            scale = 1.0 - (i * 0.25)
                            color_val = int(255 * scale)
                            grid[tsy][tsx] = ((color_val, color_val, color_val), trail_char if i < 3 else '░')
                            
            # 7. Оверлей с образовательной плашкой названия (Отображается ТОЛЬКО при фокусе)
            # Render constellation title banner ONLY when focused
            if highlight_idx is not None:
                c_name = CONSTELLATIONS[highlight_idx]["name"]
                c_rus = CONSTELLATIONS[highlight_idx]["rus_name"]
                r_mode_label = "Realistic" if render_mode == 'realistic' else "Classic"
                label_text = f" [ Constellation: {c_rus} ({c_name}) | Mode: {r_mode_label} ] "
                
                for char_idx, char in enumerate(label_text):
                    if char_idx < width:
                        grid[0][char_idx] = ((rgb_star[0], rgb_star[1], rgb_star[2]), char)
            elif render_mode == 'realistic':
                # В реалистичном режиме пишем в углу режим
                label_text = " [ Mode: Realistic ] "
                for char_idx, char in enumerate(label_text):
                    if char_idx < width:
                        grid[0][char_idx] = ((int(rgb_star[0]*0.7), int(rgb_star[1]*0.7), int(rgb_star[2]*0.7)), char)
                        
            # Сборка кадра в строку без мерцания
            lines = []
            for y in range(height):
                row_parts = []
                current_color = None
                
                for x in range(width):
                    color, char = grid[y][x]
                    
                    if char == ' ':
                        if current_color is not None:
                            row_parts.append(COLOR_RESET)
                            current_color = None
                        row_parts.append(' ')
                    else:
                        if color != current_color:
                            row_parts.append(f"\033[38;2;{color[0]};{color[1]};{color[2]}m")
                            current_color = color
                        row_parts.append(char)
                        
                if current_color is not None:
                    row_parts.append(COLOR_RESET)
                lines.append("".join(row_parts))
                
            frame = bg_ansi + "\n".join(lines) + COLOR_RESET
            sys.stdout.write(CURSOR_HOME + frame)
            sys.stdout.flush()
            
            time.sleep(0.03)  # ~33 FPS
            
    except KeyboardInterrupt:
        pass
    finally:
        # Восстановление консоли / Restore terminal states
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.write(CURSOR_HOME)
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
