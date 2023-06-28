from typing import List

import matplotlib.pyplot as plt

from src.host import Packet, PacketPriority
from src.router import Core


def average_queue_length(packets: List[Packet], simulation_time: float) -> float:
    result: float = 0
    change_times = []
    for packet in packets:
        if packet.dropped:
            continue
        elif not packet.service_time:
            change_times.append(packet.entry_time)
        else:
            change_times.append(packet.entry_time)
            change_times.append(packet.execution_start_time)
    change_times.append(simulation_time)
    change_times.sort()
    for i in range(0, len(change_times) - 1):
        count = 0
        for packet in packets:
            if packet.dropped:
                continue
            elif not packet.service_time and change_times[i] >= packet.entry_time:
                count += 1
            elif change_times[i] >= packet.entry_time and change_times[i + 1] < packet.execution_start_time:
                count += 1
        result += count * (change_times[i + 1] - change_times[i])
    return result / simulation_time


def average_length_of_all_queue(packets: List[Packet], simulation_time: float, policy) -> float:
    if policy == 'WRR':
        result = 0
        for e in PacketPriority:
            packets_e = []
            for packet in packets:
                if packet.priority.name == e.name:
                    packets_e.append(packet)
            result += average_queue_length(packets, simulation_time)
        return result / (len(PacketPriority))
    else:
        return average_queue_length(packets, simulation_time)


def average_time_in_all_queue(packets: List[Packet], simulation_time: float) -> float:
    total_time_in_queue: float = 0
    total_packets = 0
    for packet in packets:
        if packet.dropped:
            continue
        elif not packet.service_time:
            total_time_in_queue += simulation_time - packet.entry_time
            total_packets += 1
        else:
            total_time_in_queue += packet.execution_start_time - packet.entry_time
            total_packets += 1
    return total_time_in_queue / total_packets


def average_time_in_queue(packets: List[Packet], simulation_time: float, priority_enum) -> float:
    total_time_in_queue: float = 0
    total_packets = 0
    for packet in packets:
        if packet.dropped or not packet.priority.name == priority_enum.name:
            continue
        if not packet.service_time:
            total_time_in_queue += simulation_time - packet.entry_time
            total_packets += 1
        else:
            total_time_in_queue += packet.execution_start_time - packet.entry_time
            total_packets += 1
    return total_time_in_queue / total_packets


def average_utilization_of_core(packets: List[Packet], core: Core, simulation_time: float) -> float:
    time: float = 0
    for packet in packets:
        if packet.dropped:
            continue
        if packet.executed_by == core:
            time += packet.service_time
    return time / simulation_time


def count_of_dropped_packets(packets: List[Packet]):
    count = 0
    for packet in packets:
        if packet.dropped:
            count += 1
    return count


def accumulate_high_priority_packet_diagram(packets: List[Packet], service_policy, simulation_time: float):
    change_times = []
    for packet in packets:
        if packet.dropped or packet.priority.name != 'HIGH':
            continue
        elif not packet.service_time:
            change_times.append(packet.entry_time)
        else:
            change_times.append(packet.entry_time)
            change_times.append(packet.execution_start_time)
    change_times.append(simulation_time)
    change_times.sort()

    accumulate_times = []
    for i in range(0, len(change_times)):
        time_i = 0
        for packet in packets:
            if packet.dropped or packet.priority.name != 'HIGH':
                continue
            if packet.service_time:
                if packet.entry_time <= change_times[i]:
                    time_i += min(change_times[i], packet.execution_start_time) - packet.entry_time
            else:
                if packet.entry_time <= change_times[i]:
                    time_i += min(change_times[i], simulation_time) - packet.entry_time
        accumulate_times.append(time_i)
    # Assuming x and y are your lists
    x = ['%.2f' % elem for elem in change_times]

    plt.plot(x, accumulate_times)
    plt.xlabel('time')
    plt.ylabel('CDF time')
    plt.title(f'Accumulative time in queue for High priority packets in {service_policy}')
    plt.show()


def count_of_sent_packets(packets: List[Packet]):
    count = 0
    for packet in packets:
        if packet.service_time:
            count += 1
    return count
