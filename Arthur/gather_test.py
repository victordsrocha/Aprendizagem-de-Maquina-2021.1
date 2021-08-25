#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import math
import numpy as np
import csv
filename = 'dataset_test_.csv'


# import csv
# writer = csv.writer(open(filename,'w',newline=''))
# INP = [['x'+str(i)]+['y'+str(i)] for i in range(2)]
# INP = [j for i in INP for j in i]
# OUT = ['sentido X','sentido y','forca']
# OUT2 = [['x'+str(100+i)]+['y'+str(100+i)] for i in range(2)]
# OUT2 = [j for i in OUT2 for j in i]
# writer.writerow(INP+OUT+OUT2+['Custo','Diferença Custo','Custo Produto', 'Diferença Custo Produto','Collision_x','Collision_y'])
# 

# In[2]:


#Primeiro crio a classe bola
#A classe vai ter posição, velocidade e cor.
class Ball:
 #Inicializar default como uma bola branca no centro
 def __init__(self, pos=.5+.375j, v=0, color=(255,255,255), void=0, ball=None):
  if ball:
   pos = ball.pos
   v = ball.v
   color = ball.color
   void = ball.void
  self.pos = pos
  self.v = v
  #A cor vai ser um tuple em RGB
  self.color = color
  #as bolas encaçapadas tem void = posição que foi encaçapada, do contrário, void = 0
  self.void = void

class Player:
 #O Jogador vai ter as propriedades número, como maneira de identificá-lo e pontuação que seria o número de bolas encaçapadas
 def __init__(self,number,computer=1,score=0):
  self.number = number
  self.score = score
  self.computer = computer


# In[3]:


#Depois crio a classe pool que vai ser a mesa
class pool:
 #A mesa começa sem bolas por default, deixei a possibilidade de inicializar com uma lista de bolas, caso preciso
 def __init__(self, balls=[], players=[], turn=0):
  self.balls = balls
  self.players = players
  self.turn = turn
  self.foul = 0
  self.score = 0
 #Função de adicionar bola, adiciona uma bola à lista de bolas da mesa
 def addball(self,ball):
  self.balls.append(ball)
 def addplayer(self,player):
  self.players.append(player)
 def nextturn(self):
  self.turn = (not self.turn)


# In[4]:


#Crio uma mesa
mypool = pool()
#Adiciono 7 bolas a essa mesa
mypool.addball(Ball())
x = .8+.375j #posição inicial do triângulo
post=[x]
for pos2 in post:
 mypool.addball(Ball(pos=pos2,color=(127+np.random.randint(128),0,127+np.random.randint(127))))
mypool.addplayer(Player(0,1,0))#numero do jogador, é um computador?, score
mypool.addplayer(Player(1,1,0))
#Constantes
atrito = .998 #não é atrito de verdade, seria mais 1-coeficiente de atrito
sts = .00002 #"força por milissegundo pressionado"
maxspeed = .003
voids = [.01+.01j,.01+.74j,.99+.01j,.99+.74j]
dclosest = lambda pos: min([abs(pos-void) for void in voids])
collision = 0


# In[5]:


from numpy import angle
def angulo(x):
 return angle(x)+6.28 if x.imag<0 else angle(x)


# In[6]:


