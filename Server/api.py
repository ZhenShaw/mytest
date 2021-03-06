from flask import Flask, request, render_template, jsonify
from Spider import Spider

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/course", methods=["GET", "POST"])
def course():

    post_format = {"username": "", "password": ""}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Spider(username, password)
        user.login()
        if user.login_status:
            info = user.modify_data()
            return jsonify(info)
        else:
            return "登录失败"
    else:
        return render_template("index.html", format=post_format)


@app.route("/library", methods=["GET"])
def library():
    lib = Spider()
    visit = lib.read_library()
    return jsonify(visit)


@app.route("/grade", methods=["GET", "POST"])
def grade():

    post_format = {"username": "", "password": ""}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        grade = Spider(username, password)
        grade.login()
        if grade.login_status:
            info = grade.modify_grade()
            print(info)
            return jsonify(info)
        else:
            return "登录失败"
    else:
        return render_template("index.html", format=post_format)


if __name__ == "__main__":

    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.run("0.0.0.0")
    # app.run("0.0.0.0", ssl_context=("ssl/myapi.iego.net.pem", "ssl/myapi.iego.net.key"))

