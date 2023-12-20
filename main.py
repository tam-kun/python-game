import pygame
import sys
import math

pygame.init()

#Screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Pygame Game")

#Object Player
player_size = 20
player_x = width // 2 - player_size // 2
player_y = height // 2 - player_size // 2
player_speed = 5
dash_speed = 30

#Colors
white = (255, 255, 255)
player_color = (16, 135, 247)  
border_color = (0, 0, 0)

#hitbox

player_hitbox = pygame.Rect(player_x, player_y, player_size, player_size)
future_hitbox = pygame.Rect(player_x, player_y, player_size, player_size)
top_border_hitbox = pygame.Rect(0, 0, width, 1)
bottom_border_hitbox = pygame.Rect(0, height - 1, width, 1)
left_border_hitbox = pygame.Rect(0, 0, 1, height)
right_border_hitbox = pygame.Rect(width - 1, 0, 1, height)

#clock

clock = pygame.time.Clock()
ticks_per_second = 60

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # Handle diagonal movement with vector normalization
    move_vector = pygame.Vector2(0, 0)
    if keys[pygame.K_LEFT]:
        move_vector.x = -1
    if keys[pygame.K_RIGHT]:
        move_vector.x = 1
    if keys[pygame.K_UP]:
        move_vector.y = -1
    if keys[pygame.K_DOWN]:
        move_vector.y = 1

    # Make a vector to make diagonal movement same as the other ones
    if move_vector.length() > 0:
        move_vector.normalize_ip()

    if keys[pygame.K_SPACE]:
        future_x = player_x + move_vector.x * dash_speed
        future_y = player_y + move_vector.y * dash_speed

        future_hitbox.x = future_x
        future_hitbox.y = future_y

        # Check for collisions with the borders after the dash is over
        if not (future_hitbox.colliderect(top_border_hitbox) or
                future_hitbox.colliderect(bottom_border_hitbox) or
                future_hitbox.colliderect(left_border_hitbox) or
                future_hitbox.colliderect(right_border_hitbox)):
            player_x = future_x
            player_y = future_y

    else:
        # Check if the player is about to move outside the screen boundaries
        new_x = player_x + move_vector.x * player_speed
        new_y = player_y + move_vector.y * player_speed

        player_hitbox.x = new_x
        player_hitbox.y = new_y

        # Check for collisions with the borders
        if player_hitbox.colliderect(top_border_hitbox) or \
                player_hitbox.colliderect(bottom_border_hitbox) or \
                player_hitbox.colliderect(left_border_hitbox) or \
                player_hitbox.colliderect(right_border_hitbox):
            # stop movement if a collision is detected
            player_hitbox.x = player_x
            player_hitbox.y = player_y
        else:
            player_x = new_x
            player_y = new_y

    # Clear the screen
    screen.fill(white)

    #Border around the screen
    pygame.draw.rect(screen, border_color, top_border_hitbox)
    pygame.draw.rect(screen, border_color, bottom_border_hitbox)
    pygame.draw.rect(screen, border_color, left_border_hitbox)
    pygame.draw.rect(screen, border_color, right_border_hitbox)

    #New color for player
    pygame.draw.rect(screen, player_color, player_hitbox)

    pygame.display.flip()

    #Cap the ticks to 60 per second
    clock.tick(ticks_per_second)
