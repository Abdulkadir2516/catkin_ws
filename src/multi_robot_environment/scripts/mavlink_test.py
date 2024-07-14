from pymavlink import mavutil

# Bağlantı oluştur
the_connection = mavutil.mavlink_connection('udpin:localhost:14561')
# SIM_VEHICLE: "mavproxy.py" "--master" "tcp:127.0.0.1:5780" "--sitl" "127.0.0.1:5521" "--out" "127.0.0.1:14570" "--out" "127.0.0.1:14571" "--out" "tcpin:0.0.0.0:8200"

# İlk heartbeat mesajını bekle
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

# Dronu ARM yap
the_connection.arducopter_arm()
print(the_connection.location())