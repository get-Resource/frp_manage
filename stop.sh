kill -9 $(ps aux|grep FRP_Manage|grep -v grep|awk '{print  $2}')