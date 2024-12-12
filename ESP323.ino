#include <WiFi.h>
#include <PubSubClient.h>

// WiFi配置
const char* ssid = "d****y1";
const char* password = "60******811";

// MQTT配置
const char* mqtt_server = "hl****ce";
const int mqtt_port = ****;  // 默认MQTT端口

WiFiClient espClient;
PubSubClient client(espClient);

// 按钮引脚
const int button1Pin = 12;
const int button2Pin = 13;
const int button3Pin = 14;

// 按钮状态
int lastButton1State = HIGH;
int lastButton2State = HIGH;
int lastButton3State = HIGH;

// MQTT回调函数
void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  if (message == "#6") {
    Serial.println("hello");
    digitalWrite(5,HIGH);
  } else if (message == "#7") {
    digitalWrite(5,LOW);
    Serial.println("world");
  }
  else if (message == "#8") {
    digitalWrite(16,LOW);
    Serial.println("world");
  }
  else if (message == "#9") {
    digitalWrite(16,HIGH);
    Serial.println("world");
  }
}

// WiFi连接函数
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

// MQTT连接函数
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client123")) {
      Serial.println("connected");
      client.subscribe("4b_road");  // 替换为订阅的主题
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(5,OUTPUT);
  pinMode(16,OUTPUT);
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(button3Pin, INPUT_PULLUP);

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // 检测按钮1
  int button1State = digitalRead(button1Pin);
  if (button1State == LOW) {
    delay(100);
    while (button1State == LOW) {
      delay(100);
    }
    client.publish("4b_road", "#1");  // 替换为你的发布主题
    Serial.println("Button 1 pressed, sent #1");
  }

  // 检测按钮2
  int button2State = digitalRead(button2Pin);
  if (button2State == LOW) {
    delay(100);
    while (button2State == LOW) {
      delay(100);
    }
    client.publish("4b_road", "#2");
    Serial.println("Button 2 pressed, sent #2");
  }

  // 检测按钮3
  int button3State = digitalRead(button3Pin);
  if (button3State == LOW) {

    delay(100);
    while (button3State == LOW) {
      delay(100);
    }
    client.publish("4b_road", "#3");
    Serial.println("Button 3 pressed, sent #3");
  }
}
