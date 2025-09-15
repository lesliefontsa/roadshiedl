# Exemple de code Arduino pour envoyer des données à l'API
/*
  RoadShield Travel Agency - Arduino Sensor Code
  Ce code collecte les données de capteurs et les envoie à l'API FastAPI
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <GPS.h>
#include <Wire.h>

// Configuration WiFi
const char* ssid = "VotreWiFi";
const char* password = "VotreMotDePasse";

// Configuration API
const char* api_url = "http://votre-serveur:8003/arduino/data";
const char* device_id = "ARDUINO_001";

// Pins des capteurs
const int eyeSensorPin = A0;
const int tiltSensorPin = A1;
const int speedSensorPin = 2;
const int brakePin = 3;

// Variables globales
float latitude = 0.0;
float longitude = 0.0;
float speed = 0.0;
bool harsh_braking = false;
bool harsh_acceleration = false;

void setup() {
  Serial.begin(115200);
  
  // Initialiser WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion WiFi...");
  }
  Serial.println("WiFi connecté");
  
  // Initialiser les pins
  pinMode(speedSensorPin, INPUT);
  pinMode(brakePin, INPUT_PULLUP);
  
  // Initialiser les capteurs
  initSensors();
}

void loop() {
  // Lire les données des capteurs
  readSensorData();
  
  // Envoyer les données toutes les 5 secondes
  static unsigned long lastSend = 0;
  if (millis() - lastSend > 5000) {
    sendDataToAPI();
    lastSend = millis();
  }
  
  delay(100);
}

void readSensorData() {
  // Lire le capteur d'yeux (simulation)
  int eyeValue = analogRead(eyeSensorPin);
  float eye_closure_duration = map(eyeValue, 0, 1023, 0, 10) / 10.0;
  
  // Lire l'inclinaison de la tête
  int tiltValue = analogRead(tiltSensorPin);
  
  // Lire la vitesse (simulation avec GPS)
  speed = readGPSSpeed();
  
  // Détecter le freinage brusque
  harsh_braking = digitalRead(brakePin) == LOW;
  
  // Mettre à jour la position GPS
  updateGPSPosition();
}

void sendDataToAPI() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(api_url);
    http.addHeader("Content-Type", "application/json");
    
    // Créer le JSON avec les données
    DynamicJsonDocument doc(1024);
    doc["device_id"] = device_id;
    doc["timestamp"] = getTimestamp();
    doc["latitude"] = latitude;
    doc["longitude"] = longitude;
    doc["speed"] = speed;
    doc["eye_closure_duration"] = getEyeClosureDuration();
    doc["head_position"] = getHeadPosition();
    doc["fatigue_level"] = getFatigueLevel();
    doc["harsh_braking"] = harsh_braking;
    doc["harsh_acceleration"] = harsh_acceleration;
    
    // Ajouter des données brutes
    JsonObject raw_data = doc.createNestedObject("raw_data");
    raw_data["eye_sensor"] = analogRead(eyeSensorPin);
    raw_data["tilt_sensor"] = analogRead(tiltSensorPin);
    raw_data["temperature"] = readTemperature();
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    // Envoyer la requête
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse API: " + response);
    } else {
      Serial.println("Erreur envoi données: " + String(httpResponseCode));
    }
    
    http.end();
  }
}

float getEyeClosureDuration() {
  // Simulation de détection de fermeture des yeux
  int eyeValue = analogRead(eyeSensorPin);
  if (eyeValue < 200) {
    return random(0, 60) / 10.0; // 0-6 secondes
  }
  return 0.0;
}

String getHeadPosition() {
  int tiltValue = analogRead(tiltSensorPin);
  if (tiltValue < 300) return "nodding";
  if (tiltValue > 700) return "tilted";
  return "normal";
}

int getFatigueLevel() {
  // Calculer le niveau de fatigue basé sur plusieurs facteurs
  int eyeValue = analogRead(eyeSensorPin);
  int tiltValue = analogRead(tiltSensorPin);
  
  int fatigueScore = 0;
  if (eyeValue < 300) fatigueScore += 3;
  if (tiltValue < 400 || tiltValue > 600) fatigueScore += 2;
  
  return constrain(fatigueScore, 1, 10);
}

float readGPSSpeed() {
  // Simulation de lecture GPS
  return random(0, 120);
}

void updateGPSPosition() {
  // Simulation de mise à jour GPS
  latitude = 48.8566 + random(-100, 100) / 10000.0;
  longitude = 2.3522 + random(-100, 100) / 10000.0;
}

String getTimestamp() {
  // Retourner un timestamp simple
  return String(millis());
}

float readTemperature() {
  // Simulation de lecture de température
  return random(20, 35);
}

void initSensors() {
  // Initialiser les capteurs spécifiques
  Serial.println("Capteurs initialisés");
}