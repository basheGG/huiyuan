import redis
import json

r = redis.Redis(host='127.0.0.1', port=6379, password='', db=0, decode_responses=True)

class Token():
    Token = ""
    Id = ""
    Type = ""
    Permissions = []

    def LoadToken(self, token):
        j = r.get("FaceMakeMoney:{Token}".format(Token=token))
        o = json.loads(j)
        self.Token = o["Token"]
        self.Id = o["Id"]
        self.Type = o["Type"]
        return self


if __name__ == '__main__':
    a = Token().LoadToken("b8716f86db774662a2a720f0573c8a1f")
    print(a.__dict__)