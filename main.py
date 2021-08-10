#importación de librerias
import psycopg2
from flask import Flask, render_template, request, redirect

#from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy

#Creamos un objeto de tipo Flask
app = Flask(__name__, static_url_path='/static')
db = SQLAlchemy(app)
conn = psycopg2.connect(

    host="ec2-44-196-250-191.compute-1.amazonaws.com",
    database="d3p9pk88t555ne",
    user="ysscidxymbivrv",
    password="48c83df0eb76d83394fc88c1745a748dc3f0387736ea533d46735690d4f9b91e"
)

#Conexión con MySQL
#mysql = MySQL()

#app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
#app.config['MYSQL_DATABASE_USER'] = 'Carolina'
#app.config['MYSQL_DATABASE_PASSWORD'] = '12345'
#app.config['MYSQL_DATABASE_DB'] = 'datos_formulario'
#app.config['MYSQL_DATABASE_PORT'] = 3306

#pip

#mysql.init_app(app)

app = Flask(__name__, static_url_path='/static')

@app.route("/")

def idex():

    return render_template("index.html")

@app.route("/rejilla")
def rejillas_html():
    return render_template("html_rejilla.html")

@app.route("/bootstrap")
def bootstrap_html():
    return render_template("html_bootstrap.html")

@app.route("/formulario")
def formulario_html():
    #conn = mysql.connect()

    connectar = conn.cursor()

    connectar.execute("select * from productos")

    datos = connectar.fetchall()

    print(datos)
    connectar.close()

    return render_template("html_formulario.html", productos=datos)


@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    producto = request.form["producto"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]

    #conn = mysql.connect()

    connectar = conn.cursor()

    connectar.execute("INSERT INTO productos(producto, precio, descripcion) VALUES (%s,%s,%s)",
                      (producto, precio, descripcion))

    conn.commit()

    connectar.close()

    #return "Dato insertado "+producto + " " + precio + " " + descripcion

    return redirect("/formulario")

@app.route("/eliminar_producto/<string:ID>")
def eliminar_producto(ID):
    #conn = mysql.connect()

    connectar = conn.cursor()

    connectar.execute("delete from productos where ID={0}".format(ID))

    conn.commit()

    connectar.close()

    return redirect("/formulario")

@app.route("/consultar_producto/<ID>")
def obtener_producto(ID):
    #conn = mysql.connect()

    connectar = conn.cursor()

    connectar.execute("select * from productos where ID= %s", (ID))

    dato=connectar.fetchone()

    print(dato)

    connectar.close()

    return render_template("form_editar_producto.html", producto=dato)

@app.route("/editar_producto/<ID>", methods=['POST'])
def editar_producto(ID):
    producto = request.form["producto"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]

    #conn = mysql.connect()

    connectar = conn.cursor()

    connectar.execute("update productos set Producto=%s, Precio=%s, Descripcion=%s where ID=%s", (producto, precio, descripcion, ID))

    conn.commit()

    connectar.close()

    return redirect("/formulario")

if __name__ == '__main__':

    app.run(port = 80,debug = True)
