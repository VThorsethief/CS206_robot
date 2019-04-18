import constants as c
from enviornment import ENVIORNMENT
import pyrosim as sim
class ENVIORNMENTS:
    def __init__(self):
        self.envs = {}
        for e in range(0, c.numEnvs):
            self.envs[e] = ENVIORNMENT(e, c.spiderRadius)


            
