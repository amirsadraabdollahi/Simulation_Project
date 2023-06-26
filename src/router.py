from typing import List, Optional

from src.host import Packet
from src.queue import Queue


class Core:
    def __init__(self, poisson_parameter: float):
        self.poisson_parameter = poisson_parameter

    def get_release_time(self) -> float:
        return 0

    def release(self):
        pass

    def is_free(self) -> bool:
        return False

    def execute(self, packet):
        pass


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
