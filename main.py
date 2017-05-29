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
keyboard = Window.get_keyboard()

screen = "MENU"
current_button = "PLAY"

button_play = GameImage("resources/images/Play.png")
button_play_x = canvas.width / 2 - button_play.width / 2
button_play_y = canvas.height / 2 + button_play.height / 2

button_options = GameImage("resources/images/Options.png")
button_options_x = ((canvas.width / 2 - button_options.width / 2) - button_options.width / 2) - 30
button_options_y = (canvas.height / 2 + button_play.height / 2) + button_options.height + 10

button_credits = GameImage("resources/images/Credits.png")
button_credits_x = ((canvas.width / 2 - button_credits.width / 2) + button_credits.width / 2) + 30
button_credits_y = (canvas.height / 2 + button_play.height / 2) + button_credits.height + 10

score = 0
score_streak = 1

background = GameImage("resources/images/Background.png")
background2 = GameImage("resources/images/Background.png")
background_x = 0
background2_x = 800

clouds = GameImage("resources/images/Nuvens.png")
clouds2 = GameImage("resources/images/Nuvens.png")
clouds_x = 0
clouds2_x = 800

bush = GameImage("resources/images/Arbusto.png")
bush2 = GameImage("resources/images/Arbusto.png")
bush_x = 0
bush2_x = 800

player = Sprite("resources/images/Player.png", 24)
player_x = 20
player_y = 300
player_color = "RED"

player_flag_down = True
player_flag_up = True
player_flag_space = True

enemies = []
enemies_colors = []
enemies_flag_create = True
#endregion

#region Functions
#region Moment Functions
#############
###A Funcao on_create e a primeira funcao de jogo, ela define parametros das instancias de classe.
############
def on_create():
    canvas.set_title("Color Enchantment")

    player.set_position(player_x, player_y)
    player.set_sequence(0,8)
    player.set_total_duration(1600)

    button_play.set_position(button_play_x, button_play_y)
    button_options.set_position(button_options_x, button_options_y)
    button_credits.set_position(button_credits_x, button_credits_y)


############
###A Funcao on_restart reinicia as variaveis necessarias para o gameplay.
############
def on_restart():
    global player_x, player_y, player_color, enemies, enemies_colors, background_x, background2_x, clouds_x, clouds2_x, bush_x, bush2_x

    player_x = 20
    player_y = 300
    player_color = "RED"

    enemies = []
    enemies_colors = []

    background_x = 0
    background2_x = 800

    clouds_x = 0
    clouds2_x = 800

    bush_x = 0
    bush2_x = 800

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
        if(player_y >= 150 and player_y < 450 and player_flag_down):
            player_y += 150
            player_flag_down = False
    else:
        player_flag_down = True

    if(keyboard.key_pressed("UP")):
        if(player_y > 150 and player_y <= 450 and player_flag_up):
            player_y -= 150
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
    enemy_y = (150 * layer) + 150

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
    global background_x, background2_x

    background_x += -200 * canvas.delta_time()
    background2_x += -200 * canvas.delta_time()

    if(background_x <= -800):
        background_x = 800
        background2_x = 0
    if(background2_x <= -800):
        background2_x = 800
        background_x = 0

    background.set_position(background_x,0)
    background2.set_position(background2_x,0)


############
###A Funcao clouds_move e responsavel pela movimentacao das nuvens.
############
def clouds_move():
    global clouds_x, clouds2_x

    clouds_x += -100 * canvas.delta_time()
    clouds2_x += -100 * canvas.delta_time()

    if(clouds_x <= -800):
        clouds_x = 800
        clouds2_x = 0
    if(clouds2_x <= -800):
        clouds2_x = 800
        clouds_x = 0

    clouds.set_position(clouds_x,0)
    clouds2.set_position(clouds2_x,0)


############
###A Funcao bush_move e responsavel pela movimentacao do arbusto.
############
def bush_move():
    global bush_x, bush2_x

    bush_x += -300 * canvas.delta_time()
    bush2_x += -300 * canvas.delta_time()

    if(bush_x <= -800):
        bush_x = 800
        bush2_x = 0
    if(bush2_x <= -800):
        bush2_x = 800
        bush_x = 0

    bush.set_position(bush_x,0)
    bush2.set_position(bush2_x,0)


############
###A Funcao background_update aglomera todas as funcoes de movimentacao de todos os fundos.
############
def background_update():
    clouds_move()
    background_move()
    bush_move()


############
###A Funcao bush_draw aglomera as funcoes de desenho dos arbustos.
############
def bush_draw():
    bush.draw()
    bush2.draw()


############
###A Funcao background_draw aglomera todas as funcoes de desenho de todos os fundos.
############
def background_draw():
    clouds.draw()
    clouds2.draw()

    background.draw()
    background2.draw()       #A funcao de movimentacao do arbusto esta diretamente no update pra poder ficar em cima de tudo
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

#region Buttons' Functions
############
###A Funcao button_draw aglomera todas as funcoes de desenho de todos os botoes.
############
def button_draw():
    button_play.draw()
    button_options.draw()
    button_credits.draw()
#endregion

#region Utility Functions
#############
###A Funcao check_gameover verifica se o status e GAMEOVER e reinicia o jogo.
############
def check_gameover():
    global screen

    if(screen == "GAMEOVER"):
        on_restart()
        screen = "MENU"


#############
###A Funcao navigate e responsavel pela navegacao no menu principal.
############
def navigate():
    global current_button, screen

    if(keyboard.key_pressed("DOWN") and current_button == "PLAY"):
        current_button = "OPTIONS"
    elif(keyboard.key_pressed("RIGHT") and current_button == "OPTIONS"):
        current_button = "CREDITS"
    elif(keyboard.key_pressed("LEFT") and current_button == "CREDITS"):
        current_button = "OPTIONS"
    elif(keyboard.key_pressed("UP") and current_button == "OPTIONS"):
        current_button = "PLAY"
    elif(keyboard.key_pressed("UP") and current_button == "CREDITS"):
        current_button = "PLAY"

    if(keyboard.key_pressed("ENTER") or keyboard.key_pressed("SPACE")):
        if(current_button == "PLAY"):
            screen = "GAMEPLAY"
        if(current_button == "OPTIONS"):
            screen = "OPTIONS"
        if(current_button == "CREDITS"):
            screen = "CREDITS"

    if(keyboard.key_pressed("ESC")):
        if(current_button == "BACK"):
            screen = "MENU"
            current_button = "PLAY"

    if(screen == "GAMEPLAY"):
        current_button = "PLAY"
    if(screen == "CREDITS" or screen == "OPTIONS"):
        current_button = "BACK"
#endregion

#region Structure Functions
#############
###A Funcao update aglomera todas as funcoes gerais de update do jogo.
############
def update():
    canvas.update()
    navigate()
    check_gameover()

    background_update()

    if(screen == "GAMEPLAY"):
        player_update()
        enemy_update()

    score_update()


############
###A Funcao draw aglomera todas as funcoes gerais de desenho do jogo.
############
def draw():
    canvas.set_background_color([255,255,255])

    background_draw()
    if(screen == "MENU"):
        button_draw()

    if(screen == "GAMEPLAY"):
        score_draw()
        player.draw()
        enemy_draw()

    bush_draw()      #O desenho do arbusto esta aqui para sobrepor todas as imagens


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
