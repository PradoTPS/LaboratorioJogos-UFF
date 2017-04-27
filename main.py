#region PROJECT PATTERN
#####################                                 #####################
##########                   PADRAO DE PROJETO                   ##########
######    Variaveis e funcoes com letra definidas em ingles e com    ######
##########    letras minusculas, separadas por UNDERLINE (_).    ##########
#####################                                 #####################
#endregion

#region Libraries
from random import randint

from PPlay.window import  *
from PPlay.sprite import *
from PPlay.collision import *
#endregion

#region Variables
#[START] Criando variaveis de jogo
canvas = Window(800,600)
keyboard = Window.get_keyboard()

player = Sprite("Player.png", 24)
player_x = 20
player_y = 50
player_color = "RED"

player_flag_down = True
player_flag_up = True
player_flag_space = True

enemies = []
enemies_flag_create = True
#[END] Criando variaveis de jogo
#endregion

#region Functions
############
###A Funcao on_create e a primeira funcao de jogo, ela define parametros das instancias de classe.
############
def on_create():
    canvas.set_title("JOGO")

    player.set_position(player_x, player_y)
    player.set_sequence(0,8)
    player.set_total_duration(1600)

#region Player's Functions
############
###A Funcao player_move e a responsavel pela movimentacao do personagem.
############
def player_move():
    global player_x, player_y, player_flag_up, player_flag_down

    if(keyboard.key_pressed("DOWN")):
        if(player_y >= 50 and player_y < 450 and player_flag_down):
            player_y += 200
            player_flag_down = False
    else:
        player_flag_down = True

    if(keyboard.key_pressed("UP")):
        if(player_y > 50 and player_y <= 450 and player_flag_up):
            player_y -= 200
            player_flag_up = False
    else:
        player_flag_up = True

    player.set_position(player_x, player_y)

############
###A Funcao player_change_color e a responsavel pela troca de cores do personagem.
############
def player_change_color():
    global player_color, player_flag_space

    if(keyboard.key_pressed("SPACE")):
        if(player_flag_space):
            player_flag_space = False
            temp_curr_frame = player.get_curr_frame()

            if(player_color == "RED"):
                player_color = "GREEN"
                player.set_sequence(9,16)
                player.set_curr_frame(temp_curr_frame + 8)

            elif(player_color == "GREEN"):
                player_color = "BLUE"
                player.set_sequence(17,24)
                player.set_curr_frame(temp_curr_frame + 8)

            elif(player_color == "BLUE"):
                player_color = "RED"
                player.set_sequence(0,8)
                player.set_curr_frame(temp_curr_frame - 16)
    else:
        player_flag_space = True

############
###A Funcao player_update e responsavel por aglomerar todas as funcoes do personagem com necessidade de loop.
############
def player_update():
    player_move()
    player_change_color()
    player.update()
#endregion

#region Enemies' Functions
############
###A Funcao enemy_create e responsavel por criar os inimigos de forma ordenada.
############
def enemy_create():
    global enemies_flag_create

    if((canvas.time_elapsed() / 1000) % 2 == 0 and enemies_flag_create):     #Criando inimigos a cada 2 segundos
        type = randint(1,3)                                                  #RED = 1, GREEN = 2 , BLUE = 3
        enemy_image = {1 : "EnemyRed.png", 2 : "EnemyGreen.png", 3 : "EnemyBlue.png"}[type]

        enemy = Sprite(enemy_image, 8)
        enemy_setting(enemy)

        enemies_flag_create = False

    if((canvas.time_elapsed() / 1000) % 2 != 0 and not enemies_flag_create):
        enemies_flag_create = True

############
###A Funcao enemy_setting recebe um inimigo para entregar seus comportamentos.
############
def enemy_setting(enemy):
    layer = randint(0,2)                                                     #Layer 1 = 0, Layer 2 = 1, Layer 3 = 2
    enemy_x = canvas.width
    enemy_y = (200 * layer) + 50

    enemy.set_position(enemy_x, enemy_y)
    enemy.set_total_duration(500)

    enemies.append(enemy)

############
###A Funcao enemy_update e responsavel por aglomerar todas as funcoes com necessidade de update de todos os inimigos.
############
def enemy_update():
    enemy_create()

    for enemy in enemies:
        enemy.move_x(-250 * canvas.delta_time())
        enemy.update()

############
###A Funcao enemy_draw e responsavel por aglomerar a funcao de desenho de todos os inimigos.
############
def enemy_draw():
    for enemy in enemies:
        enemy.draw()
#endregion

#############
###A Funcao update aglomera todas as funcoes gerais de update do jogo.
############
def update():
    canvas.update()
    player_update()
    enemy_update()

############
###A Funcao draw aglomera todas as funcoes gerais de desenho do jogo.
############
def draw():
    canvas.set_background_color([255,255,255])
    player.draw()
    enemy_draw()

############
###A funcao loop e responsavel pelo loop de jogo.
############
def loop():
    while(True):
        draw()
        update()
#endregion

#region Calling Functions
#[START] Chamando funcoes de criacao e loop
on_create()
loop()
#[END] Chamando funcoes de criacao e loop
#endregion