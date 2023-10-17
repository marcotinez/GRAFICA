import pyglet
from pyglet.window import Window
from pyglet import shapes
from pyglet.app import run
import random

#configs de la ventana.
WIDTH = 1000
HEIGHT = 800
WINDOW_TITLE = "Tarea 1"
FULL_SCREEN = False
ventana = Window(WIDTH,HEIGHT,WINDOW_TITLE, resizable = False)
ventana.set_fullscreen(FULL_SCREEN)
naves = pyglet.graphics.Batch()

#NAVE CENTRAL
nave_central = pyglet.graphics.Batch()
#base central
base1 = shapes.Triangle(500,450,550,200,450,200, color=(88,42,129,255), batch=nave_central)
base2 = shapes.Triangle(450,200,550,200,500,150, color=(88,42,129,255), batch=nave_central)
#ala izquierda
base3 = shapes.Triangle(500,310,450,200,300,220, color=(88,42,129,255), batch=nave_central)
base4 = shapes.Triangle(350,370,350,220,300,220, color=(88,42,129,255), batch=nave_central)
#ala derecha
base5 = shapes.Triangle(500,310,700,220,550,200, color=(88,42,129,255), batch=nave_central)
base6 = shapes.Triangle(650,370,700,220,650,220, color=(88,42,129,255), batch=nave_central)
#parte inferior
rectangle1 = shapes.Rectangle(460,150, width=20, height=100, color=(88,42,129,255), batch=nave_central)
rectangle2 = shapes.Rectangle(520,150, width=20, height=100, color=(88,42,129,255), batch=nave_central)
base7 = shapes.Triangle(520,150,550,150,520,120, color=(88,42,129,255), batch=nave_central)
base8 = shapes.Triangle(480,150,450,150,480,120, color=(88,42,129,255), batch=nave_central)
#capa 2 colores
sup1 = shapes.Triangle(500,430,540,220,460,220, color=(173,69,12,255), batch=nave_central)
sup2 = shapes.Triangle(540,220,460,220,500,170, color=(173,69,12,255), batch=nave_central)
sup3 = shapes.Triangle(470,290,455,220,320,225, color=(173,69,12,255), batch=nave_central)
sup4 = shapes.Triangle(530,290,545,220,680,225, color=(173,69,12,255), batch=nave_central)


#NAVE IZQ
nave2 = pyglet.graphics.Batch()
izq1 = shapes.Triangle(180,250,180,150,120,80, color = (25,25,112,255), batch=nave2)
izq2 = shapes.Triangle(180,250,240,80,180,150, color = (25,25,112,255), batch=nave2)
#izq3 = shapes.Triangle(130,220,230,220,180,80, color = (0,128,128,255), batch=nave2)
izq4 = shapes.Triangle(180,300,200,150,180,100, color = (72,209,204,255), batch=nave2)
izq5 = shapes.Triangle(180,300,180,100,160,150, color = (72,209,204,255), batch=nave2)

#NAVE DER
nave3 = pyglet.graphics.Batch()
izq6 = shapes.Triangle(820,250,820,150,880,80, color = (25,25,112,255), batch=nave3)
izq7 = shapes.Triangle(820,250,760,80,820,150, color = (25,25,112,255), batch=nave3)
#izq8 = shapes.Triangle(870,220,770,220,820,80, color = (0,128,128,255), batch=nave3)
izq9 = shapes.Triangle(820,300,800,150,820,100, color = (72,209,204,255), batch=nave3)
izq10 = shapes.Triangle(820,300,820,100,840,150, color = (72,209,204,255), batch=nave3)

#Estrellas
estrellas = pyglet.graphics.Batch()
star1 = shapes.Star(random.randint(0,ventana.width),810,10,15,6,rotation=2,color=(105,147,236),batch=estrellas)
star2 = shapes.Star(random.randint(0,ventana.width),810,3,9,5,rotation=2,color=(105,147,236),batch=estrellas)
star3 = shapes.Star(random.randint(0,ventana.width),810,2,8,5,rotation=2,color=(200,200,100),batch=estrellas)
star4 = shapes.Star(random.randint(0,ventana.width),810,5,7,6,rotation=2,color=(105,147,236),batch=estrellas)
star5 = shapes.Star(random.randint(0,ventana.width),810,4,8,5,rotation=2,color=(208,70,70),batch=estrellas)
star6 = shapes.Star(random.randint(0,ventana.width),810,3,10,5,rotation=2,color=(105,147,236),batch=estrellas)
star7 = shapes.Star(random.randint(0,ventana.width),810,5,10,5,rotation=2,color=(200,200,100),batch=estrellas)
star8 = shapes.Star(random.randint(0,ventana.width),810,7,12,6,rotation=2,color=(105,147,236),batch=estrellas)
star9 = shapes.Star(random.randint(0,ventana.width),810,1,5,5,rotation=2,color=(208,70,70),batch=estrellas)
star10 = shapes.Star(random.randint(0,ventana.width),810,5,10,5,rotation=2,color=(105,147,236),batch=estrellas)

#funcion que haga que las estrellas caigan en bucle
def caida(t):
    star1.y -= 1
    if star1.y < 0:
        star1.y = 815
        star1.x = random.randint(0,ventana.width)
    star2.y -= 2
    if star2.y < 0:
        star2.y = 815
        star2.x = random.randint(0,ventana.width)
    star3.y -= 3
    if star3.y < 0:
        star3.y = 815
        star3.x = random.randint(0,ventana.width)
    star4.y -= 4
    if star4.y < 0:
        star4.y = 815
        star4.x = random.randint(0,ventana.width)
    star5.y -= 5
    if star5.y < 0:
        star5.y = 815
        star5.x = random.randint(0,ventana.width)
    star6.y -= 6
    if star6.y < 0:
        star6.y = 815
        star6.x = random.randint(0,ventana.width)
    star7.y -= 7
    if star7.y < 0:
        star7.y = 815
        star7.x = random.randint(0,ventana.width)
    star8.y -= 8
    if star8.y < 0:
        star8.y = 815
        star8.x = random.randint(0,ventana.width)
    star9.y -= 9
    if star9.y < 0:
        star9.y = 815
        star9.x = random.randint(0,ventana.width)
    star10.y -= 10
    if star10.y < 0:
        star10.y = 815
        star10.x = random.randint(0,ventana.width)
    
@ventana.event
def on_draw():
    ventana.clear()
    estrellas.draw()
    nave_central.draw()
    nave2.draw()
    nave3.draw()

pyglet.clock.schedule_interval(caida, 1/180)

run()


