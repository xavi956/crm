from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import sqlite3
import os


root = Tk()
root.title("CRM")

conn = sqlite3.connect("crm.db")
c = conn.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        n_archivo TEXT NOT NULL,
        dni TEXT NOT NULL,
        direccion TEXT NOT NULL,
        tlf TEXT NOT NULL,
        notas TEXT NOT NULL,
        email TEXT NOT NULL,
        archivo TEXT
    );
    """
)


def render_clientes():
    rows = c.execute("SELECT * FROM cliente").fetchall()

    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))


def insertar(cliente):
    c.execute(
        """
        INSERT INTO cliente (nombre, n_archivo, dni, direccion, tlf, notas, email, archivo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)   
        """, (cliente["nombre"], cliente["n_archivo"], cliente["dni"], cliente["direccion"], cliente["tlf"], cliente["notas"], cliente["email"], cliente["archivo"]))
    conn.commit()
    render_clientes()


def editar_cliente():
    id = tree.selection()[0]

    cliente = c.execute("SELECT * FROM cliente WHERE id = ?", (id,)).fetchone()

    def guardar():
        notas_modificadas = notas.get("1.0", END)
        c.execute("UPDATE cliente SET notas = ? WHERE id = ?", (notas_modificadas, id))
        conn.commit()
        messagebox.showinfo("Cliente Modificado", "Las notas del cliente han sido actualizadas.")
        top.destroy()

    top = Toplevel()
    top.title("Ver/Editar Notas")

    lnotas = Label(top, text="Notas")
    lnotas.grid(row=0, column=0)

    notas = Text(top, width=40, height=10)
    notas.insert("1.0", cliente[6])  # Insertar las notas actuales del cliente en el campo de texto
    notas.grid(row=1, column=0)

    guardar_btn = Button(top, text="Guardar", command=guardar)
    guardar_btn.grid(row=2, column=0)

    top.mainloop()


def nuevo_cliente():
    def guardar():
        if not nombre.get() or not n_archivo.get() or not dni.get() or not direccion.get() or not tlf.get() or not notas.get("1.0", END) or not email.get():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        cliente = {
            "nombre": nombre.get(),
            "n_archivo": n_archivo.get(),
            "dni": dni.get(),
            "direccion": direccion.get(),
            "tlf": tlf.get(),
            "notas": notas.get("1.0", END),
            "email": email.get(),
            "archivo": archivo.get()
        }
        insertar(cliente)
        top.destroy()

    def seleccionar_carpeta():
        carpeta_seleccionada = filedialog.askdirectory()
        archivo.delete(0, END)  # Limpiar el contenido actual del Entry
        archivo.insert(0, carpeta_seleccionada)  # Insertar la ruta de la carpeta seleccionada

    top = Toplevel()
    top.title("Nuevo Cliente")

    lnombre = Label(top, text="Nombre")
    nombre = Entry(top, width=40)
    lnombre.grid(row=0, column=0)
    nombre.grid(row=0, column=1)

    ln_archivo = Label(top, text="n.archivo")
    n_archivo = Entry(top, width=40)
    ln_archivo.grid(row=1, column=0)
    n_archivo.grid(row=1, column=1)

    ldni = Label(top, text="DNI")
    dni = Entry(top, width=40)
    ldni.grid(row=2, column=0)
    dni.grid(row=2, column=1)

    ldireccion = Label(top, text="Dirección")
    direccion = Entry(top, width=40)
    ldireccion.grid(row=3, column=0)
    direccion.grid(row=3, column=1)

    ltlf = Label(top, text="Teléfono")
    tlf = Entry(top, width=40)
    ltlf.grid(row=4, column=0)
    tlf.grid(row=4, column=1)

    lnotas = Label(top, text="Notas")
    notas = Text(top, width=40, height=5)
    lnotas.grid(row=5, column=0)
    notas.grid(row=5, column=1)

    lemail = Label(top, text="Email")
    email = Entry(top, width=40)
    lemail.grid(row=6, column=0)
    email.grid(row=6, column=1)

    larchivo = Label(top, text="Archivo")
    larchivo.grid(row=7, column=0)

    archivo = Entry(top, width=40)
    archivo.grid(row=7, column=1)

    seleccionar_btn = Button(top, text="Seleccionar Carpeta", command=seleccionar_carpeta)
    seleccionar_btn.grid(row=7, column=2)

    guardar_btn = Button(top, text="Guardar", command=guardar)
    guardar_btn.grid(row=8, column=1)

    top.mainloop()


def eliminar_cliente():
    id = tree.selection()[0]

    cliente = c.execute("SELECT * FROM cliente WHERE id = ?", (id,)).fetchone()
    respuesta = messagebox.askokcancel(
        "Seguro", "¿Estás seguro de eliminar el cliente " + cliente[1] + "?")
    if respuesta:
        c.execute("DELETE FROM cliente WHERE id = ?", (id,))
        conn.commit()
        render_clientes()
    else:
        pass


def abrir_carpeta():
    id = tree.selection()[0]

    cliente = c.execute("SELECT * FROM cliente WHERE id = ?", (id,)).fetchone()
    ruta_carpeta = cliente[8]

    if ruta_carpeta:
        if os.path.exists(ruta_carpeta):
            os.startfile(ruta_carpeta)
        else:
            messagebox.showerror("Error", "La carpeta no existe.")
    else:
        messagebox.showerror("Error", "El cliente no tiene una carpeta asociada.")


def buscar_cliente():
    criterio = busqueda_entry.get()
    query = "SELECT * FROM cliente WHERE nombre LIKE ? OR n_archivo LIKE ? OR dni LIKE ? OR direccion LIKE ? OR tlf LIKE ? OR notas LIKE ? OR email LIKE ? OR archivo LIKE ?"
    parametros = ('%' + criterio + '%', '%' + criterio + '%', '%' + criterio + '%', '%' + criterio + '%', '%' + criterio + '%', '%' + criterio + '%', '%' + criterio + '%', '%' + criterio + '%')

    rows = c.execute(query, parametros).fetchall()

    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))



btn = Button(root, text="Nuevo Cliente", command=nuevo_cliente)
btn.grid(column=0, row=0)

btn_ver_notas = Button(root, text="Ver/Editar Notas", command=editar_cliente)
btn_ver_notas.grid(column=1, row=0)

btn_eliminar = Button(root, text="Eliminar Cliente", command=eliminar_cliente)
btn_eliminar.grid(column=2, row=0)

busqueda_entry = Entry(root, width=40)
busqueda_entry.grid(column=0, row=2)

buscar_btn = Button(root, text="Buscar", command=buscar_cliente)
buscar_btn.grid(column=1, row=2)

tree = ttk.Treeview(root)
tree["columns"] = ("nombre", "n_archivo", "dni", "direccion", "tlf", "notas", "email", "archivo")
tree.column("#0", width=0, stretch=NO)
tree.column("nombre")
tree.column("n_archivo")
tree.column("dni")
tree.column("direccion")
tree.column("tlf")
tree.column("notas")
tree.column("email")
tree.column("archivo")

tree.heading("nombre", text="Nombre")
tree.heading("n_archivo", text="n.archivo")
tree.heading("dni", text="DNI")
tree.heading("direccion", text="Dirección")
tree.heading("tlf", text="Teléfono")
tree.heading("notas", text="Notas")
tree.heading("email", text="Email")
tree.heading("archivo", text="Archivo")
tree.grid(column=0, row=1, columnspan=3)

abrir_carpeta_btn = Button(root, text="Abrir Carpeta", command=abrir_carpeta)
abrir_carpeta_btn.grid(column=3, row=1)

conn.commit()

render_clientes()

root.mainloop()
