
from tkinter import *
import sqlite3


root = Tk()
root.title("Lista de tareas")
root.geometry("400x500")


conn = sqlite3.connect("todo.db")

c= conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL 
    );
"""
)

conn.commit()

#función para eliminar elementos de la lista de tareas

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?",(id, ))
        conn.commit()
        render_todos()
    return _remove
    



#función para marcar como completa  una tarea
def complete(id):
    def _complete():
        todo=c.execute("SELECT * from todo WHERE id = ?",(id, )).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id=?",(not todo[3],id))
        conn.commit()
        render_todos()
       
    return _complete  



#función para renderizar  las tareas en el frame " mis tareas"
def render_todos():
    rows=c.execute("SELECT * FROM todo").fetchall()
    
    for widget in Frame.winfo_children():
        widget.destroy()



    for i in range(0,len(rows)):
        id=rows[i][0]
        completed  = rows[i][3]
        description = rows[i][2]
        color="#757474" if completed else "#030202"
        l=Checkbutton(Frame,text=description,fg=color, width=42,anchor="w",command=complete(id))
        l.grid(row=i,column=0,sticky="w")
        btn = Button(Frame,text="Eliminar",command=remove(id))
        btn.grid(row=i, column=1)
        l.select() if completed else l.deselect()



#funciín para agregar tarea
def addTodo():
    todo =e.get()
    if todo:
        c.execute(
            """
            INSERT INTO todo(description,completed) VALUES (?,?)
            
            """,(todo,False))
        conn.commit()   
        e.delete(0,END)
        render_todos()
    else:
        pass    



l =Label(root,text="tarea")
l.grid(row=0,column=0)

e =Entry(root,width=40)
e.grid(row=0,column=1)

btn= Button(root,text="Agregar",command=addTodo)
btn.grid(row=0,column=2)


Frame =LabelFrame(root,text="Mis tareas",padx=5,pady=5)
Frame.grid(row=1,column=0,columnspan=3,sticky="nswe",padx=5)


e.focus()

render_todos()
root.bind("<Return>",lambda x: addTodo())

root.mainloop()
