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
import platform
setproctitle.setproctitle("FRP_Manage")
plat = platform.system().lower()
basedir = os.path.dirname(os.path.abspath(__file__))
appsdir = os.path.join(basedir,"frp_apps")
current_run_json = os.path.join(basedir,"current_run.json")

def getConfigJson(configName):
    with open(configName, 'rb') as file:
        jsonStr = yaml.safe_load(file)
    return jsonStr

config = getConfigJson(os.path.join(basedir,"frp_manage_config.yaml"))
os.makedirs(appsdir,exist_ok=True)


    
def write_config(appconfigdir,data):
    configini = configparser.ConfigParser() # 类实例化
    for section in data:
        configini.add_section(section) # 首先添加一个新的section
        for key in data[section]:
            configini.set(section,key,str(data[section][key]))  # 写入数据
        configini.write(open(appconfigdir,'w'))            #保存数据


def get_current_run():
    try:
        file = open(current_run_json, 'r')
        jsonStr =  json.loads(file.read(10240))
        
    except Exception as e:
        jsonStr = {}
    return jsonStr
current_run = get_current_run()


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
        # while True:
        try:
            print(cwd,f)
            res = subprocess.Popen(cmd, shell=True, stdout=f,
                                stderr=subprocess.STDOUT, cwd=cwd, executable='bash')
            self.res = res
            while subprocess.Popen.poll(res) != 0:
                if self.signal:
                    time.sleep(2)
                else:
                    os.system("kill -9 %s" % res.pid)
                    res.kill()
                    res.wait()
                    break
            # break
        except Exception as e:
            print(e)
        self.state = False

    def getpid(self):
        return self.res.pid

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



if __name__ == "__main__":
    apptype = config["name"]
    old_execute = os.path.join(basedir,apptype)
    threaded_list = []
    import psutil

    for appname in config[apptype]:
        # 初始化相关路径
        appconfig = config[apptype][appname]
        appdir = os.path.join(appsdir,apptype)
        os.makedirs(appdir,exist_ok=True)
        appconfigdir = os.path.join(appdir,f"{appname}.ini")
        # 更新保存配置
        write_config(appconfigdir,appconfig)
        if os.path.exists(appconfigdir):
            current_md5 = to_hex(open(appconfigdir,"r").read(102400))
        else:
            current_md5 = to_hex(time.strftime("%Y-%m-%d-%H_%M_%S%f", time.localtime(time.time())))

        run_md5 = to_hex(time.strftime("%Y-%m-%d-%H_%M_%S%f", time.localtime(time.time())))
        pid = None
        run_pid = None
        if appname in current_run:
            run_data = current_run[appname]
            pid = run_data["pid"]
            if run_data["type"] == apptype and run_data["config"] == appconfigdir:
                # 相同的app正在运行
                run_md5 = run_data["md5"]
        process = os.popen('ps aux|grep %s|grep -v grep'% appconfigdir)
        # 读取进程信息，获取字符串
        process_info_list = []
        process_info = process.read()
        if process_info:
            # 按空格切割split(" ")，
            for i in process_info.split(' '):
                # 判断不为空，添加到process_info_list中
                if i != "":
                    process_info_list.append(i)
            # 列表第0位是字符串类型pid，转换成int类型，方便执行stop_process()
            run_pid = int(process_info_list[1])
        if run_md5 != current_md5 or run_pid is None:
            app_command = f"{old_execute} -c {appconfigdir}"
            applogdir = os.path.join(appdir,f"{appname}.log")
            outfile = open(applogdir,"w+")

            args = (appdir, app_command, outfile)
            apprunname = f"{apptype}_{appname}"
            job_thread = myThread(args=args,name=f"{apptype}_{appname}")
            # runenumerate = threading.enumerate()
            # apprunnames = [th.name for th in runenumerate]
            try:
                if run_pid is not None:
                    if plat == 'windows':
                        os.system('taskill /f /pid %s'%pid)
                    elif plat == 'linux':
                        os.kill(pid, -9)
            except:
                pass
            job_thread.setDaemon(True)
            job_thread.start()
            time.sleep(2)
            current_run[appname] = {
                "type": apptype,
                "pid": job_thread.getpid(),
                "config": appconfigdir,
                "md5": current_md5,
            }
            threaded_list.append(job_thread)
            with open(current_run_json, 'w') as file_obj:
                json.dump(current_run, file_obj, ensure_ascii = False, indent = 4)
    # for th in threading.enumerate():
    #     print(th.name)
    for th in threaded_list:
        print(th.join())
    else:
        print("配置无变化，进程自动退出，运行情况：\n",json.dumps(current_run, ensure_ascii = False, indent = 4))

