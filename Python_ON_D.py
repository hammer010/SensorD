import time
import dht22
import datetime
import os
print("Temporisation initialisation Raspberry")
time.sleep(180)

print("Demarrage programme")
from ftplib import FTP
from pyA20.gpio import gpio
from pyA20.gpio import port

# initialize GPIO
#gpio.setwarnings(False)
#gpio.setmode(GPIO.BCM)
PIN2 = port.PA6
gpio.init()
#gpio.cleanup()

while 1 :
    
    # Connexion serveur FTP
    ftp = FTP('192.168.1.170', 'pi', 'raspberry')
    etat = ftp.getwelcome()
    print "Etat : ",etat

    def average(list): 
        if (list!= []): return float(sum(list)) / len(list)
        
    # read data using pin 14
    instance = dht22.DHT22(pin=PIN2)

    i = 0
    list_temp = []
    list_hum = []
    
    while 1 :
        result = instance.read()
        if result.is_valid():
            list_temp.append(result.temperature)
            list_hum.append(result.humidity)
            i = i + 1
            os.system('clear')
            print(str(i) + "0%")
            time.sleep(6)
            os.system('clear')
            if i == 10 : 
                break
       
    temp_int= int(average(list_temp))
    temp_dec= int((average(list_temp) - int(average(list_temp)))*100)
    print("Horodatage: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
    print("Temperature: " + str(average(list_temp)) + " C")
    print("Humidite: " + str(average(list_hum)) + " %")

# Creation fichier de resultats
    fichier = open("sensorA.txt", "w")
    fichier.write(datetime.datetime.now().strftime("%H:%M"))
    fichier.write("\n" + str(average(list_temp)))
    fichier.write("\n" + str(average(list_hum)))
    fichier.write("\n" + str(temp_int))
    fichier.write("\n" + str(temp_dec))
    fichier.close()

# Envoi resultats vers serveur FTP
    ftp.cwd("/var/www/html")
    fichier = "/home/orangepi/SensorA/sensorA.txt"
    file = open(fichier,'rb')
    ftp.storbinary('STOR '+'sensorA.txt', file)
    ftp.retrlines('LIST')
    print ftp.dir()
    ftp.close()

# Fin du programme
    print("Resultats OK")
    print("Sleep ...")
    time.sleep(180)
