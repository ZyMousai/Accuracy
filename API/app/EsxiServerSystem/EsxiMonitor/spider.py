import requests
import paramiko
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from config import globals_config
import os
import datetime

requests.packages.urllib3.disable_warnings()


class EsxiSpider(object):

    def __init__(self, hostname):
        self.hostname = hostname
        self.username = "dingzj"
        self.pwd = "Ff!4242587"
        self.__thread_num = 20

    def get_esxi_cookie(self):
        body = f'<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Body><Login xmlns="urn:vim25"><_this type="SessionManager">ha-sessionmgr</_this><userName>{self.username}</userName><password>{self.pwd}</password><locale>zh-CN</locale></Login></Body></Envelope>'
        url = f"https://{self.hostname}/sdk/"
        r = requests.post(url, data=body, verify=False)
        cookie = "vmware_client=VMware;" + r.headers["Set-Cookie"]
        return cookie

    def get_esxi_machine(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=22, username=self.username, password=self.pwd)
        cmd_shutdown = "vim-cmd vmsvc/getallvms"
        stdin, stdout, stderr = ssh.exec_command(cmd_shutdown)
        cmd_result = stdout.read()
        ssh.close()
        a = str(cmd_result.decode("utf-8")).split("\n")[2:-1]
        machine_code = []
        for i in a:
            line_split = i.split("     ")
            if line_split:
                machine_code.append({
                    "vmid": line_split[0],
                    "name": line_split[1],
                })
        return machine_code

    def spider_esxi_monitor_img(self):
        cookie = self.get_esxi_cookie()
        machine_code_list = self.get_esxi_machine()

        executor = ThreadPoolExecutor(max_workers=self.__thread_num)

        print(datetime.datetime.now())
        sub_list = []
        for machine_code in machine_code_list:
            img_url = "https://{}/screen?id={}".format(self.hostname, machine_code["vmid"])

            args = [img_url, cookie, machine_code["name"]]
            sub = executor.submit(lambda p: self.spider_img(*p), args)
            sub_list.append(sub)
        futures.wait(sub_list)
        print(datetime.datetime.now())

        # result = [data for machine_code_list in executor.map(self.spider_img, img_url, cookie, )]

    def spider_img(self, img_url, cookie, name):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": cookie
        }
        req = requests.get(img_url, headers=headers, verify=False)
        esxiimg_file = os.path.join(globals_config.basedir, 'app/EsxiServerSystem/EsxiImg')
        with(open("{}/auto_{}.jpg".format(esxiimg_file, str(name).lstrip()), 'wb')) as f:
            f.write(req.content)


if __name__ == '__main__':
    es = EsxiSpider("173.208.146.242")
    es.spider_esxi_monitor_img()
