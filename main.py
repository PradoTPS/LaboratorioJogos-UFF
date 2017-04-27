#region PROJECT PATTERN
#####################                                 #####################
##########                   PADRAO DE PROJETO                   ##########
######    Variaveis e funcoes com letra definidas em ingles e com    ######
##########    letras minusculas, separadas por UNDERLINE (_).    ##########
#####################                                 #####################
#endregion

#region Libraries
from PPlay.window import  *
from PPlay.sprite import *
#endregion

#region Variables
#[START] Criando variaveis de jogo
canvas = Window(800,600)
keyboard = Window.get_keyboard()

player = Sprite("boy.png", 24)
player_x = 20
player_y = 50
player_color = "RED"

player_flag_down = True
player_flag_up = True
player_flag_space = True
#[END] Criando variaveis de jogo
#endregion

#region Functions
############
###A Funcao on_create e a primeira funcao de jogo, ela define parametros das instancias de classe.
############
def on_create():
    player.set_position(player_x, player_y)
    player.set_sequence(0,8)
    player.set_total_duration(1600)

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

#############
###A Funcao update aglomera todas as funcoes gerais de update do jogo.
############
def update():
    canvas.update()
    player_update()

############
###A Funcao draw aglomera todas as funcoes gerais de desenho do jogo.
############
def draw():
    canvas.set_background_color([255,255,255])
    player.draw()

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