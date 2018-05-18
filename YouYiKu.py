from flask import Flask

import GetQQData
import GetWbData

app = Flask(__name__)


@app.route('/<string:WbID>')
def hello_world(WbID):
    return GetWbData.getData(WbID)


@app.route('/<QQnum>/<g_qzonetoken>/<cookisstr>')
def show_post(QQnum, g_qzonetoken, cookisstr):
    return GetQQData.getQQData(str(QQnum), str(g_qzonetoken), str(cookisstr))



if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
