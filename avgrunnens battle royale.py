import tkinter as tk
from tkinter import messagebox
import os


# CLASES
#zx
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
        self.vida = 75
        self.vida_maxima = 75
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
        self.vida = 60
        self.vida_maxima = 60
        self.fila = None
        self.columna = None
        self.daño = 20
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
        self.vida = 150
        self.vida_maxima = 150
        self.fila = None
        self.columna = None
        self.daño = 35
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
        self.vida = 250
        self.vida_maxima = 250
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
        self.vida = 120
        self.vida_maxima = 120
        self.fila = None
        self.columna = None
        self.daño = 35
        self.velocidad = 2
        self.habilidad = "Ataque Doble (2 golpes)"
        self.turnos_habilidad = 3
        self.turnos_restantes = 0
        self.tipo = "soldado"
        self.turnos_congelada = 0


class Arquero(Unidad):
    #Arquero: daño extra contra torres
    def __init__(self):
        self.nombre = "Arquero"
        self.costo = 100
        self.vida = 100
        self.vida_maxima = 100
        self.fila = None
        self.columna = None
        self.daño = 25
        self.velocidad = 3
        self.habilidad = "Daño Extra contra Torres (+50%)"
        self.turnos_habilidad = 2
        self.turnos_restantes = 0
        self.tipo = "arquero"
        self.turnos_congelada = 0


class Mago(Unidad):
    #Mago: unidad de soporte con habilidad de curación
    def __init__(self):
        self.nombre = "Mago"
        self.costo = 120
        self.vida = 80
        self.vida_maxima = 80
        self.fila = None
        self.columna = None
        self.daño = 20
        self.velocidad = 2
        self.habilidad = "Curación (restaura 40 vida a aliado)"
        self.turnos_habilidad = 3
        self.turnos_restantes = 0
        self.tipo = "mago"
        self.turnos_congelada = 0


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
        self.dinero_por_dano_ronda = 0
    
    def ganar_por_eliminar_unidad(self, tipo_unidad):
        #Gana dinero al eliminar una unidad enemiga
        recompensas = {
            "Soldado": 80,
            "Arquero": 150,
            "Mago": 120
        }
        cantidad = recompensas.get(tipo_unidad, 0)
        self.dinero_por_dano_ronda=self.dinero_por_dano_ronda+cantidad
        return cantidad
    def ganar_por_dañar_unidad(self, tipo_unidad):
        #Gana dinero al dañar una unidad enemiga
        recompensas = {
            "Soldado": 30,
            "Arquero": 60,
            "Mago": 45
        }
        cantidad = recompensas.get(tipo_unidad, 0)
        self.dinero_por_dano_ronda=self.dinero_por_dano_ronda+cantidad
        return cantidad


class Atacante(Jugador):
    def __init__(self, nombre):
        self.nombre = nombre
        self.rol = "Atacante"
        self.dinero = 500
        self.unidades = []
        self.dinero_por_dano_ronda = 0
    
    def ganar_por_dañar_torre(self, tipo_torre):
        #Gana dinero por dañar una torre
        recompensas = {
            "Torre Básica": 30,
            "Torre Pesada": 60,
            "Torre Mágica": 45
        }
        cantidad = recompensas.get(tipo_torre, 0)
        self.dinero_por_dano_ronda=self.dinero_por_dano_ronda+cantidad
        return cantidad
    
    def ganar_por_destruir_torre(self, tipo_torre):
        #Gana dinero por destruir una torre
        recompensas = {
            "Torre Básica": 80,
            "Torre Pesada": 150,
            "Torre Mágica": 120
        }
        cantidad = recompensas.get(tipo_torre, 0)
        self.dinero_por_dano_ronda=self.dinero_por_dano_ronda+cantidad
        return cantidad
    
    def ganar_por_destruir_base(self):
        #Gana dinero por dañar la base
        cantidad = 100
        self.dinero_por_dano_ronda= self.dinero_por_dano_ronda+cantidad
        return cantidad


