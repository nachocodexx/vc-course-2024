import time as T
from mictlanx.v3.services.summoner import Summoner,SummonContainerPayload
from mictlanx.v3.interfaces.payloads import ExposedPort
from option import Some,NONE


if __name__ == "__main__":

    summoner = Summoner(
        ip_addr="localhost",
        port=15000
    )
    payload = SummonContainerPayload(
        container_id="consumer-0",
        image="consumer",
        hostname="consumer-0",
        exposed_ports=[
            ExposedPort(host_port=10121,container_port=10121, ip_addr=NONE, protocolo=NONE)
        ],
        envs={
            "CONFIG_PATH":"/app/config/config.yml"
        },
        memory=1000000000,
        cpu_count=1,
        mounts={
            "/source/configs/config-docker_consumer.yml":"/app/config/config.yml",
            "/sink/consumer-0":"/sink"
        },
        network_id="mictlanx",
        selected_node=NONE,
        labels={
            "mictlanx":""
        },
        force=Some(True),
        ip_addr=NONE,
    )

    result = summoner.summon(
        payload=payload
    )
    print("DEPLOYED CONSUMER",result)
    T.sleep(10)
    payload = SummonContainerPayload(
        container_id="encrypt-0",
        image="encrypt",
        hostname="encrypt-0",
        exposed_ports=[
            ExposedPort(host_port=10122,container_port=10122, ip_addr=NONE, protocolo=NONE)
        ],
        envs={
            "XOLO_SECRET_KEY":"ed448c7a5449e9603058ce630e26c9e3befb2b15e3692411c001e0b4256852d2",
            "CONFIG_PATH":"/app/config/config.yml"
        },
        memory=1000000000,
        cpu_count=1,
        mounts={
            "/source/configs/config-docker_encrypt.yml":"/app/config/config.yml",
            "/sink/encrypt-0":"/sink",
            "/sink/consumer-0":"/source"
        },
        network_id="mictlanx",
        selected_node=NONE,
        labels={
            "mictlanx":""
        },
        force=Some(True),
        ip_addr=NONE,
    )

    result = summoner.summon(
        payload=payload
    )
    
    print("DEPLOYED ENCRYPT",result)
    T.sleep(10)
    payload = SummonContainerPayload(
        container_id="producer-0",
        image="producer",
        hostname="producer-0",
        exposed_ports=[
            ExposedPort(host_port=10123,container_port=10123, ip_addr=NONE, protocolo=NONE)
        ],
        envs={
            "CONFIG_PATH":"/app/config/config.yml"
        },
        memory=1000000000,
        cpu_count=1,
        mounts={
            "/source/configs/config-docker_producer.yml":"/app/config/config.yml",
            "/sink/encrypt-0":"/source"
        },
        network_id="mictlanx",
        selected_node=NONE,
        labels={
            "mictlanx":""
        },
        force=Some(True),
        ip_addr=NONE,
    )
    result = summoner.summon(payload=payload)
    print("PRODUCER",result)