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
            xs = np.append(xs,self.x)
            self.t-=1/self.rate
        return xs
    
class ParticleSystem:
    def __init__(self) -> None:
        self.xs = np.empty(shape=[0,2])
        self.vs = np.empty(shape=self.xs.shape)
        self.sources = []

    def update_pos(self,dt):
        self.random_vel()
        self.xs = self.xs+self.vs*dt

    def add_source(self,x,rate,max_particles=1000):
        self.sources.append(ParticleSource(x,rate,max_particles))
    
    def update_sources(self,dt):
        for source in self.sources:
            self.xs = source.spawn(self.xs,dt)

    def random_vel(self):
        self.vs = np.interp(np.random.rand(*self.vs.shape),[0,1],[-1,1])

    def step(self,dt):
        self.update_sources(dt)
        self.update_pos(dt)

    def get_xs(self):
        return self.xs.copy()
    
    def get_num_particles(self):
        return self.xs.shape[0]