class SistemaDinero:
    def __init__(self):
        self.bono_por_ronda = 100

    def iniciar_ronda(self, defensor, atacante):
        defensor.dinero = defensor.dinero + self.bono_por_ronda
        atacante.dinero = atacante.dinero + self.bono_por_ronda
        atacante.dinero = atacante.dinero + atacante.dinero_por_dano_ronda
        defensor.dinero = defensor.dinero + defensor.dinero_por_dano_ronda
        

    def comprar(self, jugador, costo):
        if jugador.dinero >= costo:
            jugador.dinero = jugador.dinero - costo
            return True
        else:
            return False

    def defensor_gana_por_unidad(self, defensor, dinero_ganado):
        defensor.dinero = defensor.dinero + dinero_ganado

    def atacante_gana_por_dano(self, atacante, dano):
        dinero_ganado = dano * 5
        atacante.dinero_por_dano_ronda = atacante.dinero_por_dano_ronda + dinero_ganado

    def defensor_gana_por_dano(self, defensor, dano):
        dinero_ganado = dano * 5
        defensor.dinero_por_dano_ronda = defensor.dinero_por_dano_ronda + dinero_ganado


class TopJugadores:
    def __init__(self):
        self.archivo = "top_jugadores.txt"

    def registrar_victoria(self, nombre, rol):
        jugadores = self.leer_jugadores()
        encontrado = False

        for jugador in jugadores:
            if jugador[0] == nombre:
                if rol == "Defensor":
                    jugador[1] = jugador[1] + 1
                elif rol == "Atacante":
                    jugador[2] = jugador[2] + 1
                encontrado = True

        if encontrado == False:
            if rol == "Defensor":
                jugadores.append([nombre, 1, 0])
            elif rol == "Atacante":
                jugadores.append([nombre, 0, 1])

        self.guardar_jugadores(jugadores)

    def leer_jugadores(self):
        jugadores = []

        if os.path.exists(self.archivo) == False:
            return jugadores

        archivo = open(self.archivo, "r")
        lineas = archivo.readlines()
        archivo.close()

        for linea in lineas:
            datos = linea.strip().split(",")
            if len(datos) == 3:
                nombre = datos[0]
                victorias_defensor = int(datos[1])
                victorias_atacante = int(datos[2])
                jugadores.append([nombre, victorias_defensor, victorias_atacante])

        return jugadores

    def guardar_jugadores(self, jugadores):
        archivo = open(self.archivo, "w")

        for jugador in jugadores:
            linea = f"{jugador[0]},{jugador[1]},{jugador[2]}\n"
            archivo.write(linea)

        archivo.close()

    def top_defensores(self):
        jugadores = self.leer_jugadores()
        jugadores.sort(key=lambda jugador: jugador[1], reverse=True)
        return jugadores[:5]

    def top_atacantes(self):
        jugadores = self.leer_jugadores()
        jugadores.sort(key=lambda jugador: jugador[2], reverse=True)
        return jugadores[:5]


def mostrar_top_jugadores():
    top = TopJugadores()

    ventana_top = tk.Toplevel(ventana)
    ventana_top.title("Top de jugadores")
    ventana_top.geometry("450x350")

    titulo = tk.Label(ventana_top, text="TOP DE JUGADORES", font=("Arial", 16, "bold"))
    titulo.pack(pady=10)

    tk.Label(ventana_top, text="Top defensores", font=("Arial", 13, "bold")).pack()

    defensores = top.top_defensores()
    if len(defensores) == 0:
        tk.Label(ventana_top, text="No hay victorias registradas").pack()
    else:
        for i, jugador in enumerate(defensores, start=1):
            texto = f"{i}. {jugador[0]} - {jugador[1]} victoria(s)"
            tk.Label(ventana_top, text=texto).pack()

    tk.Label(ventana_top, text="Top atacantes", font=("Arial", 13, "bold")).pack(pady=(15,0))

    atacantes = top.top_atacantes()
    if len(atacantes) == 0:
        tk.Label(ventana_top, text="No hay victorias registradas").pack()
    else:
        for i, jugador in enumerate(atacantes, start=1):
            texto = f"{i}. {jugador[0]} - {jugador[2]} victoria(s)"
            tk.Label(ventana_top, text=texto).pack()


