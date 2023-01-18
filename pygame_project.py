import os
import sys
import pygame
import sqlite3
from random import randrange
pygame.init()
size = width, height = 900, 450
pygame.display.set_caption('Penalty')
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
statistics_sprite = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class PenaltyGoalkeeper(pygame.sprite.Sprite):
    def __init__(self, *group, team):
        super().__init__(*group)
        if team == "p1":
            self.image = load_image("penalty_goalkeepercom.png", -1)
        else:
            self.image = load_image("penalty_goalkeeper.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = 415
        self.rect.y = 110


class PenaltyPlayer(pygame.sprite.Sprite):
    def __init__(self, *group, team):
        super().__init__(*group)
        if team == "p1":
            self.image = load_image("penalty_player.png", -1)
        else:
            self.image = load_image("penalty_com.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 175

    def shoot(self):
        self.rect = self.rect.move(4, -1)


class Arrow(pygame.sprite.Sprite):
    image = load_image("penalty_arrow.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Arrow.image
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def update(self, *args):
        if pygame.mouse.get_focused():
            if args and args[0].type == pygame.MOUSEMOTION:
                self.rect.x = args[0].pos[0] - 33
                self.rect.y = args[0].pos[1] - 33
        else:
            self.rect.x = -100
            self.rect.y = -100


class PenaltyBall(pygame.sprite.Sprite):
    image = load_image("penalty_ball.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = PenaltyBall.image
        self.rect = self.image.get_rect()
        self.rect.x = 435
        self.rect.y = 345


class PlayButton(pygame.sprite.Sprite):
    image = load_image("play_button.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = PlayButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 75
        self.rect.y = 100


class MainButton(pygame.sprite.Sprite):
    image = load_image("main_button.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = MainButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50


class StatisticsButton(pygame.sprite.Sprite):
    image = load_image("statistics_button.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = StatisticsButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 75
        self.rect.y = 250


class Goal(pygame.sprite.Sprite):
    image = load_image("goal.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Goal.image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 150


class Win(pygame.sprite.Sprite):
    image = load_image("win.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Win.image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 150


class Draw(Win):
    image = load_image("draw.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Draw.image


class Loss(Win):
    image = load_image("loss.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Loss.image


class Counter(pygame.sprite.Sprite):
    image = load_image("counter.png")

    def __init__(self, *group):
        super().__init__(*group)
        self. image = Counter.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


running = True
penalty = False
howtoplay = False
statistics = False
main_screen = True
start_sprites = pygame.sprite.Group()
game_fon = load_image("game_fon.jpg", -1)
play_button = PlayButton(start_sprites)
statistics_button = StatisticsButton(start_sprites)
while running:
    if main_screen:
        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, 150)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                x = event.pos[0]
                y = event.pos[1]
                if 75 <= x <= 275 and 100 <= y <= 138:
                    play_button.image = load_image("play_button1.png", -1)
                else:
                    play_button.image = load_image("play_button.png", -1)
                if 75 <= x <= 275 and 250 <= y <= 288:
                    statistics_button.image = load_image("statistics_button1.png", -1)
                else:
                    statistics_button.image = load_image("statistics_button.png", -1)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = event.pos[0]
                y = event.pos[1]
                if 75 <= x <= 275 and 100 <= y <= 138:
                    p1 = 0
                    com = 0
                    all_sprites = pygame.sprite.Group()
                    end_sprites = pygame.sprite.Group()
                    main_screen = False
                    penalty = True
                    fl = True
                    fon = load_image("penalty_fon.png", -1)
                    screen.blit(fon, (0, 0))
                    goalkeeper = PenaltyGoalkeeper(all_sprites, team="com")
                    ball = PenaltyBall(all_sprites)
                    player = PenaltyPlayer(all_sprites, team="p1")
                    arrow = Arrow(all_sprites)
                    counter = Counter(all_sprites)
                    counter.image = load_image("counter.png", -1)
                    shoot = False
                    player_shoot = True
                    shoots = 1
                    im = 1
                    count = -1
                    a = 0
                    switch = False
                if 75 <= x <= 275 and 175 <= y <= 213:
                    pass
                if 75 <= x <= 275 and 250 <= y <= 288:
                    statistics = True
                    main_screen = False
                    main_button = MainButton(statistics_sprite)
        screen.fill("black")
        screen.blit(game_fon, (0, 0))
        start_sprites.draw(screen)
    if statistics:
        screen.fill("black")
        game_fon = load_image("game_fon.jpg", -1)
        screen.blit(game_fon, (0, 0))
        statistics_sprite.draw(screen)
        con = sqlite3.connect("data/statistics.sqlite3")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM stat""")
        arr = []
        for elem in result:
            arr.append(elem)
        f1 = pygame.font.Font(None, 30)
        games = f1.render(f"Количество игр: {str(arr[0][0])}", True, "red")
        wins = f1.render(f"Количество побед: {str(arr[0][1])}", True, "red")
        draws = f1.render(f"Количество ничей: {str(arr[0][2])}", True, "red")
        losses = f1.render(f"Количество поражений: {str(arr[0][3])}", True, "red")
        screen.blit(games, (50, 100))
        screen.blit(wins, (50, 125))
        screen.blit(draws, (50, 150))
        screen.blit(losses, (50, 175))
        if arr[0][0] != 0:
            w = round(arr[0][1] / (arr[0][0] / 100) * 5)
            d = round(arr[0][2] / (arr[0][0] / 100) * 5)
            l = round(arr[0][3] / (arr[0][0] / 100) * 5)
            pygame.draw.line(screen, "green", (200, 300), (200 + w, 300), width=20)
            pygame.draw.line(screen, "grey", (200 + w, 300), (200 + w + d, 300), width=20)
            pygame.draw.line(screen, "red", (200 + w + d, 300), (200 + w + d + l, 300), width=20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 50 <= event.pos[0] <= 250 and 50 <= event.pos[1] <= 88:
                    statistics = False
                    main_screen = True
    if penalty:
        if shoots < 6:
            if player_shoot:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEMOTION:
                        screen.fill("black")
                        screen.blit(fon, (0, 0))
                        all_sprites.update(event)
                        all_sprites.draw(screen)
                        if pygame.mouse.get_focused():
                            screen.fill("black")
                            screen.blit(fon, (0, 0))
                            all_sprites.update(event)
                            all_sprites.draw(screen)
                            pygame.mouse.set_visible(False)

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        screen.fill("black")
                        arrow.image = load_image("white.png", -1)
                        screen.blit(fon, (0, 0))
                        all_sprites.update(event)
                        all_sprites.draw(screen)
                        x = event.pos[0] - 435
                        y = event.pos[1] - 355
                        shoot = True
                    if shoot:
                        if event.type == MYEVENTTYPE:
                            if im < 4:
                                player.rect = player.rect.move(100, -15)
                            if im < 5:
                                player.image = load_image(f"penalty_player{im}.png", -1)
                                im += 1
                            if 4 < im < 15:
                                pygame.time.set_timer(MYEVENTTYPE, 40)
                                vx = x // 10
                                vy = y // 10
                                ball.rect = ball.rect.move(vx, vy)
                                im += 1
                            if im == 15:
                                pos = randrange(1, 5)
                                goalkeeper.image = load_image(f"penalty_goalkeeper{pos}.png", -1)
                                if pos == 1:
                                    goalkeeper.rect = goalkeeper.rect.move(-150, -50)
                                if pos == 2:
                                    goalkeeper.rect = goalkeeper.rect.move(75, -50)
                                if pos == 3:
                                    goalkeeper.rect = goalkeeper.rect.move(50, 15)
                                if pos == 4:
                                    goalkeeper.rect = goalkeeper.rect.move(-160, 15)
                                goalkeeper.mask = pygame.mask.from_surface(goalkeeper.image)
                                ball.mask = pygame.mask.from_surface(ball.image)
                                if pygame.sprite.collide_mask(goalkeeper, ball):
                                    count = 0
                                    vx = - 30
                                    vy = 18
                                    pygame.draw.circle(counter.image, "red", (30 + 13 * shoots, 13), 5)
                                else:
                                    count = -2
                                im += 1
                            if 0 <= count < 10:
                                ball.rect = ball.rect.move(vx, vy)
                                count += 1
                            elif count == -2:
                                if 230 <= ball.rect.x <= 670 and 40 <= ball.rect.y <= 235:
                                    goal = Goal(all_sprites)
                                    pygame.draw.circle(counter.image, "green", (30 + 13 * shoots, 13), 5)
                                    p1 += 1
                                    a += 1
                                else:
                                    pygame.draw.circle(counter.image, "red", (30 + 13 * shoots, 13), 5)
                                    a += 1
                            if count == 10 or a == 10:
                                switch = True
                    screen.fill("black")
                    screen.blit(fon, (0, 0))
                    all_sprites.update(event)
                    all_sprites.draw(screen)
                if switch:
                    pygame.time.wait(3000)
                    screen.fill("black")
                    fon = load_image("penalty_fon.png", -1)
                    screen.blit(fon, (0, 0))
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(counter)
                    goalkeeper = PenaltyGoalkeeper(all_sprites, team="p1")
                    ball = PenaltyBall(all_sprites)
                    player = PenaltyPlayer(all_sprites, team="com")
                    arrow = Arrow(all_sprites)
                    arrow.image = load_image("glove.png", -1)
                    shoot = False
                    player_shoot = False
                    im = 1
                    count = -1
                    pygame.time.set_timer(MYEVENTTYPE, 150)
                    a = 0
                    switch = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEMOTION:
                        screen.fill("black")
                        screen.blit(fon, (0, 0))
                        all_sprites.update(event)
                        all_sprites.draw(screen)
                        if pygame.mouse.get_focused():
                            screen.fill("black")
                            screen.blit(fon, (0, 0))
                            all_sprites.update(event)
                            all_sprites.draw(screen)
                            pygame.mouse.set_visible(False)

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        screen.fill("black")
                        arrow.image = load_image("white.png", -1)
                        screen.blit(fon, (0, 0))
                        all_sprites.update(event)
                        all_sprites.draw(screen)
                        x, y = event.pos[0], event.pos[1]
                        if x < 467 and y < 152:
                            pos = 1
                        elif x > 467 and y < 152:
                            pos = 2
                        elif x < 467 and y > 152:
                            pos = 4
                        elif x > 467 and y > 152:
                            pos = 3
                        x = randrange(250, 660) - 435
                        y = randrange(60, 215) - 355
                        shoot = True
                    if shoot:
                        if event.type == MYEVENTTYPE:
                            if im < 4:
                                player.rect = player.rect.move(100, -15)
                            if im < 5:
                                player.image = load_image(f"penalty_com{im}.png", -1)
                                im += 1
                            if 4 < im < 15:
                                pygame.time.set_timer(MYEVENTTYPE, 40)
                                vx = x // 10
                                vy = y // 10
                                ball.rect = ball.rect.move(vx, vy)
                                im += 1
                            if im == 15:
                                goalkeeper.image = load_image(f"penalty_goalkeepercom{pos}.png", -1)
                                if pos == 1:
                                    goalkeeper.rect = goalkeeper.rect.move(-150, -50)
                                if pos == 2:
                                    goalkeeper.rect = goalkeeper.rect.move(75, -50)
                                if pos == 3:
                                    goalkeeper.rect = goalkeeper.rect.move(50, 15)
                                if pos == 4:
                                    goalkeeper.rect = goalkeeper.rect.move(-160, 15)
                                goalkeeper.mask = pygame.mask.from_surface(goalkeeper.image)
                                ball.mask = pygame.mask.from_surface(ball.image)
                                if pygame.sprite.collide_mask(goalkeeper, ball):
                                    count = 0
                                    vx = - 30
                                    vy = 18
                                    pygame.draw.circle(counter.image, "red", (30 + 13 * shoots, 35), 5)
                                else:
                                    count = -2
                                im += 1
                            if 0 <= count < 10:
                                ball.rect = ball.rect.move(vx, vy)
                                count += 1
                            elif count == -2:
                                if 230 <= ball.rect.x <= 670 and 40 <= ball.rect.y <= 235:
                                    pygame.draw.circle(counter.image, "green", (30 + 13 * shoots, 35), 5)
                                    com += 1
                                    a += 1
                                else:
                                    pygame.draw.circle(counter.image, "red", (30 + 13 * shoots, 35), 5)
                                    a += 1
                            if count == 10 or a == 10:
                                switch = True
                    screen.fill("black")
                    screen.blit(fon, (0, 0))
                    all_sprites.update(event)
                    all_sprites.draw(screen)
                if switch:
                    pygame.time.wait(3000)
                    screen.fill("black")
                    fon = load_image("penalty_fon.png", -1)
                    screen.blit(fon, (0, 0))
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(counter)
                    goalkeeper = PenaltyGoalkeeper(all_sprites, team="com")
                    ball = PenaltyBall(all_sprites)
                    player = PenaltyPlayer(all_sprites, team="p1")
                    arrow = Arrow(all_sprites)
                    shoot = False
                    player_shoot = True
                    im = 1
                    count = -1
                    pygame.time.set_timer(MYEVENTTYPE, 150)
                    switch = False
                    shoots += 1
                    a = 0
        else:
            if fl:
                con = sqlite3.connect("data/statistics.sqlite3")
                cur = con.cursor()
                result = cur.execute("""SELECT * FROM stat""")
                arr = []
                for elem in result:
                    arr.append(elem)
                if p1 > com:
                    win = Win(end_sprites)
                    cur.execute(f"""UPDATE stat
                                SET wins = {arr[0][1] + 1}""")
                elif p1 == com:
                    draw = Draw(end_sprites)
                    cur.execute(f"""UPDATE stat
                                                SET draws = {arr[0][2] + 1}""")
                else:
                    loss = Loss(end_sprites)
                    cur.execute(f"""UPDATE stat
                                                SET losses = {arr[0][3] + 1}""")
                cur.execute(f"""UPDATE stat
                                            SET games = {arr[0][0] + 1}""")
                con.commit()
                fl = False
            main_button = MainButton(end_sprites)
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 50 <= event.pos[0] <= 250 and 50 <= event.pos[1] <= 88:
                        penalty = False
                        main_screen = True
            end_sprites.draw(screen)
    pygame.display.flip()