import constants as c
from enviornment import ENVIORNMENT
from jump_platform import PLATFORM
import pyrosim as sim

class PLATFORMS():
    def __init__(self):
        self.envs = {}
        for e in range(0, c.numEnvs):
            self.envs[e] = PLATFORM(e, c.spiderRadius)


            
