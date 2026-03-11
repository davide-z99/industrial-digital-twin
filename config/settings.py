"""
Centralized configuration for the Industrial Digital Twin application.
"""

import os
from typing import Final

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ============================================================================
# MQTT Configuration
# ============================================================================

MQTT_BROKER: Final[str] = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT: Final[int] = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC: Final[str] = os.getenv("MQTT_TOPIC", "factory/machine1/telemetry")
MQTT_KEEPALIVE: Final[int] = int(os.getenv("MQTT_KEEPALIVE", "60"))

# ============================================================================
# Anomaly Detection Thresholds
# ============================================================================

TEMP_THRESHOLD: Final[float] = float(os.getenv("TEMP_THRESHOLD", "80.0"))
VIBRATION_THRESHOLD: Final[float] = float(os.getenv("VIBRATION_THRESHOLD", "0.5"))

# ============================================================================
# Simulator Configuration
# ============================================================================

SIMULATOR_INTERVAL: Final[int] = int(os.getenv("SIMULATOR_INTERVAL", "5"))
SIMULATOR_RPM_MIN: Final[int] = int(os.getenv("SIMULATOR_RPM_MIN", "900"))
SIMULATOR_RPM_MAX: Final[int] = int(os.getenv("SIMULATOR_RPM_MAX", "1100"))
SIMULATOR_TEMP_MIN: Final[float] = float(os.getenv("SIMULATOR_TEMP_MIN", "70.0"))
SIMULATOR_TEMP_MAX: Final[float] = float(os.getenv("SIMULATOR_TEMP_MAX", "90.0"))
SIMULATOR_VIB_MIN: Final[float] = float(os.getenv("SIMULATOR_VIB_MIN", "0.1"))
SIMULATOR_VIB_MAX: Final[float] = float(os.getenv("SIMULATOR_VIB_MAX", "0.8"))

# ============================================================================
# API Configuration
# ============================================================================

API_HOST: Final[str] = os.getenv("API_HOST", "127.0.0.1")
API_PORT: Final[int] = int(os.getenv("API_PORT", "8000"))

# ============================================================================
# Logging Configuration
# ============================================================================

LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