#Aqui vamos definir como a sinuca ficará após um instante que idealmente seria 0
def next(mypool,ghost):
    for ball in mypool.balls:
      #velocidade mínima
      if abs(ball.v)<.0001: continue
      nextpos = ball.pos+ball.v
      if nextpos.real < .01: #batida no lado esquerdo da sinuca
       ball.pos = .01+nextpos.imag*1j
       ball.v = -ball.v.real+ball.v.imag*1j #troca o componente x da velocidade
       continue
      if nextpos.imag < .01: #batida na parte de cima da sinuca
       ball.pos=nextpos.real+1j*.01
       ball.v = ball.v.real-ball.v.imag*1j #troca o componente y da velocidade
       continue
      if nextpos.real > .99: #batida no lado direito da sinuca
       ball.pos=.99+nextpos.imag*1j
       ball.v = -ball.v.real+ball.v.imag*1j #troca o componente x da velocidade
       continue
      if nextpos.imag > .74: #batida na parte de baixo da sinuca
       ball.pos=nextpos.real+1j*.74
       ball.v = ball.v.real-ball.v.imag*1j #troca o componente y da velocidade
       continue
      #aqui vou navegar por todas as bolas e ver se alguma encosta, ou seja, tem uma distância menor que a soma dos raios
      for secball in mypool.balls:
       if secball.color == ball.color: continue
       if secball.void: continue #ignora bolas encaçapadas
       #se tiver a distância menor que a soma dos raios, muda a velocidade das duas
       if abs(nextpos-secball.pos)<.02:
        #(ball.real - sec.real) < 0 and (ball.imag - sec.imag)<0 rot negativa
        #(ball.real - sec.real) > 0 and (ball.imag - sec.imag)>0 rot negativa
        rot = math.pi/2
        #a (x0i + y0j) + b (x1i +y1j) = (x2i + y2j)
        #variáveis conhecidas: x0,x1,x2,y0,y1,y2
        #a x0 + b x1 = x2
        #a y0 + b y1 = y2
        #a = (x2 * y1 - x1 * y2) / (x0 * y1 - x1 * y0)
        #b = (x0 * y2 - x2 * y0) / (x0 * y1 - x1 * y0)
        momento = ball.v# a resultante tem que ser igual a isso
        secball.v = (nextpos-secball.pos)/abs(nextpos-secball.pos)
        ball.v = (nextpos-secball.pos)/abs(nextpos-secball.pos)*(math.e**(1j*rot))
        #print(momento)
        #print(secball.v)
        #print(ball.v)
        if abs(angulo(ball.v)-angulo(momento))>math.pi/2:
         rot *= -1
        ball.v = (nextpos-secball.pos)/abs(nextpos-secball.pos)*(math.e**(1j*rot))        
        #a (ball.v.reali + ball.v.imagj) + b (secball.v.reali +secball.v.imagj) = (momento.reali + momento.imagj)
        #variáveis conhecidas: ball.v.real,secball.v.real,momento.real,ball.v.imag,secball.v.imag,momento.imag
        #a ball.v.real + b secball.v.real = momento.real
        #a ball.v.imag + b secball.v.imag = momento.imag
        a = (momento.real * secball.v.imag - secball.v.real * momento.imag) / (ball.v.real * secball.v.imag - secball.v.real * ball.v.imag)
        b = (ball.v.real * momento.imag - momento.real * ball.v.imag) / (ball.v.real * secball.v.imag - secball.v.real * ball.v.imag)
        ball.v*=a
        secball.v*=b
        #pygame.draw.line(screen, (255,255,255), ((ball.pos).real*sz[0],(ball.pos).imag*sz[0]), ((10000*secball.v+ball.pos).real*sz[0],(10000*ball.v+ball.pos).imag*sz[0]),3)
        #pygame.display.update()
       #enquanto elas não desencostarem, elas tem que se mexer
        while abs(nextpos-secball.pos)<.02:
         global collision
         if not collision: collision = nextpos
         secball.pos += secball.v
         ball.pos += ball.v
         if ball.pos.real < .01: #batida no lado esquerdo da sinuca
          ball.pos = .01+nextpos.imag*1j
          ball.v = -ball.v.real+ball.v.imag*1j #troca o componente x da velocidade
         if ball.pos.imag < .01: #batida na parte de cima da sinuca
          ball.pos=nextpos.real+1j*.01
          ball.v = ball.v.real-ball.v.imag*1j #troca o componente y da velocidade
         if ball.pos.real > .99: #batida no lado direito da sinuca
          ball.pos=.99+nextpos.imag*1j
          ball.v = -ball.v.real+ball.v.imag*1j #troca o componente x da velocidade
         if ball.pos.imag > .74: #batida na parte de baixo da sinuca
          ball.pos=nextpos.real+1j*.74
          ball.v = ball.v.real-ball.v.imag*1j #troca o componente y da velocidade
        continue
      #Aqui só chega se não houver nenhuma colisão 
      #Para ver se a bola foi encaçapada, verificamos se a velocidade está abaixo do aceitável e se a distância do centro
      #da bola para um dos buracos está adequada
      if ghost==False:
       for void in voids:
        if abs(nextpos - void)<.015 and abs(ball.v)<.005:
         if ball.color==(255,255,255): #se a bola for branca ela deve ser levada à sua posição inicial
          ball.void = 1
          ball.v = 0
          mypool.foul = 1 #se houver falta, será adicionada uma nova bola branca
         else:
          ball.v=0
          nextpos=void
          ball.void=void
          mypool.score=1
      ball.pos=nextpos
      ball.v*=atrito
    return mypool
    


