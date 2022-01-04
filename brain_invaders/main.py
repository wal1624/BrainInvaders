import intro

from component import *

START_MENU_STAGE = 0
INTRO_STAGE = 1
SHOOTER_STAGE = 2
WIN_STAGE = 3

DROP_INTERVAL = 20

DEFEATED_STRINGS = []

high_score_mode = False
high_score = 0
score = 0

size = width, height = 600, 400
speed = [2, 2]
black = 0, 0, 0

tick_time = 0
spawn_interval = None
drop_speed = None
spawn_countdown = None
defeated_strings = None
player = None

game_stage = None

win_stage_tick_time = 0
win_stage_string = None


def reinitialize(screen: pg.surface.Surface):
    global tick_time, spawn_interval, drop_speed, spawn_countdown, defeated_strings, player

    screen_rect = screen.get_rect()

    ALL.empty()
    ENEMY_LETTERS.empty()
    BULLETS.empty()
    ENEMY_STRINGS.clear()

    tick_time = 0
    spawn_interval = 500
    drop_speed = 3

    spawn_countdown = 10
    defeated_strings = 0

    # Initialize components
    comp_x1 = 20
    comp_x2 = screen_rect.width - COMPONENT_SIZE - 20
    comp_y1 = screen_rect.height - COMPONENT_SIZE - 10
    comp_y2 = comp_y1 - COMPONENT_SIZE - 10
    grades = Component("grades", pos=(comp_x1, comp_y1))
    health = Component("health", pos=(comp_x1, comp_y2))
    rest = Component("relationships", pos=(comp_x2, comp_y1))
    relationships = Component("rest", pos=(comp_x2, comp_y2))

    player = Player()
    player.rect.move_ip(screen_rect.centerx, screen_rect.bottom - player.rect.height - 6)


