from network import Network 
import pygame

TURQUOISE = (64, 224, 208)
RED = (255, 0, 0)
GREEN = (0, 256, 0)
GREEN = (0, 255, 0)
BLUE=(0,0,255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)

pygame.init()
pygame.font.init()

WIDTH = 700
HEIGHT = 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CLIENT WINDOW")


class Button:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 100
        self.text = text
        self.color = tuple(color)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, WHITE)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def is_clicked(self, pos):
        x1, y1 = pos
        if (self.x <= x1 <= self.x+self.width) and (self.y <= y1 <= self.y+self.width):
            return True
        return False


def redrawWindow(win, game, p):
    win.fill(GREY)
    if not game.is_connected():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, RED, True)
        win.blit(text, ((WIDTH//2 - text.get_width()//2),
                        (HEIGHT//2 - text.get_height()//2)))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, CYAN)
        win.blit(text, (80, 200))
        text = font.render("Opponents", 1, CYAN)
        win.blit(text, (380, 200))
        move_p1 = game.get_player_moves()[0]
        move_p2 = game.get_player_moves()[1]
        if game.bothWent():
            text1 = font.render(move_p1, 1, BLACK)
            text2 = font.render(move_p2, 1, BLACK)
            pygame.time.delay(1000)
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move_p1, 1, BLACK)
            elif game.p1Went:
                text1 = font.render("Locked In...", 1, BLACK)
            else:
                text1 = font.render("Waiting...", 1, BLACK)
            if p == 1 and game.p2Went  :
                text2 = font.render(move_p2, 1, BLACK)
            elif game.p2Went:
                text2 = font.render("Locked In...", 1, BLACK)
            else:
                text2 = font.render("Waiting...", 1, BLACK)

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))
        for btn in btns:
            btn.draw(win)
    pygame.display.update()


btns = [Button(50, 500, "Rock", BLACK), Button(250, 500, "Scissors", RED), Button(450, 500, "Paper", BLUE)]


def mainGame():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_pos())
    pygame.init()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.is_clicked(pos) and game.is_connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("[END] Game Ended")
            break
        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("[END] Game Ended")
            font = pygame.font.SysFont("comicsans", 80)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won! ", 1, RED)
            elif game.winner() == -1:
                text = font.render("Tie Game! ", 1, RED)
            else:
                print("YOU LOST")
                text = font.render("You Lost...", 1, RED)
            win.blit(text, ((WIDTH-text.get_width()) //
                            2, (HEIGHT-text.get_height())//2))
            pygame.display.update()
            pygame.time.delay(2000)
        redrawWindow(win, game, player)

def menu_screen():
    run=True
    clock=pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill(GREY)
        font=pygame.font.SysFont("comisans",60)
        text=font.render("Click To Play!",1,RED)
        win.blit(text,((WIDTH-text.get_width())//2,(HEIGHT-text.get_height())//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                run=False
                break

    mainGame()

if __name__ == '__main__':
    while True:
        pygame.time.delay(500)
        menu_screen()
