from app.models.product_model import ProductModel

class cs_test():
    def cst(self):
        return 5

    def t(self):
        res = ProductModel().get_data_consul()
        print(res)
if __name__ == '__main__':
    res = cs_test().t()
    print(res)