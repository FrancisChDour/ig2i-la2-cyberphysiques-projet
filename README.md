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
$ ls -l /dev/ | grep ttyAMA0
lrwxrwxrwx  1 root root           7 avril  7 09:33 serial1 -> ttyAMA0
crw-rw----  1 root dialout 204,  64 avril  7 09:34 ttyAMA0

```

## Comandes X,Y du robot
*Victorine ; Sacha ; Martin*
