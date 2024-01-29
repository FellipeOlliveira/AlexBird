import pygame
from pygame.locals import *

pygame.init()

#colocando o tamanho da tela
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width,screen_height))

#titulo
pygame.display.set_caption('Alex Bird')

#carregando imagens
bg = pygame.image.load()

#colocando loop pra rodar o jogo
run = True
while run:

    #for para analisar os eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()