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

## Comandes X,Y du robot
*Victorine ; Sacha ; Martin*
