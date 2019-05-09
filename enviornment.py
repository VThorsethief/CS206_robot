import constants as c
class ENVIORNMENT:
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
        if id == 0:
            self.Place_Light_Source_To_The_Front()
        elif id ==1:
            self.Place_Light_Source_To_The_Right()
        elif id == 2:
            self.Place_Light_Source_To_The_Back()
        elif id == 3:
            self.Place_Light_Source_To_The_Left()
        # print("Size:[", self.l, self.w, self.h, "] Pos:[", self.x, self.y, self.z, "]")
        
    def Place_Light_Source_To_The_Front(self):
        self.y = self.legSize * c.lightSourceDistance
        self.lx = self.l * 1000
    
    def Place_Light_Source_To_The_Right(self):
        self.x = self.legSize * c.lightSourceDistance
        self.ly = self.l * 1000

    def Place_Light_Source_To_The_Back(self):
        self.y = self.legSize * -c.lightSourceDistance
        self.lx = self.l * 1000

    
    def Place_Light_Source_To_The_Left(self):
        self.x = self.legSize * -c.lightSourceDistance
        self.ly = self.l * 1000

    def Send_To(self, sim):
        #Need to  change the arguments for the experimental pyrosim
        
        # lightSource = sim.send_box(position =[self.x * 5, self.y * 5, self.large_box_size], sides = [self.l,self.l,self.l], collision_group = "light", color = [1,0,0])
        # light_stand = sim.send_box(position =[self.x * 2, self.y * 2, self.l], sides = [.1,.1,self.l * 2], collision_group = "env")
        # sim.add_light_to_body(body_id = lightSource, intensity = 0.25)
        lightSource = sim.send_box(position = [self.x, self.y, self.large_box_size * 0.25], sides = [self.lx,self.ly,self.large_box_size/2], color = [0, 0, 1], collision_group = "env")
        return lightSource
        # sim.send_box(position = [self.x, self.y, self.large_box_size/2], \
        #     sides = [self.large_box_size, self.large_box_size, self.large_box_size* .0001],color = [1,0,0], collision_group = "env")

