#include <Servo.h>
#define SER 3 //Pin para el servo
 
Servo servo; //Objeto servo
int mssg; //Variable para guardar el mensaje recibido por serial
  
void setup()
{
   //Inicializamos el servo y el Serial:
   servo.attach(SER);
   Serial.begin(115200);
}
  
void loop(){
    while(Serial.read()!='k'){}
    int D=distancia(20);
    Serial.println(D);
    
  
    while(Serial.read()!='s'){}
     mssg = Serial.parseInt(); //Leemos el serial
     servo.write(mssg); //Movemos el servo
}




float distancia(int n)
{
  long suma=0;
  for(int i=0;i<n;i++)
  {
    suma=suma+analogRead(A0);
  }  
  float adc=suma/n;
  float distancia_cm = (17569.7 * pow(adc, -1.2062));
  return(distancia_cm);
}
