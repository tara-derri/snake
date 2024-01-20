import pygame
import sys
import random

pygame.init()

WHITE = (255, 255, 255)
PINK = (255, 182, 193)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

width, height = 600, 400
cell_size = 20
snake_size = 20

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((width // 2), (height // 2))]
        self.direction = random.choice([0, 1, 2, 3])
        self.color = PINK

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.get_head_position()
        if self.direction == 0:
            y -= cell_size
        elif self.direction == 1:
            y += cell_size
        elif self.direction == 2:
            x -= cell_size
        elif self.direction == 3:
            x += cell_size
        x = x % width
        y = y % height
        self.positions = [((x, y))] + self.positions[:self.length - 1]

    def render(self, surface):
        for i, p in enumerate(self.positions):
            pygame.draw.rect(surface, self.color, (p[0], p[1], snake_size, snake_size))
            if i == 0:
                draw_eyes(surface, p)

def draw_eyes(surface, head_position):
    eye_radius = 4
    eye_distance = 5
    pupil_distance = 2
    left_eye = (head_position[0] + eye_distance, head_position[1] + eye_distance)
    right_eye = (head_position[0] + snake_size - eye_distance - 2 * eye_radius, head_position[1] + eye_distance)
    pupil_radius = 2  # Taille de la pupille modifiée
    pygame.draw.circle(surface, WHITE, head_position, eye_radius)
    pygame.draw.circle(surface, WHITE, left_eye, eye_radius)
    pygame.draw.circle(surface, WHITE, right_eye, eye_radius)
    
    # Dessiner des pupilles noires au centre des yeux
    pygame.draw.circle(surface, BLACK, (left_eye[0] + pupil_distance, left_eye[1]), pupil_radius)
    pygame.draw.circle(surface, BLACK, (right_eye[0] + pupil_distance, right_eye[1]), pupil_radius)

class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = GREEN
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (width - cell_size) // cell_size) * cell_size,
                         random.randint(0, (height - cell_size) // cell_size) * cell_size)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], snake_size, snake_size))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 1:
                    snake.direction = 0
                elif event.key == pygame.K_DOWN and snake.direction != 0:
                    snake.direction = 1
                elif event.key == pygame.K_LEFT and snake.direction != 3:
                    snake.direction = 2
                elif event.key == pygame.K_RIGHT and snake.direction != 2:
                    snake.direction = 3

        snake.update()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            score += 1

        screen.fill(WHITE)
        snake.render(screen)
        apple.render(screen)

        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()
