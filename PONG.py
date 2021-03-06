from tkinter import *
from random import *
import schedule
import time
   

def Parameters_bouton():
    color = ["red","green","blue","white","yellow","purple"]
    color_al = choice(color)
    print (color_al)
    return color_al
def Parameters_fill():
    color = ["red","green","blue","white","yellow","purple"]
    color_al = choice(color)
    return color_al


class Window(Tk):
    def __init__(self, width=600, height=400):
        Tk.__init__(self)
        self.flag = 0

        self.quit = Button(self,text="Quit Game",command=self.destroy)
        self.quit.grid(column=4,row=0,sticky="NE")

        self.new = Button(self,text="New Game",command=self.new_game)
        self.new.grid(column=0,row=0,sticky="NW")

        self.can = Canvas(self,width=width,height=height,bg="black")
        self.can.grid(column=0,row=1,sticky="SW",columnspan=5)

        self.new = Button(self,text="Couleurs joueur1",command=Parameters_bouton)
        self.new.grid(column=1,row=4,sticky="NW")

        self.new = Button(self,text="Couleurs joueur2",command=Parameters_bouton)
        self.new.grid(column=3,row=4,sticky="NE")

        self.new = Button(self,text="Balle",command=Parameters_bouton)
        self.new.grid(column=2,row=4)

        self.can.create_line(width/2,0, width/2, height, fill="white",dash=(2,2), width=10)

        self.can.create_line(4,0,4,height+5, fill="blue", width=4)
        self.can.create_line(width,0,width,height+5, fill="red", width=4)
        
        
        
    
    def new_game(self):
        if self.flag == 0 :
            self.flag = 1
            self.pads = Pad(self.can,self.flag)
            self.ball = Ball(self.can,self.pads,self.flag)
            self.bonus = Bonus(self.can,self.flag)
            self.bonus.summon(self.can)
            

class Pad:
    def __init__(self,canvas,flag):
        self.canvas = canvas
        self.flag = flag
        self.height = canvas.winfo_height()
        self.width = canvas.winfo_width()
        self.x1,self.y1 = 10,self.height/2-30
        self.x2,self.y2 = self.width-25,self.height/2-30
                
        
        self.Pad2 = canvas.create_rectangle(self.x2,self.y2,self.x2+15,self.y2+60,fill=Parameters_fill()) 
        self.Pad1 = canvas.create_rectangle(self.x1,self.y1,self.x1+15,self.y1+60,fill=Parameters_fill())
        
        canvas.bind_all("<Up>",self.move_up2)
        canvas.bind_all("<Down>", self.move_down2)
        canvas.bind_all("<z>",self.move_up1)
        canvas.bind_all("<s>", self.move_down1)

        
        self.dy2 = 25

    def move_up1(self,event):
        if self.y1>5 :
            self.y1=self.y1-10
            self.canvas.coords(self.Pad1,self.x1,self.y1,self.x1+15,self.y1+60)
            
    def move_down1(self,event):
        if self.y1+60<(self.height-5):
            self.y1=self.y1+10
            self.canvas.coords(self.Pad1,self.x1,self.y1,self.x1+15,self.y1+60)

    def move_up2(self,event):
        if self.y2>5 :
            self.y2=self.y2-10
            self.canvas.coords(self.Pad2,self.x2,self.y2,self.x2+15,self.y2+60)
            
    def move_down2(self,event):
        if self.y2+60<(self.height-5):
            self.y2=self.y2+10
            self.canvas.coords(self.Pad2,self.x2,self.y2,self.x2+15,self.y2+60)

class Ball:
    def __init__(self,canvas,pad,flag):
        self.canvas = canvas
        self.pad = pad
        self.height = canvas.winfo_height()
        self.width = canvas.winfo_width()
        self.flag = flag
        self.x1,self.y1 = self.width/2.1,self.height/2
        self.dx,self.dy = 30,30
        self.Ball = canvas.create_oval(self.x1, self.y1, self.x1+20, self.y1+20, width=2, fill=Parameters_fill())
        self.pointA, self.pointB = 0,0
        
        self.ready()
    
    def ready(self):
        self.starter=0
        self.score= Label(app,text="%d : %d" % (self.pointA,self.pointB), bg="black",fg="white")
        self.score.grid(column =2,row=1,sticky="S")
        self.x1,self.y1 = self.height/2,self.width/2
        app.titre = Label(app,text="PRESS ANY KEY TO START", bg="black",fg="white")
        app.titre.grid(column =2,row=2,sticky="S")
        self.canvas.bind_all("<Key>",self.start)
       

    def start(self,event):
        self.starter=1
        self.move()  
        
    def move(self):
        if self.starter==1:
            self.x1, self.y1 = self.x1 +self.dx, self.y1 + self.dy
                 
            if self.y1 >self.height-30:
                self.dx, self.dy = self.dx, -20

            if self.y1 <2:
                self.dx, self.dy = self.dx, 20
       
            if self.x1 < self.pad.x1+20:
                if self.pad.y1 < self.y1 < self.pad.y1+60:
                    self.dx, self.dy = 20, self.dy

            if self.x1+30 >  self.pad.x2-1:
                if self.pad.y2<self.y1+10<self.pad.y2+60:
                     self.dx, self.dy = -20, self.dy

            if self.x1 < 0:
                self.starter = 0
                self.pointB = self.pointB+1
                self.ready()
            
        
            if self.x1+20 > self.width:
                self.starter=0
                self.pointA = self.pointA+1
                self.ready()

            self.canvas.coords(self.Ball,self.x1,self.y1,self.x1+20,self.y1+20)
            if self.flag > 0:
                self.canvas.after(70,self.move)