# In[7]:


def trajetoria(taco,mypool,ball,it):
    #a bola fantasma funciona basicamente como a bola normal, só a velocidade que muda praticamente
    ghostpool=pool(balls=[])
    #[print(ball) for ball in ghostpool.balls)]
    for balls in mypool.balls:
     if balls.void: continue
     ghostpool.addball(Ball(ball=balls))
    for balls in ghostpool.balls:
     if balls.color == ball.color:
      balls.v = taco*maxspeed
    k = 0
    while(1):
      k+=1;
      if k==it: break
      for i in range(it):
       next(ghostpool,True)
      if sum([abs(balls.v) for balls in ghostpool.balls])<.0001: break
      for balls in ghostpool.balls:
       pygame.draw.circle(screen, balls.color,(balls.pos.real*sz[0],balls.pos.imag*sz[0]),1)
    


# In[9]:


i=0
tempo = 0 #tempo que segurou o mouse pra tacada
turn = 0
inplay = 1 #está em jogo
jogadas = 0
U = True
collision = 0 #variável que informa onde foi a primeira colisão

data = np.genfromtxt('dataset_test.csv', delimiter=',',dtype = np.float64)
data = data[:,:6]

line0 = 0#linha de recriação da jogada
replay_on = True
img_on = False

if img_on:
 import pygame, sys
 from pygame.locals import *
 #Inicializa o módulo pygame
 pygame.init()
 #Defini o tamanho da tela
 sz = (800,600)
 screen = pygame.display.set_mode(sz,0,32)
 #Defini a fonte que será usada no jogo
 myFont = [pygame.font.SysFont('arial', 14),
           pygame.font.SysFont('arial',16, bold=True)]

#recriar jogada
def inicializar(line):
 total = (data.shape[1]-2)//2
 for ball2 in mypool.balls: ball2.v=0
 print(data.shape)
 print(line)
 print(data[line,:])
 for i in range(total):
  mypool.balls[i].pos = data[line,2*i] + 1j*data[line,2*i+1]
  mypool.balls[i].void = 0
 mypool.balls[0].v = maxspeed*(data[line,2*total]+1j*data[line,2*total+1])
 
    

