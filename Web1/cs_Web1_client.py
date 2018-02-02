"""
模拟客户端向服务器发送数据
"""
import socket

# 创建一个socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 服务器的域名和端口
port = 80
host = "g.cn"
# 用connection函数连接上主机,参数是一个tuple
s.connect((host, port))

# 连接上服务器之后,可以通过这个函数得到本机的ip和端口
ip, port = s.getsockname()
print("本机 ip 和 port {} {}".format(ip, port))

# 构造一个http请求
http_request = "GET / HTTP/1.1\r\nhost:{}\r\n\r\n".format(host)
# send函数发送请求,只接受bytes作为参数
request = http_request.encode("utf-8")
print("请求", request)
s.send(request)

# 接受服务器的响应数据
buffer_size = 1023
response = s.recv(buffer_size)

# 输出响应的数据bytes类型
print("响应", response)
# str类型的响应数据
print("响应", response.decode("utf-8"))
