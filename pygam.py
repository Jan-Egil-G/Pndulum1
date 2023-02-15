import z_CommonFunc as zcf
from torch.multiprocessing import Process, Queue
import pygame
import math
import time
def RunPG(dummy,input_queue):
    # Initialize pygame
    pygame.init()

    # Set the width and height of the screen (width, height).
    size = (700, 500)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("pole Game")


    x_pos = 350
    time.sleep(0.001)
    # Starting angle of the pole
    angle = 0
    angle_ytre = 180


    # Length of the pole
    pole_length = 100
    pole_length_ytre = 50

    # Pivot point
    pivot_x = 350
    pivot_y = 250

    dataIn=[-1,0,0,0,0,0]
    # -------- Main Program Loop -----------
    done = False

    while not done:
        # x=x+5
        # if x>359:
        #     x=0
        # dataIn[1]=x    
        if(not (input_queue.empty())):
            dataIn=input_queue.get()   


        # # --- Main event loop
        cmd=dataIn[0]
        if cmd==1:
            done = True
            break
        # Loop until the user clicks the close button.
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # # User pressed a key
            elif event.type == pygame.KEYDOWN:
            #     # Figure out if it was an arrow key. If so
            #     # adjust speed.
                if event.key == pygame.K_LEFT:
                    done=True
  

        # Used to manage how fast the screen updates.
        clock = pygame.time.Clock()


        dataIn2=dataIn[1:]#zcf.NormToEngPosValues

        # --- Game logic should go here
        # Update the angle of the pole
        angle = 90-dataIn2[1]
        angle_ytre = 90-dataIn2[0]
        x_pos = dataIn2[2] 
        pivot_x=x_pos*50+325

        # Calculate the end point of the pole
        end_x = pivot_x + pole_length * math.sin(math.radians(angle))
        end_y = pivot_y - pole_length * math.cos(math.radians(angle))

        end_x_ytre = end_x + pole_length_ytre * math.sin(math.radians(angle_ytre))
        end_y_ytre = end_y - pole_length_ytre * math.cos(math.radians(angle_ytre))

        # --- Drawing code should go here
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))


        pygame.draw.rect(screen, (255, 144, 144), (x_pos*50+300, 250, 50, 50))
        pygame.draw.rect(screen, (255, 255, 0), (30, 350, 30, 30))
        pygame.draw.rect(screen, (255, 255, 0), (650, 350, 30, 30))
        
        # Draw the pole
        pygame.draw.line(screen, (255, 0, 0), (pivot_x, pivot_y), (end_x, end_y), 5)
        pygame.draw.line(screen, (0, 0, 255), (end_x, end_y), (end_x_ytre, end_y_ytre), 5)

        # Draw the pivot point
        pygame.draw.circle(screen, (0, 0, 0), (pivot_x, pivot_y), 10)
        pygame.draw.circle(screen, (0, 0, 0), (end_x, end_y), 7)

        # --- Go ahead and update the screen.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

        # Close the window and quit.
    pygame.quit()

#-------------------------egen process over-------------------------

class PygameProcess:
    def __init__(self):
        self.qIn = Queue()
        self.qOut = Queue()
        self.p1 = None
        
    def Start(self):
        self.Extprocess()
        return

    def Extprocess(self):
        self.p1 = Process(target=RunPG, args=(1,self.qIn))
        print("starting pygame process -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
        self.p1.start()
    
    def DoIteration(self, dataIn):#V1 dgr, V2, pos -1..1
        #print(dataIn, "dataIn")
        #RunPG(1,dataIn)
        if((self.qIn.qsize())<5):
            self.qIn.put(dataIn)
        return 


if __name__ == '__main__':
    #RunPG(1,1)
    pgpcs=PygameProcess()
    # x=0
    pgpcs.Start()
    x=0
    y=0
    y_up=True
    while True:
        x=x+5
        if x>359:
            x=0

        if y_up:
            y=y+5
            if y>100:
                y_up=False
        else:
            y=y-5
            if y<-100:
                y_up=True
        #dataIn[1]=x    

        #RunPG(1,[-1,0,0,0,0,0]) #cmd, ytre , indre, pos
        pgpcs.DoIteration([-1,x,30,y/100.0])
        time.sleep(0.1)


