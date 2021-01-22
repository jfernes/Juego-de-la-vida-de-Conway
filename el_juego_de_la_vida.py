import pygame as pg
from pygame.locals import *
import sys, random

SCREENW = 1280   #1280
SCREENH = 736  #736
LADO_CUADRADO = 16
COLOR_FONDO = (33, 33, 33)
COLOR_MUERTAS = (41, 49, 51)
COLOR_VIVAS = (235, 225, 201)
NEGRO = (0,0,0)
PROB_VIVIR = 20
TIEMPO_ESPERA = 100
FUENTE = 'bahnschrift'
TAMAÑO_FUENTE = int(SCREENW/32)
TAMAÑO_FUENTE_C = int(SCREENW/64)
TIEMPO_INTRO = 3000

class celula():
    def __init__(self, x, y, estado):
        self.x = x
        self.y = y
        self.estado = estado
        if estado == False:
            self.color = COLOR_MUERTAS
        else:
            self.color = COLOR_VIVAS

#textsurface = myfont.render('Some Text', False, (0, 0, 0))
def cinematica_intro(screen, fuente):
    screen.fill(COLOR_FONDO)
    titulo = fuente.render('E l    j u e g o    d e    l a  v i d a    -    C o n w a y', False, (COLOR_VIVAS))
    screen.blit(titulo, (int(SCREENW/2-int(TAMAÑO_FUENTE*11)), int(SCREENH/2)-int(TAMAÑO_FUENTE*7)))
    pg.display.flip()
    pg.time.wait(TIEMPO_INTRO)

def menu_inicio(screen, fuente):
    seleccion = False
    opcion = None
    while(not(seleccion)):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_1 or event.key == K_ESCAPE:
                    seleccion = True
                    opcion = 1
                elif event.key == K_2:
                    seleccion = True
                    opcion = 2

        screen.fill(COLOR_FONDO)
        titulo = fuente.render('Seleccione una opción (pulsando un numero)', False, (COLOR_VIVAS))
        op1 = fuente.render('1 - Generacion aleatoria del mapa inicial', False, (COLOR_VIVAS))
        op2 = fuente.render('2 - Cells in a row (ciclo)', False, (COLOR_VIVAS))
        op_esc = fuente.render('Pulsa esc para selección por defecto', False, (COLOR_VIVAS))
        screen.blit(titulo, (int(SCREENW/100),int(SCREENH/100)))
        screen.blit(op1, (int(SCREENW/100), int(SCREENH*10/100)))
        screen.blit(op2, (int(SCREENW/100), int(SCREENH*20/100)))
        screen.blit(op_esc, (int(SCREENW/100), int(SCREENH*90/100)))
        pg.display.flip()
    return opcion

def opciones(op):
    celulas = []
    if op == 1:
        celulas = generar_estado_inicial_aleatorio()
    elif op == 2:
        celulas = generar_cells_row()
    return celulas



def generar_estado_inicial_aleatorio():
    celulas = []
    for i in range(-LADO_CUADRADO, SCREENW + LADO_CUADRADO, LADO_CUADRADO):
        aux = []
        for j in range(-LADO_CUADRADO, SCREENH + LADO_CUADRADO, LADO_CUADRADO):
            if ((j < 0) or (j >= SCREENH) or (i < 0) or (i >= SCREENW)):
                estado = False
            else:
                estado = random.randint(0, 100) < PROB_VIVIR
            aux.append(celula(i, j, estado))
        celulas.append(aux)
    return celulas

def generar_cells_row():
    celulas = []
    for i in range(-LADO_CUADRADO, SCREENW + LADO_CUADRADO, LADO_CUADRADO):
        aux = []
        for j in range(-LADO_CUADRADO, SCREENH + LADO_CUADRADO, LADO_CUADRADO):
            if (j == 368 and i in range (560,720,LADO_CUADRADO)):
                estado = True
            else:
                estado = False
            aux.append(celula(i, j, estado))
        celulas.append(aux)
    return celulas


def calcular_estado(c, x, y):
    #print(x, y)
    vivas1 = c[x-1][y-1].estado + c[x][y-1].estado + c[x+1][y-1].estado + c[x-1][y].estado
    vivas2 = c[x+1][y].estado + c[x-1][y+1].estado + c[x][y+1].estado + c[x+1][y+1].estado
    vivas = vivas1 + vivas2

    if (vivas == 3 and c[x][y].estado == False):
        return True
    elif ((vivas==2 or vivas ==3) and c[x][y].estado == True):
        return True
    elif (vivas <= 1 or vivas > 3):
        return False
    else:
        return False

def generar_nuevo_mapa(celulas):
    celulas_nuevo = []
    for i in range(len(celulas)):
        aux = []
        for j in range(len(celulas[i])):
            if(i>0 and i<len(celulas)-1 and j>0 and j<len(celulas[i])-1):
                estado = calcular_estado(celulas, i, j)
            else:
                estado = False
            aux.append(celula((i-1)*LADO_CUADRADO, (j-1)*LADO_CUADRADO, estado))
        celulas_nuevo.append(aux)
    return celulas_nuevo

def dibuja_celulas(celulas):
    for i in range(len(celulas)):
        for j in range(len(celulas[i])):
            pg.draw.rect(screen, celulas[i][j].color, (celulas[i][j].x, celulas[i][j].y, LADO_CUADRADO, LADO_CUADRADO))


if __name__ == "__main__":
    #inicializar la ventana, con nombre y titulo
    pg.init()
    screen = pg.display.set_mode((SCREENW, SCREENH))
    pg.display.set_caption("El juego de la vida")

    #creditos iniciales y menú de inicio
    pg.font.init()
    fuente = pg.font.SysFont(FUENTE,TAMAÑO_FUENTE)
    cinematica_intro(screen, fuente)
    opcion = menu_inicio(screen, fuente)

    #crear unas condiciones iniciales
    celulas = opciones(opcion)

    #dibuajar el mapa inicial aleatorio
    dibuja_celulas(celulas)
    pg.display.flip()
    pg.time.wait(TIEMPO_ESPERA)

    #variables de control, inicializacion
    pause = False

    #bucle principal infinito
    while (True):
        #control de eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_p:
                    pause = not(pause)
                elif event.key == K_ESCAPE:
                    pause == True
                    opcion = menu_inicio(screen, fuente)
                    celulas = opciones(opcion)
                elif event.key == K_r:
                    celulas = generar_estado_inicial_aleatorio()

        if (pause == False):
            celulas = generar_nuevo_mapa(celulas)

        #dibujar los objetos
        screen.fill(COLOR_FONDO)
        dibuja_celulas(celulas)

        fuente_chikita = pg.font.SysFont(FUENTE, TAMAÑO_FUENTE_C)
        texto_esc = fuente_chikita.render('ESC para volver al menu', False, NEGRO)
        texto_p = fuente_chikita.render('P para pausar el juego', False, NEGRO)
        texto_r = fuente_chikita.render('R para plantilla aleatoria', False, NEGRO)
        screen.blit(texto_esc, (10, 10))
        screen.blit(texto_p, (10, 30))
        screen.blit(texto_r, (10, 50))

        #actualizacion de la pantalla
        pg.time.wait(TIEMPO_ESPERA)
        pg.display.flip()