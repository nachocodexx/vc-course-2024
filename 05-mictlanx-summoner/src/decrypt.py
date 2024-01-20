import os
import sys
import time as T
from mictlanx.logger.log import Log
from mictlanx.v4.xolo.api.index import XoloAPI
from mictlanx.v4.xolo.utils import Utils as XoloUtils
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
                 sink_path:str,
                 mictlanx_peers:str,
                 mictlanx_protocol:str="http",
                 xolo_api_protocol:str ="http",
                 xolo_api_hostname:str  = "localhost",
                 xolo_api_port:int      = 10001,
                 xolo_api_version:int   = 4,
                 log_path:str ="/log",
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
        
        for (root_path,_,fullnames) in os.walk(config.source_path):
            for fullname in fullnames:
                start_time = T.time()
                path = Path(root_path,fullname)
                shared_key                   = bytes.fromhex(os.environ.get("XOLO_SECRET_KEY","ed448c7a5449e9603058ce630e26c9e3befb2b15e3692411c001e0b4256852d2"))
                with open(path,"rb") as f:
                    data = f.read()
                    res = XoloUtils.decrypt_aes(
                        key=shared_key,
                        data=data,
                    )
                    if res.is_err:
                        log.error({
                            "msg":str(res.unwrap_err())
                        })
                    response= res.unwrap()
                    enc_path = Path(config.sink_path,"dec-{}".format(fullname))
                    with open(enc_path,"wb") as f:
                        f.write(response)
                    log.debug({
                        "event":"DISK.WRITE.ENCRYPTED",
                        "path":str(enc_path),
                        "size":len(response),
                    })
    except Exception as e:
        print(e)
        sys.exit(1)