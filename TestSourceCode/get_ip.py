#!/usr/bin/env python

#pythonの標準ライブラリですね
import socket

try:
    #socket.AF_INET:IVv4のアドレス, socket.SOCK_DGRAM:UDPネットワークの
    #IPv6の場合はAF_INET→IF_INET6
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    #タイムアウトを１０秒
    s.settimeout(10)
    #ipアドレス8.8.8.8:80に接続します。
    # 8.8.8.8はgoogle Public DNSPCのIP。
    # 外のアドレスなら何でもいいです。
    s.connect(("8.8.8.8", 80))
    #今の接続のソケット名を取得します。
    ip=s.getsockname()[0]
    #IPアドレス表示
    print(ip)

except socket.error:
    print('No Internet')