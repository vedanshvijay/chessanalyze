import pygame
pygame.mixer.init()
sound = pygame.mixer.Sound("sounds/move.wav")
sound.play()
input("Press Enter after you hear the sound...")