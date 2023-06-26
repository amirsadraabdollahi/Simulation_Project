from abc import ABC, abstractmethod
from typing import List, Optional

from src.host import Packet, Priority


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


class Queue(ABC):
    def __init__(self, length_limit: int):
        self.length_limit = length_limit
        self.packets: List[Packet] = []

    def get_length(self) -> int:
        return len(self.packets)

    def push(self, packet: Packet):
        if self.get_length() < self.length_limit:
            self.__push_packet(packet)

    @abstractmethod
    def __push_packet(self, packet: Packet):
        pass

    def pop(self) -> Optional[Packet]:
        if self.get_length() > 0:
            return self.packets.pop(0)


class FIFOQueue(Queue):
    def __push_packet(self, packet: Packet):
        self.packets.append(packet)


class PriorityQueue(Queue):
    def __push_packet(self, packet: Packet):
        insert_index = len(self.packets)
        while insert_index > 0 and self.packets[insert_index - 1].priority < packet.priority:
            insert_index -= 1
        self.packets.insert(insert_index, packet)


class Router(ABC):
    def __init__(self, packet_list: List[Packet], processors_num: int, core_poisson_parameter: float,
                 length_limit: int):
        self.packets = packet_list
        self.cores = [Core(core_poisson_parameter) for _ in range(processors_num)]
        self.queue = self.generate_queues(length_limit)

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

    @abstractmethod
    def generate_queues(self, length_limit):
        pass

    def insert_packet(self, packet: Packet):
        self.queue.push(packet)

    def get_packet_from_queue(self) -> Optional[Packet]:
        return self.queue.pop()


class FIFORouter(Router):
    def generate_queues(self, length_limit):
        return FIFOQueue(length_limit=length_limit)


class NPPSRouter(Router):
    def generate_queues(self, length_limit):
        return PriorityQueue(length_limit=length_limit)

