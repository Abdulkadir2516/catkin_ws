#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
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


def create_square_trajectory(drone_ns, side_length):
    # Her drone için PoseStamped yayıncıları oluşturun
    pub = rospy.Publisher(f'/{drone_ns}/mavros/setpoint_position/local', PoseStamped, queue_size=10)

    rate = rospy.Rate(1)  # 1 Hz

    # Kare yolunun köşe koordinatları
    square_coords = [
        (side_length, 0, 2),   # A noktası
        (side_length, side_length, 2),  # B noktası
        (0, side_length, 2),   # C noktası
        (0, 0, 2)  # D noktası
    ]

    # PoseStamped mesajını oluştur
    pose = PoseStamped()
    pose.header.frame_id = 'map'

    for coord in square_coords:
        # Her köşeye git
        x, y, z = coord
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z

        # Her köşede belirli bir süre bekleyin
        start_time = time.time()
        while time.time() - start_time < 3:  # 5 saniye boyunca hedef konumda kal
            pose.header.stamp = rospy.Time.now()
            pub.publish(pose)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('multi_drone_square')

    # Thread'leri oluştur
    takeoff_threads = []
    mission_threads = []

    for iha, drone in zip([iha1, iha2, iha3], ["drone1", "drone2", "drone3"]):
        takeoff_thread = threading.Thread(target=takeoff, args=(2, iha))
        takeoff_threads.append(takeoff_thread)
        mission_thread = threading.Thread(target=create_square_trajectory, args=(drone, 2))
        mission_threads.append(mission_thread)

    # Kalkış thread'lerini başlat
    for thread in takeoff_threads:
        thread.start()

    # Kalkış thread'lerinin bitmesini bekle
    for thread in takeoff_threads:  
        thread.join()

    # İniş thread'lerini başlat
    for thread in mission_threads:
        thread.start()

    # İniş thread'lerinin bitmesini bekle
    for thread in mission_threads:
        thread.join()

    print("Bütün işlemler tamamlandı.")
