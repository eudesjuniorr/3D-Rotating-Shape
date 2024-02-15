import os
from math import cos, sin, pi
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Defina a posição central da janela
os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 800, 800

pygame.display.set_icon(pygame.Surface((1, 1)))

pixel_width = 20
pixel_height = 20

A, B = 0, 0

theta_spacing = 30
phi_spacing = 5
FPS = 20.5

chars = ".,-~:;=!*#$@"

R1 = 10
R2 = 20
K2 = 200
K1 = HEIGHT * K2 * 3 / (8 * (R1 + R2))

pygame.init()

screen = pygame.display.set_mode(RES, pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20, bold=True)

def text_display(char, x, y):
    text = font.render(str(char), True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

running = True

while running:
    clock.tick(FPS)
    pygame.display.set_caption("")
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            K1 = HEIGHT * K2 * 3 / (8 * (R1 + R2))
            pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            pygame.display.flip()

    A = (A + 0.15) % (2 * pi)
    B = (B + 0.035) % (2 * pi)

    for theta in range(0, 628, theta_spacing):
        for phi in range(0, 628, phi_spacing):
            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)

            costheta = cos(theta)
            sintheta = sin(theta)
            cosphi = cos(phi)
            sinphi = sin(phi)

            # x, y coordinates before revolving
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D (x, y, z) coordinates after rotation
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z

            # x, y projection
            xp = int((WIDTH / 2) + (K1 * ooz * x))
            yp = int((HEIGHT / 2) - (K1 * ooz * y))

            if 0 <= xp < WIDTH and 0 <= yp < HEIGHT:
                luminance_index = int(cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (
                            cosA * sintheta - costheta * sinA * sinphi) * 8)
                luminance_index = max(0, min(7, luminance_index))
                text_display(chars[luminance_index], xp, yp)

    pygame.display.update()

pygame.quit()