def main():
    global tick_time, spawn_interval, drop_speed, spawn_countdown, defeated_strings, player, game_stage

    pg.init()
    pg.display.set_caption("Brain Invaders")

    # Loading the background image and sound
    # main_Function_Image()
    # main_Function_Music()

    fullscreen = False
    screen_rect = pg.rect.Rect(0, 0, width, height)
    screen = pg.display.set_mode(screen_rect.size, 0)
    game_stage = START_MENU_STAGE
    reinitialize(screen)
    bg_tile = load_image("backgrounds", "cloud_bg.png")

    clock = pg.time.Clock()

    # Cap the framerate
    clock.tick(40)

    def spawn_string():
        stringList = [line.strip() for line in open("sentences.txt", "r").readlines() if line != ""]
        string = random.choice(stringList)
        evil_visibility = max(255 - (255 / 5 * defeated_strings), 0)
        string_enemy = EnemyString(string, evil_visibility=evil_visibility)
        string_enemy.set_pos((width / 2 - string_enemy.get_rect().width / 2, 10))

    def start_menu_tick(screen, events):
        logo_img = load_image("logo.png")
        logo_img = pg.transform.scale(logo_img, (310, 190))
        logo_rect = logo_img.get_rect().move(screen_rect.centerx - logo_img.get_width() / 2, 10)
        play_img = load_image("buttons", "play_button.png")
        play_img = pg.transform.scale(play_img, (175, 80))
        play_rect = play_img.get_rect().move(screen_rect.centerx - play_img.get_width() - 10, height / 2 + 40)
        quit_img = load_image("buttons", "quit_button.png")
        quit_img = pg.transform.scale(quit_img, (175, 80))
        quit_rect = quit_img.get_rect().move(screen_rect.centerx + 10, height / 2 + 40)

        screen.blit(logo_img, logo_rect)
        screen.blit(play_img, play_rect)
        screen.blit(quit_img, quit_rect)

        def play():
            global game_stage, high_score_mode
            reinitialize(screen)
            game_stage = INTRO_STAGE
            high_score_mode = False

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(pg.mouse.get_pos()):
                    play()
                elif quit_rect.collidepoint(pg.mouse.get_pos()):
                    sys.exit()
            elif event.type == pg.KEYUP:
                if (event.key == pg.K_SPACE):
                    play()

    def intro_tick(screen, events):
        global game_stage
        if intro.intro_tick(screen, events):
            game_stage = SHOOTER_STAGE

    def shooter_stage_tick(screen, events):
        global spawn_countdown, defeated_strings, drop_speed, high_score_mode

        if high_score_mode:
            for component in COMPONENTS:
                component.kill()

        for string in ENEMY_STRINGS:
            string: EnemyString
            if string.get_rect().bottom >= height:
                if high_score_mode:
                    global game_stage
                    game_stage = main.WIN_STAGE
                    return
                else:
                    comp: Component = max(COMPONENTS.sprites(), key=lambda c: c.progress)
                    comp.decrement()
                string.kill()

        ### LOGIC

        # Bullet spawn logic for player pressing space
        ALL.update()
        Bullet.bullet_spawn_tick(player)

        if spawn_countdown <= 0:
            spawn_string()
            spawn_countdown = spawn_interval
        else:
            spawn_countdown -= 1

        for letter in pg.sprite.groupcollide(ENEMY_LETTERS, BULLETS, 0, 1):
            letter: EnemyLetter
            letter.hit()

        for enemy_string in ENEMY_STRINGS:
            enemy_string: EnemyString
            enemy_string.update()
            if enemy_string.is_good():
                enemy_string.revive_good_letters()
                if not enemy_string.is_destroyed:
                    enemy_string.begin_destruction()
                    if high_score_mode:
                        global score, high_score
                        score += drop_speed * 5
                        high_score = max(high_score, score)
                    else:
                        inc_components = get_incomplete_components()
                        if inc_components:
                            random.choice(inc_components).progression()
                    DEFEATED_STRINGS.append(enemy_string.original_string)
                    defeated_strings += 1
                    drop_speed += 1
                enemy_string.update()
            else:
                if tick_time % DROP_INTERVAL == 0: enemy_string.drop_letters(drop_speed)

        ### RENDER
        if high_score_mode:
            font = pg.font.Font("freesansbold.ttf", 20)
            score_str_img = font.render('Score: ' + str(score), True, "black", "white")
            score_str_rect = score_str_img.get_rect()
            score_str_rect.move_ip(10, height - 10 - score_str_rect.height * 2)

            high_score_str_img = font.render('High Score: ' + str(high_score), True, "black", "white")
            high_score_str_rect = high_score_str_img.get_rect()
            high_score_str_rect.move_ip(10, height - 10 - high_score_str_rect.height)
            screen.blit(score_str_img, score_str_rect)
            screen.blit(high_score_str_img, high_score_str_rect)
        ALL.draw(screen)

    def win_stage_tick(screen, events):
        global game_stage, DEFEATED_STRINGS, win_stage_string, win_stage_tick_time
        # pg.remove.all()

        logo_img = load_image("congrats.png")
        logo_img = pg.transform.scale(logo_img, (310, 190))
        logo_rect = logo_img.get_rect().move(screen_rect.centerx - logo_img.get_width() / 2, 10)
        continue_img = load_image("buttons", "continue_button.png")
        continue_img = pg.transform.scale(continue_img, (175, 80))
        continue_rect = continue_img.get_rect().move(screen_rect.centerx - continue_img.get_width() - 10,
                                                     height / 2 + 40)
        main_menu_img = load_image("buttons", "main_menu_button.png")
        main_menu_img = pg.transform.scale(main_menu_img, (175, 80))
        main_menu_rect = main_menu_img.get_rect().move(screen_rect.centerx + 10, height / 2 + 40)

        screen.blit(logo_img, logo_rect)
        screen.blit(continue_img, continue_rect)
        screen.blit(main_menu_img, main_menu_rect)

        ENEMY_LETTERS.empty()
        if win_stage_tick_time % 120 == 0 or win_stage_string == None:
            if len(DEFEATED_STRINGS) == 0:
                DEFEATED_STRINGS = ["You are enough", "You are loved"]
            win_stage_string = random.choice(DEFEATED_STRINGS)

        string_entity = EnemyString(win_stage_string)
        string_rect = string_entity.get_rect()
        string_y = height - string_rect.height - 30
        string_entity.set_pos((width / 2 - string_rect.width / 2, string_y))

        string_entity.render_letters(screen)

        def continue_game():
            global high_score_mode, game_stage, score
            reinitialize(screen)
            game_stage = SHOOTER_STAGE
            high_score_mode = True
            score = 0

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(pg.mouse.get_pos()):
                    continue_game()
                elif main_menu_rect.collidepoint(pg.mouse.get_pos()):
                    game_stage = START_MENU_STAGE
            elif event.type == pg.KEYUP:
                if (event.key == pg.K_SPACE):
                    continue_game()

        win_stage_tick_time += 1

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to fullscreen")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(screen_rect.size, 0 | pg.FULLSCREEN)
                        screen.blit(screen_backup, (0, 0))
                        fullscreen = True
                    else:
                        print("Changing to window mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(screen_rect.size)
                        screen.blit(screen_backup, (0, 0))
                        pg.display.flip()
                        fullscreen = False

        # Draw tiled background
        screen.fill("black")
        y_offset = -bg_tile.get_height() + (int(tick_time / 15) % bg_tile.get_height())
        for x in range(0, screen_rect.width, bg_tile.get_width()):
            for y in range(y_offset, screen_rect.height, bg_tile.get_height()):
                screen.blit(bg_tile, (x, y))

        if game_stage == START_MENU_STAGE:
            start_menu_tick(screen, events)
        elif game_stage == INTRO_STAGE:
            intro_tick(screen, events)
        elif game_stage == SHOOTER_STAGE:
            tick_time += 1
            if shooter_stage_tick(screen, events): game_stage = WIN_STAGE
        elif game_stage == WIN_STAGE:
            win_stage_tick(screen, events)

        pg.display.flip()


if __name__ == "__main__":
    main()
