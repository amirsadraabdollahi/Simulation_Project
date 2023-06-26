from enum import Enum
from typing import Optional, List

import numpy as np


class PacketPriority(Enum):
    HIGH = 2
    MEDIUM = 3
    LOW = 5


class Packet:

    def __init__(self, entry_time: float, priority: PacketPriority):
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

    def generate_packets(self, simulation_time: float) -> List[Packet]:
        packets = []
        time = 0
        while time <= simulation_time:
            sample_priority = PacketPriority.HIGH
            packets.append(Packet(entry_time=time, priority=sample_priority))
            time += np.random.exponential(self.poisson_parameter, 1)
        return packets
