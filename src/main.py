import pygame
import sys
import random
import math
import os

import subprocess

def update_launcher_if_needed():
    new_launcher = "launcher_new.exe"
    current_launcher = "Shadow Stocks.exe"
    updater_exe = "updater.exe"

    if os.path.exists(new_launcher) and os.path.exists(updater_exe):
        try:
            print("Найден новый лаунчер. Запускаем обновление...")
            subprocess.Popen([updater_exe, current_launcher, new_launcher])
            sys.exit()
        except Exception as e:
            print(f"Ошибка при запуске updater.exe: {e}")
            sys.exit(1)

update_launcher_if_needed()

# Инициализация Pygame
if not pygame.get_init():
    print("Initializing pygame...")
    pygame.init()

# Проверка инициализации дисплея
if not pygame.display.get_init():
    print("Initializing display...")
    pygame.display.init()

print(f"Display driver: {pygame.display.get_driver()}")
print(f"Display info: {pygame.display.Info()}")

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 32
MENU_WIDTH = 300
MENU_PADDING = 50
GRAPH_WIDTH = 400
GRAPH_HEIGHT = 300
GRAPH_PADDING = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
HOVER_COLOR = (50, 50, 50)
LINE_COLOR = (100, 100, 100)
GRAPH_LINE_COLOR = WHITE  # Белый цвет для графика
GRAPH_GRID_COLOR = GRAY  # Серый цвет для сетки
GRAPH_BACKGROUND = (20, 20, 20)  # Очень темный фон для графика

# Шрифты
try:
    TITLE_FONT = pygame.font.Font("C:\\Windows\\Fonts\\consola.ttf", 48)
    MENU_FONT = pygame.font.Font("C:\\Windows\\Fonts\\consola.ttf", 24)
    GRAPH_FONT = pygame.font.Font("C:\\Windows\\Fonts\\consola.ttf", 16)
except:
    TITLE_FONT = pygame.font.Font(None, 48)
    MENU_FONT = pygame.font.Font(None, 24)
    GRAPH_FONT = pygame.font.Font(None, 16)

# Список возможных названий акций
STOCK_NAMES = [
    "SHADOW", "DARK", "NIGHT", "MOON", "STAR",
    "BLACK", "ECHO", "GHOST", "SPIRIT", "SOUL"
]

