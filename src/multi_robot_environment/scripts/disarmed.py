from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import threading

iha2 = connect("127.0.0.1:14560", wait_ready=True)
iha1 = connect("127.0.0.1:14550", wait_ready=True)
iha3 = connect("127.0.0.1:14570", wait_ready=True)


def land_and_disarm(iha):
    # İHA iniş moduna geçiriliyor
    print(f"{iha} iniş moduna geçiriliyor.")
    iha.mode = VehicleMode("LAND")
    
    # İHA'nın yere inmesini bekliyoruz
    while iha.location.global_relative_frame.alt > 0.1:
        print(f"{iha} iniyor. Mevcut irtifa: {iha.location.global_relative_frame.alt:.1f} metre")
        time.sleep(1)
    
    print(f"{iha} yere indi.")
    
    # İHA'nın disarm edilmesi
    iha.armed = False
    
    while iha.armed is True:
        print(f"{iha} disarm ediliyor...")
        time.sleep(0.5)
    
    print(f"{iha} disarm edildi.")

# Thread'leri oluştur
land_threads = []

for iha in [iha1, iha2, iha3]:#
    land_thread = threading.Thread(target=land_and_disarm, args=(iha,))
    land_threads.append(land_thread)

# İniş thread'lerini başlat
for thread in land_threads:
    thread.start()

# İniş thread'lerinin bitmesini bekle
for thread in land_threads:
    thread.join()

print("Bütün işlemler tamamlandı.")
