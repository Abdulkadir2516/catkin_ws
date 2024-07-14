import random
sayac = 0
for i in range(-150,-49,10):
    for j in range(-150, -49,10):

        bush_type = random.randint(1, 9)

        if bush_type in [5,6]:
            continue
        
        print(f'    <model name="tree_{sayac}">')
        print(f'      <pose>{i} {j} 0 0 0 0</pose>')
        print(f'      <include>')
        print(f'        <uri>model://tree_{bush_type}</uri>')
        print(f'      </include>')
        print(f'    </model>')

        print("\n")
        sayac +=1


for i in range(-150,-49,10):
    for j in range(-150, -49,10):
        print(-50,-150,5)




