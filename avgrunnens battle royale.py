import tkinter as tk
from tkinter import messagebox
import os



# CLASES

class Elemento:
    #Clase base para muros, torres, unidades y base
    def __init__(self, nombre, costo, vida=100):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.vida_maxima = vida
        self.fila = None
        self.columna = None
        self.tipo = ""


class Muro(Elemento):
    def __init__(self):
        self.nombre = "Muro"
        self.costo = 50
        self.vida = 100
        self.vida_maxima = 100
        self.fila = None
        self.columna = None
        self.tipo = "muro"


class Torre(Elemento):
    #Clase base para torres con atributos avanzados
    def __init__(self, nombre, costo, vida, daño, alcance, habilidad, turnos_habilidad):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.vida_maxima = vida
        self.fila = None
        self.columna = None
        self.daño = daño
        self.alcance = alcance
        self.habilidad = habilidad
        self.turnos_habilidad = turnos_habilidad
        self.turnos_restantes = 0
        self.tipo = ""
    
    def obtener_info(self):
        return f"{self.nombre}\nCosto: ${self.costo}\nVida: {self.vida}\nDaño: {self.daño}\nAlcance: {self.alcance}\nHabilidad: {self.habilidad}"


class TorreBasica(Torre):
    #Torre básica: daño normal, costo bajo, habilidad de disparo doble
    def __init__(self):
        self.nombre = "Torre Básica"
        self.costo = 100
        self.vida = 120
        self.vida_maxima = 120
        self.fila = None
        self.columna = None
        self.daño = 25
        self.alcance = 3
        self.habilidad = "Disparo Doble (2 ataques en 1 turno)"
        self.turnos_habilidad = 3
        self.turnos_restantes = 0
        self.tipo = "torre_basica"


class TorrePesada(Torre):
    #Torre pesada: mucha vida, daño alto, costo elevado, habilidad de daño en área
    def __init__(self):
        self.nombre = "Torre Pesada"
        self.costo = 200
        self.vida = 250
        self.vida_maxima = 250
        self.fila = None
        self.columna = None
        self.daño = 50
        self.alcance = 2
        self.habilidad = "Daño en Área (afecta 3 celdas)"
        self.turnos_habilidad = 4
        self.turnos_restantes = 0
        self.tipo = "torre_pesada"


class TorreMagica(Torre):
    #Torre mágica: daño bajo, habilidad de congelación
    def __init__(self):
        self.nombre = "Torre Mágica"
        self.costo = 150
        self.vida = 100
        self.vida_maxima = 100
        self.fila = None
        self.columna = None
        self.daño = 15
        self.alcance = 4
        self.habilidad = "Congelación (paraliza 2 turnos)"
        self.turnos_habilidad = 2
        self.turnos_restantes = 0
        self.tipo = "torre_magica"


class Base(Elemento):
    def __init__(self):
        self.nombre = "Base Central"
        self.costo = 0
        self.vida = 500
        self.vida_maxima = 500
        self.fila = None
        self.columna = None
        self.tipo = "base"


class Unidad(Elemento):
    #Clase base para unidades con atributos avanzados
    def __init__(self, nombre, costo, vida, daño, velocidad, habilidad, turnos_habilidad):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.vida_maxima = vida
        self.fila = None
        self.columna = None
        self.daño = daño
        self.velocidad = velocidad
        self.habilidad = habilidad
        self.turnos_habilidad = turnos_habilidad
        self.turnos_restantes = 0
        self.tipo = ""
    
    def obtener_info(self):
        return f"{self.nombre}\nCosto: ${self.costo}\nVida: {self.vida}\nDaño: {self.daño}\nVelocidad: {self.velocidad}\nHabilidad: {self.habilidad}"


class Soldado(Unidad):
    #Soldado: atacante versátil con ataque doble
    def __init__(self):
        self.nombre = "Soldado"
        self.costo = 75
        self.vida = 80
        self.vida_maxima = 80
        self.fila = None
        self.columna = None
        self.daño = 20
        self.velocidad = 2
        self.habilidad = "Ataque Doble (2 golpes)"
        self.turnos_habilidad = 3
        self.turnos_restantes = 0
        self.tipo = "soldado"


