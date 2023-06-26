from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Type

from src.host import Packet, PacketPriority


class Queue(ABC):
    @abstractmethod
    def __init__(self, length_limit: int):
        pass

    @abstractmethod
    def push(self, packet: Packet):
        pass

    @abstractmethod
    def pop(self) -> Optional[Packet]:
        pass


class FIFOQueue(Queue):
    def __init__(self, length_limit):
        self.length_limit = length_limit
        self.packets: List[Packet] = []

    def push(self, packet: Packet):
        if self.__get_length() < self.length_limit:
            self.__push_packet(packet)

    def pop(self) -> Optional[Packet]:
        if self.__get_length() > 0:
            return self.packets.pop(0)

    def __push_packet(self, packet: Packet):
        self.packets.append(packet)

    def __get_length(self) -> int:
        return len(self.packets)


class PriorityQueue(FIFOQueue):
    def __push_packet(self, packet: Packet):
        insert_index = len(self.packets)
        while insert_index > 0 and self.packets[insert_index - 1].priority < packet.priority:
            insert_index -= 1
        self.packets.insert(insert_index, packet)


class WRRQueue(Queue):
    def __init__(self, length_limit):
        self.queues = [FIFOQueue(length_limit=length_limit) for _ in range(len(PacketPriority))]
        self.priorities = self.get_priorities(PacketPriority)
        self.turn = 0
        self.sent_packet = 0

    def get_priorities(self, packet_priority: Type[Enum]) -> List[Enum]:
        priorities = [priority for priority in packet_priority]
        priorities.sort(key=lambda e: e.value)
        return priorities

    def push(self, packet: Packet):
        self.queues[self.priorities.index(packet.priority)].push(packet)

    def pop(self) -> Optional[Packet]:
        if self.sent_packet >= self.priorities[self.turn].value:
            self.turn = (self.turn + 1) % len(self.priorities)
            self.sent_packet = 0
        popped_packet = self.queues[self.turn].pop()
        if popped_packet:
            self.sent_packet += 1
        return popped_packet


service_policy_dict = {
    "FIFO": FIFOQueue,
    "WRR": WRRQueue,
    "NPPS": PriorityQueue
}

