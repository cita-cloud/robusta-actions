from robusta.api import *
import os
import requests
import time
import subprocess
import json
from tenacity import retry, stop_after_attempt, wait_fixed


retry_times = 5
retry_wait = 10


@retry(stop=stop_after_attempt(retry_times), wait=wait_fixed(retry_wait))
def exec_retry(cmd):
    result = subprocess.getoutput(cmd)
    if result.__contains__("Error"):
        raise Exception("exec failed: {}".format(cmd))
    return result


class CldiParams(ActionParams):
    admin_sk: str
    rpc_endpoint: str
    call_endpoint: str
    start_hour: int
    end_hour: int
    sleeping_interval: int
    timezone: int


def download_cldi(admin_sk, rpc_endpoint, call_endpoint):
    if not os.path.exists('/usr/bin/cldi'):
        print(f"cldi not found, downloading...")
        r = requests.get("https://github.com/cita-cloud/cloud-cli/releases/download/v0.5.3/cldi-x86_64-unknown-linux-musl.tar.gz", allow_redirects=True)
        open("/tmp/cldi-x86_64-unknown-linux-musl.tar.gz", 'wb').write(r.content)
        os.system(f"tar -xf /tmp/cldi-x86_64-unknown-linux-musl.tar.gz -C /usr/bin")
        subprocess.getoutput("cldi account import {} --name admin --crypto SM".format(admin_sk))
        subprocess.getoutput("cldi -r {} -e {} -u default context save default".format(rpc_endpoint, call_endpoint))
    else:
        print(f"cldi already exists, skipping download.")


def get_block_interval():
    cmd = "cldi -c default get system-config"
    cmd_result = exec_retry(cmd)
    system_config = json.loads(cmd_result)
    return system_config['block_interval']


@action
def check_schedule(event: ScheduledExecutionEvent, params: CldiParams):
    download_cldi(params.admin_sk, params.rpc_endpoint, params.call_endpoint)
    now = time.localtime()
    timezone = params.timezone
    if now.tm_hour + timezone >= params.start_hour and now.tm_hour + timezone < params.end_hour:
        msg = "working..."
        old_block_interval = get_block_interval()
        if not old_block_interval == 3:
            print(f"setting block interval to 3 second...")
            subprocess.getoutput("cldi -c default -u admin admin set-block-interval 3")
    else:
        msg = "sleeping..."
        old_block_interval = get_block_interval()
        if not old_block_interval == params.sleeping_interval:
            print(f"setting block interval to {params.sleeping_interval} second...")
            subprocess.getoutput("cldi -c default -u admin admin set-block-interval {}".format(params.sleeping_interval))
    event.add_enrichment([
        MarkdownBlock(f"Now is {msg}, params={params}"),
    ])
