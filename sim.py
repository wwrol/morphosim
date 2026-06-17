import numpy as np
from enum import Enum
import math

class Ptype(Enum):
    A=0
    B=1
    C=2

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

class ParticleGroup:
    def __init__(self,type,D,decay):
        self.xs = np.empty(shape=[0,2])
        self.vs = np.empty(shape=self.xs.shape)
        self.kv = math.sqrt(D)/2*1000
        self.kd = decay
        self.type = type
        self.sources = []

    def update_pos(self,dt):
        self.randomize_vel()
        if self.xs.size>0:
            self.xs = self.xs+self.vs*dt

    def add_source(self,x,rate,max_particles=1000):
        self.sources.append(ParticleSource(x,rate,max_particles))
    
    def update_sources(self,dt):
        for source in self.sources:
            self.xs = source.spawn(self.xs,dt)

    def update_decay(self,dt):
        thresh = np.random.random(self.xs.shape[0]) < self.kd*dt
        points = np.array(thresh.nonzero())
        if points.size>0:
            self.remove_x(points)

        

    def randomize_vel(self):
        self.vs = np.interp(np.random.rand(*self.xs.shape),[0,1],[-1,1])*self.kv

    def step(self,dt):
        self.update_decay(dt)
        self.update_sources(dt)
        self.update_pos(dt)

    def get_xs(self):
        return self.xs.copy()
    
    def add_xs(self,xs):
        self.xs = np.vstack([self.xs,xs])

    
    def remove_x(self,idxs):
        self.xs = np.delete(self.xs,idxs,0)
    
    def get_num_particles(self):
        return self.xs.shape[0]
    
class MultiParticleSim:
    def __init__(self) -> None:
        self.groups:dict[str,ParticleGroup] = {}

    def add_group(self,name,type,D,decay):
        group = ParticleGroup(type,D,decay)
        self.groups[name]=group
        return group
    
    def get_groups(self):
        return self.groups

    def step(self,dt):
        for name in self.groups.keys():
            group = self.groups.get(name)
            if group:
                group.step(dt)

    def get_num_particles(self):
        count = 0
        for group in self.groups.values():
            count += group.get_num_particles()
        return count
    
    def get_dist_mat(self,name1,name2):
        group1 = self.groups.get(name1)
        group2 = self.groups.get(name2)
    
        if group1 and group2:
            x1 = group1.get_xs()
            x2 = group2.get_xs()
            x1 = x1.reshape(np.append(x1.shape,1))
            x2 = x2.reshape(np.append(x2.shape,1))


            mat1 = np.repeat(x1,x2.shape[0],2)
            mat2 = np.repeat(x2,x1.shape[0],2).swapaxes(0,2)
            mat = mat1-mat2
            if mat.size>0:
                mat = np.linalg.vector_norm(mat,axis=1)
                return mat.copy()
            else:
                return None
        
        else:
            return None
        
                
    def update_group_inter(self,name1,name2,output,threshold):
        dist = self.get_dist_mat(name1,name2)
        if dist is not None:
            thresh = dist<threshold
            points = np.array(thresh.nonzero())

            group1 = self.groups.get(name1)
            group2 = self.groups.get(name2)
            groupO = self.groups.get(output)

            if group1 and group2 and groupO and points.size>0:
                points1 = group1.get_xs()[points[0,:]].copy()
                points2 = group2.get_xs()[points[1,:]].copy()

                group1.remove_x(points[0,:])
                group2.remove_x(points[1,:])
                groupO.add_xs(points1)
                groupO.add_xs(points2)
