# ig2i-la2-cyberphysiques-projet

*Victorine DORAL ; Sacha LESUEUR ; Martin CARON ; Mathis HALOY ; François DOURLENS-MONCHY*
**Robot 01**
## Mise en place des protocoles de connexion au robot
*Mathis ; François*

On tente dans un premier temps de se connecter au robot depuis un PC de la salle.

On définit un nouvel hôte dans la config SSH du PC pour faciliter la tâche :
```bash
host robot1
        HostName 172.22.29.61
        User pi
```

Une fois connecté en ssh avec la commande `ssh robot1`, on configure le port serial avec `raspi-config` selon la documentation suivante :
> https://www.raspberrypi.org/documentation/configuration/uart.md

```

    Start raspi-config: sudo raspi-config.
    Select option 3 - Interface Options.
    Select option P6 - Serial Port.
    At the prompt Would you like a login shell to be accessible over serial? answer 'No'
    At the prompt Would you like the serial port hardware to be enabled? answer 'Yes'
    Exit raspi-config and reboot the Pi for changes to take effect.

```

Port serial configuré :
```bash
pi@raspberrypi:/boot $ ls -l /dev/ | grep ttyS0
lrwxrwxrwx  1 root root           5 avril  7 09:33 serial0 -> ttyS0
crw-rw----  1 root dialout   4,  64 avril  7 09:33 ttyS0
```

On utilisera le port Serial ttyS0 pour la suite.

Sur le Raspberry pi, on créé le programme python suivant :

```python
#!/usr/bin/env python3
import serial
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 125200, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
```

Depuis la console Arduino du PC connecté en USB, on téléverse le code suivant :
```arduino
void setup() {
  Serial1.begin(115200);
  Serial2.begin(115200);
  Serial3.begin(115200);
  Serial.begin(115200);
}
void loop() {
  Serial.println("Hello from Serial");
  Serial1.println("Hello from Serial1");
  Serial2.println("Hello from Serial2");
  Serial3.println("Hello from Serial3");
  delay(1000);
}
```

En lançant le programe python sur le raspberry, on constate que la chaine de caractère reçue est celle passée dans le port Serial2 :

```bash
$ ./test.py 
Hello from Serial2
Hello from Serial2
Hello from Serial2
```

Dans la mêeme idée, on tente de d'emettre un message depuis le rapsberry vers le arduino, de le réceptionner et de renvoyer une réponse.
Sur la console arduino :

```arduino
void setup() {
  Serial2.begin(115200);
}

void loop() {
  if (Serial2.available() > 0) {
    String data = Serial2.readStringUntil('\n');
    Serial2.print("You sent me: ");
    Serial2.println(data);
  }
}
```

Sur le raspberry :
```python
#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    ser.flush()
    while True:
        ser.write(b"Hello from Raspberry Pi!\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)

```

Quand on lance le programme d'envoie / réception, on a le résultat suivant :
```bash
$ ./bi-directional.py 
You sent me: Hello from Raspberry Pi!
You sent me: Hello from Raspberry Pi!
You sent me: Hello from Raspberry Pi!
```
## Comandes X,Y du robot
*Victorine ; Sacha ; Martin*
