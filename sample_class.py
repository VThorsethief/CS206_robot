class SampleClass:
    def __init__(self, ID, value):
        self.ID = ID
        self.value = value

    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value
    
    def __str__(self):
        return str(self.ID) +', ' + str(self.value) + "|"

    def __repr__(self):
        return self.__str__()