class Bonus:
    def __init__(self,canvas,flag):
        self.height = canvas.winfo_height()
        self.width = canvas.winfo_width()
        self.canvas = canvas
        self.px,self.py = self.width/2.05,self.height/1.95
        self.flag = flag 
    
    def summon(self,canvas):
        self.n = randrange(1,3)
        if self.n == 1:
            self.Bonus_ballg = canvas.create_oval(self.px, self.py, self.px+10, self.py+10, width=2,outline="green", fill="black")
        elif self.n == 2:
            self.Bonus_ballr = canvas.create_oval(self.px, self.py, self.px+10, self.py+10, width=2,outline="red", fill="black")
        elif self.n == 3:
            self.Bonus_bally = canvas.create_oval(self.px, self.py, self.px+10, self.py+10, width=2,outline="yellow", fill="black")

        self.summon_effect()
        
    def bonus(self,Ball,Pad):

        if self.Ball.x1 < self.Pad.x1+20:
            if self.Pad.y1 < self.Ball.y1 < self.Pad.y1+60:
                if self.px and self.py == self.Ball.dx and self.Ball.dy:
                    self.Pad.pad1 = canvas.create_rectangle(self.x1,self.y1,self.x1+15,self.y1+80,fill=Parameters_fill())
                    self.canvas.after(30,self.summon.destroy())
                else:
                    pass

        if self.Ball.x1+30 >  self.Pad.x2-1:
            if self.Pad.y2 < self.Ball.y1+10 < self.Pad.y2+60:
                if self.px and self.py == self.Ball.dx and self.Ball.dy:
                    self.Pad.pad2 = canvas.create_rectangle(self.x2,self.y2,self.x2+15,self.y2+80,fill=Parameters_fill())
                    self.canvas.after(70,self.summon.destroy())
                else:
                    pass
    
    def malus(self,Ball,Pad):
        if self.Ball.x1+30 >  self.Pad.x2-1:
            if self.Pad.y2 < self.Ball.y1+10 < self.Pad.y2+60:
                if self.px and self.py == self.Ball.dx and self.Ball.dy:
                    self.Pad.pad2 = canvas.create_rectangle(self.x2,self.y2,self.x2+15,self.y2+30,fill=Parameters_fill())
                    self.canvas.after(30,self.summon.destroy())
                else:
                    pass

        if self.Ball.x1 < self.Pad.x1+20:
            if self.Pad.y1 < self.Ball.y1 < self.Pad.y1+60:
                if self.px and self.py == self.Ball.dx and self.Ball.dy:
                    self.Pad.pad1 = canvas.create_rectangle(self.x1,self.y1,self.x1+15,self.y1+30,fill=Parameters_fill())
                    self.canvas.after(30,self.summon.destroy())
                else:
                    pass
    
    def malus_share(self,Ball,Pad):
        if self.px and self.py == self.Ball.dx and self.Ball.dy:
            self.Pad.pad1 = canvas.create_rectangle(self.x1,self.y1,self.x1+15,self.y1+80,fill=Parameters_fill())
            self.Pad.pad2 = canvas.create_rectangle(self.x2,self.y2,self.x2+15,self.y2+80,fill=Parameters_fill())
            self.canvas.after(30,self.summon.destroy())

        elif self.px and self.py == self.Ball.dx and self.Ball.dy:
            self.Pad.pad2 = canvas.create_rectangle(self.x2,self.y2,self.x2+15,self.y2+80,fill=Parameters_fill())
            self.Pad.pad1 = canvas.create_rectangle(self.x1,self.y1,self.x1+15,self.y1+80,fill=Parameters_fill())
            self.canvas.after(30,self.summon.destroy())

        else:
            pass


    def summon_effect(self):
        if self.n == 1:
            self.bonus()
        elif self.n == 2:
            self.malus()
        elif self.n ==3:
            self.malus_share()
    
        if self.flag > 0:
            self.canvas.after(30,self.summon)
        

if __name__ == "__main__":
    app = Window()
    app.mainloop()