"""
##################################################
##################################################
### Ciencia da Computacao - UFMT               ###
### Disciplina: Programação de Computadores    ###
###                                            ###
###                                            ###
### Academico: Anthony Muniz Prado de Oliveira ###
### python code: LEAVING ORBIT                 ###
### RGA:202011722003                           ###
##################################################
##################################################

"""

# Biblioteca PyGame
import pygame
# Biblioteca para geracao de numeros pseudoaleatorios
import random
# Modulo da biblioteca PyGame que permite o acesso as teclas utilizadas
from pygame.locals import *

POINTS = 0
Contador_PONTOS = 0
# Definir as dimensões da tela
screen_width = 800
screen_height = 600

# Título da tela
pygame.display.set_caption("LEAVING ORBIT")


# Classe que representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("img/space_ship.png")#Define a imagem que representa o player
        self.surf.set_colorkey((255,0,255))
        self.surf = pygame.transform.rotate(self.surf, -90) # rotaciona a nave para ficar deitada
        self.surf = pygame.transform.scale(self.surf,(65,45)) # define o tamanho do player
        self.rect = self.surf.get_rect()

    # Determina acao de movimento conforme teclas pressionadas
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(- 5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip( 5, 0)

        # Mantem o jogador nos limites da tela do jogo
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

# Classe que representa os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("img/asteroid.png")#Define a imagem que representa o inmigo
        self.surf.set_colorkey((255,0,255))
        self.surf = pygame.transform.rotate(self.surf, -90)
        self.surf = pygame.transform.scale(self.surf,(random.randint(40, 70),random.randint(20, 60))) # Define randomicamente o tamanho dos inimigos
        self.rect = self.surf.get_rect( #Coloca na extrema direita (entre 830 e 900) e sorteia sua posicao em relacao a coordenada y (entre 0 e 900)
            center=(random.randint(830, 1000), random.randint(0, 1000))
        )
        if Contador_PONTOS > 50:
            self.speed = random.uniform(3, POINTS/5) #Sorteia sua velocidade, entre 5 e quantidade de pontos/5
            Contador_PONTOS == 0
        elif Contador_PONTOS > 20:
            self.speed = random.uniform(3, 6) #Sorteia sua velocidade, entre 3 e 6
            Contador_PONTOS == 0
        else:
            self.speed = random.uniform(1, 3) #Sorteia sua velocidade, entre 1 e 3

    # Funcao que atualiza a posiçao do inimigo em funcao da sua velocidade e termina com ele quando ele atinge o limite esquerdo da tela (x < 0)
    def update(self):
        self.rect.move_ip(-self.speed,random.randint(0, 2))
        if self.rect.right < 0:
            self.kill()  
    
   

    
counter = 0

# Inicializa pygame
pygame.init()

#Adiciona a musica do jogo 
music_de_fundo = pygame.mixer.music.load('music/BackMusic.mp3')
pygame.mixer.music.play(-1)

# Cria a tela com resolução 800x600 px
screen = pygame.display.set_mode((screen_width, screen_height))

#Cria um evento para acumular os pontos do jogador a cada segundo


Relogio = pygame.time.Clock()


# Cria um evento para adicao de inimigos
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 180) #Define um intervalo para a criacao de cada inimigo (milisegundos)

# Cria o jogador (nossa nave)
player = Player()

# Define o plano de fundo
background = pygame.image.load("img/space.jpg")#Define a imagem do fundo
background = pygame.transform.scale(background, (screen_width, screen_height)) # a scala da imagem adicionada

enemies = pygame.sprite.Group() #Cria o grupo de inimigos
all_sprites = pygame.sprite.Group() #Cria o grupo de todos os Sprites
all_sprites.add(player) #Adicionar o player no grupo de todos os Sprites

running = True #Flag para controle do jogo

