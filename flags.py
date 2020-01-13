
class ProcessFlags():
    def __init__(self):
        self.predict = False

    def getPredictFlag(self):
        return self.predict
        
    def setPredictFlag(self,state):
        self.predict=state