class Arquero(Unidad):
    #Arquero: daño extra contra torres
    def __init__(self):
        self.nombre = "Arquero"
        self.costo = 100
        self.vida = 60
        self.vida_maxima = 60
        self.fila = None
        self.columna = None
        self.daño = 18
        self.velocidad = 3
        self.habilidad = "Daño Extra contra Torres (+50%)"
        self.turnos_habilidad = 2
        self.turnos_restantes = 0
        self.tipo = "arquero"


class Mago(Unidad):
    #Mago: unidad de soporte con habilidad de curación
    def __init__(self):
        self.nombre = "Mago"
        self.costo = 120
        self.vida = 70
        self.vida_maxima = 70
        self.fila = None
        self.columna = None
        self.daño = 12
        self.velocidad = 2
        self.habilidad = "Curación (restaura 40 vida a aliado)"
        self.turnos_habilidad = 3
        self.turnos_restantes = 0
        self.tipo = "mago"


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
        self.nombre = nombre
        self.rol = "Defensor"
        self.dinero = 500
        self.base = None
        self.defensas = []
    
    def ganar_por_eliminar_unidad(self, tipo_unidad):
        #Gana dinero al eliminar una unidad enemiga
        recompensas = {
            "Soldado": 50,
            "Arquero": 60,
            "Mago": 75
        }
        cantidad = recompensas.get(tipo_unidad, 0)
        self.ganar_dinero(cantidad)
        return cantidad


class Atacante(Jugador):
    def __init__(self, nombre):
        self.nombre = nombre
        self.rol = "Atacante"
        self.dinero = 500
        self.unidades = []
    
    def ganar_por_dañar_torre(self, tipo_torre):
        #Gana dinero por dañar una torre
        recompensas = {
            "Torre Básica": 30,
            "Torre Pesada": 60,
            "Torre Mágica": 45
        }
        cantidad = recompensas.get(tipo_torre, 0)
        self.ganar_dinero(cantidad)
        return cantidad
    
    def ganar_por_destruir_torre(self, tipo_torre):
        #Gana dinero por destruir una torre
        recompensas = {
            "Torre Básica": 80,
            "Torre Pesada": 150,
            "Torre Mágica": 120
        }
        cantidad = recompensas.get(tipo_torre, 0)
        self.ganar_dinero(cantidad)
        return cantidad
    
    def ganar_por_dañar_base(self):
        #Gana dinero por dañar la base
        cantidad = 100
        self.ganar_dinero(cantidad)
        return cantidad


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
fase = "defensor_base"
elemento_actual = None
tipo_elemento_actual = None

# Referencias a elementos en el mapa
objetos_en_mapa = {}  # {(fila, col): objeto}

# DICCIONARIO DE IMÁGENES
imagenes = {}



# FUNCIONES DE CARGA DE IMÁGENES

def cargar_imagenes():
    #Carga imágenes PNG desde carpeta imagenes/elementos/
    global imagenes
    
    ruta_base = "imagenes/elementos/"
    ruta_fondo = "imagenes/fondo/"

    fondo = ["fondo"]
    
    elementos = [
        "muro",
        "torre_basica",
        "torre_pesada",
        "torre_magica",
        "soldado",
        "arquero",
        "mago",
        "base"
    ]
    
    
    for elemento in elementos:
        # Intentar cargar PNG (Python 3.13+)
        ruta_png = os.path.join(ruta_base, f"{elemento}.png")
        
        imagen_cargada = False
        
        if os.path.exists(ruta_png):
            imagen = tk.PhotoImage(file=ruta_png)
            imagenes[elemento] = imagen
            imagen_cargada = True
        
        
        # Si no se cargó nada
        if not imagen_cargada:
            imagenes[elemento] = None
                



# FUNCIONES DEL JUEGO

