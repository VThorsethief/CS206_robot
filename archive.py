# Class for saving the genome as well as the cppn. This is to 
# remain as simple as possible to avoid any weird things with pickling later
class Archive:
    def __init__(self, genome, cppn):
        self.genome = genome
        self.cppn = cppn