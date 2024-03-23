import pygame
import sys
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 40
ENEMY_SIZE = 40
ROOM_WIDTH = 400
ROOM_HEIGHT = 300

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('knight.jpg')  # Load player image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 40

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, PLAYER_SIZE, 5))  # Player health bar
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health * PLAYER_SIZE // 40, 5))

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('rat.jpg')  # Load enemy image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 10

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, ENEMY_SIZE, 5))  # Enemy health bar
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health * ENEMY_SIZE // 10, 5))

class Room:
    def __init__(self, enemies):
        self.enemies = enemies

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('boss.jpg')  # Load boss image
        self.health = 30

def attack(target):
    damage = random.randint(1, 3)
    target.health -= damage
    return damage

def power_attack(target):
    damage = random.randint(3, 6)
    target.health -= damage
    return damage

def run():
    pass

def battle_screen(screen, player, enemy):
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    player_turn = True
    battle_history = []

    while player.health > 0 and enemy.health > 0:
        screen.fill(LIGHT_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        action_text = None

        if player_turn:
            possible_actions_text = font.render('1: Attack   2: Power Attack   3: Run', True, BLACK)
            screen.blit(possible_actions_text, (10, SCREEN_HEIGHT - 50))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                damage = attack(enemy)
                action_text = f'You attacked for {damage} damage!'
                battle_history.append(action_text)
                player_turn = False
            elif keys[pygame.K_2]:
                damage = power_attack(enemy)
                action_text = f'You power attacked for {damage} damage!'
                battle_history.append(action_text)
                player_turn = False
            elif keys[pygame.K_3]:
                run()
                action_text = 'You ran away!'
                battle_history.append(action_text)
                break

        else:
            damage = random.randint(1, 3)
            player.health -= damage
            action_text = f'Enemy attacked for {damage} damage!'
            battle_history.append(action_text)
            player_turn = True

        enemy.draw(screen)
        player.draw(screen)

        pygame.draw.rect(screen, WHITE, (10, SCREEN_HEIGHT - 100, 400, 40))
        if battle_history:
            history_y = SCREEN_HEIGHT - 90
            for line in battle_history[::-1]:
                history_text = font.render(line, True, BLACK)
                screen.blit(history_text, (20, history_y))
                history_y -= 30

        pygame.display.flip()
        clock.tick(5)

    if player.health <= 0:
        print("You died!")
    elif enemy.health <= 0:
        print("Enemy defeated!")

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Custom Graphics RPG Game")

    player = Player(50, 50)

    # Define rooms and their enemies
    room1 = Room([Enemy(400, 300), Enemy(200, 200)])
    room2 = Room([Boss(400, 300)])  # Room with the boss

    current_room = room1
    in_battle = False
    boss_defeated = False

    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not in_battle:
            if keys[pygame.K_LEFT]:
                player.move(-5, 0)
            if keys[pygame.K_RIGHT]:
                player.move(5, 0)
            if keys[pygame.K_UP]:
                player.move(0, -5)
            if keys[pygame.K_DOWN]:
                player.move(0, 5)

            for enemy in current_room.enemies:
                if (player.rect.colliderect(enemy.rect)):
                    in_battle = True
                    battle_screen(screen, player, enemy)
                    in_battle = False

            # Check if all enemies are defeated
            if all(enemy.health <= 0 for enemy in current_room.enemies):
                if current_room == room1:
                    current_room = room2  # Transition to room 2
                else:
                    print("You defeated the boss! You win!")
                    pygame.quit()
                    sys.exit()

        for enemy in current_room.enemies:
            enemy.draw(screen)

        player.draw(screen)

        pygame.display.flip()
        clock.tick(30)

        if player.health <= 0:
            print("You died!")
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
