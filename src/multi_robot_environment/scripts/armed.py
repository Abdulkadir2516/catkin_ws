from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import threading

iha2 = connect("127.0.0.1:14560", wait_ready=True)
iha1 = connect("127.0.0.1:14550", wait_ready=True)
iha3 = connect("127.0.0.1:14570", wait_ready=True)

def takeoff(irtifa, iha):
    while iha.is_armable is not True:
        print(f"{iha} arm edilebilir durumda değil.")
        time.sleep(1)

    print(f"{iha} arm edilebilir.")

    iha.mode = VehicleMode("GUIDED")

    iha.armed = True

    while iha.armed is not True:
        print(f"{iha} arm ediliyor...")
        time.sleep(0.5)

    print(f"{iha} arm edildi.")

    iha.simple_takeoff(irtifa)
    
    while iha.location.global_relative_frame.alt < irtifa * 0.9:
        print(f"{iha} hedefe yükseliyor.")
        time.sleep(1)

# Thread'leri oluştur
takeoff_threads = []

for iha in [iha1, iha2, iha3]:#
    takeoff_thread = threading.Thread(target=takeoff, args=(10, iha))
    takeoff_threads.append(takeoff_thread)
    
# Kalkış thread'lerini başlat
for thread in takeoff_threads:
    thread.start()

# Kalkış thread'lerinin bitmesini bekle
for thread in takeoff_threads:  
    thread.join()
