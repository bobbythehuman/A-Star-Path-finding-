class createNode():
    def __init__(self,walkable,x,y,state):
        self.xPos=x
        self.yPos=y
        self.walkable=walkable
        self.state=state

        self.gCost=0
        self.hCost=0
        self.fCost=self.gCost+self.hCost
        self.parent=""
        self.button=""

    def update(self):
        self.fCost=self.gCost+self.hCost

    def reset(self):
        self.gCost=0
        self.hCost=0
        self.fCost=self.gCost+self.hCost
        self.parent=""
        self.state="-"