while running:
    #Laco para verificacao do evento que ocorreu
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #Verifica se a tecla ESC foi pressionada
                running = False
        elif event.type == QUIT: #Verifica se a janela foi fechada
            running = False
        elif(event.type == ADDENEMY): #Verifica se e o evento de criar um inimigo
            new_enemy = Enemy() #Cria um novo inimigo
            enemies.add(new_enemy) #Adiciona o inimigo no grupo de inimigos
            all_sprites.add(new_enemy) #Adiciona o inimigo no grupo de todos os Sprites

    screen.blit(background, (0, 0)) #Atualiza a exibicao do plano de fundo do jogo (neste caso nao surte efeito)
    pressed_keys = pygame.key.get_pressed() #Captura as as teclas pressionadas
    player.update(pressed_keys) #Atualiza a posicao do player conforme teclas usadas
    enemies.update() #Atualiza posicao dos inimigos
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect) #Atualiza a exibicao de todos os Sprites

    #Adiciona o Score na tela

    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render("TIME ALIVE: "+ str(POINTS), True, (0, 255, 0), (0,0,0,))
    textRect = text.get_rect()
    textRect.center = (screen_width/2, 20)  #Posiciona o texto a partir do centro da tela 800/2 -> 400

    screen.blit(text, textRect)

    # conta 1 ponto se passarem 120 ticks (1s)
    if counter == 120:
        counter = 0
        POINTS += 1
        Contador_PONTOS += 1


    if pygame.sprite.spritecollideany(player, enemies): #Verifica se ocorreu a colisao do player com um dos inimigos
       #Se ocorrer a colisao, encerra o player
        player.kill()
        music_de_fundo = pygame.mixer.music.load('music/meteror_drop.wav')
        pygame.mixer.music.play(0)
        
        morreu = True 

        while morreu:


            screen.fill((255,0,0)) #Atualiza a exibicao do plano de fundo do jogo
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                
                    if event.key == K_ESCAPE: #Verifica se a tecla ESC foi pressionada
                        morreu = False
                        running = False
                elif event.type == QUIT: #Verifica se a janela foi fechada
                    morreu = False
                    running = False
            
                    
            font = pygame.font.Font("freesansbold.ttf", 32)
            text2 = font.render("VOCE PERDEU", True, (0, 0, 0), (255,0,0,))
            text3 = font.render("TIME ALIVE: "+ str(POINTS), True, (0, 0, 0), (255,0,0,))
            textRect2 = text2.get_rect()
            textRect3 = text3.get_rect()
            textRect2.center = (screen_width/2, 270)
            textRect3.center = (screen_width/2, 300)
            screen.blit(text2, textRect2)
            screen.blit(text3, textRect3)
            
            pygame.display.flip() #Atualiza a projecao do jogo
        
    elif Contador_PONTOS == 100: #SE O JOGADOR GANHAR CHEGANDO A 100 PONTOS

        ganhou = True

        # muda a música            
        pygame.mixer.music.load("music/04.Hardware.mp3")
        pygame.mixer.music.play(0)


        while ganhou:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                
                    if event.key == K_ESCAPE: #Verifica se a tecla ESC foi pressionada
                        morreu = False
                        running = False

                elif event.type == QUIT: #Verifica se a janela foi fechada
                    morreu = False
                    running = False

            # Carregar a imagem de fundo
            background_image = pygame.image.load("img/background.jpg")
            background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

            # Desenhar a imagem de fundo na superfície
            screen.blit(background_image, (0, 0))

            # Definir a fonte do texto
            font = pygame.font.Font("freesansbold.ttf", 25)

            # Criar a mensagem "A nave escapou da terra antes do colapso. Parabéns!"
            message = font.render("A nave escapou da terra antes do colapso, Parabéns!", True, (255, 255, 255))
            messageRect = message.get_rect()
            messageRect.center = (screen_width/2, 50)

            # Desenhar as mensagens na tela
            screen.blit(message, messageRect)
            
            pygame.display.flip() #Atualiza a projecao do jogo
            

    pygame.display.flip() #Atualiza a projecao do jogo
    counter += 1

    Relogio.tick(120)
    