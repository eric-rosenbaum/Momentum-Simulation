import pygame
import sys
import math

# Input Coefficients
SPEED = 10  # magnitude of velocity (m/s)
ANGLE = -3  # angle of speed from positive x-axis (in degrees)

# Simulation Coefficients
REST_COEFF = 0.99  # need to be high or simulation breaks
FRICTION_COEFF = 0.01  # Friction coefficient between the ball and the ground
TARGET_LOCATION = [10, 5]  # in meters
MIN_SPEED_THRESHOLD = 0.2  # Minimum speed threshold to stop the ball

# Initial velocities
vx_input = SPEED*math.cos(-1*math.radians(ANGLE))
vy_input = SPEED*math.sin(-1*math.radians(ANGLE))


TARGET_LOCATION = [10, 6 - TARGET_LOCATION[1]]

# Initialize Pygame
pygame.init()

# Window Setup
scale = 100  # 100 pixels = 1 meter
width, height = 1200, 600  # Window size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Momentum Simulator")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
background_color = (0, 150, 0)

# Ball Properties
ball_radius = 15
white_ball_position = [100, height // 2] # starts at (1, 3) meters
black_ball_position = [white_ball_position[0] + 200, height // 2]  # Initially place at (3, 3) meters
ball_speed_scale = 60  # Scale speed from m/s to pixels/second

# Simulation State
running = True
clock = pygame.time.Clock()
fps = 60  # Frames per second

white_ball_velocity = [vx_input * ball_speed_scale / fps, vy_input * ball_speed_scale / fps]
black_ball_velocity = [0, 0]


def calculate_new_velocities(pos1, vel1, pos2, vel2):
    # Assume dx and dy are the differences in x and y positions between the two balls, respectively
    dx = black_ball_position[0] - white_ball_position[0]
    dy = black_ball_position[1] - white_ball_position[1]

    # Calculate the normal and tangent vectors for the collision
    norm = math.sqrt(dx ** 2 + dy ** 2)
    nx = dx / norm
    ny = dy / norm
    tx = -ny
    ty = nx

    # Decompose velocities into normal and tangential components
    v1n = nx * white_ball_velocity[0] + ny * white_ball_velocity[1]
    v1t = tx * white_ball_velocity[0] + ty * white_ball_velocity[1]
    v2n = nx * black_ball_velocity[0] + ny * black_ball_velocity[1]
    v2t = tx * black_ball_velocity[0] + ty * black_ball_velocity[1]

    # Calculate new normal velocities using the restitution coefficient
    v1n_final = v2n * REST_COEFF
    v2n_final = v1n * REST_COEFF

    # Convert the scalar normal and tangential velocities back into 2D vectors
    white_ball_velocity[0] = v1n_final * nx + v1t * tx
    white_ball_velocity[1] = v1n_final * ny + v1t * ty
    black_ball_velocity[0] = v2n_final * nx + v2t * tx
    black_ball_velocity[1] = v2n_final * ny + v2t * ty


def apply_friction(velocity):
    # Reduce velocity by the friction coefficient
    velocity[0] *= (1 - FRICTION_COEFF)
    velocity[1] *= (1 - FRICTION_COEFF)

    # Stop the ball if moving really slow
    if abs(velocity[0]) < MIN_SPEED_THRESHOLD and abs(velocity[1]) < MIN_SPEED_THRESHOLD:
        velocity[0] = 0
        velocity[1] = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(background_color)
    # Define the position and radius of the red circle
    red_circle_position = (TARGET_LOCATION[0]*100, TARGET_LOCATION[1]*100)
    red_circle_radius = 20  # Adjust the radius as needed

    # Draw the red circle in the background
    pygame.draw.circle(screen, (255, 0, 0), red_circle_position, red_circle_radius)

    # Update ball positions
    apply_friction(white_ball_velocity)
    apply_friction(black_ball_velocity)
    white_ball_position[0] += white_ball_velocity[0]
    white_ball_position[1] += white_ball_velocity[1]
    black_ball_position[0] += black_ball_velocity[0]
    black_ball_position[1] += black_ball_velocity[1]

    # Collision detection and response
    distance = math.hypot(white_ball_position[0] - black_ball_position[0],
                          white_ball_position[1] - black_ball_position[1])
    if distance < ball_radius * 2:
        calculate_new_velocities(white_ball_position, white_ball_velocity, black_ball_position, black_ball_velocity)

    # Draw balls
    pygame.draw.circle(screen, white, (int(white_ball_position[0]), int(white_ball_position[1])), ball_radius)
    pygame.draw.circle(screen, black, (int(black_ball_position[0]), int(black_ball_position[1])), ball_radius)

    pygame.display.flip()
    clock.tick(fps)
