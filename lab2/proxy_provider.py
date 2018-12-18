import random

class ProxyProvider:

    def __init__(self):
        self.proxies = []
        self.__lastProxyIndex = 0

    def getRandomProxy(self):
        return self.proxies[random.randint(0, len(self.proxies) - 1)]

    def getNextProxy(self):
        length = len(self.proxies)

        if(length == 0):
            return None

        if(self.__lastProxyIndex == length):
            self.__lastProxyIndex = 0

        self.__lastProxyIndex += 1

        return self.proxies[self.__lastProxyIndex-1]