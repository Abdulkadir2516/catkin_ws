from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import threading

iha2 = connect("127.0.0.1:14560", wait_ready=True)
iha1 = connect("127.0.0.1:14550", wait_ready=True)
iha3 = connect("127.0.0.1:14570", wait_ready=True)

# print(iha.is_armable)
# print(iha.armed)
# iha.mode = VehicleMode("GUIDED")
# iha.armed = True 
# iha.simple_takeoff(10)

def takeoff(irtifa, iha):
    while iha.is_armable is not True:
        print("İHA arm edilebilir durumda değil.")
        time.sleep(1)

    print("İHA arm edilebilir.")

    iha.mode = VehicleMode("GUIDED")

    iha.armed = True

    while iha.armed is not True:
        print("İHA arm ediliyor...")
        time.sleep(0.5)

    print("İHA arm edildi.")

    iha.simple_takeoff(irtifa)
    
    while iha.location.global_relative_frame.alt < irtifa * 0.9:
        print("İha hedefe yükseliyor.")
        time.sleep(1)

def land_and_disarm(iha):
    # İHA iniş moduna geçiriliyor
    print("İHA iniş moduna geçiriliyor.")
    iha.mode = VehicleMode("LAND")
    
    # İHA'nın yere inmesini bekliyoruz
    while iha.location.global_relative_frame.alt > 0.1:
        print(f"İHA iniyor. Mevcut irtifa: {iha.location.global_relative_frame.alt:.1f} metre")
        time.sleep(1)
    
    print("İHA yere indi.")
    
    # İHA'nın disarm edilmesi
    iha.armed = False
    
    while iha.armed is True:
        print("İHA disarm ediliyor...")
        time.sleep(0.5)
    
    print("İHA disarm edildi.")


takeoff(2,iha1)
takeoff(2,iha2)
takeoff(2,iha3)



land_and_disarm(iha1)
land_and_disarm(iha2)
land_and_disarm(iha3)
