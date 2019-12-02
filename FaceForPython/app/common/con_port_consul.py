class Consul:
    def __init__(self, host='127.0.0.1', port=8500):
        self.host = host
        self.port = port


class Config:
    def __init__(self, consul: Consul):
        self.consul = consul


config = Config(
    consul=Consul()
)
