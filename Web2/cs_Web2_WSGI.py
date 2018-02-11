"""
简单的WSGI的Web服务器
"""
from wsgiref.simple_server import make_server


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def application(environ, start_response):
    """
    WSGI处理函数
    :param environ: 一个包含所有HTTP请求信息的dict对象
    :param start_response: 一个发送HTTP响应的函数
    :return: HTTP响应的body发送给浏览器
    """
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, {}</h1>'.format(environ['PATH_INFO'])
    log(environ['PATH_INFO'])
    return [body.encode('utf-8')]


# 创建一个服务器
http_server = make_server('', 5000, application)
log('Serving HTTP on port 5000...')

# 开始监听HTTP请求
http_server.serve_forever()
