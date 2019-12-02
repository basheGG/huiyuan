# 主体函数

# 实例化app
from app import create_app
import datetime

# 调用默认的配置信息
app = create_app('DEBUGGING')

app.run(host = '0.0.0.0',port=8889,debug=True)
