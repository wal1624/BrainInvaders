import pygame
import os


# Calling a file for the main image
image_dir = 'textures'

def get_images_in_dir(*path):
    return os.listdir(os.path.join(image_dir, *path))

def load_image(*path):
    # Gets us our image
    file = os.path.join(image_dir, *path)
    try:
        surface = pygame.image.load(file)
    except:
        raise SystemExit("Image could not be converted '%s' %s" % (file, pygame.get_error()))
    return surface.convert_alpha()


sound_directory = "audio"


# Loading our sounds
def load_sound(file):
    if not pygame.mixer:
        return None
    file = os.path.join(sound_directory, "data", file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print("Warning the sound is not able to load, %s" % file)
    return None


def main_Function_Image():

    bits = 16
    win_style = 0
    bit_depth = pygame.display.mode_ok(SCREEN_RECT.size, win_style, bits)
    screen = pygame.display.set_mode(SCREEN_RECT.size, win_style, bit_depth)

    # Decorating the game window
    game_icon = pygame.image.load("relative_path_icon")
    pygame.display.set_icon(game_icon)

    # Create the background, tile the bgd image
    bdg_tile = load_image("relative_path_file")
    background = pygame.Surface(SCREEN_RECT.size)

    # Create an offset that updates to make the illusion of the tiles moving; it should originally be negative

    for x in range(0, SCREEN_RECT.width, bdg_tile.get_width()):
        background.blit(bdg_tile, (x, 0))
    pygame.display.flip()
    running = True


def main_Function_Music():
    # Load the sound in
    # sound_Name = load_sound("relative_path_sound")  # We can use this for any sound effects we need
    volume = -1
    if pygame.mixer:
        # For background music
        music = os.path.join(sound_directory, "Relative path of sound")
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(volume)
