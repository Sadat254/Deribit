from deribit_api import RestClient

class Clients:
    def __init__(self):
        pass


    def authenticate(self):
        # testing version
        url = "wss://test.deribit.com/ws/api/v2"
        # real
        # url = "wss://www.deribit.com/ws/api/v2"
        deribitClient = RestClient(key="1H37RfiB", secret="uwzosu7y179KMaMw1W7wbI9I8DxfYjSq0mfLnbbrPF8",url=url)

        return {"deribit": deribitClient, "url":url}


