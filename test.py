import pygame

# Define the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the color of the line
BLUE = (0, 0, 255)

# Draw the line
pygame.draw.line(screen, BLUE, (0, 100), (SCREEN_WIDTH, 100),5)

# Update the display
pygame.display.flip()

# Wait for the user to quit
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()