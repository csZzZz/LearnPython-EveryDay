"""
一个服务器程序,打开 localhost:2000就能访问
"""
import socket

# host为空字符串,表示可以接受任何ip地址的连接
host = ""
port = 2000

# 创建一个socket实例
s = socket.socket()
# bind用于绑定固定的端口
s.bind((host, port))

# 无限循环来处理请求
while True:
    # 首先用s.listen开始监听
    s.listen(5)

    # 当有请求过来的时候,accept函数就会返回2个值
    # 分别是连接和客户端的ip地址
    connection, ip = s.accept()
    buffer_size = 1023
    # recv函数可以接受客户端发送过来的数据
    request = connection.recv(buffer_size)

    print("ip 和 请求, {}\n{}".format(ip, request.decode("utf-8")))

    # 创建一个响应 b""表示这个一个bytes对象
    response = b"HTTP/1.1 200 OK\r\n\r\n<h1>Hello World!</h1>"
    # 用sendall函数发送给客户端
    connection.sendall(response)
    # 关闭连接
    connection.close()
