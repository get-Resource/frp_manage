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
按照https://gofrp.org/docs/ 规范修改 frp_config.yaml
# 启动
sh start.sh
# 重新加载配置启动
sh restart.sh
# 贡献项目
https://github.com/fatedier/frp.git

# frp使用教程
https://gofrp.org/docs/