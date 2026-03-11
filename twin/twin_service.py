"""MQTT Twin Service for machine state monitoring."""

import json
import logging
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path to allow imports from sibiling modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import paho.mqtt.client as mqtt

from config.settings import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, MQTT_KEEPALIVE, LOG_LEVEL
from state import MachineState
from anomaly import check_anomaly

# Logging configuration
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Instance of the machine state
machine = MachineState()


def on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
    """Callback for processing received MQTT messages.
    
    Args:
        client: MQTT Client
        userdata: User data (not used)
        msg: Received MQTT message
    """
    try:
        # Decode the message payload
        data = json.loads(msg.payload.decode())
        logger.debug(f"Received message: {data}")
        
        # Update the machine state
        machine.update(data)
        logger.info(f"Machine state updated: RPM={machine.rpm}, "
                   f"Temp={machine.temperature}°C, Vib={machine.vibration}")
        
        # Check for anomalies
        alerts = check_anomaly(data)
        if alerts:
            logger.warning(f"⚠️ ALERTS DETECTED: {alerts}")
    
    except json.JSONDecodeError:
        logger.error(f"Failed to decode message: {msg.payload}")
    except KeyError as e:
        logger.error(f"Missing required field in message: {e}")
    except Exception as e:
        logger.error(f"Unexpected error processing message: {e}")


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
        client.subscribe(MQTT_TOPIC)
        logger.info(f"✅ Subscribed to topic: {MQTT_TOPIC}")
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
    """Start the Twin Service."""
    logger.info("Starting Twin Service...")
    
    try:
        # Create the MQTT client
        client = mqtt.Client()
        client.on_message = on_message
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        
        # Connect to the broker
        logger.info(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=MQTT_KEEPALIVE)
        
        # Start the loop
        logger.info("Starting MQTT event loop...")
        client.loop_forever()
    
    except KeyboardInterrupt:
        logger.info("Twin Service interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error in Twin Service: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()