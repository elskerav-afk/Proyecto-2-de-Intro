import tkinter as tk
from tkinter import messagebox

# CLASES

class Elemento:
    #Clase base para muros, torres, unidades y base
    def __init__(self, nombre, costo, vida=100):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.fila = None
        self.columna = None


class Muro(Elemento):
    def __init__(self):
        Elemento.__init__(self, "Muro", 50, 100)


class Torre(Elemento):
    def __init__(self):
        Elemento.__init__(self, "Torre", 100, 150)


class Base(Elemento):
    def __init__(self):
        Elemento.__init__(self, "Base", 0, 500)


class Soldado(Elemento):
    def __init__(self):
        Elemento.__init__(self, "Soldado", 75, 80)


class Arquero(Elemento):
    def __init__(self):
        Elemento.__init__(self, "Arquero", 100, 60)


class Jugador:
    def __init__(self, nombre, rol, dinero=500):
        self.nombre = nombre
        self.rol = rol
        self.dinero = dinero

    def puede_comprar(self, costo):
        return self.dinero >= costo

    def gastar_dinero(self, costo):
        if self.puede_comprar(costo):
            self.dinero -= costo
            return True
        return False

    def ganar_dinero(self, cantidad):
        self.dinero += cantidad


class Defensor(Jugador):
    def __init__(self, nombre):
        super().__init__(nombre, "Defensor", 500)
        self.base = None
        self.defensas = []


class Atacante(Jugador):
    def __init__(self, nombre):
        super().__init__(nombre, "Atacante", 500)
        self.unidades = []


# VARIABLES GLOBALES

ANCHO = 11
ALTO = 11
TAM_CELDA = 50

# Matriz: 0=vacío, 1=muro, 2=torre, 3=unidad, 4=base
matriz = [[0 for _ in range(ANCHO)] for _ in range(ALTO)]

# Jugadores
defensor = Defensor("Defensor 1")
atacante = Atacante("Atacante 1")

# Estado del juego
fase = "defensor_base"  # defensor_base, defensor_defensas, atacante_unidades
elemento_actual = None  # Qué tipo de elemento se está colocando

# Referencias a elementos en el mapa
objetos_en_mapa = {}  # {(fila, col): objeto}


# FUNCIONES

def dibujar_mapa():
    #Dibuja el mapa en el canvas
    canvas.delete("all")
    
    for fila in range(ALTO):
        for col in range(ANCHO):
            x1 = col * TAM_CELDA
            y1 = fila * TAM_CELDA
            x2 = x1 + TAM_CELDA
            y2 = y1 + TAM_CELDA
            
            valor = matriz[fila][col]
            color = "white"
            texto = ""
            
            if valor == 1:  # Muro
                color = "#8B4513"
                texto = "M"
            elif valor == 2:  # Torre
                color = "#696969"
                texto = "T"
            elif valor == 3:  # Unidad
                color = "#360505"
                texto = "U"
            elif valor == 4:  # Base
                color = "#FFD700"
                texto = "B"
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)
            
            if texto:
                canvas.create_text(
                    x1 + TAM_CELDA // 2,
                    y1 + TAM_CELDA // 2,
                    text=texto,
                    fill="white",
                    font=("Arial", 10, "bold")
                )


def actualizar_labels():
    #Actualiza los labels de fase y dinero
    if fase == "defensor_base":
        label_fase.config(text="FASE: Defensor coloca BASE")
        label_dinero.config(text=f"Dinero: ${defensor.dinero}")
    elif fase == "defensor_defensas":
        label_fase.config(text="FASE: Defensor coloca MUROS y TORRES")
        label_dinero.config(text=f"Dinero: ${defensor.dinero}")
    elif fase == "atacante_unidades":
        label_fase.config(text="FASE: Atacante coloca UNIDADES")
        label_dinero.config(text=f"Dinero: ${atacante.dinero}")


def limpiar_botones():
    #Elimina todos los botones de acción
    for widget in frame_botones_accion.winfo_children():
        widget.destroy()


