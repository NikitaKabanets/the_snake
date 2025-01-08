from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Игровой объект"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Функция отрисовки, переопределяется в дочерних классах"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def randomize_position(self):
        """Функция случайного выбора позиции яблока"""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        """Функция отричовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2
                           * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def update_direction(self):
        """Функция обновления направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает положение головы змейки"""
        return self.positions[0]

    def move(self):
        """Функция движения змейки"""
        head = self.positions[0]
        new_head = ((head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                    (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)

        if self.length > 1:
            self.positions.pop()

        if new_head in self.positions:
            Snake.reset(self)
        else:
            self.positions.insert(0, new_head)
            self.length += 1

    def reset(self):
        """Функция возвращения начальной позиции змейки"""
        Snake.draw_death(self)
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2
                           * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def draw_death(self):
        """Функция стирания умершей змеи"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def draw(self):
        """Функция отрисовки змеи"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.length > 1:
            if self.positions[-1]:
                last_rect = pygame.Rect(self.positions[-1], (GRID_SIZE,
                                                             GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция меин"""
    pygame.init()
    snake = Snake()
    apple = Apple()
    running = True

    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.positions.insert(snake.length - 1,
                                   snake.positions[-1])
            apple.randomize_position()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
