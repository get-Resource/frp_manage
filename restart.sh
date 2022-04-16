cd ./
kill -9 $(ps aux|grep FRP_Manage|grep -v grep|awk '{print  $2}')
nohup python frp.py >/dev/null 2>&1 &