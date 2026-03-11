"""Machine state module for Industrial Digital Twin."""

from datetime import datetime
from typing import Optional, Dict, Any


class MachineState:
    """It represents the current state of the industrial machine.
    
    Attributes:
        rpm: Rotations per minute (RPM)
        temperature: Temperature in degrees Celsius
        vibration: Vibration level (0-1)
        status: Operational status of the machine
        last_updated: Timestamp of the last update
    """

    def __init__(self) -> None:
        """Initialize the machine state with null values."""
        self.rpm: Optional[float] = None
        self.temperature: Optional[float] = None
        self.vibration: Optional[float] = None
        self.status: str = "UNKNOWN"
        self.last_updated: Optional[datetime] = None

    def update(self, data: Dict[str, Any]) -> None:
        """Update the machine state with new data.
        
        Args:
            data: Dictionary containing rpm, temperature, vibration, status
        
        Raises:
            KeyError: If required keys are missing from the dictionary
            TypeError: If the data has an invalid type
        """
        self.rpm = data["rpm"]
        self.temperature = data["temperature"]
        self.vibration = data["vibration"]
        self.status = data["status"]
        self.last_updated = datetime.now()