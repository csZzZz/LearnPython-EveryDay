import socket
import ssl

"""
资料:

一、使用 https
    1, https 请求的默认端口是 443
    2, https 的 socket 连接需要 import ssl
        并且使用 s = ssl.wrap_socket(socket.socket()) 来初始化

    试试用这个请求豆瓣电影 top250
    url = 'https://movie.douban.com/top250'

    你就能得到网页的 html 源代码
    然后保存为 html 文件 你就能用浏览器打开


二、HTTP 协议的 301 状态
    请求豆瓣电影 top250 (注意协议)
    http://movie.douban.com/top250
    返回结果是一个 301
    301 状态会在 HTTP 头的 Location 部分告诉你应该转向的 URL
    所以, 如果遇到 301, 就请求新地址并且返回
        HTTP/1.1 301 Moved Permanently
        Date: Sun, 05 Jun 2016 12:37:55 GMT
        Content-Type: text/html
        Content-Length: 178
        Connection: keep-alive
        Keep-Alive: timeout=30
        Location: https://movie.douban.com/top250
        Server: dae
        X-Content-Type-Options: nosniff

        <html>
        <head><title>301 Moved Permanently</title></head>
        <body bgcolor="white">
        <center><h1>301 Moved Permanently</h1></center>
        <hr><center>nginx</center>
        </body>
        </html>

https 的默认端口是 443, 所以你需要在 get 函数中根据协议设置不同的默认端口
"""


def log(*args, **kwargs):
    # 用log代替原生的print
    print("log", *args, **kwargs)


def parsed_url(url):
    # 检查协议
    protocol = "http"
    if url[:7] == "http://":
        u = url.split("://")[1]
    elif url[:8] == "https://":
        protocol = "https"
        u = url.split("://")[1]
    else:
        u = url

    # 检查path
    i = u.find("/")
    if i == -1:
        host = u
        path = "/"
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        "http": 80,
        "https": 443,
    }
    port = port_dict[protocol]
    if ":" in host:
        h = host.split(":")
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    # 通过协议,来创建相应的socket对象
    if protocol == "http":
        s = socket.socket()
    elif protocol == "https":
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    # 得到响应
    response = b""
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    # 解析响应,得到响应头,状态码,响应体
    header, body = r.split("\r\n\r\n", 1)
    h = header.split("\r\n")
    status_code = h[0].split()[1]
    status_code = int(status_code)

    header = {}
    for line in h[1:]:
        k, v = line.split(": ")
        header[k] = v
    return header, status_code, body


def get(url):
    """
    用GET请求url并返回响应
    """
    protocol, host, port, path = parsed_url(url)

    # 创建一个socket对象
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    # 创建一个请求
    request = "GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n".format(path, host)
    # 发送请求
    encoding = "utf-8"
    s.send(request.encode(encoding))
    # 得到响应
    response = response_by_socket(s)
    print(response)
    r = response.decode(encoding)

    # 解析响应
    header, status_code, body = parsed_response(r)
    if status_code in [301, 302]:
        url = header["location"]
        return get(url)
    return header, status_code, body


def main():
    url = "https://movie.douban.com/top250"
    header, status_code, body = get(url)
    print("main", status_code)


if __name__ == "__main__":
    main()
