import constants as c
from table import Table
class PLATFORM:
    def __init__(self, id, legSize):
        self.ID = id
        self.legSize = legSize
        self.l = legSize
        self.w = legSize
        self.h = legSize
        self.x = 0
        self.y = 0
        self.ly = self.l
        self.lx = self.l
        self.large_box_size = c.spiderRadius * 20
        self.z = self.large_box_size
        self.x_disp = 0
        self.y_disp = 0
        if id == 0:
            self.Platform_To_The_Front()
        elif id ==1:
            self.Platform_To_The_Right()
        elif id == 2:
            self.Platform_To_The_Back()
        elif id == 3:
            self.Platform_To_The_Left()
        # print("Size:[", self.l, self.w, self.h, "] Pos:[", self.x, self.y, self.z, "]")
        
    def Platform_To_The_Front(self):
        self.y = self.legSize * c.lightSourceDistance
        self.lx = self.l * 7.5
        self.x_disp = 0
        self.y_disp = self.l * 10
    
    def Platform_To_The_Right(self):
        self.x = self.legSize * c.lightSourceDistance
        self.ly = self.l * 7.5
        self.y_disp = 0
        self.x_disp = self.l * 10

    def Platform_To_The_Back(self):
        self.y = self.legSize * -c.lightSourceDistance
        self.lx = self.l * 7.5
        self.x_disp = 0
        self.y_disp = -self.l * 10

    
    def Platform_To_The_Left(self):
        self.x = self.legSize * -c.lightSourceDistance
        self.ly = self.l * 7.5
        self.y_disp = 0
        self.x_disp = -self.l * 10

    def Send_To(self, sim):
        #Need to  change the arguments for the experimental pyrosim

        # platform_1 = sim.send_box(position = [0, 0, 1], sides = [self.l * 20, self.l * 20, .1],\
        #     collision_group = "env", color = [0, 1, 0])

        # platform_2 = sim.send_box(position = [self.x, self.y, 1], sides = [self.l * 20, self.l * 20, .1],\
        #     collision_group = "env", color = [0, 1, 0])

        table1 = Table(sim, [0,0,1], self.l * 20, c.vertical_displacement)

        table2 = Table(sim, [self.x, self.y, 1], self.l * 20, c.vertical_displacement)

        # jumpBeacon = sim.send_box(position =[self.x, self.y + self.l * 10, c.vertical_displacement + self.l * 10 + 0.5], sides = [self.l * 7.5,self.l,self.l* 10], collision_group = "light", color = [0,0,1])
        
        
        jumpBeacon = sim.send_box(position =[self.x + self.x_disp, self.y + self.y_disp, c.vertical_displacement + self.l * 10 + 0.5], sides = [self.lx,self.ly,self.l* 10], collision_group = "light", color = [0,0,1])
        # jumpBeacon = sim.send_box(position =[self.x + self.x_disp, self.y , c.vertical_displacement + self.l * 10 + 0.5], sides = [self.lx,self.ly,self.l* 10], collision_group = "light", color = [0,0,1])
        
        
        # sim.send_box(position = [self.x, self.y, self.large_box_size * 0.25], sides = [self.lx,self.ly,self.large_box_size/2], color = [0, 0, 1], collision_group = "env")
        return jumpBeacon
        # sim.send_box(position = [self.x, self.y, self.large_box_size/2], \
        #     sides = [self.large_box_size, self.large_box_size, self.large_box_size* .0001],color = [1,0,0], collision_group = "env")

