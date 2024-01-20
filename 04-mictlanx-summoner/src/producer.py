import os
import sys
import time as T
from mictlanx.logger.log import Log
from mictlanx.utils.index import Utils
from mictlanx.v4.client import Client
from mictlanx.v4.xolo.api.index import XoloAPI
from option import Option,Some,NONE
from yaml import load
from pathlib import Path
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class Config(object):
    def __init__(self,
                 client_id:str,
                 password:str,
                 bucket_id:str,
                 source_path:str,
                 mictlanx_peers:str,
                 mictlanx_protocol:str="http",
                 xolo_api_protocol:str ="http",
                 xolo_api_hostname:str  = "localhost",
                 xolo_api_port:int      = 10001,
                 xolo_api_version:int   = 4,
                 log_path:str ="/log"
    ):
        self.client_id                     = client_id
        self.password                      = password
        self.bucket_id                     = bucket_id
        self.source_path                     = source_path
        self.mictlanx_peers                = mictlanx_peers
        self.mictlanx_protocol             = mictlanx_protocol
        self.xolo_api_protocol             = xolo_api_protocol
        self.xolo_api_hostname             = xolo_api_hostname
        self.xolo_api_port:Option[int]     = NONE if xolo_api_port == -1  else Some(xolo_api_port)
        self.xolo_api_version              = xolo_api_version
        self.log_path                      =log_path

if __name__ =="__main__":
    try:
        config_path = os.environ.get("CONFIG_PATH","/home/nacho/Programming/Docker/course_2024/03-xolo_QR_consume/config/dev.yml")
        with open(config_path) as f:
            config = Config(**load(f, Loader=Loader))

        log            = Log(
            name = config.client_id,
            console_handler_filter=lambda x: True,
            interval=24,
            when="h",
            path=config.log_path
        )
        xolo_api = XoloAPI(
            protocol = config.xolo_api_protocol,
            hostname = config.xolo_api_hostname,
            port     = config.xolo_api_port,
            version  = config.xolo_api_version
        )

        auth_result = xolo_api.auth(
            username = config.client_id.strip(),
            password = config.password.strip()
        )

        if auth_result.is_err:
            reason ="Unauthorized: Incorrect username or password. For further assistance, please contact me at jesus.castillo.b@cinvestav.mx."
            log.error({
                "msg":reason,
                "raw_error":str(auth_result.unwrap_err())
            })
            raise Exception(reason)
        
        authenticated_response = auth_result.unwrap()
        role = authenticated_response.role
        can_read = xolo_api.check(role=role,resource=config.bucket_id, permission="write")
        if not can_read:
            msg = "Xolo: Access Denied: you don't have permission to write to {}".format(config.bucket_id)
            log.error({
                "msg":msg,
            })
            raise Exception(msg)

        peers = list(Utils.peers_from_str_v2(config.mictlanx_peers,protocol=config.mictlanx_protocol))
        client              = Client(
            client_id       = os.environ.get("MICTLANX_CLIENT_ID",config.client_id),
            peers           = peers ,
            daemon          = bool(int(os.environ.get("MICTLANX_DAEMON","1"))),
            debug           = bool(int(os.environ.get("MICTLANX_DEBUG","0"))),
            show_metrics    = bool(int(os.environ.get("MICTLANX_SHOW_METRICS","0"))),
            disable_log     = bool(int(os.environ.get("MICTLANX_DISABLE_LOG","1"))),
            max_workers     = int(os.environ.get("MICTLANX_MAX_WORKERS","4")),
            bucket_id       = config.bucket_id,
            check_peers_availavility_interval=os.environ.get("MICTLANX_CHECK_PEER_AVAILABILITY_INTERVAL","15m"),
            heartbeat_interval=os.environ.get("MICTLANX_HEARTBEAT_INTERVAL","10s"),
            lb_algorithm=os.environ.get("MICTLANX_LB_ALGORITHM","2CHOICES_UF"),
            log_interval= int(os.environ.get("MICTLANX_LOG_INTERVAL","24")),
            log_when=os.environ.get("MICTLANX_LOG_WHEN","h"),
            metrics_buffer_size= int(os.environ.get("MICTLANX_METRICS_BUFFER_SIZE","100")),
            output_path=os.environ.get("MICTLANX_OUTPUT_PATH","/mictlanx/client")
        )
        for (root_path,_,fullnames) in os.walk(config.source_path):
            for fullname in fullnames:
                start_time = T.time()
                path = Path(root_path,fullname)
                result = client.put_file(path=str(path),bucket_id=config.bucket_id,update=True, source_folder=config.source_path,tags={
                    "algorithm":"AES",
                    "security_level":"256",
                })
                if result.is_err:
                    log.error({
                        "msg":str(result.unwrap_err())
                    })
                else:
                    response = result.unwrap()
                    log.debug({
                        "event":"PUT.SUCCESSFULLY",
                        "key":response.key,
                        "node_id":response.node_id,
                        "response_time":response.response_time
                    })
        

        # start_time = T.time()
        # gen = client.get_all_bucket_data(bucket_id=config.bucket_id,output_folder=config.sink_path,bucket_folder_as_root=True)
        # xs = list(gen)
        # if len(xs)==0:
        #     log.debug({
        #         "event":"HIT.ALL.DATA",
        #         "bucket_id":config.bucket_id
        #     })
        #     sys.exit(0)
        # for x in xs:
        #     log.debug({
        #         "event":"GET.SUCCESSFULLY",
        #         "path":config.sink_path,
        #         "key":x.key,
        #         "response_time": T.time() -start_time
        #     })

    except Exception as e:
        print(e)
        sys.exit(1)