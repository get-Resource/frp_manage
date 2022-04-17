# frp_manage
frp管理脚本


## 安装使用教程

git clone https://github.com/get-Resource/frp_manage.git
wget https://github.com/fatedier/frp/releases/download/v0.41.0/frp_0.41.0_linux_amd64.tar.gz
tar -xvf frp_0.41.0_linux_amd64.tar.gz -C ./frp_manage
mv ./frp_manage/frp_0.41.0_linux_amd64/* ./frp_manage/

cd ./frp_manage/
pip install -r requirements.txt
# 
按照https://gofrp.org/docs/规范修改frp_config.yaml
sh start.sh
或
sh restart.sh

# 管理模型
 1. 下载frp_manage
```
git clone https://github.com/get-Resource/frp_manage.git
wget https://github.com/fatedier/frp/releases/download/v0.41.0/frp_0.41.0_linux_amd64.tar.gz
tar -xvf frp_0.41.0_linux_amd64.tar.gz -C ./frp_manage
mv ./frp_manage/frp_0.41.0_linux_amd64/* ./frp_manage/

cd ./frp_manage/
pip install -r requirements.txt
```
 2. pip install -r requirements.txt
 3. 执行下面命令使其加载服务并启动
```
sudo cp ./frp_manage.service /etc/systemd/system/frp_manage.service #复制服务文件
chmod +x /etc/systemd/system/frp_manage.service # 添加执行权限
sudo systemctl daemon-reload # 重载系统服务
systemctl start frp_manage.service # 启动服务
systemctl status frp_manage.service # 看指定服务状态
systemctl enable frp_manage.service # 将服务注册为开机启动
```

 4. 关于 systemctl 的命令
```
systemctl start frp_manage.service # 启动服务
systemctl status # 查看所有服务的状态
systemctl disable frp_manage.service # 禁用服务开机启动
systemctl stop sfrp_manage.service # 停止服务
```
# 贡献项目
https://github.com/fatedier/frp.git

# frp使用教程
https://gofrp.org/docs/