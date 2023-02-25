import pygame
import numpy as np
import pyaudio

# Set up the Screen of the pygame
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice-controlled Ball Game")

# Set up the ball properties and background
ball_radius = 20
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_color = (255, 0, 0)
background_color = (0, 128, 0)  # green color for background

# Set up PyAudio
CHUNK = 1024
RATE = 44100
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

# Start the game loop
clock = pygame.time.Clock()
velocity = 0
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Get the sound input and calculate its volume
    data = stream.read(CHUNK, exception_on_overflow=False)
    volume = np.abs(np.frombuffer(data, dtype=np.int16)).mean()

    # Move the ball based on the volume of the sound input
    velocity += volume / 1000000
    ball_pos[0] += velocity

    # Wrap the ball around to the left side of the screen
    if ball_pos[0] > WIDTH + ball_radius:
        ball_pos[0] = -ball_radius

    # Draw the background and ball
    screen.fill(background_color)
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

    # Update the display and limit the frame rate
    pygame.display.update()
    clock.tick(60)
