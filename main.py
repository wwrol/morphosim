import pygame
import numpy as np
import matplotlib.pyplot as plt


class Particle:
    
    def __init__(self,x = np.array([0.0,0.0])):
        self.x = x.copy()
        self.v = np.array([0.0,0.0])
        self.alive = True

    def set_random_vel(self):
        self.v = np.interp(np.random.random(self.v.size),[0,1],[-2/5,2/5])

    def decay(self,dt):
        if self.alive:
            self.alive = np.random.random(1)[0]>dt*0.0001
    def update_pos(self,dt:float):
        self.decay(dt)
        if self.alive:
            self.set_random_vel()
            self.x += self.v * dt

    def get_pos(self):
        return self.x.copy()
    
    def get_speed(self):
        return np.linalg.norm(self.v)

class ParticleSource:
    def __init__(self,x=np.array([0.0,0.0]),rate=1.0,max_particles = 1000) -> None:
        self.x = x
        self.rate = rate
        self.MAX_PARTICLES = max_particles
        self.t = 0

    def spawn(self,xs,dt):
        self.t+=dt
        while self.t*self.rate>1 and xs.shape[0]<self.MAX_PARTICLES:
            xs = np.vstack([xs,self.x])
            self.t-=1/self.rate
        return xs
    
class ParticleSystem:
    def __init__(self,x0) -> None:
        self.xs = np.empty(shape=[0,2])        
        self.vs = np.empty(shape=self.xs.shape)
        self.sources = []

    def update_pos(self,dt):
        self.random_vel()
        if self.xs.size>0:
            self.xs = self.xs+self.vs*dt

    def add_source(self,x,rate,max_particles=1000):
        self.sources.append(ParticleSource(x,rate,max_particles))
    
    def update_sources(self,dt):
        for source in self.sources:
            self.xs = source.spawn(self.xs,dt)

    def random_vel(self):
        self.vs = np.interp(np.random.rand(*self.xs.shape),[0,1],[-1,1])

    def step(self,dt):
        self.update_sources(dt)
        self.update_pos(dt)

    def get_xs(self):
        return self.xs.copy()
    
    def get_num_particles(self):
        return self.xs.shape[0]

class ParticleRenderer:
    def __init__(self,screen) -> None:
        pygame.init()
        self.screen = screen

    def render(self,ps:ParticleSystem):
        xs = ps.get_xs()
        for i in range(xs.shape[0]):
            pygame.draw.circle(self.screen,"white",xs[i],2)


def run_sim():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    game_font = pygame.font.SysFont("arial",30)

    running = True
    
    x0 = np.array([screen.get_width()/2,screen.get_height()/2])

    ps = ParticleSystem(x0)

    ps.add_source(x0,1)

    pr = ParticleRenderer(screen)

    

    while running:

        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #Physics
        dt = clock.tick()
        ps.step(dt)


        screen.fill("purple")



        pr.render(ps)

        txt_numpart = game_font.render(f'Number of Particles: {ps.get_num_particles()}', True, "white")
        #txt_renpart = game_font.render(f'Number of Rendered Particles: {rendered_particles}', True, "white")
        if dt>0:
            txt_frmrt = game_font.render(f'Framerate: {(1/(dt/1000)):.0f} FPS',True,"white")
        else:
            txt_frmrt = game_font.render(f'Framerate: NaN FPS',True,"white")

        screen.blit(txt_numpart,(25,50))
        #screen.blit(txt_renpart,(25,100))
        screen.blit(txt_frmrt, (25,150))
        pygame.display.update()
        pygame.display.flip()

    
    pygame.quit()
    print("Goodbye")


def main():
    print("Hello from morphosim!")
    run_sim()


if __name__ == "__main__":
    main()
