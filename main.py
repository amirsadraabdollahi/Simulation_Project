# X: poisson parameter for sender host
# Y: exponential parameter for router
# T: simulation time

from src.host import Host, PacketPriority
from src.queue import service_policy_dict
from src.router import Router
from src.statistics import average_length_of_all_queue, average_time_in_all_queue, average_time_in_queue, \
    average_utilization_of_core, count_of_dropped_packets, accumulate_high_priority_packet_diagram, \
    count_of_sent_packets


def main():
    X, Y, T = 6, 1 / 2, 20
    PROCESSORS_NUM = 2
    LENGTH_LIMIT = 10
    SERVICE_POLICY = "NPPS"
    queue = service_policy_dict[SERVICE_POLICY](length_limit=LENGTH_LIMIT)
    host = Host(poisson_parameter=X)
    packets = host.generate_packets(simulation_time=T)
    router = Router(packet_list=packets.copy(), processors_num=PROCESSORS_NUM, core_exponential_parameter=Y,
                    queue=queue)
    router.simulate(simulation_time=T)

    print(f'average queue length: {average_length_of_all_queue(packets, T, SERVICE_POLICY)}')
    print(f'average time in all queues: {average_time_in_all_queue(packets, T)}')
    if SERVICE_POLICY == 'WRR':
        for e in PacketPriority:
            print(f'average time in queue {e.name}: {average_time_in_queue(packets, T, e)}')

    cores = router.get_cores()
    for core in cores:
        print(f'average utilization of {core}: {average_utilization_of_core(packets, core, T)}')
    print(f'count of dropped packets: {count_of_dropped_packets(packets)}')
    print(f'count of sent packets: {count_of_sent_packets(packets)}')
    accumulate_high_priority_packet_diagram(packets, SERVICE_POLICY, T)


if __name__ == '__main__':
    main()
