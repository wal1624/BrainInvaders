import pygame as pg
import sys

font_name = 'freesansbold.ttf'
font_size = 20
font = None

y_start = 40
y_padding = 2
y_group_padding = 18

screen_lines = [
    [["Recently, you haven't been feeling too well...",
      "Your brain is constantly overworked."],

     ["Your physical health is poor."],
     ["Your grades are falling."],
     ["You hardly get any sleep."],
     ["You don't spend time with friends and family..."],

     ["It feels like your entire life is in ruins."]],

    [
        ["You're constantly plagued with negative thoughts...",
         "but you don't know how to get better."],

        ["Fortunately, the Brain Ship is here to soothe your mind"],
        ["and turn your negative thoughts into positive ones."],

        ["Bringing change like a beautiful butterfly!"],

        ["Destroy the bad parts of your thoughts!",
         "Use the space and arrow keys to play!"]
    ]
]

line_progression = 1
screen_num = 0


# Returns a 2D list of tuple(surface, rect)
def get_line_img_rect_groups(screen_width):
    line_groups = screen_lines[screen_num]
    img_groups = []
    y = y_start
    for line_group in line_groups:
        img_group = []
        img_groups.append(img_group)
        for line in line_group:
            img = font.render(line.strip(), True, "white", "black")
            rect = img.get_rect().move(screen_width / 2 - img.get_width() / 2, y)
            y += font_size + y_padding
            img_group.append((img, rect))
        y += y_group_padding
    return img_groups


def intro_tick(screen: pg.surface.Surface, events):
    global line_progression, font, screen_num

    if (screen_num >= len(screen_lines)): return True
    font = pg.font.Font(font_name, font_size)

    line_img_groups = get_line_img_rect_groups(screen.get_width())

    for event in events:
        if (event.type == pg.KEYDOWN and event.key == pg.K_SPACE) or event.type == pg.MOUSEBUTTONDOWN:
            line_progression += 1
            if line_progression > len(line_img_groups):
                line_progression = 1
                screen_num += 1
                if (screen_num >= len(screen_lines)): return True
                line_img_groups = get_line_img_rect_groups(screen.get_width())

    screen.fill("black")

    instr = font.render('Press Space to Continue', True, "gray", "black")
    instr_rect = instr.get_rect(center=(screen.get_width() / 2, screen.get_height() * 16 / 17))
    screen.blit(instr, instr_rect)  # displays instructions on screen -- tells user to press space bar

    for i in range(line_progression):
        line_img_group = line_img_groups[i]
        for line_img, line_rect in line_img_group:
            screen.blit(line_img, line_rect)
