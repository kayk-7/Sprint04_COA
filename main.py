import time
time.sleep(0.1) # Wait for USB to become ready

from machine import Pin

energia_restante = 0
estados = ["Recarga autorizada", "Recarga reduzida", "Recarga bloqueada"]

vd = Pin(0, Pin.OUT) 
am = Pin(1, Pin.OUT) 
vm = Pin(2, Pin.OUT) 

l1 = Pin(27, Pin.OUT)
l2 = Pin(26, Pin.OUT)
l3 = Pin(22, Pin.OUT)

def on_off_charger(c, e):

    if c.value() == 1:
        c.value(0)
        x = 2000
    else:
        c.value(1)
        x = -2000

    if e + x <= 0:
        am.value(0)
        vd.value(0)
        vm.value(1)
    elif e + x < 2000:
        am.value(1)
        vd.value(0)
        vm.value(0)
    else:
        am.value(0)
        vd.value(1)
        vm.value(0)
    
    return x

while True:
    print("""Escolha uma opereção:
[ 1 ] On/off carregador 1
[ 2 ] On/off carregador 2
[ 3 ] On/off carregador 3
[ 4 ] Definir geração de energia
[ 5 ] Visualizar status""")
    op = input()
    if op == "1":
        energia_restante += on_off_charger(l1, energia_restante)
    elif op == "2":
        energia_restante += on_off_charger(l2, energia_restante)
    elif op == "3":
        energia_restante += on_off_charger(l3, energia_restante)
    elif op == "4":
        l3.value(0)
        l2.value(0)
        l1.value(0)
        print("Carregadores desligados")
        energia_restante = int(input("Geração em W: "))
        if energia_restante <= 0:
            am.value(0)
            vd.value(0)
            vm.value(1)
        elif energia_restante < 2000:
            am.value(1)
            vd.value(0)
            vm.value(0)
        else:
            am.value(0)
            vd.value(1)
            vm.value(0)
    elif op == "5":
        consumo = l1.value()*2000 + l2.value()*2000 + l3.value()*2000
        geracao = energia_restante + consumo
        if vd.value() == 1:
            i = 0
        elif am.value() == 1:
            i = 1
        elif vm.value() == 1:
            i = 2
        
        status = estados[i]
        print("== STATUS DO SISTEMA ==")
        print(f"Geração de energia: {geracao}W")
        print(f"Consumo de energia: {consumo}W")
        print(f"Energia diponíveel: {energia_restante}W")  
        print(f"Estado do sistema:  {status}") 
        print()           