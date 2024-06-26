import pygame
import sys
import math
from server import send_notification
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Vehicles with Circle")

# Load the background image

image_path = os.path.join("ambulance_project", "map.jpg")
background_image = pygame.image.load(image_path)
background_image = pygame.transform.scale(background_image, (width, height))

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Set up the vehicles
vehicle_width = 30
vehicle_height = 30
ambulance_speed = 1.5
car1_speed = 0.6
car2_speed = -0.6
car3_speed = 0.8
car4_speed = -0.8

# Load the images for vehicles
ambulance_image = pygame.image.load('ambulance.png')
ambulance_image = pygame.transform.scale(ambulance_image, (30, 30))

car1_image = pygame.image.load('car1.png')
car1_image = pygame.transform.scale(car1_image, (30, 30))

car2_image = pygame.image.load('car2.png')
car2_image = pygame.transform.scale(car2_image, (40, 40))

car3_image = pygame.image.load('car3.png')
car3_image = pygame.transform.scale(car3_image, (40, 40))

car4_image = pygame.image.load('car4.png')
car4_image = pygame.transform.scale(car4_image, (50, 50))


# Set up the circle
circle_radius = 100

# Initialize the position of the vehicles
ambulance_x, ambulance_y = 480, 162.0
car_1_x, car_1_y = 480, 350
car_2_x, car_2_y = 480, 700
car_3_x, car_3_y = 200,320
car_4_x, car_4_y = 750,315

# L-shaped path points
l_path_points = [
    (width // 4, height // 3.05),
    (width // 4, 4.28 * height // 4),
    (3 * width // 7.3, 4.28 * height // 4)
]

# Shift the path to the left
shift_amount = -230
shifted_path = [(x - shift_amount, y) for x, y in l_path_points]

# Increase the vertical height by adding a certain value to y-coordinates
vertical_increase = -100
extended_path = [(x, y + vertical_increase) for x, y in shifted_path]

# Game loop
clock = pygame.time.Clock()

l_path_index = 0
car1_l_path_index = 0
car2_l_path_index = 0

notification_sent_car_1 = False
notification_sent_car_2 = False
notification_sent_car_3 = False
notification_sent_car_4 = False


ambulance_move = False  # Flag to track whether the ambulance should start moving

running = True  # Flag to control the game loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check if any key is pressed
            ambulance_move = True

    # Move the ambulance along the path when the key is pressed
    if ambulance_move and l_path_index < len(extended_path):
        target_x, target_y = extended_path[l_path_index]
        direction_x = 1 if target_x > ambulance_x else -1
        direction_y = 1 if target_y > ambulance_y else -1

        if ambulance_x != target_x:
            ambulance_x += direction_x * ambulance_speed
        if ambulance_y != target_y:
            ambulance_y += direction_y * ambulance_speed

        # Check if the ambulance is close to the current target point on the L-shaped path
        if abs(ambulance_x - target_x) < ambulance_speed and abs(ambulance_y - target_y) < ambulance_speed:
            l_path_index += 1

    # Move the vehicles along their respective paths
    if car1_l_path_index < len(extended_path):
        target_x, target_y = extended_path[car1_l_path_index]
        # Reverse the direction for car 1
        direction_x = -1 if target_x > car_1_x else 1
        direction_y = -1 if target_y > car_1_y else 1

        if car_1_x != target_x:
            car_1_x += direction_x * car1_speed
        if car_1_y != target_y:
            car_1_y += direction_y * car1_speed

        # Check if car 1 is close to the end of the L-shaped path
        if (
                car1_l_path_index < len(extended_path) - 1
                and abs(car_1_x - extended_path[-1][0]) < car1_speed
                and abs(car_1_y - extended_path[-1][1]) < car1_speed
        ):
            car1_l_path_index = len(extended_path)  # Stop car 1 at the end of the path

    if car2_l_path_index < len(extended_path):
        target_x, target_y = extended_path[car2_l_path_index]
        # Reverse the direction for car 2
        direction_x = -1 if target_x > car_2_x else 1
        direction_y = -1 if target_y > car_2_y else 1

        if car_2_x != target_x:
            car_2_x += direction_x * car2_speed
        if car_2_y != target_y:
            car_2_y += direction_y * car2_speed

        # Check if car 2 is close to the end of the L-shaped path
        if (
                car2_l_path_index < len(extended_path) - 1
                and abs(car_2_x - extended_path[-1][0]) < car2_speed
                and abs(car_2_y - extended_path[-1][1]) < car2_speed
        ):
            car2_l_path_index = len(extended_path)  # Stop car 2 at the end of the path

    # Check the proximity of cars to the ambulance
    distance_car_1 = math.sqrt((ambulance_x - car_1_x) ** 2 + (ambulance_y - car_1_y) ** 2)
    distance_car_2 = math.sqrt((ambulance_x - car_2_x) ** 2 + (ambulance_y - car_2_y) ** 2)
    distance_car_3 = math.sqrt((ambulance_x - car_3_x) ** 2 + (ambulance_y - car_3_y) ** 2)
    distance_car_4 = math.sqrt((ambulance_x - car_4_x) ** 2 + (ambulance_y - car_4_y) ** 2)

    car_3_x += car3_speed
    car_4_x += car4_speed

    # Notify if cars are within the circle of the ambulance
    if not notification_sent_car_1 and distance_car_1 < circle_radius:
        #send_notification("car_1")
        notification_sent_car_1 = True

    if not notification_sent_car_2 and distance_car_2 < circle_radius:
        send_notification("car_2")
        notification_sent_car_2 = True
    
    if not notification_sent_car_3 and distance_car_3 < circle_radius:
        #send_notification("car_3")
        notification_sent_car_3 = True
    
    if not notification_sent_car_4 and distance_car_4 < circle_radius:
        #send_notification("car_4")
        notification_sent_car_4 = True

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the L-shaped path
    pygame.draw.lines(screen, blue, False, extended_path, 7)

    #Draw the Horizontal line
    pygame.draw.line(screen, blue, (0, 350), (width, 350),5)

    # Draw the ambulance
    screen.blit(ambulance_image, (ambulance_x - vehicle_width // 2, ambulance_y - vehicle_height // 2))

    # Draw the circle
    pygame.draw.circle(screen, blue, (int(ambulance_x), int(ambulance_y)), circle_radius, 2)

    # Draw the first car
    screen.blit(car1_image, (car_1_x - vehicle_width // 2, car_1_y - vehicle_height // 2))

    # Draw the second car
    screen.blit(car2_image, (car_2_x - vehicle_width // 2, car_2_y - vehicle_height // 2))

    #Draw the third car
    screen.blit(car3_image, (car_3_x , car_3_y))

    # Draw the fourth car
    screen.blit(car4_image, (car_4_x , car_4_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

print(notification_sent_car_1)
print(notification_sent_car_2)
print(notification_sent_car_3)
print(notification_sent_car_4)

# Quit Pygame
pygame.quit()
sys.exit()



