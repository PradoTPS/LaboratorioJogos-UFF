#region PROJECT PATTERN
#####################                                 #####################
##########                   PADRAO DE PROJETO                   ##########
######    Variaveis e funcoes com letra definidas em ingles e com    ######
##########    letras minusculas, separadas por UNDERLINE (_).    ##########
#####################                                 #####################
#endregion

#region Libraries
from random import randint

from PPlay.window import *
from PPlay.sprite import *
from PPlay.collision import *
from PPlay.gameimage import *
#endregion

#region Variables
canvas = Window(800,600)
canvas_initial_time = canvas.delta_time()
keyboard = Window.get_keyboard()

screen = "GAMEPLAY"

background = GameImage("resources/images/Background.png")
background2 = GameImage("resources/images/Background.png")
background_x = 0
background2_x = 1600

player = Sprite("resources/images/Player.png", 24)
player_x = 20
player_y = 250
player_color = "RED"

player_flag_down = True
player_flag_up = True
player_flag_space = True

enemies = []
enemies_colors = []
enemies_flag_create = True

score = 0
score_streak = 1
#endregion

#region Functions
#region Moment Functions
#############
###A Funcao on_create e a primeira funcao de jogo, ela define parametros das instancias de classe.
############
def on_create():
    canvas.set_title("JOGO")

    player.set_position(player_x, player_y)
    player.set_sequence(0,8)
    player.set_total_duration(1600)


############
###A Funcao on_restart reinicia as variaveis necessarias para o gameplay.
############
def on_restart():
    global player_x, player_y, player_color, enemies, enemies_colors, background_x, background2_x

    player_x = 20
    player_y = 250
    player_color = "RED"

    enemies = []
    enemies_colors = []

    background_x = 0
    background2_x = 1600

    player.set_position(player_x, player_y)
    player.set_sequence(0,8)

    background.set_position(background_x, 0)
    background2.set_position(background2_x, 0)
#endregion

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
        enemy_color = {"EnemyRed.png": "RED", "EnemyGreen.png": "GREEN", "EnemyBlue.png": "BLUE"}[enemy_image]

        enemy = Sprite("resources/images/" + enemy_image, 8)
        enemy_setting(enemy, enemy_color)

        enemies_flag_create = False

    if((canvas.time_elapsed() / 1000) % 2 != 0 and not enemies_flag_create):
        enemies_flag_create = True


############
###A Funcao enemy_setting recebe um inimigo para entregar seus comportamentos.
############
def enemy_setting(enemy, enemy_color):
    layer = randint(0,2)                                                     #Layer 1 = 0, Layer 2 = 1, Layer 3 = 2
    enemy_x = canvas.width
    enemy_y = (200 * layer) + 50

    enemy.set_position(enemy_x, enemy_y)
    enemy.set_total_duration(500)

    enemies.append(enemy)
    enemies_colors.append(enemy_color)


############
###A Funcao enemy_collision verifica as colisoes de todos os inimigos com o personagem e com o limite de destruicao.
############
def enemy_collision():
    global screen, score, score_streak

    index = 0

    for enemy in enemies:
        if (Collision.collided(enemies[index], player)):    #Verifica se um inimigo de determinado indice
            if (enemies_colors[index] == player_color):     #colidiu com o player. Se eles tem a mesma cor
                enemies.pop(index)                          #o inimigo e destruido. Se eles tem cores diferente
                enemies_colors.pop(index)                   #o jogo vai para a tela de GAMEOVER.

                score_add()
            else:
                screen = "GAMEOVER"

        index = index + 1


############
###A Funcao enemy_update e responsavel por aglomerar todas as funcoes com necessidade de update de todos os inimigos.
############
def enemy_update():
    enemy_create()

    for enemy in enemies:
        enemy.move_x(-250 * canvas.delta_time())
        enemy_collision()
        enemy.update()


############
###A Funcao enemy_draw e responsavel por aglomerar a funcao de desenho de todos os inimigos.
############
def enemy_draw():
    for enemy in enemies:
        enemy.draw()
#endregion

#region Background's Functions
############
###A Funcao background_move e responsavel pela movimentacao dos fundos.
############
def background_move():
    global canvas_initial_time, background_x, background2_x

    if(canvas_initial_time % 270 == 0):
        background_x += -1
    if(canvas_initial_time % 270 == 0):
        background2_x += -1

    if(background_x <= -1600):
            background_x = 1600
    if(background2_x <= -1600):
            background2_x = 1600

    background.set_position(background_x,0)
    background2.set_position(background2_x,0)


############
###A Funcao background_draw aglomera todas as funcoes de desenho dos fundos.
############
def background_draw():
    background.draw()
    background2.draw()
#endregion

#region Score's Functions
############
###A Funcao score_update e responsavel por aumentar os valores de score e score_streak.
############
def score_add():
    global score, score_streak

    if(score == 0):
        score = 1
    else:
        score = score + score_streak

    score_streak = score_streak + 1


############
###A Funcao score_update e responsavel por reiniciar os valores de score e score_streak.
############
def score_update():
    global score, score_streak

    if(screen == "GAMEOVER"):
        score = 0
        score_streak = 1


############
###A Funcao score_draw e responsavel por desenhar a pontuacao na tela.
############
def score_draw ():
    canvas.draw_text("Pontos: %s" % (score), 20, 20, size = 20, color = (0,0,0), font_name = "Arial", bold = True, italic = False)

    if (score != 0):
        canvas.draw_text("+%s" % (1 * score_streak), 20, 50, size = 20, color = (0,0,0), font_name = "Arial", bold = True, italic = False)
#endregion

#region Utility Functions
#############
###A Funcao check_gameover verifica se o status e GAMEOVER e reinicia o jogo.
############
def check_gameover():
    global screen

    if(screen == "GAMEOVER"):
        on_restart()
        screen = "GAMEPLAY"
#endregion

#region Structure Functions
#############
###A Funcao update aglomera todas as funcoes gerais de update do jogo.
############
def update():
    canvas.update()
    check_gameover()

    if(screen == "GAMEPLAY"):
        background_move()
        player_update()
        enemy_update()

    score_update()


############
###A Funcao draw aglomera todas as funcoes gerais de desenho do jogo.
############
def draw():
    canvas.set_background_color([255,255,255])

    if(screen == "GAMEPLAY"):
        background_draw()
        score_draw()
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
#endregion

#region Calling Functions
on_create()
loop()
#endregion
