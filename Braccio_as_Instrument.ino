#include "Arduino.h"
#include "Vrekrer_scpi_parser.h"
#include <Braccio.h>
#include <Servo.h>

SCPI_Parser my_instrument;
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

void setup()
{
  my_instrument.RegisterCommand("*IDN?", &Identify);
  my_instrument.RegisterCommand(F("Braccio#"), &WriteMovement);
  Serial.begin(9600);
  Braccio.begin();
}

void loop()
{
  my_instrument.ProcessInput(Serial, "\n");
}

void Identify(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.println(F("Hcal ,Braccio Instrument ,#00,v1.0.0"));
}

int valor = 0;
int valor2[3];
String previa = "";
void WriteMovement(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  String header = String(commands.Last());
  header.toUpperCase();
  int suffix = -1;
  sscanf(header.c_str(),"%*[BRACCIO]%u", &suffix);
  String first_parameter = String(parameters.First());
  first_parameter.toUpperCase();
  // si valor fuera un arreglo
  previa = String(first_parameter);
  int values[7];
  int index = 0;
  char separator[] = " ";
  char s_c[previa.length() + 1];
  previa.toCharArray(s_c, previa.length() + 1);
  char *ptr = strtok(s_c, separator);
  while (ptr != NULL) {
    values[index] = atoi(ptr);
    ptr = strtok(NULL, separator);
    index++;
  }
  if(suffix==0){
      Braccio.ServoMovement(values[0],values[1], values[2],values[3],values[4],values[5],values[6]);  
      //interface.println(String(values[0])+","+String(values[1])+","+String(values[2])+","+String(values[3])+","+String(values[4])+","+String(values[5])+","+String(values[6]));
    }
}
