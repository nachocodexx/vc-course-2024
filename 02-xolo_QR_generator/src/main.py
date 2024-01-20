import sys
import os
import time as T
from pathlib import Path
from yaml import load
from mictlanx.logger.log import Log
from mictlanx.utils.index import Utils
from mictlanx.v4.client import Client
from mictlanx.v4.xolo.api.index import XoloAPI
from option import Some,NONE,Option
import qrcode
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
                 sink_path:str,
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
        self.source_path                   = source_path
        self.sink_path                     = sink_path
        self.mictlanx_peers                = mictlanx_peers
        self.mictlanx_protocol             = mictlanx_protocol
        self.xolo_api_protocol             = xolo_api_protocol
        self.xolo_api_hostname             = xolo_api_hostname
        self.xolo_api_port:Option[int]     = NONE if xolo_api_port == -1  else Some(xolo_api_port)
        self.xolo_api_version              = xolo_api_version
        self.log_path                      =log_path

if __name__ =="__main__":
    try:
        config_path = os.environ.get("CONFIG_PATH","/home/nacho/Programming/Docker/course_2024/02-xolo_QR_sharing/config/dev.yml")
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
            raise Exception(reason)
        
        authenticated_response = auth_result.unwrap()
        role = authenticated_response.role
        can_write = xolo_api.check(role=role,resource=config.bucket_id, permission="write")
        if not can_write:
            msg = "Xolo: Access Denied: you don't have permission to write to {}".format(config.bucket_id)
            log.error({
                "msg":msg
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
                # bucket_relative_path = str(path.relative_to(config.source_path))
                result = client.put_file(path=str(path),bucket_id=config.bucket_id,update=True,source_folder=config.source_path)
                if result.is_err:
                    log.error({
                        "msg":str(result.unwrap_err())
                    })
                else:
                    log.debug({
                        "event":"PUT_SUCCESSFULLY",
                        "resonse_time":T.time() - start_time
                    })
                    response = result.unwrap()
                    with open(path,"rb") as f:
                        start_time = T.time()
                        data = f.read()
                        selected_peer = peers[0].base_url()
                        url = "{}/api/v4/buckets/{}/{}".format(selected_peer,config.bucket_id,response.key)
                        img = qrcode.make(url)
                        # print(type(img))
                        qr_path = "{}/{}".format(config.sink_path,"qr_{}.png".format(response.key))
                        log.debug({
                            "event":"QR.GENERATED",
                            "output_path":qr_path,
                            "service_time":T.time()- start_time
                        })
                        img.save(qr_path)
    except Exception as e:
        print(e)
        sys.exit(1)