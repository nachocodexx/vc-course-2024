import os
from flask import Flask
from flask import Flask, render_template,send_from_directory
HTML_SOURCE_PATH = os.environ.get("HTML_SOURCE_PATH","/source/html")

app = Flask(
    __name__, 
    template_folder=HTML_SOURCE_PATH,
)


@app.route("/")
def index():
    return "Hola soy el index del flask server que creaste en Python :)"

@app.route("/data/<name>")
def send_data(name):
    return send_from_directory("/data",name,as_attachment=True)

@app.route("/<name>")
def funcion_chida(name):
    return "<h1>HOLA {}</h1>".format(name)

@app.route("/html/",defaults={"x":"404"})
@app.route("/html/<path:x>",methods=["GET"])
def html_render(x:str):
    html_path = "{}/{}.html".format(HTML_SOURCE_PATH,x)
    if not os.path.exists(html_path):
        return render_template("404.html")
    return render_template("{}.html".format(x))
