const byte PIN1_1 = 7; //読み取るピン
const byte PIN1_2 = 8;
const byte PIN2_1 = 6;
const byte PIN2_2 = 5;

int up = 4500; //上端: 5000
int down = 0; //下端: 0

// the loop function runs over and over again forever
void setup() {
  Serial.begin(115200);
  Serial.println("Serial Start!");
}
 
void loop() {  
  double val1_1 = analogRead(PIN1_1);
  double val1_2 = analogRead(PIN1_2);
  double val2_1 = analogRead(PIN2_1);
  double val2_2 = analogRead(PIN2_2);

  //プロッタの縦軸固定のため追加
  Serial.print(up);
  Serial.print(",");
  Serial.print(down);
  Serial.print(",");
  // Serial.print(millis());
  // Serial.print(",");

  //Serial.print(">");
  Serial.print(val1_1);
  Serial.print(",");
  Serial.print(val1_2);
  Serial.print(",");
  Serial.print(val2_1);
  Serial.print(",");
  Serial.print(val2_2);

  Serial.println("");

  //delay(10); //Sampling Rate 100Hz
  delay(20); //50Hz ← 2023/11/20搬入時は50Hz

  /*
  double volt = val/4095*3.3; //電圧変換
  Serial.println(volt);  
  delay(50);
  */
}