def newframe():
     #newframe()
     screen.fill((0,100,0))    
     #Aqui é uma lista com o centro de cada buraco, futuramente vou checar se a distância do centro da bola é menor que
     #algum valor, e, se for, a bola será encaçapada com um .pop() no mypool.balls, não fiz ainda porque to resolvendo
     #o problema das colisões
     for void in voids:
      #aqui desenha cada buraco fazendo um circulo de 9 pixels ao redor do buraco
      #o primeiro parametro é a tela, o segundo a cor, o terceiro, que é um tuple (a,b) é a posição e o último é o raio
      pygame.draw.circle(screen, (0,0,0),(void.real*sz[0],void.imag*sz[0]),9)
     #aqui vamos desenhar cada bola presente na lista de bolas da sinuca
     for ball in mypool.balls:
      #ao redor da bola branca, desenhamos o taco
      if ball.color == (255,255,255):
       if inplay == 0:
        x,y = pygame.mouse.get_pos()
        mousepos = x/800+y/800*1j
        taco = mousepos-ball.pos
        taco=(taco/abs(taco))*1
        #Para exemplificar, um taco paralelo ao eixo x iria de
        #x = (-0.4 + x_bola_branca) e y = 0 
        #até x = (-0.05 + x_bola_branca) e y = 0
        #Seja u o vetor x+iy que representa a bola branca e v o vetor x+iy que representa o início do taco,
        #o taco tendo 0.35 u.c. de comprimento, ele vai de
        # -0.4v+u  até -0.05v+u
        #o primeiro parametro é a tela, o segundo a cor, o terceiro, que é um tuple (a,b) é a posição e o último é o raio
        pygame.draw.line(screen, (255,255,0), ((-.4*taco+ball.pos).real*sz[0],(-.4*taco+ball.pos).imag*sz[0]), ((-.05*taco+ball.pos).real*sz[0],(-.05*taco+ball.pos).imag*sz[0]),3)
        #tg = (ball.pos.real-x/800)
        #Aqui, se a bola estiver parada, ou seja, a velocidade for inferior a .0001, todas as bolas ficarão realmente
        #paradas e a trajetória é visualizada (mais ou menos) através de uma bola fantasma
        #seria aq a brincadeira
        trajetoria(taco,mypool,ball,20)
      if ball.void: continue #ignora bolas encaçapadas
      #aqui desenha cada bola 
      pygame.draw.circle(screen, (0,0,0),(ball.pos.real*sz[0],ball.pos.imag*sz[0]),9)
      pygame.draw.circle(screen,ball.color,(ball.pos.real*sz[0],ball.pos.imag*sz[0]),8)     
     pygame.display.update()
    
