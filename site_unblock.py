#!/usr/bin/python3

import socket
import time
import sys
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 8081))
server_socket.listen(200)

dummy = 'GET / HTTP/1.1\r\nHost: test.gilgil.net\r\n\r\n\r\n'
dummy_result = b"HTTP/1.1 403 Forbidden\r\nServer: nginx\r\nDate: Wed, 22 Nov 2017 00:31:14 GMT\r\nContent-Type: text/html; charset=iso-8859-1\r\nTransfer-Encoding: chunked\r\nConnection: keep-alive\r\nVary: Accept-Encoding\r\n\r\nc6\r\n<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\n<HTML><HEAD>\n<TITLE>403 Forbidden</TITLE>\n</HEAD><BODY>\n<H1>Forbidden</H1>\nYou don\'t have permission to access /\non this server.<P>\n</BODY></HTML>\n\r\n0\r\n\r\n"

def g(server_socket, client_socket):
    while 1:
        data = server_socket.recv(2048)
        if len(data) == 0:
            time.sleep(0.01)
            continue
            break
        #print("********* 서버로부터 수신 ************")
        if data[-335:] == dummy_result[-335:]: 
            #print ("넘겨버리기")
            continue
        #print(data)
        #print("------------------------------------")
        client_socket.send(data)
    
    server_socket.close()
    #print("g 함수 종료")

def f(client_socket, address):
    datas = ''
    flag  = 0
    while 1:
        data = client_socket.recv(2048).decode()
        if data == '': break
        datas += data
        
        if (not 'host' in locals().keys()) and "\r\nHost" in datas:
            host = datas.split("Host: ")[1].split("\r\n")[0]
            if ':' in host:
                host, port = host.split(":")
                port = int(port)
            else: port = 80
            Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #print ("---------------------------")
            #print ("host: ", host)
            #print ("---------------------------")
            Server.connect((host, port))
            t = threading.Thread(target=g, args=(Server, client_socket))
            t.start()
        if 'Server' in locals().keys():
            if flag == 0: 
                datas = dummy + datas
                flag = 1
            Server.send(datas.encode())
            if datas.endswith('\r\n\r\n'):
                flag = 0
            #print("********* 보내는 데이터 ************")
            #print (datas)
            #print (datas.encode())
            datas = ''
        
        #print("데이터 수신")
    t.join()
    
    #print(address, " is closed.")
    client_socket.close()

while 1:
    client_socket, address = server_socket.accept()
    print ("I got a connection from ", address)
    t = threading.Thread(target=f, args=(client_socket, address))
    t.start()

server_socket.close()
