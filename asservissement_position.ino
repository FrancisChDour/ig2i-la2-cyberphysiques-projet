#include <FlexiTimer2.h>

int increment=0;
int consigne=0;
int byte_read;
int erreur=0;

const int maxPwm=60;

const float kp=8;
const float ki=2;
int somerreur=0;

int pwm=0;

void setup() {

Serial.begin(9600);
pinMode(6,OUTPUT);
pinMode(5,OUTPUT);
pinMode(3,INPUT);
attachInterrupt(digitalPinToInterrupt(3), codeur, RISING);

FlexiTimer2::set(30, asserv); // call every 500 1ms "ticks"
FlexiTimer2::start();
}
void loop() {
    if ( Serial.available() ) {
    int sens=1;
    consigne=0;
    while ( Serial.available() ) {
    byte_read = Serial.read();
    if (byte_read==45) {sens=-1;}
    if ( is_a_number(byte_read) ) {
    consigne = ascii2int(consigne, byte_read);
    }
    delay(2);
    }
    consigne*=sens;
    consigne*=8;
}}
boolean is_a_number(int n)
{
return n >= 48 && n <= 57;
}
int ascii2int(int n, int byte_read)
{
return n*10 + (byte_read - 48);
}
void codeur(){
if(pwm>=0) {increment++;}
else{increment--;}
}

void asserv(){
erreur=consigne-increment;

int corr_p=erreur*kp;
if(corr_p>maxPwm){corr_p=maxPwm;}
if(corr_p<-maxPwm){corr_p=-maxPwm;}

if(abs(somerreur+erreur)*ki<maxPwm) { somerreur+=erreur;}
else {
somerreur=maxPwm/ki;
if(erreur<0) {somerreur*=-1;}

}
if(erreur==0) {somerreur=0;}

int corr_i=somerreur*ki;
if(corr_i>maxPwm){corr_i=maxPwm;}
if(corr_i<-maxPwm){corr_i=-maxPwm;}

pwm=corr_i+corr_p;
if(pwm>maxPwm){pwm=maxPwm;}
if(pwm<-maxPwm){pwm=-maxPwm;}

if(pwm>=0){analogWrite(6,pwm); analogWrite(5,0);}
else{analogWrite(5,-pwm); analogWrite(6,0);}

Serial.print(corr_p);
Serial.print(" ");
Serial.print(corr_i);
Serial.print(" ");
Serial.print(consigne);
Serial.print(" ");
Serial.print(erreur);
Serial.print(" ");
Serial.println(increment);
}


void asservissement() {
int frequence_codeuse = frequence_echantillonnage*tick_codeuse; //100*tick_codeuse (pour obtenir des secondes)
 float vit_roue_tour_sec = (float)frequence_codeuse/(float)tick_par_tour_codeuse/(float)rapport_reducteur; //(100*tick_codeuse)/32/19
 float erreur = consigne_moteur - vit_roue_tour_sec; // pour le proportionnel
  somme_erreur += erreur; // pour l'intégrateur
   float delta_erreur = erreur-erreur_precedente; // pour le dérivateur
    erreur_precedente = erreur; // P : calcul de la commande
     vitMoteur = kp*erreur + ki*somme_erreur + kd*delta_erreur; //somme des tois erreurs