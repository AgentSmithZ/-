class TCar:
    def __init__(self, road0, p0, v0):
        self.road=road0
        self.p=p0
        self.v=v0
        self.x=0
    def move(self):
        self.x+=self.v
        if self.x>self.road.length:
            self.x=0 
            
class TRoad:
    def __init__(self):
        self.length = 0
        self.width= 0
        
    def setRoadSize(self, length0, width0):
        self.length = length0 if length0>0 else 0
        self.width= width0 if width0>0 else 0
        
    def getRoadSize(self):
        return self.length, self.width
        

N=3
cars=[]
road=TRoad()
road.setRoadSize(160, 200)
for i in range(N):
    cars.append(TCar(road, i+1, 2*(i+1)))
for k in range(100):
    for i in range(N):
        cars[i].move()
print("после 100")
for i in range(N):
    print(cars[i].x)  
    
print(road.getRoadSize())
    
