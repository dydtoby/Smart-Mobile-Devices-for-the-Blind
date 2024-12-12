#include <WiFi.h>
#include <PubSubClient.h>

// WiFi 配置
const char* ssid = "dy**y1";
const char* password = "60**9811";

// MQTT 配置
const char* mqtt_server = "hli****pace";
const int mqtt_port = 1****;

WiFiClient wifiClient;
PubSubClient client(wifiClient);

// 按钮引脚
const int button1Pin = D2;
const int button2Pin = D3;
const int button3Pin = D4;

// 输出引脚
const int output1Pin = 5;
const int output2Pin = 6;
const int output3Pin = 7;


// MQTT 回调函数
void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  // 控制输出引脚的逻辑
  if (message == "#6") {
    digitalWrite(output1Pin, HIGH);
    Serial.println("Output 1 HIGH");
  } else if (message == "#7") {
    digitalWrite(output1Pin, LOW);
    Serial.println("Output 1 LOW");
  } else if (message == "#8") {
    digitalWrite(output2Pin, HIGH);
    Serial.println("Output 2 HIGH");
  } else if (message == "#9") {
    digitalWrite(output2Pin, LOW);
    Serial.println("Output 2 LOW");
  } else if (message == "#10") {
    digitalWrite(output3Pin, HIGH);
    Serial.println("Output 3 HIGH");
  } else if (message == "#11") {
    digitalWrite(output3Pin, LOW);
    Serial.println("Output 3 LOW");
  }
}

void setup_wifi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("ArduinoUnoR4")) {
      Serial.println("connected");
      client.subscribe("4b_road");  // 替换为你的 MQTT 主题
    } else {
      Serial.print("failed, rc=");
      Serial.println(client.state());
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  // 设置按钮引脚为输入模式
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(button3Pin, INPUT_PULLUP);

  // 设置输出引脚为输出模式
  pinMode(output1Pin, OUTPUT);
  pinMode(output2Pin, OUTPUT);
  pinMode(output3Pin, OUTPUT);

  // 初始化输出为关闭
  digitalWrite(output1Pin, LOW);
  digitalWrite(output2Pin, LOW);
  digitalWrite(output3Pin, LOW);

  setup_wifi();

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // 按钮 1 逻辑
  int button1State = digitalRead(button1Pin);
  if (button1State == LOW) {
    Serial.println("press");
    delay(100);
    while (digitalRead(button1Pin) == LOW) {
      Serial.println("press");
      delay(10);
    }
    client.publish("4b_road", "#1");
    Serial.println("Button 1 pressed, sent #1");
  }

  // 按钮 2 逻辑
  int button2State = digitalRead(button2Pin);
  if (button2State == LOW) {
    while (digitalRead(button2Pin) == LOW) {
      delay(10);
    }
    client.publish("4b_road", "#2");
    Serial.println("Button 2 pressed, sent #2");
  }

  // 按钮 3 逻辑
  int button3State = digitalRead(button3Pin);
  if (button3State == LOW) {
    while (digitalRead(button3Pin) == LOW) {
      delay(10);
    }
    client.publish("4b_road", "#3");
    Serial.println("Button 3 pressed, sent #3");
  }
}