while True:

    i+=1
    if img_on:
     for event in pygame.event.get():
        if inplay==1: break
        #quando aperta o botão do mouse, começa a marcar um tempo pra determinar a força (mais tempo = mais forte)
        if event.type == pygame.MOUSEBUTTONDOWN:
         tempo = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONUP:
         #aqui temos o tempo que o mouse ficou pressionado
         tempo = pygame.time.get_ticks() - tempo
         #Aqui obtemos as coordenadas do mouse
         x,y = pygame.mouse.get_pos()
         #aqui a posição do mouse convertidas para a unidade que queremos
         mousepos = x/800+y/800*1j
         #O taco vai ser basicamente o vetor formado pela semirreta entre a bola e o mouse
         taco = mousepos-mypool.balls[0].pos
         #Normalizando o taco
         taco=(taco/abs(taco))*1
         #a força vai ser esse vetor unitário multiplicado pelo tempo que ficou pressionado, e dividi por 250.000 pra
         #ficar menor, já que o tempo é em microssegundos e a sinuca inteira tem 1 unidade de comprimento
         #eu aconselharia fazer um max(tempo,VALOR) se for usar como jogo, como só to testando o limite é o infinito
         forca = (taco)* min(tempo * sts, maxspeed)
         #essa força vai ser a velocidade da bola branca
         mypool.balls[0].v = forca
         inplay = 1
         tempo = 0
        #esse if é só pra sair do jogo quando fechar
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    #aqui chamamos a função que vai trazer o próximo estado da sinuca, ou seja, a sinuca em t = t + dt
    #para ficar mais preciso, os intervalos foram feitos menores e executados 5 vezes a cada visualização
    for j in range(1):
     mypool = next(mypool,False)
    #aqui, verificamos o fim de um turno e início do turno posterior
    
    if img_on: newframe()
    if sum([abs(ball.v) for ball in mypool.balls])<.0005:
        inplay=0
        #aqui seria o fim do turno, a velocidade é próxima de zero mas diferente de zero
        if mypool.foul == 1:
         jogadas+=1
         if sum([abs(ball.v) for ball in mypool.balls])==0: mypool.nextturn()
         for i in range(len(mypool.balls)): mypool.balls[i].v=0
         mypool.balls[0].v=0;mypool.balls[0].pos=.5+.375j; mypool.balls[0].void=0; mypool.foul=0
        if sum([abs(ball.v) for ball in mypool.balls])!=0:
         jogadas+=1
         mypool.players[mypool.turn].score+=mypool.score
         if mypool.players[mypool.turn].computer==1: #fim do turno do computador
          line0+=1
          #essas são as entradas
          INP = np.array([[pos.real,pos.imag] for pos in inputplay['posição das bolas']]).reshape(2*len(inputplay['posição das bolas'])).tolist()
          #essa seria uma saída
          OUT = [inputplay['forca'].real,inputplay['forca'].imag]+[inputplay['velocidade']]
          #e esse o resultado da saída
          OUT2complex = [ballx.pos if ballx.color!=(255,255,255) else ballx.pos for ballx in mypool.balls]
          OUT2 = np.array([[pos.real,pos.imag] for pos in OUT2complex]).reshape(2*len(OUT2complex)).tolist()
          #custo
          #distância pro buraco mais próximo
          CUSTO = np.sum([dclosest(ballx.pos) if (ballx.color!=(255,255,255) and ballx.void==0) else 0 for ballx in mypool.balls])/max(np.sum([1 if (ballx.color!=(255,255,255) and ballx.void==0) else 0 for ballx in mypool.balls]),1)
          diffCUSTO = CUSTO - inputplay['CUSTO']
          if mypool.score==1: CUSTOprod = 0; diffCUSTOprod = 0
          else:
           logCUSTOprod = np.sum([np.log(dclosest(ballx.pos)) if (ballx.color!=(255,255,255) and ballx.void==0) else 0 for ballx in mypool.balls])
           CUSTOprod = np.e**logCUSTOprod
           diffCUSTOprod = CUSTOprod / inputplay['CUSTOprod']
          #(INP+OUT+OUT2+[mypool.score]) esse vai ser o do csv
          if not img_on:
           writer = csv.writer(open(filename,'a',newline=''))
           writer.writerow(INP+OUT+OUT2+[CUSTO, diffCUSTO, CUSTOprod, diffCUSTOprod,collision.real,collision.imag])
         if mypool.score==0: mypool.nextturn()
         mypool.score=0
        for ball2 in mypool.balls: ball2.v=0
        collision=0
        if mypool.players[mypool.turn].computer==1: # início do turno do computador 
          if img_on: pygame.time.wait(1000)
          esti = (mypool.balls[1].pos-mypool.balls[0].pos)/abs(mypool.balls[1].pos-mypool.balls[0].pos)
          rand = -1+2*np.random.random()-1j+2*np.random.random()*1j
          rand /= 20
          forca = (esti+rand)/abs(esti+rand)
          mypool.balls[0].v = maxspeed*forca
          if replay_on: inicializar(line0)
          inputplay = {
              'posição das bolas': [ballx.pos if ballx.color!=(255,255,255) else ballx.pos for ballx in mypool.balls],
              'forca': forca,
              'velocidade': maxspeed,
              'CUSTOprod': np.e**(np.sum([np.log(dclosest(ballx.pos)) if (ballx.color!=(255,255,255) and ballx.void==0) else 0 for ballx in mypool.balls])),
              'CUSTO': np.sum([dclosest(ballx.pos) if (ballx.color!=(255,255,255) and ballx.void==0) else 0 for ballx in mypool.balls])/max(np.sum([1 if (ballx.color!=(255,255,255) and ballx.void==0) else 0 for ballx in mypool.balls]),1)
          }
          inplay = 1
    if mypool.players[0].score+mypool.players[1].score==len(mypool.balls)-1:
      mypool.players[0].score=0
      mypool.players[1].score=0
      mypool.balls[0].pos = .5+.375j
      #criar nova mesa
      x = .8+.375j #posição inicial do triângulo
      post=[x]
      for i in range(len(post)):
       mypool.balls[i+1].pos = post[i]
       mypool.balls[i+1].void = 0
      if replay_on: inicializar(line0)
