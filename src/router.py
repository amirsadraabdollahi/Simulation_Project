from typing import List, Optional

import numpy as np

from src.host import Packet
from src.queue import Queue


class Core:
    def __init__(self, poisson_parameter: float):
        self.poisson_parameter = poisson_parameter
        self.packet: Optional[Packet] = None

    def get_release_time(self) -> float:
        return self.packet.execution_end_time

    def release(self):
        self.packet = None

    def is_free(self) -> bool:
        return self.packet is None

    def execute(self, packet):
        self.packet = packet
        self.packet.service_time = np.random.exponential(self.poisson_parameter, 1)


class Router:
    def __init__(self, packet_list: List[Packet], processors_num: int, core_poisson_parameter: float,
                 queue: Queue):
        self.packets = packet_list
        self.cores = [Core(core_poisson_parameter) for _ in range(processors_num)]
        self.queue = queue

    def simulate(self, simulation_time):
        time = 0
        while len(self.packets) != 0 and time <= simulation_time:
            min_time_released_core = self.get_core_release_time()
            packet_entry_time = self.packets[0].get_entry_time()
            if min_time_released_core.get_release_time() <= packet_entry_time:
                time = min_time_released_core.get_release_time()
                min_time_released_core.release()
                execution_packet = self.get_packet_from_queue()
                if execution_packet:
                    execution_packet.execution_start_time = time
                    min_time_released_core.execute(execution_packet)
            else:
                self.insert_packet(self.packets.pop(0))
                time = packet_entry_time

    def get_core_release_time(self) -> Core:
        return min(self.cores, key=lambda core: core.get_release_time())

    def insert_packet(self, packet: Packet):
        self.queue.push(packet)

    def get_packet_from_queue(self) -> Optional[Packet]:
        return self.queue.pop()