# VARIABLES GLOBALES

ANCHO = 11
ALTO = 11
TAM_CELDA = 50 

# Matriz: 0=vacío, 1=muro, 2=torre, 3=unidad, 4=base
matriz = [[0 for _ in range(ANCHO)] for _ in range(ALTO)]

# Jugadores
defensor = Defensor("Defensor 1")
atacante = Atacante("Atacante 1")
sistema_dinero = SistemaDinero()
top_jugadores = TopJugadores()

# Estado del juego
fase = "defensor_base"
elemento_actual = None
tipo_elemento_actual = None

# ── SISTEMA DE RONDAS ──────────────────────────────────────────
victorias_defensor = 0
victorias_atacante = 0
ronda_actual = 1
resultado_rondas = []
registro_victorias = {}

# ── SISTEMA DE COMBATE ─────────────────────────────────────────
turno_combate = 0        # número del turno actual
log_combate = []         # mensajes de lo que pasó en cada turno
combate_en_curso = False # True mientras la animación corre

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
        # Intentar cargar PNG 
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
    
    if fondo_img is not None:
        canvas.create_image(0, 0, anchor = 'nw', image=fondo_img)
    else:
        canvas.create_rectangle(0, 0, ANCHO * TAM_CELDA, ALTO * TAM_CELDA, fill="#eeeeee", outline="")
    
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
            
            if (fila, col) in objetos_en_mapa:
                objeto = objetos_en_mapa[(fila, col)]
                tipo = objeto.tipo
                
                # Mostrar imagen del sprite
                if tipo in imagenes and imagenes[tipo] is not None:
                    canvas.create_image(
                        x + TAM_CELDA // 2,
                        y + TAM_CELDA // 2,
                        image=imagenes[tipo]
                    )
                else:
                    # Si no hay imagen, dibujar un rectángulo de color según el tipo
                    colores = {
                        "muro": "#8B4513", "torre_basica": "#696969",
                        "torre_pesada": "#404040", "torre_magica": "#9370DB",
                        "soldado": "#FF6347", "arquero": "#DC143C",
                        "mago": "#FF8C00", "base": "#FFD700"
                    }
                    color = colores.get(tipo, "#AAAAAA")
                    canvas.create_rectangle(x+3, y+3, x+TAM_CELDA-3, y+TAM_CELDA-3, fill=color, outline="white")
                    canvas.create_text(x + TAM_CELDA//2, y + TAM_CELDA//2,
                                       text=objeto.nombre[:3], fill="white", font=("Arial", 7, "bold"))

                # Barra de vida (solo durante el combate)
                if fase == "combate" and hasattr(objeto, "vida_maxima") and objeto.vida_maxima > 0:
                    barra_y = y + TAM_CELDA - 7
                    barra_w = TAM_CELDA - 4
                    porcentaje = max(0, objeto.vida / objeto.vida_maxima)
                    # Fondo rojo
                    canvas.create_rectangle(x+2, barra_y, x+2+barra_w, barra_y+5, fill="#CC0000", outline="")
                    # Vida restante en verde
                    canvas.create_rectangle(x+2, barra_y, x+2+int(barra_w*porcentaje), barra_y+5, fill="#00CC00", outline="")

                # Símbolo de congelado
                if fase == "combate" and hasattr(objeto, "turnos_congelada") and objeto.turnos_congelada > 0:
                    canvas.create_text(x + TAM_CELDA//2, y+8, text="❄", font=("Arial", 11, "bold"), fill="#00BFFF")


def actualizar_labels():
    #Actualiza los labels de fase y dinero
    if fase == "defensor_base":
        label_fase.config(text=f"RONDA {ronda_actual} — FASE: Defensor coloca BASE")
        label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
    elif fase == "defensor_defensas":
        label_fase.config(text=f"RONDA {ronda_actual} — FASE: Defensor coloca MUROS y TORRES")
        label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
    elif fase == "atacante_unidades":
        label_fase.config(text=f"RONDA {ronda_actual} — FASE: Atacante coloca UNIDADES")
        label_dinero.config(text=f"Dinero Atacante: ${atacante.dinero}")
        label_estado.config(
            text=f"Marcador → Defensor: {victorias_defensor}  |  Atacante: {victorias_atacante}",
            fg="#8B0000"
        )
    elif fase == "combate":
        label_fase.config(text=f"RONDA {ronda_actual} — COMBATE — Turno {turno_combate}", fg="#B71C1C")
        label_dinero.config(text=f"Defensor: ${defensor.dinero}  |  Atacante: ${atacante.dinero}")
        label_estado.config(
            text=f"Marcador → Defensor: {victorias_defensor}  |  Atacante: {victorias_atacante}",
            fg="#8B0000"
        )


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
    
    elif fase == "combate":
        # Durante el combate solo se muestra el botón de iniciar (se deshabilita al comenzar)
        btn_combate = tk.Button(frame_botones_accion,
                                text="Iniciar Combate",
                                command=iniciar_combate,
                                bg="#B71C1C", fg="white",
                                font=("Arial", 11, "bold"), width=16)
        btn_combate.pack(side=tk.LEFT, padx=10)
    
    elif fase == "combate":
        # Botón para resolver el combate y determinar el ganador de la ronda
        btn_combate = tk.Button(frame_botones_accion,
                                text="Iniciar Combate",
                                command=finalizar_fase_combate,
                                bg="#B71C1C", fg="white",
                                font=("Arial", 11, "bold"), width=16)
        btn_combate.pack(side=tk.LEFT, padx=10)


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


RONDA {ronda_actual}
DEFENSOR:
  • Base: 1
  • Defensas: {len(defensor.defensas)}
  • Dinero: ${defensor.dinero}

ATACANTE:
  • Unidades: {len(atacante.unidades)}
  • Dinero: ${atacante.dinero}

Presiona "Iniciar Combate" para ver la batalla.
        """
        messagebox.showinfo("¡Listo!", resumen)
        # Cambiar a fase combate (con global ya declarado arriba)
        fase = "combate"
        cancelar_elemento()
        actualizar_labels()
        crear_botones()
        label_estado.config(text="")
        dibujar_mapa()
        return
    
    cancelar_elemento()
    actualizar_labels()
    crear_botones()
    label_estado.config(text="")
    dibujar_mapa()


# ── FUNCIONES DEL SISTEMA DE RONDAS ───────────────────────────

def reiniciar_ronda():
    global fase, elemento_actual, tipo_elemento_actual, objetos_en_mapa, matriz
    global turno_combate, log_combate, combate_en_curso

    # Borrar el mapa
    objetos_en_mapa = {}
    for f in range(ALTO):
        for c in range(ANCHO):
            matriz[f][c] = 0

    # Resetear jugadores
    sistema_dinero.iniciar_ronda(defensor, atacante)
    defensor.base = None
    defensor.defensas = []
    atacante.unidades = []

    # Resetear combate
    turno_combate = 0
    log_combate = []
    combate_en_curso = False

    # Volver al inicio
    fase = "defensor_base"
    elemento_actual = None
    tipo_elemento_actual = None

    cancelar_elemento()
    actualizar_labels()
    crear_botones()
    label_estado.config(text="")
    dibujar_mapa()


def verificar_ganador_ronda():
    # Atacante gana si destruyó la base
    if defensor.base is None:
        return "atacante"

    # Defensor gana si el atacante no tiene dinero, no tiene unidades y la base sigue viva
    if atacante.dinero <= 0 and len(atacante.unidades) == 0 and defensor.base is not None:
        return "defensor"

    # Nadie ganó todavía
    return None


def registrar_ganador_ronda(ganador):
    global victorias_defensor, victorias_atacante, resultado_rondas, ronda_actual

    resultado_rondas.append(ganador)

    if ganador == "defensor":
        victorias_defensor += 1
        messagebox.showinfo("Ronda terminada",
                            f"¡El DEFENSOR ganó la ronda {ronda_actual}!\n"
                            f"Marcador → Defensor: {victorias_defensor}  |  Atacante: {victorias_atacante}")
    else:
        victorias_atacante += 1
        messagebox.showinfo("Ronda terminada",
                            f"¡El ATACANTE ganó la ronda {ronda_actual}!\n"
                            f"Marcador → Defensor: {victorias_defensor}  |  Atacante: {victorias_atacante}")

    ganador_partida = verificar_ganador_partida()
    if ganador_partida:
        terminar_partida(ganador_partida)
    else:
        ronda_actual += 1
        messagebox.showinfo("Nueva ronda",
                            f"¡Comienza la Ronda {ronda_actual}!\n"
                            "Los jugadores reciben $100 extra.\n"
                            "Reciben además el dinero acumulado por daño de la ronda anterior.")
        reiniciar_ronda()


def verificar_ganador_partida():
    if victorias_defensor == 2:
        return "defensor"
    if victorias_atacante == 2:
        return "atacante"
    return None


def terminar_partida(ganador):
    global registro_victorias

    if ganador == "defensor":
        jugador_ganador = defensor
        mensaje = f"¡{defensor.nombre} (Defensor) GANÓ LA PARTIDA!"
    else:
        jugador_ganador = atacante
        mensaje = f"¡{atacante.nombre} (Atacante) GANÓ LA PARTIDA!"

    top_jugadores.registrar_victoria(jugador_ganador.nombre, jugador_ganador.rol)

    clave = f"{jugador_ganador.nombre} ({jugador_ganador.rol})"
    if clave in registro_victorias:
        registro_victorias[clave] += 1
    else:
        registro_victorias[clave] = 1

    historial = "\n".join([f"  • {n}: {w} victoria(s)" for n, w in registro_victorias.items()])
    messagebox.showinfo("¡Partida terminada!",
                        f"{mensaje}\n\n"
                        f"Resultado: Defensor {victorias_defensor} - Atacante {victorias_atacante}\n\n"
                        f"Registro de victorias:\n{historial}")


# ── SISTEMA DE COMBATE ANIMADO ─────────────────────────────────

def distancia(a, b):
    #Distancia en celdas entre dos objetos
    return abs(a.fila - b.fila) + abs(a.columna - b.columna)


def buscar_mas_cercano(origen, lista_objetivos):
    #Devuelve el objeto más cercano de la lista
    mejor = None
    menor_d = 9999
    for obj in lista_objetivos:
        d = distancia(origen, obj)
        if d < menor_d:
            menor_d = d
            mejor = obj
    return mejor


def mover_hacia(unidad, objetivo):
    #Mueve la unidad un paso en dirección al objetivo si hay celda libre
    global objetos_en_mapa, matriz

    f_act = unidad.fila
    c_act = unidad.columna
    df = objetivo.fila - f_act
    dc = objetivo.columna - c_act

    # Armar lista de celdas candidatas en orden de preferencia
    candidatos = []
    if abs(df) >= abs(dc):
        if df != 0: candidatos.append((f_act + (1 if df > 0 else -1), c_act))
        if dc != 0: candidatos.append((f_act, c_act + (1 if dc > 0 else -1)))
    else:
        if dc != 0: candidatos.append((f_act, c_act + (1 if dc > 0 else -1)))
        if df != 0: candidatos.append((f_act + (1 if df > 0 else -1), c_act))

    for nf, nc in candidatos:
        if 0 <= nf < ALTO and 0 <= nc < ANCHO and matriz[nf][nc] == 0:
            # Mover la unidad
            del objetos_en_mapa[(f_act, c_act)]
            matriz[f_act][c_act] = 0
            unidad.fila = nf
            unidad.columna = nc
            matriz[nf][nc] = 3
            objetos_en_mapa[(nf, nc)] = unidad
            return True
    return False


def eliminar_objeto(obj):
    #Quita un objeto del mapa y de las listas de su dueño
    global objetos_en_mapa, matriz
    pos = (obj.fila, obj.columna)
    if pos in objetos_en_mapa:
        del objetos_en_mapa[pos]
        matriz[obj.fila][obj.columna] = 0
    if obj in defensor.defensas:
        defensor.defensas.remove(obj)
    if obj in atacante.unidades:
        atacante.unidades.remove(obj)
    if obj.tipo == "base":
        defensor.base = None


def fase_torres(msgs):
    #Las torres atacan a las unidades más cercanas dentro de su alcance
    tipos_torre = ("torre_basica", "torre_pesada", "torre_magica")
    torres = [d for d in list(defensor.defensas) if d.tipo in tipos_torre]

    for torre in torres:
        if not atacante.unidades:
            break

        # Buscar unidad más cercana dentro del alcance
        objetivo = None
        menor_d = 9999
        for u in atacante.unidades:
            d = distancia(torre, u)
            if d <= torre.alcance and d < menor_d:
                menor_d = d
                objetivo = u
        if objetivo is None:
            continue

        # Torre Básica: Disparo Doble cada turnos_habilidad turnos
        if torre.tipo == "torre_basica":
            torre.turnos_restantes += 1
            veces = 1
            if torre.turnos_restantes >= torre.turnos_habilidad:
                veces = 2
                torre.turnos_restantes = 0
                msgs.append(f"Torre Básica usa DISPARO DOBLE sobre {objetivo.nombre}!")
            for _ in range(veces):
                if objetivo.vida > 0:
                    objetivo.vida -= torre.daño
                    msgs.append(f"Torre Básica → {objetivo.nombre}: -{torre.daño} vida ({max(0,objetivo.vida)} restante)")

        # Torre Pesada: Daño en Área cada turnos_habilidad turnos
        elif torre.tipo == "torre_pesada":
            torre.turnos_restantes += 1
            if torre.turnos_restantes >= torre.turnos_habilidad:
                torre.turnos_restantes = 0
                msgs.append(f"Torre Pesada usa DAÑO EN ÁREA!")
                for u in list(atacante.unidades):
                    if distancia(torre, u) <= 3:
                        u.vida -= torre.daño
                        msgs.append(f"{u.nombre}: -{torre.daño} vida ({max(0,u.vida)} restante)")
            else:
                objetivo.vida -= torre.daño
                msgs.append(f"Torre Pesada → {objetivo.nombre}: -{torre.daño} vida ({max(0,objetivo.vida)} restante)")

        # Torre Mágica: ataca y cada turnos_habilidad turnos congela
        elif torre.tipo == "torre_magica":
            torre.turnos_restantes += 1
            objetivo.vida -= torre.daño
            msgs.append(f"Torre Mágica → {objetivo.nombre}: -{torre.daño} vida ({max(0,objetivo.vida)} restante)")
            if torre.turnos_restantes >= torre.turnos_habilidad:
                torre.turnos_restantes = 0
                objetivo.turnos_congelada = 2
                msgs.append(f"  ❄ {objetivo.nombre} queda CONGELADO por 2 turnos!")


def fase_unidades(msgs):
    #Las unidades atacantes se mueven hacia defensas o atacan si están adyacentes
    for unidad in list(atacante.unidades):
        # Si está congelada, descontar un turno y saltar
        if unidad.turnos_congelada > 0:
            unidad.turnos_congelada -= 1
            msgs.append(f"  ❄ {unidad.nombre} está congelado ({unidad.turnos_congelada} turnos restantes)")
            continue

        # Lista de objetivos: muros, torres y la base
        objetivos = list(defensor.defensas)
        if defensor.base is not None:
            objetivos.append(defensor.base)
        if not objetivos:
            continue

        objetivo = buscar_mas_cercano(unidad, objetivos)
        if objetivo is None:
            continue

        d = distancia(unidad, objetivo)

        if d <= 1:
            # Está adyacente: ATACAR
            daño_real = unidad.daño

            # Arquero: cada turnos_habilidad ataques hace +50% daño contra torres
            if unidad.tipo == "arquero" and objetivo.tipo in ("torre_basica", "torre_pesada", "torre_magica"):
                unidad.turnos_restantes += 1
                if unidad.turnos_restantes >= unidad.turnos_habilidad:
                    unidad.turnos_restantes = 0
                    daño_real = int(unidad.daño * 1.5)
                    msgs.append(f"{unidad.nombre} usa DAÑO EXTRA contra torre!")

            # Soldado: cada turnos_habilidad turnos ataca dos veces
            veces = 1
            if unidad.tipo == "soldado":
                unidad.turnos_restantes += 1
                if unidad.turnos_restantes >= unidad.turnos_habilidad:
                    unidad.turnos_restantes = 0
                    veces = 2
                    msgs.append(f"{unidad.nombre} usa ATAQUE DOBLE!")

            for _ in range(veces):
                if objetivo.vida > 0:
                    objetivo.vida -= daño_real
                    # Si atacó una torre, el atacante gana dinero
                    if objetivo.tipo in ("torre_basica", "torre_pesada", "torre_magica"):
                        atacante.ganar_por_dañar_torre(objetivo.nombre)
        else:
            # No está adyacente: MOVERSE (velocidad = pasos por turno)
            pasos = 0
            for _ in range(unidad.velocidad):
                if distancia(unidad, objetivo) <= 1:
                    break
                if mover_hacia(unidad, objetivo):
                    pasos += 1
                else:
                    break
            if pasos > 0:
                msgs.append(f"{unidad.nombre} avanza {pasos} paso(s) hacia {objetivo.nombre}")

    # Mago: cura al aliado con menos vida cada turnos_habilidad turnos
    for unidad in list(atacante.unidades):
        if unidad.tipo == "mago" and unidad.turnos_congelada == 0:
            unidad.turnos_restantes += 1
            if unidad.turnos_restantes >= unidad.turnos_habilidad:
                unidad.turnos_restantes = 0
                aliados = [u for u in atacante.unidades if u != unidad]
                if aliados:
                    herido = min(aliados, key=lambda u: u.vida)
                    herido.vida = min(herido.vida + 40, herido.vida_maxima)
                    msgs.append(f"Mago cura a {herido.nombre} (+40 vida → {herido.vida})")


def eliminar_muertos(msgs):
    #Elimina todo lo que quedó con vida <= 0
    for obj in list(defensor.defensas):
        if obj.vida <= 0:
            if obj.tipo in ("torre_basica", "torre_pesada", "torre_magica"):
                ganado = atacante.ganar_por_destruir_torre(obj.nombre)
                msgs.append(f"Atacante gana ${ganado} por destruir {obj.nombre}")
            msgs.append(f"{obj.nombre} fue destruido!")
            eliminar_objeto(obj)

    if defensor.base is not None and defensor.base.vida <= 0:
        msgs.append(f"¡BASE CENTRAL DESTRUIDA!")
        eliminar_objeto(defensor.base)

    for obj in list(atacante.unidades):
        if obj.vida <= 0:
            ganado = defensor.ganar_por_eliminar_unidad(obj.nombre)
            msgs.append(f"{obj.nombre} eliminado! Defensor gana ${ganado}")
            eliminar_objeto(obj)


def iniciar_combate():
    #Arranca la animación de combate. Se llama al presionar el botón.
    global combate_en_curso, turno_combate, log_combate

    # Deshabilitar el botón para que no se pueda presionar dos veces
    limpiar_botones()

    combate_en_curso = True
    turno_combate = 0
    log_combate = []

    # Registrar posiciones iniciales en cada objeto
    for (f, c), obj in objetos_en_mapa.items():
        obj.fila = f
        obj.columna = c

    # Programar el primer turno con 300ms de retraso para que se vea el mapa primero
    ventana.after(300, ejecutar_turno)


def ejecutar_turno():
    #Ejecuta UN turno de combate y se programa a sí mismo para el siguiente
    global turno_combate, combate_en_curso

    if not combate_en_curso:
        return

    turno_combate += 1
    msgs = [f"── Turno {turno_combate} ──────────────"]

    # 1. Torres atacan a unidades
    fase_torres(msgs)

    # 2. Unidades se mueven o atacan
    fase_unidades(msgs)

    # 3. Eliminar muertos y dar recompensas
    eliminar_muertos(msgs)

    log_combate.extend(msgs)

    # Mostrar los últimos 5 mensajes en pantalla
    label_estado.config(text="\n".join(log_combate[-5:]), fg="#1a1a1a")
    label_fase.config(text=f"RONDA {ronda_actual} — COMBATE — Turno {turno_combate}", fg="#B71C1C")
    label_dinero.config(text=f"Defensor: ${defensor.dinero}  |  Atacante: ${atacante.dinero}")

    # Redibujar el mapa con las posiciones nuevas
    dibujar_mapa()

    # Forzar actualización visual antes de continuar
    ventana.update()

    # Verificar si ya hay ganador
    ganador = verificar_ganador_ronda()
    if ganador is not None:
        combate_en_curso = False
        ventana.after(1000, lambda: registrar_ganador_ronda(ganador))
        return

    # Límite de 40 turnos sin ganador → gana el defensor (la base sobrevivió)
    if turno_combate >= 40:
        combate_en_curso = False
        ventana.after(1000, lambda: registrar_ganador_ronda("defensor"))
        return

    # Programar el siguiente turno en 700ms (se puede bajar para más velocidad)
    ventana.after(1200, ejecutar_turno)


def finalizar_fase_combate():
    #Este botón ya no se usa, queda por compatibilidad
    iniciar_combate()

# ───────────────────────────────────────────────────────────────


# INTERFAZ GRÁFICA

ventana = tk.Tk()
ventana.title("Avgrunnens Battle Royale")
ventana.geometry("1400x900")
ventana.state("zoomed")

try:
    fondo_img = tk.PhotoImage(file='fondo.png')
except:
    fondo_img = None

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
                         font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=12)
btn_siguiente.pack(side=tk.LEFT, padx=5)

btn_cancelar = tk.Button(frame_botones_util, text="Cancelar", command=cancelar_elemento, 
                        font=("Arial", 9), bg="#f44336", fg="white", width=12)
btn_cancelar.pack(side=tk.LEFT, padx=2)

btn_torres = tk.Button(frame_botones_util, text="Info Torres", command=mostrar_info_torres, 
                      font=("Arial", 9), bg="#FF9800", fg="white", width=12)
btn_torres.pack(side=tk.LEFT, padx=2)

btn_unidades = tk.Button(frame_botones_util, text="Info Unidades", command=mostrar_info_unidades, 
                        font=("Arial", 9), bg="#2196F3", fg="white", width=12)
btn_unidades.pack(side=tk.LEFT, padx=2)

btn_top = tk.Button(frame_botones_util, text="Top", command=mostrar_top_jugadores,
                    font=("Arial", 9), bg="#9C27B0", fg="white", width=12)
btn_top.pack(side=tk.LEFT, padx=2)

# Cargar imágenes desde carpeta
cargar_imagenes()

# Iniciar
actualizar_labels()
crear_botones()
dibujar_mapa()

ventana.mainloop()
