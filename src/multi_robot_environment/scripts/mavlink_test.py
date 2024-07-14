from pymavlink import mavutil

# Bağlantı oluştur
the_connection = mavutil.mavlink_connection('udpin:localhost:14551')

# İlk heartbeat mesajını bekle
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

print(help(the_connection))
# Dronu ARM yap