class StockGraph:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.points = []
        self.stock_name = random.choice(STOCK_NAMES)
        self.last_update = 0
        self.update_interval = 1000  # Обновление каждую секунду
        self.generate_data()
        
    def generate_data(self):
        # Генерируем случайные данные для графика
        self.points = []
        num_points = 50
        base_value = random.uniform(50, 200)  # Случайная начальная цена
        volatility = random.uniform(2, 8)  # Случайная волатильность
        
        for i in range(num_points):
            if i == 0:
                value = base_value
            else:
                # Добавляем случайное изменение с учетом предыдущего значения
                change = random.uniform(-volatility, volatility)
                value = self.points[-1] + change
                # Ограничиваем минимальное значение
                value = max(10, value)
            self.points.append(value)
    
    def update(self, current_time):
        # Обновляем данные каждую секунду
        if current_time - self.last_update > self.update_interval:
            self.last_update = current_time
            # Удаляем первую точку и добавляем новую
            self.points.pop(0)
            last_value = self.points[-1]
            volatility = random.uniform(2, 8)
            new_value = last_value + random.uniform(-volatility, volatility)
            new_value = max(10, new_value)
            self.points.append(new_value)
            
            # Случайно меняем название акции
            if random.random() < 0.1:  # 10% шанс смены названия
                self.stock_name = random.choice(STOCK_NAMES)
    
    def draw(self, screen):
        # Рисуем фон графика
        pygame.draw.rect(screen, GRAPH_BACKGROUND, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)
        
        # Рисуем сетку
        for x in range(self.rect.left, self.rect.right, 40):
            pygame.draw.line(screen, GRAPH_GRID_COLOR, (x, self.rect.top), (x, self.rect.bottom))
        for y in range(self.rect.top, self.rect.bottom, 40):
            pygame.draw.line(screen, GRAPH_GRID_COLOR, (self.rect.left, y), (self.rect.right, y))
        
        # Находим минимальное и максимальное значения для масштабирования
        if self.points:
            min_val = min(self.points)
            max_val = max(self.points)
            range_val = max_val - min_val
            
            # Определяем цвет графика на основе последнего изменения
            last_change = self.points[-1] - self.points[-2]
            line_color = (0, 255, 0) if last_change >= 0 else (255, 0, 0)  # Зеленый или красный
            
            # Рисуем линию графика
            points = []
            for i, value in enumerate(self.points):
                x = self.rect.left + (i / (len(self.points) - 1)) * (self.rect.width - 1)
                y = self.rect.bottom - ((value - min_val) / range_val) * (self.rect.height - 1)
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, line_color, False, points, 2)
        
        # Рисуем подписи
        if self.points:
            # Название акции
            name_text = GRAPH_FONT.render(self.stock_name, True, WHITE)
            screen.blit(name_text, (self.rect.left + 10, self.rect.top + 10))
            
            # Текущее значение
            current_value = self.points[-1]
            value_text = GRAPH_FONT.render(f"${current_value:.2f}", True, WHITE)
            screen.blit(value_text, (self.rect.right - 80, self.rect.top + 10))
            
            # Изменение
            change = current_value - self.points[0]
            change_color = (0, 255, 0) if change >= 0 else (255, 0, 0)
            change_text = GRAPH_FONT.render(f"{change:+.2f}", True, change_color)
            screen.blit(change_text, (self.rect.right - 80, self.rect.top + 30))

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.normal_font = MENU_FONT
        self.hover_font = pygame.font.Font("C:\\Windows\\Fonts\\consola.ttf", 28) if "consola.ttf" in pygame.font.get_fonts() else pygame.font.Font(None, 28)

    def draw(self, screen):
        # Проверяем наведение мыши
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Выбираем шрифт в зависимости от состояния наведения
        current_font = self.hover_font if self.is_hovered else self.normal_font
        
        # Рисуем текст
        text_surface = current_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        
        # Если наведено, рисуем серый прямоугольник под текстом
        if self.is_hovered:
            hover_rect = pygame.Rect(
                self.rect.x,
                self.rect.y,
                text_rect.width + 20,  # Ширина текста + отступы
                self.rect.height
            )
            pygame.draw.rect(screen, HOVER_COLOR, hover_rect)
        
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        # Обновляем состояние наведения
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            return self.action
        return None

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.graph = StockGraph(
            screen.get_width() - GRAPH_WIDTH - GRAPH_PADDING,
            screen.get_height() // 2 - GRAPH_HEIGHT // 2,
            GRAPH_WIDTH,
            GRAPH_HEIGHT
        )
        self.setup_buttons()

    def setup_buttons(self):
        button_height = 40
        start_y = (self.screen.get_height() - (button_height * 3 + 20 * 2)) // 2

        # Кнопка "Одиночная игра"
        self.buttons.append(Button(
            MENU_PADDING, start_y,
            MENU_WIDTH, button_height,
            "Одиночная игра",
            "start_game"
        ))

        # Кнопка "Настройки"
        self.buttons.append(Button(
            MENU_PADDING, start_y + button_height + 20,
            MENU_WIDTH, button_height,
            "Настройки",
            "settings"
        ))

        # Кнопка "Выход"
        self.buttons.append(Button(
            MENU_PADDING, start_y + (button_height + 20) * 2,
            MENU_WIDTH, button_height,
            "Выход",
            "exit"
        ))

    def update(self, current_time):
        self.graph.update(current_time)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC всегда возвращает в меню, независимо от текущего состояния
                    if self.game_state != "menu":
                        print("Escape key pressed - returning to menu")
                        self.game_state = "menu"
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_SPACE and self.game_state == "game":
                    x = random.randint(0, self.screen.get_width() - TILE_SIZE)
                    y = random.randint(0, self.screen.get_height() - TILE_SIZE)
                    obj = GameObject(x, y, TILE_SIZE, TILE_SIZE)
                    self.objects.append(obj)

        # Обработка событий меню
        if self.game_state == "menu":
            for button in self.buttons:
                # Проверяем наведение мыши
                mouse_pos = pygame.mouse.get_pos()
                button.is_hovered = button.rect.collidepoint(mouse_pos)
                
                # Проверяем клики
                if pygame.mouse.get_pressed()[0] and button.is_hovered:
                    action = button.action
                    if action == "start_game":
                        self.game_state = "game"
                    elif action == "settings":
                        self.game_state = "settings"
                    elif action == "exit":
                        return "exit"
        
        return None

    def draw(self):
        self.screen.fill(BLACK)
        
        # Рисуем заголовок
        title = TITLE_FONT.render("SHADOW STOCKS", True, WHITE)
        title_rect = title.get_rect(midright=(self.screen.get_width() - MENU_PADDING, 100))
        self.screen.blit(title, title_rect)
        
        # Рисуем декоративную полосу под названием
        line_y = title_rect.bottom + 20
        line_length = min(400, self.screen.get_width() - 2 * MENU_PADDING)  # Ограничиваем длину полосы
        line_x = self.screen.get_width() - MENU_PADDING - line_length
        
        # Создаем поверхность для полосы с прозрачностью
        line_surface = pygame.Surface((line_length, 2), pygame.SRCALPHA)
        
        # Рисуем полосу с эффектом исчезающих краев
        for x in range(line_length):
            # Вычисляем прозрачность (альфа) для эффекта исчезающих краев
            distance_from_center = abs(x - line_length / 2)
            alpha = int(255 * (1 - distance_from_center / (line_length / 2)))
            pygame.draw.line(line_surface, (255, 255, 255, alpha), (x, 0), (x, 2), 1)
        
        # Рисуем полосу
        self.screen.blit(line_surface, (line_x, line_y))
        
        # Рисуем вертикальные линии меню
        pygame.draw.line(self.screen, LINE_COLOR, 
                        (MENU_PADDING - 20, 0), 
                        (MENU_PADDING - 20, self.screen.get_height()))
        pygame.draw.line(self.screen, LINE_COLOR, 
                        (MENU_PADDING + MENU_WIDTH + 20, 0), 
                        (MENU_PADDING + MENU_WIDTH + 20, self.screen.get_height()))
        
        # Рисуем кнопки
        for button in self.buttons:
            button.draw(self.screen)
        
        # Рисуем график
        self.graph.draw(self.screen)
            
        pygame.display.flip()

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Game:
    def __init__(self):
        self.fullscreen = True  # Начинаем в полноэкранном режиме
        # Устанавливаем позицию окна в центр экрана
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        # Инициализируем видео режим
        try:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
            print("Window created successfully in fullscreen mode")
        except pygame.error as e:
            print(f"Error creating window: {e}")
            sys.exit(1)
            
        pygame.display.set_caption("Shadow Stocks")
        self.clock = pygame.time.Clock()
        self.running = True
        self.menu = Menu(self.screen)
        self.game_state = "menu"  # menu, game, settings
        
        # Игровые объекты
        self.objects = []
        self.create_objects()
        
        print(f"Window size: {self.screen.get_size()}")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
            print("Switched to fullscreen mode")
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
            print("Switched to windowed mode")
        self.menu = Menu(self.screen)

    def create_objects(self):
        for _ in range(10):
            x = random.randint(0, self.screen.get_width() - TILE_SIZE)
            y = random.randint(0, self.screen.get_height() - TILE_SIZE)
            obj = GameObject(x, y, TILE_SIZE, TILE_SIZE)
            self.objects.append(obj)

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.game_state == "menu":
            self.menu.update(current_time)
        elif self.game_state == "game":
            for obj in self.objects:
                obj.rect.y += 1
                if obj.rect.y > self.screen.get_height():
                    obj.rect.y = -TILE_SIZE

    def draw(self):
        if self.game_state == "menu":
            self.menu.draw()
        elif self.game_state == "game":
            self.screen.fill(BLACK)
            
            # Рисуем сетку
            for x in range(0, self.screen.get_width(), TILE_SIZE):
                pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.screen.get_height()))
            for y in range(0, self.screen.get_height(), TILE_SIZE):
                pygame.draw.line(self.screen, GRAY, (0, y), (self.screen.get_width(), y))
            
            # Рисуем все объекты
            for obj in self.objects:
                obj.draw(self.screen)
        elif self.game_state == "settings":
            self.screen.fill(BLACK)
            text = MENU_FONT.render("Настройки (ESC - вернуться в меню, F11 - переключить полноэкранный режим)", True, WHITE)
            text_rect = text.get_rect(midleft=(MENU_PADDING, self.screen.get_height()//2))
            self.screen.blit(text, text_rect)
            
        pygame.display.flip()

    def run(self):
        print("Game starting...")
        last_time = pygame.time.get_ticks()
        
        while self.running:
            try:
                current_time = pygame.time.get_ticks()
                delta_time = current_time - last_time
                last_time = current_time
                
                # Обработка событий через handle_events
                action = self.handle_events()
                if action == "exit":
                    self.running = False
                
                self.update()
                self.draw()
                
                # Ограничение FPS
                self.clock.tick(FPS)
                
                # Вывод текущего FPS
                current_fps = self.clock.get_fps()
                if current_time % 1000 < 100:  # Выводим FPS примерно раз в секунду
                    print(f"Current FPS: {current_fps:.1f}")
                
            except Exception as e:
                print(f"Error during game loop: {e}")
                self.running = False

        print("Game closing...")
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC всегда возвращает в меню, независимо от текущего состояния
                    if self.game_state != "menu":
                        print("Escape key pressed - returning to menu")
                        self.game_state = "menu"
                elif event.key == pygame.K_q:  # Используем Q для переключения режима окна
                    self.toggle_fullscreen()
                elif event.key == pygame.K_SPACE and self.game_state == "game":
                    x = random.randint(0, self.screen.get_width() - TILE_SIZE)
                    y = random.randint(0, self.screen.get_height() - TILE_SIZE)
                    obj = GameObject(x, y, TILE_SIZE, TILE_SIZE)
                    self.objects.append(obj)

        # Обработка событий меню
        if self.game_state == "menu":
            for button in self.menu.buttons:
                # Проверяем наведение мыши
                mouse_pos = pygame.mouse.get_pos()
                button.is_hovered = button.rect.collidepoint(mouse_pos)
                
                # Проверяем клики
                if pygame.mouse.get_pressed()[0] and button.is_hovered:
                    action = button.action
                    if action == "start_game":
                        self.game_state = "game"
                    elif action == "settings":
                        self.game_state = "settings"
                    elif action == "exit":
                        return "exit"
        
        return None

if __name__ == "__main__":
    game = Game()
    game.run() 