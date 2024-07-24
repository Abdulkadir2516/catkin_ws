"""from cali_tarama_tekli import DroneNavigator
import time
nesne = DroneNavigator()

class miras(DroneNavigator):

    def __init__(self):
        super().__init__()
        print(self.tarama_durumu)

print(miras().get_tarama())

bush_names =["bush_0","bush_1","bush_2","bush_3","bush_4","bush_5","bush_6"] 
exit()"""

from cali_tespiti import ImageConverter

while True:
    print(ImageConverter().algilandi)


"""

import random
sayac = 0
for i in range(30,100,10):
    for j in range(30, 100,10):

        bush_type = random.randint(0, 6)

        if bush_type == 1:
            bush_type = 0
        if bush_type == 6:
            bush_type = 5
        
        print(f'    <model name="bush_{sayac}">')
        print(f'      <pose>{i} {j} 0 0 0 0</pose>')
        print(f'      <include>')
        print(f'        <uri>model://bush_{bush_type}</uri>')
        print(f'      </include>')
        print(f'    </model>')

        print("\n")
        sayac +=1

"""
"""for i in range(50,150,10):
    for j in range(50, 150,10):
        print(f"({i},{j},5)")"""




