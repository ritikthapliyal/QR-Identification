from flask import Flask
import myroutes

app = Flask(__name__, static_url_path='/static')
app.secret_key = "secret123"
app.config["UPLOAD_FOLDER"] = "./uploads/"

app.add_url_rule('/register', view_func = myroutes.register, methods = ['GET', 'POST'])
app.add_url_rule('/', view_func = myroutes.login, methods = ['GET', 'POST'])
app.add_url_rule('/profile', view_func = myroutes.profile, methods=['GET'])
app.add_url_rule('/logged_in', view_func = myroutes.logged_in, methods=['GET' , 'POST'])
app.add_url_rule('/download', view_func = myroutes.download, methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)
