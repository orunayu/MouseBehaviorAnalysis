import processing.serial.*;

Serial myPort;
PrintWriter output;
String fileName;

void setup()
{
  int serial_num = 1;
  // ここでシリアルポートを選択します。環境によって Serial.list()[]の[]内の数字が異なることに注意
  myPort = new Serial(this, Serial.list()[serial_num], 115200);
  myPort.bufferUntil('\n');
  println("conect port = ", Serial.list()[serial_num]);

  //mouse_sensor.csvという名前のファイルを作成し、データを書き込みます。
  String   dateName = year()+"-"+month()+"-"+day()+"_"+hour()+"-"+minute()+"-"+second()+"_";
  fileName = dateName + "pc0_rotationData.csv";//base0の部分はマザーの番号によって変える
  output = createWriter(fileName);
  output.println("pc0");//番号はマザーの番号で変える
}

void draw() 
{
  // メインの描画ループですが、今回は何も描画しません。
}

void serialEvent(Serial myPort)
{
  try {
    if(output != null){
      String inString = myPort.readStringUntil('\n');
      if (inString != null) {
        println(inString);
        synchronized(output) {
          String current_time = year() + "/" + month() + "/" + day() + "," + hour() + ":" + minute() + ":" + second() + ":" + millis() + ",";
          output.println(current_time + trim(inString));
        }
      }
    }
  } catch (Exception e) {
    e.printStackTrace();
    println("Error in serialEvent: " + e.getMessage());
  }
}

void keyPressed()
{
  // キーが押されたときにCSVファイルを保存し、プログラムを終了します。
  output.flush();
  output.close();
  exit();
}
