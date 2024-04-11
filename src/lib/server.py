
class  SittyTalkyServer():
    # TODO: implement message listener

    def __init__(self,):
        pass

    def start_server(self):
        # TODO : server setup
        print("starting server")
        pass

    def stop_server(self):
        # TODO : Server garbage collection
        print("stoping server")
        pass

    def on_message(self, callback:callable):
        """Bind on message event of server with callback"""
        # callback("msg got", "peername")
        self.on_msg_callback = callback

    def test_triger(self):
        """Testing the on_message callback"""
        self.on_msg_callback("test message", "bRuttaZz")


