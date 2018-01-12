# encoding: UTF-8

from time import sleep

from ccRpc import RpcClient


########################################################################
class TestClient(RpcClient):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, reqAddress, subAddress):
        """Constructor"""
        super(TestClient, self).__init__(reqAddress, subAddress)
        
    #----------------------------------------------------------------------
    def callback(self,data):
        """回调函数实现"""
        print('client received data:', data.decode('utf-8'))
    

if __name__ == '__main__':
    reqAddress = 'tcp://localhost:2014'
    subAddress = 'tcp://localhost:0602'
    reqAddress = 'tcp://192.168.40.108:2014'
    subAddress = 'tcp://192.168.40.108:0602'

    tc = TestClient(reqAddress, subAddress)
    tc.subscribeTopic(b'')
    tc.start()
    
    while 1:
        print(tc.send('client999'.encode('utf-8')))
        sleep(2)