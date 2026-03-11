"""MQTT Simulator for generating machine telemetry data."""

import json
import logging
import random
import sys
import time
from typing import Dict, Any
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import paho.mqtt.client as mqtt

from config.settings import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_TOPIC,
    SIMULATOR_INTERVAL,
    SIMULATOR_RPM_MIN,
    SIMULATOR_RPM_MAX,
    SIMULATOR_TEMP_MIN,
    SIMULATOR_TEMP_MAX,
    SIMULATOR_VIB_MIN,
    SIMULATOR_VIB_MAX,
    LOG_LEVEL,
)

# Logging configuration
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def generate_telemetry() -> Dict[str, Any]:
    """Generate random telemetry data for simulation.
    
    Returns:
        Dictionary with telemetry data: rpm, temperature, vibration, status
    """
    payload = {
        "rpm": random.randint(SIMULATOR_RPM_MIN, SIMULATOR_RPM_MAX),
        "temperature": round(random.uniform(SIMULATOR_TEMP_MIN, SIMULATOR_TEMP_MAX), 2),
        "vibration": round(random.uniform(SIMULATOR_VIB_MIN, SIMULATOR_VIB_MAX), 3),
        "status": "RUN"
    }
    return payload


def on_connect(client: mqtt.Client, userdata: Any, flags: dict, rc: int) -> None:
    """Callback for MQTT broker connection.
    
    Args:
        client: MQTT Client
        userdata: User data (not used)
        flags: Connection flags
        rc: Return code of the connection
    """
    if rc == 0:
        logger.info(f"✅ Connected to MQTT broker {MQTT_BROKER}:{MQTT_PORT}")
    else:
        logger.error(f"❌ Failed to connect to MQTT broker. Return code: {rc}")


def on_disconnect(client: mqtt.Client, userdata: Any, rc: int) -> None:
    """Callback for MQTT broker disconnection.
    
    Args:
        client: MQTT Client
        userdata: User data (not used)
        rc: Return code of the disconnection
    """
    if rc != 0:
        logger.warning(f"Unexpected disconnection from MQTT broker. Return code: {rc}")
    else:
        logger.info("Disconnected from MQTT broker")


def main() -> None:
    """Start the telemetry simulator."""
    logger.info("Starting Machine Telemetry Simulator...")
    
    try:
        # Create MQTT client
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        
        # Connect to the broker
        logger.info(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        
        # Wait for the connection
        time.sleep(1)
        
        logger.info(f"Publishing telemetry to topic: {MQTT_TOPIC}")
        logger.info(f"Publishing interval: {SIMULATOR_INTERVAL} seconds")
        logger.info("Simulator running (press Ctrl+C to stop)...")
        
        # Publish loop
        while True:
            payload = generate_telemetry()
            client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
            logger.debug(f"Published: {payload}")
            print(f"📊 {payload}")
            
            time.sleep(SIMULATOR_INTERVAL)
    
    except KeyboardInterrupt:
        logger.info("Simulator interrupted by user")
        client.loop_stop()
        client.disconnect()
        logger.info("Simulator stopped")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error in Simulator: {e}")
        client.loop_stop()
        client.disconnect()
        sys.exit(1)


if __name__ == "__main__":
    main()