import pygame
import sys
import math
from server import send_notification

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Vehicles with Circle")

# Load the background image
background_image = pygame.image.load('map.jpg')  # Change this to the actual filename
background_image = pygame.transform.scale(background_image, (width, height))

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Set up the vehicles
vehicle_width = 30
vehicle_height = 30
ambulance_speed = 2
car1_speed = 1
car2_speed = 0.5

# Load the images for vehicles
ambulance_image = pygame.image.load('ambulance.png')  # Change this to the actual filename
ambulance_image = pygame.transform.scale(ambulance_image, (vehicle_width, vehicle_height))

car1_image = pygame.image.load('car1.png')  # Change this to the actual filename
car1_image = pygame.transform.scale(car1_image, (vehicle_width, vehicle_height))

car2_image = pygame.image.load('car2.png')  # Change this to the actual filename
car2_image = pygame.transform.scale(car2_image, (vehicle_width, vehicle_height))

# Set up the circle
circle_radius = 100

# Initialize the position of the vehicles
ambulance_x, ambulance_y = 46, 100
car_1_x, car_1_y = 46, 300
car_2_x, car_2_y = 46, 500

# Phone number map
phone_map = {
    "car_1": "+918529622974",
    "car_2": "+919993074778"
}

# L-shaped path points
l_path_points = [
    (width // 4, height // 4),
    (width // 4, 4.35 * height // 4),
    (3 * width // 7, 4.35 * height // 4)
]    

# Shift the path to the left
shift_amount = 204
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the vehicles along their respective paths
    if l_path_index < len(extended_path):
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

    # Notify if cars are within the circle of the ambulance
    if not notification_sent_car_1 and distance_car_1 < circle_radius:
        # send_notification(phone_map["car_1"])
        notification_sent_car_1 = True

    if not notification_sent_car_2 and distance_car_2 < circle_radius:
        send_notification(phone_map["car_2"])
        notification_sent_car_2 = True

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the L-shaped path
    pygame.draw.lines(screen, black, False, extended_path, 2)

    # Draw the ambulance
    screen.blit(ambulance_image, (ambulance_x - vehicle_width // 2, ambulance_y - vehicle_height // 2))

    # Draw the circle
    pygame.draw.circle(screen, blue, (int(ambulance_x), int(ambulance_y)), circle_radius, 2)

    # Draw the car for the first car
    screen.blit(car1_image, (car_1_x - vehicle_width // 2, car_1_y - vehicle_height // 2))

    # Draw the car for the second car
    screen.blit(car2_image, (car_2_x - vehicle_width // 2, car_2_y - vehicle_height // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
