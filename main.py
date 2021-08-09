#importación de librerias
import psycopg2
from flask import Flask, render_template, request, redirect

#from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy

#Creamos un objeto de tipo Flask
app = Flask(__name__, static_url_path='/static')
db = SQLAlchemy(app)
conn = psycopg2.connect(

    host="ec2-34-197-105-186.compute-1.amazonaws.com",
    database="d4rpk4sfoiglj7",
    user="nlfszitavdcnzj",
    password="24472049d38dcbb2177d99a65cebf4b7bc2ddcd9e2c6b3552e438fca0cbf7d69"
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

@app.route("/boostrap")
def boostrap():
    return render_template("/boostrap.html")

@app.route("/formulario")
def formulario_html():
    #conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("select * from productos")

    datos = cursor.fetchall()

    print(datos)
    cursor.close()

    return render_template("html_formulario.html", productos=datos)


@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    producto = request.form["producto"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]

    #conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO productos(producto, precio, descripcion) VALUES (%s,%s,%s)",
                   (producto, precio, descripcion))

    conn.commit()

    cursor.close()

    #return "Dato insertado "+producto + " " + precio + " " + descripcion

    return redirect("/formulario")

@app.route("/eliminar_producto/<string:ID>")
def eliminar_producto(ID):
    #conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("delete from productos where ID={0}".format(ID))

    conn.commit()

    cursor.close()

    return redirect("/formulario")

@app.route("/consultar_producto/<ID>")
def obtener_producto(ID):
    #conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("select * from productos where ID= %s", (ID))

    dato=cursor.fetchone()

    print(dato)

    cursor.close()

    return render_template("form_editar_producto.html", producto=dato)

@app.route("/editar_producto/<ID>", methods=['POST'])
def editar_producto(ID):
    producto = request.form["producto"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]

    #conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("update productos set Producto=%s, Precio=%s, Descripcion=%s where ID=%s", (producto, precio, descripcion,ID))

    conn.commit()

    cursor.close()

    return redirect("/formulario")

if __name__ == '__main__':

    app.run(port = 80,debug = True)
