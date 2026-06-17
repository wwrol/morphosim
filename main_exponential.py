import pygame
import numpy as np
from sim import MultiParticleSim,Ptype

CMAP =  {Ptype.A:"red",Ptype.B:"blue",Ptype.C:"green"}

class ParticleRenderer:
    def __init__(self,screen) -> None:
        pygame.init()
        self.screen = screen

    def render(self,mps:MultiParticleSim):
        groups = mps.get_groups()
        for name in groups.keys():
            group = groups.get(name)
            if group:
                xs = group.get_xs()
                for i in range(xs.shape[0]):
                    pygame.draw.circle(self.screen,CMAP[group.type],xs[i],2)

        
        

def run_sim():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    game_font = pygame.font.SysFont("arial",20)

    running = True
    
    x0 = np.array([screen.get_width()/2,screen.get_height()/2])
    spacer = np.array([250,0])
    MAX_PART = 30000

    mps = MultiParticleSim()
    groupA = mps.add_group("a",Ptype.A,12.5,0.1)
    groupA.add_source(x0-spacer,400,MAX_PART)

    pr = ParticleRenderer(screen)
    
    while running:

        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #Physics
        dt = clock.tick()/1000 #s
        mps.step(dt)

        #Main Render
        screen.fill("black")
        pr.render(mps)

        #HUD
        txt_numpart = game_font.render(f'Number of Particles: {mps.get_num_particles()}', True, "white")

        if dt>0:
            txt_frmrt = game_font.render(f'Framerate: {(1/dt):.0f} FPS',True,"white")
        else:
            txt_frmrt = game_font.render(f'Framerate: NaN FPS',True,"white")
        screen.blit(txt_numpart,(25,50))
        screen.blit(txt_frmrt, (25,100))
        pygame.display.update()
        pygame.display.flip()


    
    pygame.quit()
    print("Goodbye")


def main():
    print("Hello from morphosim!")
    run_sim()


if __name__ == "__main__":
    main()