def dibujar_mapa():
    #Dibuja el mapa con sprites PNG desde carpeta
    canvas.delete("all")
    
    
    canvas.create_image(0, 0, anchor = 'nw', image=fondo_img)
    
    # Cuadrícula
    for fila in range(ALTO + 1):
        y = fila * TAM_CELDA
        canvas.create_line(0, y, ANCHO * TAM_CELDA, y, fill="#CCCCCC", width=1)
    
    for col in range(ANCHO + 1):
        x = col * TAM_CELDA
        canvas.create_line(x, 0, x, ALTO * TAM_CELDA, fill="#CCCCCC", width=1)
    
    # Dibujar elementos
    for fila in range(ALTO):
        for col in range(ANCHO):
            x = col * TAM_CELDA
            y = fila * TAM_CELDA
            
            # Buscar objeto en esta celda
            if (fila, col) in objetos_en_mapa:
                objeto = objetos_en_mapa[(fila, col)]
                tipo = objeto.tipo
                
                # Intentar mostrar imagen
                if tipo in imagenes and imagenes[tipo] is not None:
                    # Mostrar sprite
                    canvas.create_image(
                        x + TAM_CELDA // 2,
                        y + TAM_CELDA // 2,
                        image=imagenes[tipo]
                    )
               


def actualizar_labels():
    #Actualiza los labels de fase y dinero
    if fase == "defensor_base":
        label_fase.config(text="FASE: Defensor coloca BASE")
        label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
    elif fase == "defensor_defensas":
        label_fase.config(text="FASE: Defensor coloca MUROS y TORRES")
        label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
    elif fase == "atacante_unidades":
        label_fase.config(text="FASE: Atacante coloca UNIDADES")
        label_dinero.config(text=f"Dinero Atacante: ${atacante.dinero}")


def limpiar_botones():
    #Elimina todos los botones de acción
    for widget in frame_botones_accion.winfo_children():
        widget.destroy()


def crear_botones():
    #Crea los botones según la fase actual
    limpiar_botones()
    
    if fase == "defensor_base":
        btn = tk.Button(frame_botones_accion, text="Colocar Base", 
                       command=lambda: seleccionar_elemento("base", "Base Central"), 
                       bg="#FFD700", width=12)
        btn.pack(side=tk.LEFT, padx=5)
    
    elif fase == "defensor_defensas":
        btn0 = tk.Button(frame_botones_accion, text="Muro ($50)", 
                        command=lambda: seleccionar_elemento("muro", "Muro"), 
                        bg="#8B4513", fg="white", width=10)
        btn0.pack(side=tk.LEFT, padx=3)
        
        btn1 = tk.Button(frame_botones_accion, text="Torre Básica ($100)", 
                        command=lambda: seleccionar_elemento("torre", "Torre Básica"), 
                        bg="#696969", fg="white", width=15)
        btn1.pack(side=tk.LEFT, padx=3)
        
        btn2 = tk.Button(frame_botones_accion, text="Torre Pesada ($200)", 
                        command=lambda: seleccionar_elemento("torre", "Torre Pesada"), 
                        bg="#404040", fg="white", width=15)
        btn2.pack(side=tk.LEFT, padx=3)
        
        btn3 = tk.Button(frame_botones_accion, text="Torre Mágica ($150)", 
                        command=lambda: seleccionar_elemento("torre", "Torre Mágica"), 
                        bg="#9370DB", fg="white", width=15)
        btn3.pack(side=tk.LEFT, padx=3)
    
    elif fase == "atacante_unidades":
        btn1 = tk.Button(frame_botones_accion, text="Soldado ($75)", 
                        command=lambda: seleccionar_elemento("unidad", "Soldado"), 
                        bg="#FF6347", fg="white", width=12)
        btn1.pack(side=tk.LEFT, padx=3)
        
        btn2 = tk.Button(frame_botones_accion, text="Arquero ($100)", 
                        command=lambda: seleccionar_elemento("unidad", "Arquero"), 
                        bg="#DC143C", fg="white", width=12)
        btn2.pack(side=tk.LEFT, padx=3)
        
        btn3 = tk.Button(frame_botones_accion, text="Mago ($120)", 
                        command=lambda: seleccionar_elemento("unidad", "Mago"), 
                        bg="#FF8C00", fg="white", width=12)
        btn3.pack(side=tk.LEFT, padx=3)


