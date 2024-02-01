import pygame
from pygame.locals import *

pygame.init()

#colocando o tamanho da tela e o framerate

clock = pygame.time.Clock()
fps = 60

screen_width = 288 #400
screen_height = 624

screen = pygame.display.set_mode((screen_width,screen_height))


#Variaveis do jogo
ground_scroll = 0
scroll_spd = 2
voar = False
game_over = False

#titulo
pygame.display.set_caption('Alex Bird')

#carregando imagens do background
bg = pygame.image.load('img/bg_teste.png') #background
ground = pygame.image.load('img/ground_teste.png') #chão(sensação de movimento)

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
            img = pygame.image.load(f'img/bluebird{i}.png')
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
            if self.rect.bottom < 512:
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

#Criando o obj passaro e colocando ele no game cm os sprites
bird_group = pygame.sprite.Group()

alex = Bird(100,int(screen_height / 2))

bird_group.add(alex)


#colocando loop pra rodar o jogo
run = True
while run:

    #colocando o framrate
    clock.tick(fps)

    #carregando background
    screen.blit(bg , (0,0))

    #desenhando o passaro na tela
    bird_group.draw(screen)
    bird_group.update()

    # colocando o ground
    screen.blit(ground, (ground_scroll, 512))

    #chegar c o passaro acerto o chão
    if alex.rect.bottom > 512:
        game_over = True
        voar = False

    #criando a sensação de movimento
    if game_over == False:
        ground_scroll -= scroll_spd

        #fazendo o loop do background
        if abs(ground_scroll) > 45:
            ground_scroll = 0

    #for para analisar os eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and voar == False and game_over == False:
            voar = True
    pygame.display.update()

pygame.quit()