def crear_botones():
    #Crea los botones según la fase actual
    limpiar_botones()
    
    if fase == "defensor_base":
        btn = tk.Button(frame_botones_accion, text="Colocar Base", command=lambda: seleccionar_elemento("base"), bg="#FFD700", width=12)
        btn.pack(side=tk.LEFT, padx=5)
    
    elif fase == "defensor_defensas":
        btn1 = tk.Button(frame_botones_accion, text="Muro ($50)", command=lambda: seleccionar_elemento("muro"), bg="#8B4513", fg="white", width=12)
        btn1.pack(side=tk.LEFT, padx=5)
        btn2 = tk.Button(frame_botones_accion, text="Torre ($100)", command=lambda: seleccionar_elemento("torre"), bg="#696969", fg="white", width=12)
        btn2.pack(side=tk.LEFT, padx=5)
    
    elif fase == "atacante_unidades":
        btn1 = tk.Button(frame_botones_accion, text="Soldado ($75)", command=lambda: seleccionar_elemento("soldado"), bg="#360505", fg="white", width=12)
        btn1.pack(side=tk.LEFT, padx=5)
        btn2 = tk.Button(frame_botones_accion, text="Arquero ($100)", command=lambda: seleccionar_elemento("arquero"), bg="#DC143C", fg="white", width=12)
        btn2.pack(side=tk.LEFT, padx=5)


def seleccionar_elemento(tipo):
    #Selecciona el tipo de elemento a colocar
    global elemento_actual
    
    # Verificar que tiene dinero
    if tipo == "muro" and not defensor.puede_comprar(50):
        messagebox.showerror("Error", "No tienes dinero para un muro ($50)")
        return
    elif tipo == "torre" and not defensor.puede_comprar(100):
        messagebox.showerror("Error", "No tienes dinero para una torre ($100)")
        return
    elif tipo == "soldado" and not atacante.puede_comprar(75):
        messagebox.showerror("Error", "No tienes dinero para un soldado ($75)")
        return
    elif tipo == "arquero" and not atacante.puede_comprar(100):
        messagebox.showerror("Error", "No tienes dinero para un arquero ($100)")
        return
    
    elemento_actual = tipo
    label_estado.config(text=f"Colocando {tipo.upper()} - Haz clic en el mapa (clic derecho para cancelar)")
    label_estado.config(fg="green")


def cancelar_elemento():
    #Cancela la colocación actual
    global elemento_actual
    elemento_actual = None
    label_estado.config(text="")


def on_canvas_click(event):
    #Maneja los clics en el canvas
    global elemento_actual
    if elemento_actual is None:
        messagebox.showwarning("Aviso", "Primero selecciona qué colocar")
        return
    
    col = event.x // TAM_CELDA
    fila = event.y // TAM_CELDA
    
    # Validar límites
    if fila >= ALTO or col >= ANCHO or fila < 0 or col < 0:
        messagebox.showerror("Error", "Haz clic dentro del mapa")
        return
    
    # Validar que esté vacío
    if matriz[fila][col] != 0:
        messagebox.showerror("Error", "Esa celda ya está ocupada")
        return
    
    exito = False
    
    # DEFENSOR - BASE
    if elemento_actual == "base":
        if defensor.base is None:
            base = Base()
            defensor.base = base
            matriz[fila][col] = 4
            objetos_en_mapa[(fila, col)] = base
            exito = True
            
            elemento_actual = None  # Una sola base
            label_estado.config(text="Base colocada. Haz clic en 'Siguiente'")
            label_estado.config(fg="green")
        else:
            messagebox.showerror("Error", "Ya colocaste una base")
    
    # DEFENSOR - MURO
    elif elemento_actual == "muro":
        if defensor.gastar_dinero(50):
            muro = Muro()
            defensor.defensas.append(muro)
            matriz[fila][col] = 1
            objetos_en_mapa[(fila, col)] = muro
            exito = True
            label_dinero.config(text=f"Dinero: ${defensor.dinero}")
        else:
            messagebox.showerror("Error", "No tienes dinero suficiente")
    
    # DEFENSOR - TORRE
    elif elemento_actual == "torre":
        if defensor.gastar_dinero(100):
            torre = Torre()
            defensor.defensas.append(torre)
            matriz[fila][col] = 2
            objetos_en_mapa[(fila, col)] = torre
            exito = True
            label_dinero.config(text=f"Dinero: ${defensor.dinero}")
        else:
            messagebox.showerror("Error", "No tienes dinero suficiente")
    
    # ATACANTE - SOLDADO
    elif elemento_actual == "soldado":
        if atacante.gastar_dinero(75):
            unidad = Soldado()
            atacante.unidades.append(unidad)
            matriz[fila][col] = 3
            objetos_en_mapa[(fila, col)] = unidad
            exito = True
            label_dinero.config(text=f"Dinero: ${atacante.dinero}")
        else:
            messagebox.showerror("Error", "No tienes dinero suficiente")
    
    # ATACANTE - ARQUERO
    elif elemento_actual == "arquero":
        if atacante.gastar_dinero(100):
            unidad = Arquero()
            atacante.unidades.append(unidad)
            matriz[fila][col] = 3
            objetos_en_mapa[(fila, col)] = unidad
            exito = True
            label_dinero.config(text=f"Dinero: ${atacante.dinero}")
        else:
            messagebox.showerror("Error", "No tienes dinero suficiente")
    
    if exito:
        dibujar_mapa()


