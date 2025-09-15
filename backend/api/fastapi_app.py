# api/fastapi_app.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import json
import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from vehicles.models import Vehicle, VehicleTracking
from alerts.models import Alert
from accounts.models import DriverProfile

# FastAPI app
app = FastAPI(title="Travel Agency Arduino API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for Arduino data
class ArduinoSensorData(BaseModel):
    device_id: str = Field(..., description="Arduino device identifier")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Location data
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    speed: Optional[float] = None  # km/h
    
    # Driver monitoring
    eye_closure_duration: Optional[float] = None  # seconds
    head_position: Optional[str] = None  # "normal", "nodding", "tilted"
    fatigue_level: Optional[int] = None  # 1-10 scale
    
    # Vehicle data
    fuel_level: Optional[float] = None
    engine_temperature: Optional[float] = None
    harsh_braking: Optional[bool] = None
    harsh_acceleration: Optional[bool] = None
    
    # Raw sensor values
    raw_data: Optional[dict] = None

class AlertResponse(BaseModel):
    alert_id: int
    message: str
    severity: str
    timestamp: datetime

class VehicleStatus(BaseModel):
    vehicle_id: str
    status: str
    last_update: datetime
    driver_status: str

# Helper functions
async def get_vehicle_by_device_id(device_id: str) -> Vehicle:
    try:
        vehicle = Vehicle.objects.get(arduino_device_id=device_id)
        return vehicle
    except Vehicle.DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Vehicle with device_id {device_id} not found")

async def process_drowsiness_alert(vehicle: Vehicle, sensor_data: ArduinoSensorData):
    """Process drowsiness detection and create alerts"""
    if sensor_data.eye_closure_duration and sensor_data.eye_closure_duration > 2.0:
        severity = "critical" if sensor_data.eye_closure_duration > 5.0 else "high"
        
        # Get current driver
        try:
            driver = DriverProfile.objects.get(current_vehicle=vehicle)
        except DriverProfile.DoesNotExist:
            return None
        
        # Create alert
        alert = Alert.objects.create(
            vehicle=vehicle,
            driver=driver,
            alert_type='drowsiness',
            severity=severity,
            message=f"Somnolence détectée: fermeture des yeux pendant {sensor_data.eye_closure_duration:.1f} secondes",
            location_latitude=sensor_data.latitude,
            location_longitude=sensor_data.longitude,
            speed_at_time=sensor_data.speed,
            arduino_data=sensor_data.dict()
        )
        
        return alert
    return None

async def process_speed_alert(vehicle: Vehicle, sensor_data: ArduinoSensorData):
    """Process speed violations"""
    if sensor_data.speed and sensor_data.speed > 90:  # Speed limit
        severity = "critical" if sensor_data.speed > 110 else "high"
        
        try:
            driver = DriverProfile.objects.get(current_vehicle=vehicle)
        except DriverProfile.DoesNotExist:
            return None
        
        alert = Alert.objects.create(
            vehicle=vehicle,
            driver=driver,
            alert_type='speeding',
            severity=severity,
            message=f"Excès de vitesse: {sensor_data.speed:.1f} km/h (limite: 90 km/h)",
            location_latitude=sensor_data.latitude,
            location_longitude=sensor_data.longitude,
            speed_at_time=sensor_data.speed,
            arduino_data=sensor_data.dict()
        )
        
        return alert
    return None

# API Endpoints
@app.post("/arduino/data", response_model=dict)
async def receive_arduino_data(
    sensor_data: ArduinoSensorData,
    background_tasks: BackgroundTasks
):
    """Receive and process data from Arduino sensors"""
    
    # Get vehicle
    vehicle = await get_vehicle_by_device_id(sensor_data.device_id)
    
    # Save tracking data
    if sensor_data.latitude and sensor_data.longitude:
        VehicleTracking.objects.create(
            vehicle=vehicle,
            latitude=sensor_data.latitude,
            longitude=sensor_data.longitude,
            speed=sensor_data.speed or 0,
            fuel_level=sensor_data.fuel_level,
            engine_temperature=sensor_data.engine_temperature
        )
    
    # Process alerts in background
    alerts_created = []
    
    # Check for drowsiness
    drowsiness_alert = await process_drowsiness_alert(vehicle, sensor_data)
    if drowsiness_alert:
        alerts_created.append({
            "type": "drowsiness",
            "severity": drowsiness_alert.severity,
            "message": drowsiness_alert.message
        })
    
    # Check for speeding
    speed_alert = await process_speed_alert(vehicle, sensor_data)
    if speed_alert:
        alerts_created.append({
            "type": "speeding",
            "severity": speed_alert.severity,
            "message": speed_alert.message
        })
    
    # Check for harsh events
    if sensor_data.harsh_braking:
        try:
            driver = DriverProfile.objects.get(current_vehicle=vehicle)
            Alert.objects.create(
                vehicle=vehicle,
                driver=driver,
                alert_type='harsh_braking',
                severity='medium',
                message="Somnolence attention détecté",
                location_latitude=sensor_data.latitude,
                location_longitude=sensor_data.longitude,
                speed_at_time=sensor_data.speed,
                arduino_data=sensor_data.dict()
            )
            alerts_created.append({
                "type": "harsh_braking",
                "severity": "medium",
                "message": "Freinage brusque détecté"
            })
        except DriverProfile.DoesNotExist:
            pass
    
    return {
        "status": "success",
        "message": "Data received and processed",
        "vehicle_id": vehicle.registration_number,
        "alerts_created": alerts_created,
        "timestamp": datetime.now()
    }

@app.get("/arduino/vehicle/{device_id}/status", response_model=VehicleStatus)
async def get_vehicle_status(device_id: str):
    """Get current vehicle status"""
    vehicle = await get_vehicle_by_device_id(device_id)
    
    # Get latest tracking data
    latest_tracking = VehicleTracking.objects.filter(vehicle=vehicle).first()
    
    # Get current driver
    try:
        driver = DriverProfile.objects.get(current_vehicle=vehicle)
        driver_status = "active" if driver.is_available else "unavailable"
    except DriverProfile.DoesNotExist:
        driver_status = "no_driver"
    
    return VehicleStatus(
        vehicle_id=vehicle.registration_number,
        status=vehicle.status,
        last_update=latest_tracking.timestamp if latest_tracking else vehicle.created_at,
        driver_status=driver_status
    )

@app.get("/arduino/alerts/recent")
async def get_recent_alerts(limit: int = 10):
    """Get recent alerts for monitoring dashboard"""
    alerts = Alert.objects.select_related('vehicle', 'driver__user').order_by('-timestamp')[:limit]
    
    return [
        {
            "id": alert.id,
            "type": alert.alert_type,
            "severity": alert.severity,
            "message": alert.message,
            "vehicle": alert.vehicle.registration_number,
            "driver": alert.driver.user.get_full_name(),
            "timestamp": alert.timestamp,
            "status": alert.status
        }
        for alert in alerts
    ]

@app.post("/arduino/emergency")
async def emergency_stop(device_id: str):
    """Emergency stop signal for vehicle"""
    vehicle = await get_vehicle_by_device_id(device_id)
    
    try:
        driver = DriverProfile.objects.get(current_vehicle=vehicle)
        Alert.objects.create(
            vehicle=vehicle,
            driver=driver,
            alert_type='emergency',
            severity='critical',
            message="ARRÊT D'URGENCE DÉCLENCHÉ",
            arduino_data={"emergency_stop": True, "timestamp": datetime.now().isoformat()}
        )
    except DriverProfile.DoesNotExist:
        pass
    
    return {
        "status": "success",
        "message": "Emergency stop signal sent",
        "vehicle_id": vehicle.registration_number
    }

@app.get("/")
async def root():
    return {"message": "Travel Agency Arduino API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)