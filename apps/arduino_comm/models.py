from dataclasses import dataclass, field
from bson.objectid import ObjectId

@dataclass
class Sensor:
    """Representation of a Sensor document in MongoDB."""
    id: str = field(default_factory=lambda: str(ObjectId()))  # Use MongoDB ObjectId as string
    name: str = ""
    type: str = "input"  # "input" or "output"
    mode: str = "digital"  # "digital" or "analog"
    status: str = "off"  # "on" or "off"
    value: int = 0
    active: bool = False

