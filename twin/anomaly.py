"""Anomaly detection module for machine telemetry."""

import logging
from typing import Dict, Any, List

from config.settings import TEMP_THRESHOLD, VIBRATION_THRESHOLD

logger = logging.getLogger(__name__)


def check_anomaly(data: Dict[str, Any]) -> List[str]:
    """Detects anomalies in the machine telemetry data.
    
    Checks if temperature and vibration exceed the configured thresholds
    and returns a list of any detected alerts.
    
    Args:
        data: Dictionary with telemetry data (temperature, vibration)
    
    Returns:
        List of strings with detected anomalies (empty if no anomalies)
    
    Example:
        >>> check_anomaly({"temperature": 85, "vibration": 0.6})
        ['High Temperature', 'High Vibration']
    """
    alerts: List[str] = []

    # Check temperature threshold
    if data.get("temperature", 0) > TEMP_THRESHOLD:
        alert = f"High Temperature ({data['temperature']}°C > {TEMP_THRESHOLD}°C)"
        alerts.append(alert)
        logger.warning(alert)

    # Check vibration threshold
    if data.get("vibration", 0) > VIBRATION_THRESHOLD:
        alert = f"High Vibration ({data['vibration']} > {VIBRATION_THRESHOLD})"
        alerts.append(alert)
        logger.warning(alert)

    return alerts