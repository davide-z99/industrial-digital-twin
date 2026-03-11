# Industrial Digital Twin

IoT application for real time monitoring of industrial machines with anomaly detection.

## 🎯 Description

**Industrial Digital Twin** is a comprehensive IoT monitoring system that creates a 
virtual representation of an industrial machine in real-time. It captures live telemetry 
data, detects operational anomalies, and exposes a synchronized state through REST APIs 
and MQTT messaging.

### Key Features:
- 📊 **Real-time Telemetry Collection**: Continuous monitoring of RPM, temperature, and vibration
- 🔔 **Intelligent Anomaly Detection**: Automatic alerts for out-of-threshold conditions
- 🌐 **REST API Integration**: Access machine state via modern HTTP endpoints
- 📱 **MQTT Communication**: Decoupled components using publish/subscribe pattern
- 🔢 **State Management**: Synchronized machine state across all system components
- ⚙️ **Configurable Thresholds**: Customizable alert parameters for different scenarios

### Architecture

```
┌─────────────────────────────────────────────────┐
│         MQTT Broker (Mosquitto)                 │
│              localhost:1883                     │
└──────────────┬─────────────────┬────────────────┘
               │                 │
               │                 │
        ┌──────▼────┐    ┌──────▼──────┐
        │ Simulator │    │ Twin Service│
        │(Publish)  │    │(Subscribe)  │
        │           │    │  - State    │
        │  - RPM    │    │  - Anomaly  │
        │  - Temp   │    │  Detection  │
        │  - Vib    │    └──────┬──────┘
        │  - Status │           │
        └───────────┘           │
                          ┌─────▼──────┐
                          │ FastAPI    │
                          │ /machine   │
                          │ :8000      │
                          └────────────┘
```

## 🚀 Quick Start

### Requirements
- Python 3.8+
- MQTT Broker (Mosquitto)
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/tuonome/industrial-digital-twin.git
cd industrial-digital-twin
```

2. **Install the dependences**
```bash
pip install -r requirements.txt
```

3. **Start the MQTT Broker** (in a separated terminal)
```bash
# On Windows with Mosquitto
mosquitto -p 1883

# Otherwise with Docker
docker run -it -p 1883:1883 --name mosquitto eclipse-mosquitto
```

4. **Start the components** (in separated terminals)

Terminal 1 - Twin Service (MQTT Subscriber):
```bash
cd twin
python twin_service.py
```

Terminal 2 - Simulator (MQTT Publisher):
```bash
cd simulator
python simulator.py
```

Terminal 3 - API Server:
```bash
cd api
uvicorn main:app --reload --port 8000
```

5. **Tests the API**
```bash
curl http://localhost:8000/machine
```

## 📁 Project Structure

```
industrial-digital-twin/
├── README.md                 # This file
├── .gitignore               # File ignored by Git
├── requirements.txt         # Python Dependences
│
├── simulator/
│   └── simulator.py         # Generates MQTT telemetry data
│
├── twin/
│   ├── state.py            # Current machine state
│   ├── anomaly.py          # Anomalies detection logic
│   └── twin_service.py     # MQTT Subscriber
│
└── api/
    └── main.py             # API FastAPI
```

## 📋 Components

### 1. **Simulator** (`simulator/simulator.py`)
It publishes random telemetry data every 5 seconds on MQTT.

**Published parameters:**
- `rpm`: Velocity (900-1100)
- `temperature`: Temperature °C (70-90)
- `vibration`: Vibration 0-1 (0.1-0.8)
- `status`: Operative status (RUN)

### 2. **Twin Service** (`twin/twin_service.py`)
It subscribes to MQTT topic and it monitors the machine status.

**Features:**
- ✅ Updates machine status at real time
- ✅ Detects the anomalies
- ✅ Print alerts if necessary

**Alert tresholds:**
- Temperature > 80°C
- Vibration > 0.5

### 3. **API** (`api/main.py`)
Exposes the REST endpoint `/machine` to read the status.

**Endpoint:**
- `GET /machine` - Returns current machine status

## 🔧 Configuration

The connection parameters are configured in:
- `BROKER = "localhost"`
- `TOPIC = "factory/machine1/telemetry"`

To change them, modify the respective components files.

## 📊 Monitoring

### Check data at real time

**With mosquitto_sub:**
```bash
mosquitto_sub -h localhost -t "factory/machine1/telemetry"
```

**By API:**
```bash
curl http://localhost:8000/machine | jq
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" on MQTT | Make sure that Mosquitto is running on localhost:1883 |
| FastAPI doesn't start | Verify that `uvicorn` is installed: `pip install uvicorn` |
| "ModuleNotFoundError" | Install the dependences: `pip install -r requirements.txt` |

## 🔮 Future Improvements

- [ ] Status synchronization between Twin Service and API
- [ ] Structured logging
- [ ] Configuration via environment variables
- [ ] Unit test
- [ ] Docker Compose to automatic start
- [ ] Dashboard web for visualization
- [ ] Data history with database
- [ ] Configurable alert rules

## 📝 License

MIT License - see `LICENSE` FILE to details

## 👤 Author

Davide Ziglioli

## 📧 Contacts

For questions or suggestions, opens an issue on GitHub.

---