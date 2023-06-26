# X: poisson parameter for sender host
# Y: exponential parameter for router
# T: simulation time

from src.host import Host
from src.queue import service_policy_dict
from src.router import Router


def main():
    X, Y, T = 3, 1/4, 20
    PROCESSORS_NUM = 3
    SERVICE_POLICY = "FIFO"
    LENGTH_LIMIT = 10
    queue = service_policy_dict[SERVICE_POLICY](length_limit=LENGTH_LIMIT)
    host = Host(poisson_parameter=X)
    packets = host.generate_packets(simulation_time=T)
    router = Router(packet_list=packets, processors_num=PROCESSORS_NUM, core_exponential_parameter=Y,
                    queue=queue)
    router.simulate(simulation_time=T)


if __name__ == '__main__':
    main()
