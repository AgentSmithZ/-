class Soda:
    def __init__(self):
        self.type = 0
        self.dict_type = {
            1:'ВИШНЁВАЯ',
            2:'ЛИМОННАЯ',
            3:'КОКИ КОЛА'}
        
    def addType(self, number):
        self.type=number
          
    def show_my_drink(self):
        return self.dict_type.pop(self.type)
        

soda=Soda()
soda.addType(2)
print(soda.show_my_drink())
        
