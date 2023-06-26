from enum import Enum
from typing import Optional, List

import numpy as np


class PriorityProbability(Enum):
    HIGH = 0.2
    MEDIUM = 0.3
    LOW = 0.5


class Packet:

    def __init__(self, entry_time: float):
        self.entry_time: float = entry_time
        self.execution_start_time: Optional[float] = None
        self.service_time: Optional[float] = None
        self.served_time: Optional[float] = None
        self.execution_end_time: Optional[float] = None


class Host:
    def __init__(self, poisson_parameter):
        self.poisson_parameter = poisson_parameter

    def generate_packets(self, simulation_time: int) -> List[Packet]:
        packets = []
        time = 0
        while time <= simulation_time:
            packets.append(Packet(entry_time=time))
            time += np.random.exponential(self.poisson_parameter, 1)
        return packets