def seleccionar_elemento(tipo, subtipo):
    #Selecciona el tipo de elemento a colocar
    global elemento_actual, tipo_elemento_actual
    
    costos = {
        "Muro": 50,
        "Torre Básica": 100,
        "Torre Pesada": 200,
        "Torre Mágica": 150,
        "Soldado": 75,
        "Arquero": 100,
        "Mago": 120,
        "Base Central": 0
    }
    
    costo = costos.get(subtipo, 0)
    
    if tipo == "muro" and not defensor.puede_comprar(50):
        messagebox.showerror("Error", "No tienes dinero para un muro ($50)")
        return
    elif tipo == "torre":
        jugador = defensor
        if not jugador.puede_comprar(costo):
            messagebox.showerror("Error", f"No tienes dinero para {subtipo} (${costo})")
            return
    elif tipo == "unidad":
        jugador = atacante
        if not jugador.puede_comprar(costo):
            messagebox.showerror("Error", f"No tienes dinero para {subtipo} (${costo})")
            return
    
    elemento_actual = tipo
    tipo_elemento_actual = subtipo
    label_estado.config(text=f"Colocando {subtipo} - Haz clic en el mapa (clic derecho para cancelar)")
    label_estado.config(fg="green")


def cancelar_elemento():
    #Cancela la colocación actual
    global elemento_actual, tipo_elemento_actual
    elemento_actual = None
    tipo_elemento_actual = None
    label_estado.config(text="")


def on_canvas_click(event):
    #Maneja los clics en el canvas
    global elemento_actual, tipo_elemento_actual
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
            
            elemento_actual = None
            tipo_elemento_actual = None
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
            label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
        else:
            messagebox.showerror("Error", "No tienes dinero suficiente")
    
    # DEFENSOR - TORRES
    elif elemento_actual == "torre":
        if tipo_elemento_actual == "Torre Básica":
            if defensor.gastar_dinero(100):
                torre = TorreBasica()
                defensor.defensas.append(torre)
                matriz[fila][col] = 2
                objetos_en_mapa[(fila, col)] = torre
                exito = True
                label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
        elif tipo_elemento_actual == "Torre Pesada":
            if defensor.gastar_dinero(200):
                torre = TorrePesada()
                defensor.defensas.append(torre)
                matriz[fila][col] = 2
                objetos_en_mapa[(fila, col)] = torre
                exito = True
                label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
        elif tipo_elemento_actual == "Torre Mágica":
            if defensor.gastar_dinero(150):
                torre = TorreMagica()
                defensor.defensas.append(torre)
                matriz[fila][col] = 2
                objetos_en_mapa[(fila, col)] = torre
                exito = True
                label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
        
        if not exito:
            messagebox.showerror("Error", "No tienes dinero suficiente")
    
    # ATACANTE - UNIDADES
    elif elemento_actual == "unidad":
        if tipo_elemento_actual == "Soldado":
            if atacante.gastar_dinero(75):
                unidad = Soldado()
                atacante.unidades.append(unidad)
                matriz[fila][col] = 3
                objetos_en_mapa[(fila, col)] = unidad
                exito = True
                label_dinero.config(text=f"Dinero Atacante: ${atacante.dinero}")
        elif tipo_elemento_actual == "Arquero":
            if atacante.gastar_dinero(100):
                unidad = Arquero()
                atacante.unidades.append(unidad)
                matriz[fila][col] = 3
                objetos_en_mapa[(fila, col)] = unidad
                exito = True
                label_dinero.config(text=f"Dinero Atacante: ${atacante.dinero}")
        elif tipo_elemento_actual == "Mago":
            if atacante.gastar_dinero(120):
                unidad = Mago()
                atacante.unidades.append(unidad)
                matriz[fila][col] = 3
                objetos_en_mapa[(fila, col)] = unidad
                exito = True
                label_dinero.config(text=f"Dinero Atacante: ${atacante.dinero}")
        
        if not exito:
            messagebox.showerror("Error", "No tienes dinero suficiente")
    
    if exito:
        dibujar_mapa()


