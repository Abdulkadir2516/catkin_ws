
from math import radians

for i in range(361):    
    print(radians(i), end="\t")

"""
import random
sayac = 0
for i in range(3,41,5):
    for j in range(3, 31,5):

        bush_type = random.randint(0, 6)

        if bush_type == 1:
            bush_type = 0
        if bush_type == 2:
            bush_type = 5
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