'''
Referencia sobre o canvas:
http://effbot.org/tkinterbook/canvas.htm
'''

from __future__ import unicode_literals

try:
    # python 2.6
    import Tkinter as tk
    def bytecar(cod):
        return chr(cod)
except ImportError:
    # python 3
    import tkinter as tk
    def bytecar(cod):
        return bytes([cod])

import sys
import math

CEL = 40
LATERAL = CEL * 6
DIST_APROX = 2 # distancia considerada suficientemente proxima para ser igual

ESTILO_ROTULO = dict(anchor='center', font='courier 24', fill='gray')
ESTILO_CAR = dict(anchor='center', font='times 32', fill='black')
ESTILO_LEGENDA = dict(anchor='w', font='helvetica 32', fill='black')

CODEPAGES = ['ASCII',
    'cp437', 'cp850', 'MacRoman', 'ISO-8859-1',
    'ISO-8859-15', 'Windows-1252', 'ISO-8859-2',  'ISO-8859-7',
    'ISO-8859-8', 'ISO-8859-5', 'Windows-1251', 'KOI8-R', 'cp437', ]

COLORS = ['blue', '#700', '#070', 'orange']

INTERVALO = 40
FATOR_ACEL = .2

class Glifo(object):
    ativos = {}
    movendo = {}

    def __init__(self, canvas, unicar, x, y, color='black'):
        self.canvas = canvas
        self.unicar = unicar
        self.x = x
        self.y = y
        self.vx = self.vy = self.ax = self.ay = 0
        self.x_dest = self.y_dest = None
        Glifo.ativos[self.unicar] = self
        ESTILO_CAR['fill'] = color
        self.handle = self.canvas.create_text(x, y,
                        text=unicar, **ESTILO_CAR)

    def partir(self, x_dest, y_dest):
        Glifo.movendo[self.unicar] = self
        self.x_dest = x_dest
        self.y_dest = y_dest
        self.direcao = math.atan2(self.y_dest-self.y, self.x_dest-self.x)
        self.vx = math.cos(self.direcao)
        self.vy = math.sin(self.direcao)
        self.ax = self.vx*FATOR_ACEL
        self.ay = self.vy*FATOR_ACEL
        self.distancia = math.hypot(self.x-self.x_dest, self.y-self.y_dest)

    def mover(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay
        distancia = math.hypot(self.x-self.x_dest, self.y-self.y_dest)
        if distancia <= DIST_APROX or distancia > self.distancia: # chegamos ou passamos
            self.parar()
        else:
            self.distancia = distancia
        self.canvas.coords(self.handle, (self.x, self.y))
        #print self.unicar, self.x, self.y, self.vx, self.vy, self.direcao

    def parar(self):
        self.x = self.x_dest
        self.y = self.y_dest
        self.vx = self.vy = self.ax = self.ay = 0
        del Glifo.movendo[self.unicar]
        if hasattr(self, 'saindo') and self.saindo:
            del Glifo.ativos[self.unicar]
            self.canvas.delete(self.handle)

    def sair(self):
        # y = 13*CEL # saindo todos pelo mesmo y
        y = self.canvas.coords(self.handle)[1]  # mantendo o y
        self.partir(24*CEL, y)
        self.saindo = True

class Janela(tk.Tk):
    def __init__(self, raiz):
        tk.Tk.__init__(self, raiz)
        self.canvas = tk.Canvas(raiz, width=CEL*17+LATERAL, height=CEL*17)
        self.cels = [[0]*16 for i in range(16)]
        self.id_pg = 0 # ASCII
        self.canvas.pack()
        self.desenhar_base()
        self.canvas.bind('<Double-Button-1>', lambda e: sys.exit())
        self.bind_all('<Left>', lambda e: self.desenhar_tabela(-1))
        self.bind_all('<Right>', lambda e: self.desenhar_tabela(1))
        self.geometry('+1800+300')

    def mudar_legenda(self, texto):
        if hasattr(self, 'legenda'):
            self.canvas.delete(self.legenda)
        ESTILO_LEGENDA['fill'] = self.cor()
        self.legenda = self.canvas.create_text(17.5*CEL, 1.5*CEL, text=texto, **ESTILO_LEGENDA)

    def cor(self):
        if self.id_pg == 0: # ASCII
            return 'black'
        return COLORS[(self.id_pg-1)%len(COLORS)]

    def desenhar_tabela(self, muda_cod):
        self.id_pg_anterior = self.id_pg
        self.id_pg += muda_cod
        if self.id_pg < 0:
            self.id_pg = len(CODEPAGES)-1
        elif self.id_pg == len(CODEPAGES):
            self.id_pg = 0
        encoding = CODEPAGES[self.id_pg]
        self.mudar_legenda(encoding)
        unicars_sobrando = set(Glifo.ativos)
        if self.id_pg > 0: # alem do ASCII
            for i in range(8, 16):
                for j in range(16):
                    unicar = bytecar(i*16+j).decode(encoding, 'ignore')
                    if not unicar:
                        continue
                    if i == 8 and j == 5 and unicar == '\x85':
                        continue # ignorar gremlim na forma de &Aacute; dentro de um quadrado
                    glifo = Glifo.ativos.get(unicar)
                    if glifo is None:
                        glifo = Glifo(self.canvas, unicar, 17.5*CEL, 1.5*CEL, color=self.cor())
                    else:
                        unicars_sobrando.remove(unicar)
                    glifo.partir((j+1.5)*CEL, (i+1.5)*CEL)
        for unicar in unicars_sobrando:
            glifo = Glifo.ativos.get(unicar)
            glifo.sair()
        self.atualizar()

    def atualizar(self):
        # print Glifo.movendo.keys()
        if Glifo.movendo:
            for unicar, glifo in list(Glifo.movendo.items()):
                glifo.mover()
            self.after(INTERVALO, self.atualizar)
        else:
            # limpar rastros
            remendo = self.canvas.create_rectangle(CEL*17.1, 0, CEL*17+LATERAL, CEL*17, fill="white", outline='white')
            self.canvas.tag_lower(remendo)
            self.mudar_legenda(CODEPAGES[self.id_pg])

    def desenhar_base(self):
        c = self.canvas
        self.mudar_legenda('ASCII')
        ESTILO_CAR['fill'] = 'black'

        for i in range(17):
            # linhas
            c.create_line(CEL, (i+1)*CEL, 17*CEL, (i+1)*CEL)
            c.create_line((i+1)*CEL, CEL, (i+1)*CEL, 17*CEL)
            if i < 16:
                # rotulo
                c.create_text((i+1.6)*CEL, CEL/2, text='_%X'%i, **ESTILO_ROTULO)
                c.create_text(CEL/2, (i+1.5)*CEL, text='%X0'%i, **ESTILO_ROTULO)
                for j in range(16):
                    # tabela ASCII
                    code = i*16 + j
                    if 32 <= code < 128:
                        self.cels[i][j] = c.create_text((j+1.5)*CEL, (i+1.5)*CEL, text=chr(code), **ESTILO_CAR)
                    elif code == 128:
                        break




janela = Janela(None)
janela.mainloop()
