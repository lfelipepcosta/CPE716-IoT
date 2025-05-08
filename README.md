# Trabalho Prático 1 - Sensor de Fumaça Inteligente

## Objetivo
Sistema de detecção de fumaça com ESP32 que envia alertas via Telegram

## Estrutura
- `codigos/`: Contém os arquivos fonte
  - `praticaIoT.ino`: Código para o ESP32
  - `server.py`: Servidor Flask para envio de mensagens

## Requisitos
- ESP32 com WiFi
- Python 3.x com Flask
- Conta no Telegram com bot configurado

## Como executar
1. Carregar o código .ino no ESP32
2. Executar o servidor: `python server.py`
3. Pressionar o botão conectado ao ESP32
