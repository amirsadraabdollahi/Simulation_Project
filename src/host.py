from enum import Enum
from typing import Optional, List

import numpy as np


class Priority(Enum):
    HIGH = 5
    MEDIUM = 10 / 3
    LOW = 2


class Packet:

    def __init__(self, entry_time: float, priority: Priority):
        self.entry_time: float = entry_time
        self.execution_start_time: Optional[float] = None
        self.service_time: Optional[float] = None
        self.execution_end_time: Optional[float] = None
        self.priority = priority

    def get_entry_time(self):
        return self.entry_time


class Host:
    def __init__(self, poisson_parameter):
        self.poisson_parameter = poisson_parameter

    def generate_packets(self, simulation_time: int) -> List[Packet]:
        packets = []
        time = 0
        while time <= simulation_time:
            sample_priority = Priority.HIGH
            packets.append(Packet(entry_time=time, priority=sample_priority))
            time += np.random.exponential(self.poisson_parameter, 1)
        return packets
