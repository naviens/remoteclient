from remoteclient import RemoteClient


def example1():
    rclient = RemoteClient()
    hosts = ['127.0.0.1,naveen,password', '172.30.30.143,user,password']
    for host in hosts:
        rclient.add_host(host)
    rclient.connect()
    rclient.copy('README.md', '/tmp/README.md')
    rclient.run('uptime')


if __name__ == '__main__':
    example1()
