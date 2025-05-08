#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "network";
const char* password = "password";
const char* servidor = "http://192.168.1.240:5000/alert";
const int pinoBotao = 18;

void setup() {
  Serial.begin(115200);
  pinMode(pinoBotao, INPUT); // Modo INPUT padrão (sem PULLUP interno)
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Conectado ao Wi-Fi");
}

void loop() {
  // Leitura com resistor externo 10kΩ (LOW = solto, HIGH = pressionado)
  if (digitalRead(pinoBotao) == HIGH) { // Invertemos a lógica para pull-down
    enviarAlerta("🚨 Alerta de fumaça!");
    delay(1000); // Debounce
  }
}

void enviarAlerta(const String& mensagem) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(servidor);
    http.addHeader("Content-Type", "application/json");
    
    // Formação da mensagem JSON
    String corpo = "{\"mensagem\":\"" + mensagem + "\","
                 "\"tipo\":\"alerta\","
                 "\"dispositivo\":\"esp32\"}";
    
    Serial.println("Enviando: " + corpo);
    int httpCode = http.POST(corpo);
    
    if (httpCode > 0) {
      Serial.println("✅ Código HTTP: " + String(httpCode));
    } else {
      Serial.println("❌ Erro: " + http.errorToString(httpCode));
    }
    http.end();
  }
}