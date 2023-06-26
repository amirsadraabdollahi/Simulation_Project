# X: poisson parameter for sender host
# Y: exponential parameter for router
# T: simulation time
from src.host import Host
from src.queue import service_policy_dict
from src.router import Router


def main():
    X, Y, T = float(input("X:")), float(input("Y:")), float(input("T:"))
    PROCESSORS_NUM = 5
    SERVICE_POLICY = "WRR"
    LENGTH_LIMIT = 100
    queue = service_policy_dict[SERVICE_POLICY](length_limit=LENGTH_LIMIT)
    host = Host(poisson_parameter=X)
    packets = host.generate_packets(simulation_time=T)
    router = Router(packet_list=packets, processors_num=PROCESSORS_NUM, core_poisson_parameter=Y,
                    queue=queue)
    router.simulate(simulation_time=T)


if __name__ == '__main__':
    main()
