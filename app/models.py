from dataclasses import dataclass
from datetime import date
from typing import Optional, List


@dataclass
class User:
    id: int
    name: str
    email: str
    role: str


@dataclass
class ComponentType:
    id: int
    name: str


@dataclass
class Component:
    id: int
    name: str
    component_type_id: int
    active: bool = True


@dataclass
class ComponentPrice:
    component_id: int
    price: float
    effective_from: date
    effective_to: Optional[date] = None


@dataclass
class ConfigurationComponent:
    component_id: int
    quantity: int
    unit_price: float

    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Configuration:
    id: int
    name: str
    created_by: int
    components: List[ConfigurationComponent]
    status: str = "DRAFT"

    def calculate_total(self) -> float:
        return sum(
            item.subtotal()
            for item in self.components
        )