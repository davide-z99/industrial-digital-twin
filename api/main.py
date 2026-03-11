"""FastAPI server for Industrial Digital Twin."""

import logging
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from twin.state import MachineState

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Instance of FastAPI
app = FastAPI(
    title="Industrial Digital Twin API",
    description="API REST for industrial machine monitoring",
    version="1.0.0"
)

# Instance of the machine state (shared with the Twin Service)
twin = MachineState()


# ============================================================================
# Pydantic Models
# ============================================================================

class MachineStateResponse(BaseModel):
    """Response model for the machine state.
    
    Attributes:
        rpm: Rotations per minute
        temperature: Temperature in degrees Celsius
        vibration: Vibration level (0-1)
        status: Operative status
        last_updated: Timestamp of the last update
    """
    rpm: Optional[float] = Field(None, description="RPM of the machine")
    temperature: Optional[float] = Field(None, description="Temperature in °C")
    vibration: Optional[float] = Field(None, description="Vibration level")
    status: str = Field("UNKNOWN", description="Operative status")
    last_updated: Optional[datetime] = Field(None, description="Timestamp of the last update")

    class Config:
        """Configuration of the model."""
        json_schema_extra = {
            "example": {
                "rpm": 1000,
                "temperature": 75.5,
                "vibration": 0.45,
                "status": "RUN",
                "last_updated": "2026-03-06T10:30:00"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field("ok", description="Status of the service")
    message: str = Field("Service is running", description="Status message")


# ============================================================================
# Endpoints
# ============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Verify that the service is available"
)
def health_check() -> HealthResponse:
    """Endpoint to verify the health of the service."""
    logger.info("Health check requested")
    return HealthResponse(status="ok", message="Service is running")


@app.get(
    "/machine",
    response_model=MachineStateResponse,
    tags=["Machine"],
    summary="Get Machine State",
    description="Returns the current state of the machine"
)
def get_machine_state() -> MachineStateResponse:
    """Returns the current state of the industrial machine.
    
    Returns:
        MachineStateResponse: The current state of the machine
        
    Raises:
        HTTPException: If the state has never been updated
    """
    if twin.last_updated is None:
        logger.warning("Machine state requested but no data received yet")
        raise HTTPException(
            status_code=503,
            detail="No machine data available yet. Waiting for telemetry..."
        )
    
    logger.debug(f"Machine state requested: {twin.__dict__}")
    return MachineStateResponse(
        rpm=twin.rpm,
        temperature=twin.temperature,
        vibration=twin.vibration,
        status=twin.status,
        last_updated=twin.last_updated
    )


@app.get(
    "/machine/rpm",
    response_model=dict,
    tags=["Machine"],
    summary="Get RPM",
    description="Returns only the current speed of the machine"
)
def get_rpm() -> dict:
    """Returns the current speed of the machine."""
    if twin.rpm is None:
        raise HTTPException(
            status_code=503,
            detail="No RPM data available yet"
        )
    return {"rpm": twin.rpm}


@app.get(
    "/machine/temperature",
    response_model=dict,
    tags=["Machine"],
    summary="Get Temperature",
    description="Returns only the current temperature of the machine"
)
def get_temperature() -> dict:
    """Returns the current temperature of the machine."""
    if twin.temperature is None:
        raise HTTPException(
            status_code=503,
            detail="No temperature data available yet"
        )
    return {"temperature": twin.temperature}


@app.get(
    "/machine/vibration",
    response_model=dict,
    tags=["Machine"],
    summary="Get Vibration",
    description="Returns only the current vibration level of the machine"
)
def get_vibration() -> dict:
    """Returns the current vibration level of the machine."""
    if twin.vibration is None:
        raise HTTPException(
            status_code=503,
            detail="No vibration data available yet"
        )
    return {"vibration": twin.vibration}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )