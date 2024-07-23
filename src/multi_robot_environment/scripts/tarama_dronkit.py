from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

# Connect to the Vehicle
print("Connecting to vehicle on: '127.0.0.1:14550'")
vehicle = connect('127.0.0.1:14570', wait_ready=True)

# Function to arm and takeoff to a specified altitude
def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Function to send the vehicle to a specific location
def goto_position_target_global_int(aLocation):
    vehicle.simple_goto(aLocation)
    while True:
        distance = get_distance_metres(vehicle.location.global_frame, aLocation)
        print("Distance to target: ", distance)
        if distance <= 1:
            print("Reached target location")
            break
        time.sleep(2)

# Function to calculate distance between two locations
def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def main():
    # Set default speed
    vehicle.airspeed = 500  # Set airspeed to 5 m/s
    vehicle.groundspeed = 50  # Set groundspeed to 5 m/s

    # Define the coordinates for the corners of the area (100m x 100m)
    starting_location = vehicle.location.global_relative_frame
    coords = [
        (starting_location.lat, starting_location.lon),
        (starting_location.lat, starting_location.lon + 0.0009),
        (starting_location.lat + 0.0009, starting_location.lon + 0.0009),
        (starting_location.lat + 0.0009, starting_location.lon)
    ]

    # Arm and take off to 10 meters
    arm_and_takeoff(10)

    # Go to each corner
    for coord in coords:
        location = LocationGlobalRelative(coord[0], coord[1], 10)
        goto_position_target_global_int(location)
        time.sleep(5)  # Wait for a bit at each corner

    print("Landing...")
    vehicle.mode = VehicleMode("LAND")

if __name__ == '__main__':
    main()
