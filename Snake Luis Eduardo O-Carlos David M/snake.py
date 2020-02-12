# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import RedNeuronal as RN
import time
import math
import numpy as np

class Snake:
    def __init__(self,tamColum=150,tamFilas=40):
        self.tamColum=tamColum
        self.tamFilas=tamFilas
        self.movimientos=100
        self.moviDif=0
        self.score=0
        self.snake = [[int(tamFilas/2),int(tamColum/2)], [int(tamFilas/2),int(tamColum/2)-1], [int(tamFilas/2),int(tamColum/2)-2]] # Initial snake co-ordinates
        self.food = [10,20]                                                     # First food co-ordinates
        self.key = KEY_RIGHT
        self.time=0                                                    # Initializing values
        

    def interpreta(self,array):
        mayor=max(array)
        resp=[]
        if(array[0]==mayor):resp.append(119)
        if(array[1]==mayor):resp.append(97)
        if(array[2]==mayor):resp.append(115)
        if(array[3]==mayor):resp.append(100)
        
        return resp

    def distancia(self,p1,p2):
        dist=math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
        return dist
    
    def distancias(self):
        res=[]
        tempSn=self.snake
        tempSn[0][0]-=1
        res.append(self.distancia(tempSn[0],self.food)) #arriba
        
        tempSn=self.snake
        tempSn[0][1]-=1
        res.append(self.distancia(tempSn[0],self.food)) #izquierda
        
        tempSn=self.snake
        tempSn[0][0]+=1
        res.append(self.distancia(tempSn[0],self.food)) #abajo
        
        tempSn=self.snake
        tempSn[0][1]+=1
        res.append(self.distancia(tempSn[0],self.food)) #derecha
        return res


    def error(self):
        return self.distancia(self.snake[0],self.food)        
    
    def juego(self,red,hijo=0,generacion=0):
        tF=self.tamFilas
        tC=self.tamColum
        moves=self.movimientos
        
        key=self.key
        snake=self.snake
        food=self.food
        score=self.score

        start=time.time()
        
        curses.initscr()            ###crea la ventanita
        win = curses.newwin((int)(tF),(int) (tC), 0, 0)  ##determina el tamaño de la ventana
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        win.border(0)
        win.nodelay(1)

        segundos = self.time
        
        win.addch(food[0], food[1], '0')                                   # Prints the food

        errores=[]
        err=0
        while (key != 27 and moves>0 and (score+1)*30>segundos):                                               # While Esc key is not pressed
            prevKey = key   
            ambiente=[snake[0][0],snake[0][1],food[0],food[1]]+self.distancias()+[0]+[0]+[tF]+[tC]+[prevKey]
            #ambiente=self.distancias()
            #ambiente=[snake[0][0],snake[0][1],food[0],food[1]]
            #ambiente=[food[0],food[1]]
            #ambiente=self.distancias()+food
            segundos= time.time()-start
            
            
            win.border(0)
            win.addstr(0, 2, 'Score : ' + str(score) + '  Solo distancias')                # Printing 'Score' and
            win.addstr(0, (int)(tC/2-8), ' SNAKE ')
            win.addstr(0,(int)(tC)-20,' Movimientos:{} '.format(moves))
            win.addstr((int)(tF)-1,2,' Tiempo:{}'.format(int(segundos)))                                # 'SNAKE' strings
            win.addstr((int)(tF)-1,20,' redNeuronal:{}'.format(red.probar(ambiente)))##Borrar
            win.addstr(int(tF)-1,int(tC)-20,'Hijo: {}'.format(hijo))
            win.addstr(int(tF)-1,int(tC)-10,'Gen: {}'.format(generacion))
            win.timeout((int)(20))
            #win.timeout((int)(150 - 3(len(snake)/5 + len(snake)/10)%120))          # Increases the speed of Snake as its length increases
            
                                                           # Previous key pressed
            event = win.getch()
            if(event==112):
                print(red.p)
            if(event==120):
                exit()
            
            opciones=self.interpreta(red.probar(ambiente))
            if(len(opciones)>1):
                event=opciones[randint(0,len(opciones)-1)]
                err+=20
            else:
                event=opciones[0]

            if(event==119 or event==87): event =  KEY_UP # tecla w
            if(event==97  or event==65): event =  KEY_LEFT # tecla a
            if(event==115 or event==83): event =  KEY_DOWN # tecla s
            if(event==100 or event==68): event =  KEY_RIGHT # tecla d
            
            if(event==KEY_UP and prevKey == KEY_DOWN): event= prevKey
            if(event==KEY_LEFT and prevKey == KEY_RIGHT): event= prevKey
            if(event==KEY_DOWN and prevKey == KEY_UP): event= prevKey
            if(event==KEY_RIGHT and prevKey == KEY_LEFT): event= prevKey

            key = key if event == -1 else event 


            if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
                key = -1                                                   # one (Pause/Resume)
                while key != ord(' '):
                    key = win.getch()
                    if key == 120:
                        exit()
                key = prevKey
                continue
            if key != prevKey:
                self.moviDif+=1
                moves-=1


            if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
                key = prevKey
                

            # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
            # This is taken care of later at [1].
            snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

            # If snake crosses the boundaries, make it enter from the other side
            """if snake[0][0] == 0: snake[0][0] = tF-2           #choca arriba 
            if snake[0][1] == 0: snake[0][1] = tC-2           #choca izquierda
            if snake[0][0] == tF-1: snake[0][0] = 1           #choca abajo
            if snake[0][1] == tC-1: snake[0][1] = 1           #choca derecha
            """
            # Exit if snake crosses the boundaries (Uncomment to enable)
            if snake[0][0] == 0 or snake[0][0] == tF-1 or snake[0][1] == 0 or snake[0][1] == tC-1: break

            # If snake runs over itself
            if snake[0] in snake[1:]: break

            if snake[0] == food:                                            # When snake eats the food
                food = []
                score += 1
                while food == []:
                    food = [randint(1, tF-2), randint(1, tC-2)]                 # Calculating next food's coordinates
                    if food in snake: food = []
                win.addch(food[0], food[1], '0')
                moves+=10
            else:    
                last = snake.pop()                                          # [1] If it does not eat the food, length decreases
                win.addch(last[0], last[1], ' ')
            win.addch(snake[0][0], snake[0][1], '#')

            errores.append(self.error())
            self.key=key
            self.snake=snake
            self.food=food
        curses.endwin()
        self.score=score
        self.movimientos=moves
        self.time=segundos
        return np.mean(errores)+err
        """print("\nScore - " + str(self.score))
        print("Movimientos Restantes {}".format(self.movimientos))
        print("snake: {}".format(snake))
        print("http://bitemelater.in\n")"""
