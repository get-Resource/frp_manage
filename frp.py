import os
import json
import yaml
import configparser
import threading
from threading import Thread
import shutil
import subprocess
import time
import hashlib
import setproctitle
setproctitle.setproctitle("FRP_Manage")
def getConfigJson(configName):
    with open(configName, 'rb') as file:
        jsonStr = yaml.safe_load(file)
    return jsonStr

def writeini(appconfigdir,data):
    print(data)
    configini = configparser.ConfigParser() # 类实例化
    for section in data:
        configini.add_section(section) # 首先添加一个新的section
        for key in data[section]:
            configini.set(section,key,str(data[section][key]))  # 写入数据
        configini.write(open(appconfigdir,'w'))            #保存数据

class myThread(threading.Thread):
    def __init__(self, *args, **parameter):
        self.args = parameter.pop("args")
        threading.Thread.__init__(self,*args,**parameter)
        # super(Thread,self).__init__(*args,**parameter)
        self.signal = True
        self.state = False

    def run(self):
        cwd, cmd, f = self.args
        self.state = True
        while True:
            try:
                res = subprocess.Popen(cmd, shell=True, stdout=f,
                                    stderr=subprocess.STDOUT, cwd=cwd)
                print(f)
                while True:
                    if self.signal:
                        time.sleep(2)
                    else:
                        os.system("kill -9 %s" % res.pid)
                        res.kill()
                        res.wait()
                        break
                break
            except Exception as e:
                print(e)
        self.state = False

    def getpid(self):
        return os.getpid()

def to_hex(data,hash_type = "md5"):
    hash_val = hashlib.md5()
    if "sha1" == hash_type:
        hash_val = hashlib.sha1()
    if "sha224" == hash_type:
        hash_val = hashlib.sha224()
    if "sha256" == hash_type:
        hash_val = hashlib.sha256()
    if "sha384" == hash_type:
        hash_val = hashlib.sha384()
    if "sha512" == hash_type:
        hash_val = hashlib.sha512()
    hash_val.update(data.encode())
    res = hash_val.hexdigest()
    return res


basedir = os.path.dirname(os.path.abspath(__file__))
appsdir = os.path.join(basedir,"frp_apps")
config = getConfigJson(os.path.join(basedir,"frp_config.yaml"))
os.makedirs(appsdir,exist_ok=True)

if __name__ == "__main__":
    apptype = config["name"]
    old_execute = os.path.join(basedir,apptype)
    threaded_list = []
    for appname in config[apptype]:
        appconfig = config[apptype][appname]
        appdir = os.path.join(appsdir,apptype)
        os.makedirs(appdir,exist_ok=True)

        appconfigdir = os.path.join(appdir,f"{appname}.ini")
        mddir = os.path.join(appdir,f"{appname}.md")

        writeini(appconfigdir,appconfig)
        if os.path.exists(mddir):
            old_md5 = open(mddir,"r").read(102400)
        else:
            old_md5 = "None"
        if os.path.exists(appconfigdir):
            current_md5 = to_hex(open(appconfigdir,"r").read(102400))
        else:
            current_md5 = to_hex("")
        open(mddir,"w").write(current_md5)
        app_command = f"chmod +x {old_execute};{old_execute} -c {appconfigdir}"
        applogdir = os.path.join(appdir,f"{appname}.log")
        outfile = open(applogdir,"w+")
        args = (appdir, app_command, outfile)
        apprunname = f"{apptype}_{appname}"
        job_thread = myThread(args=args,name=f"{apptype}_{appname}")
        runenumerate = threading.enumerate()
        apprunnames = [th.name for th in runenumerate]
        if apprunname not in apprunnames or current_md5 != old_md5:
            try:
                tid = apprunnames.index(apprunname)
                runenumerate[tid].signal = False
                pid = runenumerate[tid].getpid()
                while runenumerate[tid].state:
                    time.sleep(2)
            except:
                pass
            job_thread.setDaemon(True)
            job_thread.start()
        threaded_list.append(job_thread)
    # for th in threading.enumerate():
    #     print(th.name)
    for th in threaded_list:
        print(th.join())
    
