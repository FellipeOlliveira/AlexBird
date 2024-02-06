import pygame
from pygame.locals import *
import random
pygame.init()

#colocando o tamanho da tela e o framerate

clock = pygame.time.Clock()
fps = 60

screen_width =  288
screen_height = 652

screen = pygame.display.set_mode((screen_width,screen_height))

#font define
font = pygame.font.SysFont('Neon Led Light', 60)

#color define
white = (255, 255, 255)

#Variaveis do jogo
ground_scroll = 0
scroll_spd = 2
voar = False
game_over = False
pipe_gap = 150
pipe_frequence = 1500 #milisegundos
last_pipe = pygame.time.get_ticks() - pipe_frequence
score = 0
pass_pipe = False


#titulo
pygame.display.set_caption('Alex Bird')

#carregando imagens do background
bg = pygame.image.load('img/bg_teste.png') #background
ground = pygame.image.load('img/ground.png') #chão(sensação de movimento)
btn_img = pygame.image.load('img/restart.png')

def desenhar_score(text,font, text_col, x , y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y ))

def reset_game():
    obstaculo_group.empty()
    alex.rect.x = 100
    alex.rect.y = int(screen_height / 2)
    score = 0

    return score


#Criando a classe Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0 #spd da animação
        self.spd = 0 #spd do flappy
        self.clicked = False #para saber o click no jogo

        #carregando as imagens
        for i in range(1,4):
            img = pygame.image.load(f'img/Alex{i}.png')
            self.images.append(img)

        #pegando so a imagem do momento
        self.image =  self.images[self.index]

        #posicionando o passaro
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):

        #colocando gravidade
        if voar == True:
            self.spd += 0.5
            if self.spd > 8:
                self.spd = 8
            #print(self.spd)
            if self.rect.bottom < 640:
                self.rect.y += int(self.spd)

        if game_over == False:
            #colocando o pulo
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.spd = -10

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            #criando a animação
            self.counter += 1
            alex_cooldown = 5

            if self.counter > alex_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #criando a rotação do passaro
            self.image = pygame.transform.rotate(self.images[self.index], self.spd * -2)

        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x , y , position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/tubulacao.png')
        self.rect = self.image.get_rect()
        # 1 for top and -1 for bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x , y + int(pipe_gap / 2)]
    def update(self):
        self.rect.x -= scroll_spd
        if self.rect.right < 50:
            self.kill()

class Button():

    def __init__(self,x ,y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        #pegando a posição do mouse
        pos = pygame.mouse.get_pos()

        #checando c o mouse esta emcima do botao
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #desenhando o botao
        screen.blit(self.image, (self.rect.x , self.rect.y))

        return action

#Criando o obj passaro e obstaculo colocando ele no game cm os sprites
bird_group = pygame.sprite.Group()
obstaculo_group = pygame.sprite.Group()
btn = Button(screen_width // 2 - 50, screen_height // 2 - 100, btn_img)

alex = Bird(100,int(screen_height / 2))
bird_group.add(alex)



#colocando loop pra rodar o jogo
run = True
while run:

    #colocando o framrate
    clock.tick(fps)

    #carregando background
    screen.blit(bg , (0,0))

    #desenhando na tela
    bird_group.draw(screen)
    bird_group.update()

    obstaculo_group.draw(screen)


    # colocando o ground
    screen.blit(ground, (ground_scroll, 512))

    #checando o score
    if len(obstaculo_group) > 0:
        if bird_group.sprites()[0].rect.left > obstaculo_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < obstaculo_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > obstaculo_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    #print(score)
    desenhar_score(str(score), font, white, int(screen_width/2), 20)

    #procurando colisão
    if pygame.sprite.groupcollide(bird_group, obstaculo_group, False, False) or alex.rect.top < 0:
        game_over = True

    #chegar c o passaro acerto o chão
    if alex.rect.bottom > 508:
        game_over = True
        voar = False

    #Atualização do jogo
    if game_over == False and voar == True:

        #gerando novos obstaculos
        pipe_hight = random.randint(-80, 80)
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequence:
            top_pipe = Obstaculo(screen_width, int(screen_height / 2) + pipe_hight, 1)
            btm_pipe = Obstaculo(screen_width, int(screen_height / 2) + pipe_hight, -1)

            obstaculo_group.add(btm_pipe)
            obstaculo_group.add(top_pipe)

            last_pipe = time_now

        ground_scroll -= scroll_spd

        #fazendo o loop do background
        if abs(ground_scroll) > 30:
            ground_scroll = 0

        obstaculo_group.update()

    #checando o gameover e resetando
    if game_over == True:
        if btn.draw() == True:
            game_over = False
            score = reset_game()


    #for para analisar os eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and voar == False and game_over == False:
            voar = True
    pygame.display.update()

pygame.quit()