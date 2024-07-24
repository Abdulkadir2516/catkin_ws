#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
from pymavlink import mavutil

# Drone'a bağlanma
iha1 = connect("127.0.0.1:14550", wait_ready=True)

def arm_and_takeoff(target_altitude):
    while not iha1.is_armable:
        print("Araç arm edilebilir durumda değil, bekleniyor...")
        time.sleep(1)

    iha1.mode = VehicleMode("GUIDED")
    while iha1.mode != 'GUIDED':
        print("GUIDED moduna geçiliyor...")
        time.sleep(1)

    iha1.armed = True
    while not iha1.armed:
        print("Arming...")
        time.sleep(1)

    iha1.simple_takeoff(target_altitude)
    while True:
        print("Yükseliyor: ", iha1.location.global_relative_frame.alt)
        if iha1.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Hedef yüksekliğe ulaşıldı")
            break
        time.sleep(1)

def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlon = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlon * dlon)) * 1.113195e5

def set_velocity_body(vehicle, vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,  # Bit mask, hangi parametrelerin geçerli olduğunu belirtir
        30, 50, 0,        # Pozisyon
        vx, vy, vz,     # Hız
        0, 0, 0,        # Hızlanma
        0, 0)           # Yönelim
    vehicle.send_mavlink(msg)
    vehicle.flush()

def goto_position_target_global_int(aLocation):
    msg = iha1.message_factory.set_position_target_global_int_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000111111111000,  # Bit mask
        aLocation.lat * 1e7,
        aLocation.lon * 1e7,
        aLocation.alt,
        0, 0, 0,
        0, 0, 0,
        0, 0)
    iha1.send_mavlink(msg)

def goto_waypoint(lat, lon, alt, airspeed):
    point = LocationGlobalRelative(lat, lon, alt)
    iha1.simple_goto(point, airspeed=airspeed)

    while True:
        current_location = iha1.location.global_relative_frame
        target_distance = get_distance_metres(current_location, point)
        print("Hedefe uzaklık: ", target_distance)
        if target_distance < 1:
            print("Hedefe ulaşıldı")
            break
        time.sleep(1)

waypoints = [
    (-35.364261, 149.165230, 7),  # Örnek waypoint koordinatları
    (-35.363261, 149.165230, 7)
]

airspeed = 50  # Hızı metre/saniye olarak ayarlayın

if __name__ == '__main__':
    try:
        arm_and_takeoff(7)

        iha1.airspeed = airspeed  # Genel hava hızını ayarlayın

        for waypoint in waypoints:
            lat, lon, alt = waypoint
            goto_waypoint(lat, lon, alt, airspeed)
        
        print("Tüm hedeflere ulaşıldı, iniş yapılıyor...")
        iha1.mode = VehicleMode("LAND")
        
        while iha1.armed:
            print("İniş yapılıyor...")
            time.sleep(1)
        
        print("İniş tamamlandı, araç disarm edildi.")

    except KeyboardInterrupt:
        print("Görev iptal edildi, araç disarm ediliyor.")
        iha1.armed = False
        while iha1.armed:
            time.sleep(1)
    finally:
        iha1.close()
        print("Bağlantı kapatıldı.")
