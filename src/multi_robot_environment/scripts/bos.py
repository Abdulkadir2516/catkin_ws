import random
sayac = 0

bush_names =["bush_0","bush_1","bush_2","bush_3","bush_4","bush_5","bush_6"] 

for i in range(50,150,10):
    for j in range(50, 150,10):

        bush_type = random.randint(1, 6)

        if bush_type in [7,6]:
            continue
        
        print(f'    <model name="bush_{sayac}">')
        print(f'      <pose>{i} {j} 0 0 0 0</pose>')
        print(f'      <include>')
        print(f'        <uri>model://bush_{bush_type}</uri>')
        print(f'      </include>')
        print(f'    </model>')

        print("\n")
        sayac +=1


for i in range(50,150,10):
    for j in range(50, 150,10):
        print(f"({i},{j},5)")