def on_canvas_right_click(event):
    #Cancela con clic derecho
    cancelar_elemento()


def mostrar_info_torres():
    #Muestra información detallada de todas las torres
    info = "TORRES DISPONIBLES\n\n"
    torres = [TorreBasica(), TorrePesada(), TorreMagica()]
    for torre in torres:
        info += torre.obtener_info() + "\n\n"
    messagebox.showinfo("Información de Torres", info)


def mostrar_info_unidades():
    #Muestra información detallada de todas las unidades
    info = "UNIDADES DISPONIBLES\n\n"
    unidades = [Soldado(), Arquero(), Mago()]
    for unidad in unidades:
        info += unidad.obtener_info() + "\n\n"
    messagebox.showinfo("Información de Unidades", info)


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
        
        resumen = f"""

      ¡PREPARACIÓN COMPLETADA!         


DEFENSOR:
  • Base: 1
  • Defensas: {len(defensor.defensas)}
  • Dinero: ${defensor.dinero}

ATACANTE:
  • Unidades: {len(atacante.unidades)}
  • Dinero: ${atacante.dinero}

La batalla está lista para comenzar.
        """
        messagebox.showinfo("¡Listo!", resumen)
        return
    
    cancelar_elemento()
    actualizar_labels()
    crear_botones()
    label_estado.config(text="")
    dibujar_mapa()


# INTERFAZ GRÁFICA

ventana = tk.Tk()
ventana.title("Avgrunnens Battle Royale")

ventana.state("zoomed")

fondo_img = tk.PhotoImage(file='fondo.png')

# Frame superior con información
frame_info = tk.Frame(ventana)
frame_info.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

label_fase = tk.Label(frame_info, text="", font=("Arial", 12, "bold"), fg="#2E7D32")
label_fase.pack(anchor=tk.W)

label_dinero = tk.Label(frame_info, text="", font=("Arial", 11), fg="#1565C0")
label_dinero.pack(anchor=tk.W)

label_estado = tk.Label(frame_info, text="", font=("Arial", 10))
label_estado.pack(anchor=tk.W)

# Canvas del mapa
canvas = tk.Canvas(
    ventana,
    width=ANCHO * TAM_CELDA,
    height=ALTO * TAM_CELDA,
    bg="black",
    cursor="cross",
    relief=tk.SUNKEN,
    bd=2
)
canvas.pack(padx=10, pady=10)
canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<Button-3>", on_canvas_right_click)

# Frame inferior con botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

frame_botones_accion = tk.Frame(frame_botones)
frame_botones_accion.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Frame botones de utilidad
frame_botones_util = tk.Frame(frame_botones)
frame_botones_util.pack(side=tk.RIGHT)

btn_siguiente = tk.Button(frame_botones_util, text="Siguiente", command=siguiente_fase, 
                         font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=10)
btn_siguiente.pack(side=tk.LEFT, padx=5)

btn_cancelar = tk.Button(frame_botones_util, text="Cancelar", command=cancelar_elemento, 
                        font=("Arial", 9), bg="#f44336", fg="white", width=10)
btn_cancelar.pack(side=tk.LEFT, padx=2)

btn_torres = tk.Button(frame_botones_util, text="Info Torres", command=mostrar_info_torres, 
                      font=("Arial", 9), bg="#FF9800", fg="white", width=10)
btn_torres.pack(side=tk.LEFT, padx=2)

btn_unidades = tk.Button(frame_botones_util, text="Info Unidades", command=mostrar_info_unidades, 
                        font=("Arial", 9), bg="#2196F3", fg="white", width=10)
btn_unidades.pack(side=tk.LEFT, padx=2)

# Cargar imágenes desde carpeta
cargar_imagenes()

# Iniciar
actualizar_labels()
crear_botones()
dibujar_mapa()

ventana.mainloop()