def on_canvas_right_click(event):
    #Cancela con clic derecho
    cancelar_elemento()


def siguiente_fase():
    #Avanza a la siguiente fase
    global fase
    
    if fase == "defensor_base":
        if defensor.base is None:
            messagebox.showwarning("Aviso", "Primero coloca la base central")
            return
        fase = "defensor_defensas"
    
    elif fase == "defensor_defensas":
        if len(defensor.defensas) == 0:
            messagebox.showwarning("Aviso", "Coloca al menos una defensa (muro o torre)")
            return
        fase = "atacante_unidades"
    
    elif fase == "atacante_unidades":
        if len(atacante.unidades) == 0:
            messagebox.showwarning("Aviso", "Coloca al menos una unidad atacante")
            return
        messagebox.showinfo("¡Listo!", "Ronda lista para comenzar.")
        # Aquí iría la lógica de batalla
        return
    
    cancelar_elemento()
    actualizar_labels()
    crear_botones()
    label_estado.config(text="")
    dibujar_mapa()


# INTERFAZ GRÁFICA

ventana = tk.Tk()
ventana.title("Avgrunnens Battle Royal")
ventana.geometry("600x700")
ventana.state("zoomed")

# Frame superior con información
frame_info = tk.Frame(ventana)
frame_info.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

label_fase = tk.Label(frame_info, text="", font=("Arial", 12, "bold"))
label_fase.pack(anchor=tk.W)

label_dinero = tk.Label(frame_info, text="", font=("Arial", 11))
label_dinero.pack(anchor=tk.W)

label_estado = tk.Label(frame_info, text="", font=("Arial", 10))
label_estado.pack(anchor=tk.W)

# Canvas del mapa
canvas = tk.Canvas(
    ventana,
    width=ANCHO * TAM_CELDA,
    height=ALTO * TAM_CELDA,
    bg="white",
    cursor="cross"
)
canvas.pack(padx=10, pady=10)
canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<Button-3>", on_canvas_right_click)

# Frame inferior con botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

frame_botones_accion = tk.Frame(frame_botones)
frame_botones_accion.pack(side=tk.LEFT)

btn_siguiente = tk.Button(frame_botones, text="Siguiente", command=siguiente_fase, font=("Arial", 10), bg="#4CAF50", fg="white", width=12)
btn_siguiente.pack(side=tk.RIGHT, padx=5)

btn_cancelar = tk.Button(frame_botones, text="Cancelar (clic der)", command=cancelar_elemento, font=("Arial", 9), bg="#f44336", fg="white")
btn_cancelar.pack(side=tk.RIGHT, padx=5)

# Iniciar
actualizar_labels()
crear_botones()
dibujar_mapa()

ventana.mainloop()
