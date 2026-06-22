import tkinter as tk
from tkinter import messagebox
import os
import json


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
        self.usuario = None

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
        self.usuario = None
    
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
        #Gana dinero al dañar una unidad enemiga (igualado al atacante)
        recompensas = {
            "Soldado": 10,
            "Arquero": 20,
            "Mago": 15
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
        self.usuario = None
    
    def ganar_por_dañar_torre(self, tipo_torre):
        #Gana dinero por dañar una torre (reducido para equilibrar)
        recompensas = {
            "Torre Básica": 10,
            "Torre Pesada": 20,
            "Torre Mágica": 15
        }
        cantidad = recompensas.get(tipo_torre, 0)
        self.dinero_por_dano_ronda=self.dinero_por_dano_ronda+cantidad
        return cantidad
    
    def ganar_por_destruir_torre(self, tipo_torre):
        #Gana dinero por destruir una torre (reducido para equilibrar)
        recompensas = {
            "Torre Básica": 80,
            "Torre Pesada": 150,
            "Torre Mágica": 120
        }
        cantidad = recompensas.get(tipo_torre, 0)
        self.dinero_por_dano_ronda=self.dinero_por_dano_ronda+cantidad
        return cantidad
    
    def ganar_por_destruir_base(self):
        #Gana dinero por destruir la base
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


class GestorUsuarios:
    def __init__(self):
        self.archivo = "usuarios.json"
        self.cargar_o_crear()

    def cargar_o_crear(self):
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump({}, f)

    def usuario_existe(self, usuario):
        with open(self.archivo, "r") as f:
            usuarios = json.load(f)
        return usuario in usuarios

    def registrar(self, usuario, contraseña):
        with open(self.archivo, "r") as f:
            usuarios = json.load(f)
        
        if usuario in usuarios:
            return False
        
        usuarios[usuario] = {
            "contraseña": contraseña,
            "victorias_defensor": 0,
            "victorias_atacante": 0
        }
        
        with open(self.archivo, "w") as f:
            json.dump(usuarios, f, indent=2)
        return True

    def verificar(self, usuario, contraseña):
        with open(self.archivo, "r") as f:
            usuarios = json.load(f)
        
        if usuario not in usuarios:
            return False
        
        return usuarios[usuario]["contraseña"] == contraseña

    def obtener_stats(self, usuario):
        with open(self.archivo, "r") as f:
            usuarios = json.load(f)
        
        if usuario not in usuarios:
            return None
        
        return usuarios[usuario]

    def actualizar_victoria(self, usuario, rol):
        with open(self.archivo, "r") as f:
            usuarios = json.load(f)
        
        if usuario not in usuarios:
            return False
        
        if rol == "Defensor":
            usuarios[usuario]["victorias_defensor"] += 1
        elif rol == "Atacante":
            usuarios[usuario]["victorias_atacante"] += 1
        
        with open(self.archivo, "w") as f:
            json.dump(usuarios, f, indent=2)
        return True

    def obtener_ranking(self):
        with open(self.archivo, "r") as f:
            usuarios = json.load(f)
        
        ranking = []
        for usuario, data in usuarios.items():
            ranking.append({
                "usuario": usuario,
                "victorias_defensor": data["victorias_defensor"],
                "victorias_atacante": data["victorias_atacante"],
                "total": data["victorias_defensor"] + data["victorias_atacante"]
            })
        
        return ranking


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


def mostrar_pantalla_login():
    # Muestra pantalla de login/registro
    frame_juego.pack_forget()
    frame_inicio.pack_forget()
    frame_login.pack(fill=tk.BOTH, expand=True)
    canvas_login.bind("<Configure>", lambda e: _redibujar_login())
    _redibujar_login()


def _redibujar_login():
    # Redibuja la pantalla de login
    canvas_login.delete("all")
    ancho = canvas_login.winfo_width() or 1400
    alto = canvas_login.winfo_height() or 900
    
    # Fondo
    if fondo_inicio_img is not None:
        canvas_login.create_image(0, 0, anchor="nw", image=fondo_inicio_img)
    else:
        canvas_login.create_rectangle(0, 0, ancho, alto, fill=BG, outline="")
    
    cx = ancho // 2
    cy = alto // 2
    
    # Título
    canvas_login.create_text(cx, cy - 150,
                            text="Avgrunnens\nBattle Royale",
                            font=("Arial", 36, "bold"), fill="white",
                            justify="center")
    
    # Label Usuario
    canvas_login.create_text(cx - 120, cy - 20,
                            text="Usuario:", font=("Arial", 12, "bold"), fill="white")
    entry_usuario.pack_forget()
    canvas_login.create_window(cx + 50, cy - 20, window=entry_usuario, width=150)
    
    # Label Contraseña
    canvas_login.create_text(cx - 120, cy + 20,
                            text="Contraseña:", font=("Arial", 12, "bold"), fill="white")
    entry_password.pack_forget()
    canvas_login.create_window(cx + 50, cy + 20, window=entry_password, width=150)
    
    # Botones
    estilo_btn = {
        "font": ("Arial", 12, "bold"),
        "bg": "#2c2c2c",
        "fg": "white",
        "activebackground": "#444444",
        "activeforeground": "white",
        "relief": tk.FLAT,
        "bd": 0,
        "width": 15,
        "cursor": "hand2",
    }
    
    btn_iniciar = tk.Button(canvas_login, text="Iniciar Sesión",
                            command=iniciar_sesion, **estilo_btn)
    canvas_login.create_window(cx - 80, cy + 80, window=btn_iniciar)
    
    btn_registrar = tk.Button(canvas_login, text="Registrarse",
                             command=registrarse, **estilo_btn)
    canvas_login.create_window(cx + 80, cy + 80, window=btn_registrar)
    
    btn_volver = tk.Button(canvas_login, text="Volver", command=mostrar_pantalla_inicio,
                          **estilo_btn)
    canvas_login.create_window(cx, cy + 150, window=btn_volver)


def iniciar_sesion():
    global usuario_defensor, usuario_atacante
    
    usuario = entry_usuario.get()
    contraseña = entry_password.get()
    
    if not usuario or not contraseña:
        messagebox.showerror("Error", "Completa todos los campos")
        return
    
    if not gestor_usuarios.verificar(usuario, contraseña):
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        return
    
    # Primer jugador (Defensor)
    if usuario_defensor is None:
        usuario_defensor = usuario
        defensor.nombre = usuario

        entry_usuario.delete(0, tk.END)
        entry_password.delete(0, tk.END)

        messagebox.showinfo(
            "Defensor registrado",
            f"{usuario} será el Defensor.\n\nAhora inicia sesión como Atacante."
        )

    # Segundo jugador (Atacante)
    elif usuario_atacante is None:

        if usuario == usuario_defensor:
            messagebox.showerror(
                "Error",
                "El atacante debe ser un usuario diferente al defensor."
            )
            return

        usuario_atacante = usuario
        atacante.nombre = usuario

        entry_usuario.delete(0, tk.END)
        entry_password.delete(0, tk.END)

        messagebox.showinfo(
            "Atacante registrado",
            f"{usuario} será el Atacante.\n\n¡Comienza la partida!"
        )

        iniciar_juego()
    
    


def registrarse():
    usuario = entry_usuario.get()
    contraseña = entry_password.get()
    
    if not usuario or not contraseña:
        messagebox.showerror("Error", "Completa todos los campos")
        return
    
    if gestor_usuarios.registrar(usuario, contraseña):
        messagebox.showinfo("Éxito", f"Usuario {usuario} registrado correctamente")
        entry_usuario.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "El usuario ya existe")


def mostrar_top_jugadores():
    gestor = GestorUsuarios()
    ranking = gestor.obtener_ranking()
    ranking.sort(key=lambda x: x["total"], reverse=True)
    
    ventana_top = tk.Toplevel(ventana)
    ventana_top.title("Top de Jugadores")
    ventana_top.geometry("600x600")
    ventana_top.configure(bg=BG)
    
    # Canvas para el fondo
    canvas_top = tk.Canvas(ventana_top, bg=BG, highlightthickness=0)
    canvas_top.pack(fill=tk.BOTH, expand=True)
    
    # Cargar fondo si existe
    fondo_top_img = None
    try:
        ruta_fondo = os.path.join("imagenes", "fondo", "inicio.png")
        if os.path.exists(ruta_fondo):
            fondo_top_img = tk.PhotoImage(file=ruta_fondo)
    except:
        fondo_top_img = None
    
    def dibujar():
        canvas_top.delete('all')
        w = canvas_top.winfo_width() or 600
        h = canvas_top.winfo_height() or 600
        
        if fondo_top_img is not None:
            canvas_top.create_image(w//2, h//2, image=fondo_top_img)
        
        canvas_top.create_text(
            w//2, 40,
            text='Top 10 Jugadores',
            fill='white',
            font=('Arial', 32, 'bold')
        )
        
        colores = ["#FFD700", "#C0C0C0", "#CD7F32", "white", "white", "#E0E0E0", "#E0E0E0", "#E0E0E0", "#E0E0E0", "#E0E0E0"]
        y = 100
        
        for i in range(min(10, len(ranking))):
            jugador = ranking[i]
            color = colores[i] if i < len(colores) else "white"
            
            canvas_top.create_rectangle(
                w // 2 - 250, y - 20,
                w // 2 + 250, y + 20,
                fill='#000000',
                stipple='gray25',
                outline=''
            )
            
            canvas_top.create_text(
                w // 2 - 200, y,
                text=f'{i+1}.',
                fill=color,
                font=('Arial', 14, 'bold'),
                anchor='w'
            )
            
            canvas_top.create_text(
                w // 2 - 150, y,
                text=f'{jugador["usuario"]}',
                fill=color,
                font=('Arial', 12, 'bold'),
                anchor='w'
            )
            
            canvas_top.create_text(
                w // 2 + 100, y,
                text=f'D:{jugador["victorias_defensor"]} A:{jugador["victorias_atacante"]}',
                fill=color,
                font=('Arial', 11),
                anchor='e'
            )
            
            y += 50
    
    canvas_top.bind('<Configure>', lambda e: dibujar())


# VARIABLES GLOBALES

ANCHO = 11
ALTO = 11
TAM_CELDA = 50 

# Matriz: 0=vacío, 1=muro, 2=torre, 3=unidad, 4=base
matriz = [[0 for _ in range(ANCHO)] for _ in range(ALTO)]

# Gestor de usuarios
gestor_usuarios = GestorUsuarios()
usuario_defensor = None
usuario_atacante = None

# Jugadores
defensor = Defensor("Defensor 1")
atacante = Atacante("Atacante 1")
sistema_dinero = SistemaDinero()
top_jugadores = TopJugadores()

# Estado del juego
fase = "defensor_base"
elemento_actual = None
tipo_elemento_actual = None
modo_borrar = False

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
# Imagen de fondo de la matriz (se carga en cargar_imagenes)
fondo_matriz_img = None



# FUNCIONES DE CARGA DE IMÁGENES

def cargar_imagenes():
    #Carga imágenes PNG desde carpeta imagenes/elementos/ y el fondo de la matriz
    global imagenes, fondo_matriz_img
    
    ruta_base = "imagenes/elementos/"
    ruta_fondo = "imagenes/fondo/"

    # Cargar fondo de la matriz
    ruta_fondo_png = os.path.join(ruta_fondo, "fondo.png")
    if os.path.exists(ruta_fondo_png):
        fondo_matriz_img = tk.PhotoImage(file=ruta_fondo_png)
    
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
    
    if fondo_matriz_img is not None:
        canvas.create_image(0, 0, anchor='nw', image=fondo_matriz_img)
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
        label_fase.config(text=f"RONDA {ronda_actual} — FASE: Defensor coloca BASE", fg="#aaaaaa")
        label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}", fg="#cccccc")
    elif fase == "defensor_defensas":
        label_fase.config(text=f"RONDA {ronda_actual} — FASE: Defensor coloca MUROS y TORRES", fg="#aaaaaa")
        label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}", fg="#cccccc")
    elif fase == "atacante_unidades":
        label_fase.config(text=f"RONDA {ronda_actual} — FASE: Atacante coloca UNIDADES", fg="#aaaaaa")
        label_dinero.config(text=f"Dinero Atacante: ${atacante.dinero}", fg="#cccccc")
        label_estado.config(
            text=f"Marcador → Defensor: {victorias_defensor}  |  Atacante: {victorias_atacante}",
            fg="#e0e0e0"
        )
    elif fase == "combate":
        label_fase.config(text=f"RONDA {ronda_actual} — COMBATE — Turno {turno_combate}", fg="#e57373")
        label_dinero.config(text=f"Defensor: ${defensor.dinero}  |  Atacante: ${atacante.dinero}", fg="#cccccc")
        label_estado.config(
            text=f"Marcador → Defensor: {victorias_defensor}  |  Atacante: {victorias_atacante}",
            fg="#e0e0e0"
        )


def limpiar_botones():
    #Elimina todos los botones de acción
    for widget in frame_botones_accion.winfo_children():
        widget.destroy()


def crear_botones():
    #Crea los botones según la fase actual en estilo monocromático
    limpiar_botones()

    # Estilo base para todos los botones de acción
    s = {
        "font": ("Arial", 10, "bold"),
        "bg": "#2c2c2c",
        "fg": "white",
        "activebackground": "#484848",
        "activeforeground": "white",
        "relief": tk.FLAT,
        "bd": 0,
        "cursor": "hand2",
    }
    
    if fase == "defensor_base":
        btn = tk.Button(frame_botones_accion, text="Colocar Base",
                       command=lambda: seleccionar_elemento("base", "Base Central"),
                       width=14, **s)
        btn.pack(side=tk.LEFT, padx=5)
    
    elif fase == "defensor_defensas":
        btn0 = tk.Button(frame_botones_accion, text="Muro  $50",
                        command=lambda: seleccionar_elemento("muro", "Muro"),
                        width=12, **s)
        btn0.pack(side=tk.LEFT, padx=3)
        btn1 = tk.Button(frame_botones_accion, text="Torre Básica  $100",
                        command=lambda: seleccionar_elemento("torre", "Torre Básica"),
                        width=18, **s)
        btn1.pack(side=tk.LEFT, padx=3)
        btn2 = tk.Button(frame_botones_accion, text="Torre Pesada  $200",
                        command=lambda: seleccionar_elemento("torre", "Torre Pesada"),
                        width=18, **s)
        btn2.pack(side=tk.LEFT, padx=3)
        btn3 = tk.Button(frame_botones_accion, text="Torre Mágica  $150",
                        command=lambda: seleccionar_elemento("torre", "Torre Mágica"),
                        width=18, **s)
        btn3.pack(side=tk.LEFT, padx=3)
    
    elif fase == "atacante_unidades":
        btn1 = tk.Button(frame_botones_accion, text="Soldado  $75",
                        command=lambda: seleccionar_elemento("unidad", "Soldado"),
                        width=14, **s)
        btn1.pack(side=tk.LEFT, padx=3)
        btn2 = tk.Button(frame_botones_accion, text="Arquero  $100",
                        command=lambda: seleccionar_elemento("unidad", "Arquero"),
                        width=14, **s)
        btn2.pack(side=tk.LEFT, padx=3)
        btn3 = tk.Button(frame_botones_accion, text="Mago  $120",
                        command=lambda: seleccionar_elemento("unidad", "Mago"),
                        width=14, **s)
        btn3.pack(side=tk.LEFT, padx=3)
    
    elif fase == "combate":
        # Botón de iniciar combate (se deshabilita al comenzar)
        btn_combate = tk.Button(frame_botones_accion,
                                text="Iniciar Combate",
                                command=iniciar_combate,
                                font=("Arial", 11, "bold"),
                                bg="#3a3a3a", fg="white",
                                activebackground="#555555", activeforeground="white",
                                relief=tk.FLAT, bd=0, width=18, cursor="hand2")
        btn_combate.pack(side=tk.LEFT, padx=10)


def seleccionar_elemento(tipo, subtipo):
    #Selecciona el tipo de elemento a colocar
    global elemento_actual, tipo_elemento_actual, modo_borrar
    
    modo_borrar = False
    
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


def activar_borrar():
    #Activa el modo de borrar elementos
    global elemento_actual, tipo_elemento_actual, modo_borrar
    
    elemento_actual = None
    tipo_elemento_actual = None
    modo_borrar = True
    label_estado.config(text="Modo BORRAR - Haz clic en un elemento para borrarlo", fg="#FF6B6B")


def cancelar_elemento():
    #Cancela la colocación actual
    global elemento_actual, tipo_elemento_actual, modo_borrar
    elemento_actual = None
    tipo_elemento_actual = None
    modo_borrar = False
    label_estado.config(text="")


def on_canvas_click(event):
    #Maneja los clics en el canvas
    global elemento_actual, tipo_elemento_actual, modo_borrar
    
    col = event.x // TAM_CELDA
    fila = event.y // TAM_CELDA
    
    # Validar límites
    if fila >= ALTO or col >= ANCHO or fila < 0 or col < 0:
        messagebox.showerror("Error", "Haz clic dentro del mapa")
        return
    
    # Modo borrar
    if modo_borrar:
        if (fila, col) not in objetos_en_mapa:
            messagebox.showerror("Error", "No hay nada que borrar en esa celda")
            return
        
        objeto = objetos_en_mapa[(fila, col)]
        
        # No se puede borrar la base
        if objeto.tipo == "base":
            messagebox.showerror("Error", "No puedes borrar la base")
            return
        
        # Devolver dinero según el elemento
        if objeto.tipo == "muro":
            if fase == "defensor_defensas":
                defensor.ganar_dinero(50)
                label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
        elif objeto.tipo.startswith("torre"):
            costos_torres = {
                "torre_basica": 100,
                "torre_pesada": 200,
                "torre_magica": 150
            }
            costo = costos_torres.get(objeto.tipo, 0)
            if fase == "defensor_defensas":
                defensor.ganar_dinero(costo)
                label_dinero.config(text=f"Dinero Defensor: ${defensor.dinero}")
                if objeto in defensor.defensas:
                    defensor.defensas.remove(objeto)
        elif objeto.tipo in ["soldado", "arquero", "mago"]:
            costos_unidades = {
                "soldado": 75,
                "arquero": 100,
                "mago": 120
            }
            costo = costos_unidades.get(objeto.tipo, 0)
            if fase == "atacante_unidades":
                atacante.ganar_dinero(costo)
                label_dinero.config(text=f"Dinero Atacante: ${atacante.dinero}")
                if objeto in atacante.unidades:
                    atacante.unidades.remove(objeto)
        
        del objetos_en_mapa[(fila, col)]
        matriz[fila][col] = 0
        modo_borrar = False
        label_estado.config(text="")
        dibujar_mapa()
        return
    
    # Modo colocación normal
    if elemento_actual is None:
        messagebox.showwarning("Aviso", "Primero selecciona qué colocar")
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
    info = "INFORMACIÓN DE TORRES:\n\n"
    
    torres_info = [
        TorreBasica(),
        TorrePesada(),
        TorreMagica()
    ]
    
    for torre in torres_info:
        info += torre.obtener_info() + "\n\n"
    
    messagebox.showinfo("Info Torres", info)


def mostrar_info_unidades():
    #Muestra información detallada de todas las unidades
    info = "INFORMACIÓN DE UNIDADES:\n\n"
    
    unidades_info = [
        Soldado(),
        Arquero(),
        Mago()
    ]
    
    for unidad in unidades_info:
        info += unidad.obtener_info() + "\n\n"
    
    messagebox.showinfo("Info Unidades", info)


def siguiente_fase():
    #Avanza a la siguiente fase
    global fase, modo_borrar
    
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


def reiniciar_ronda():
    global fase, elemento_actual, tipo_elemento_actual, objetos_en_mapa, matriz
    global turno_combate, log_combate, combate_en_curso, modo_borrar

    # Borrar el mapa
    objetos_en_mapa = {}
    for f in range(ALTO):
        for c in range(ANCHO):
            matriz[f][c] = 0

    # Dar bono de ronda + dinero acumulado por daño
    sistema_dinero.iniciar_ronda(defensor, atacante)
    defensor.dinero_por_dano_ronda = 0
    atacante.dinero_por_dano_ronda = 0
    defensor.base = None
    defensor.defensas = []
    atacante.unidades = []

    # Resetear combate
    turno_combate = 0
    log_combate = []
    combate_en_curso = False
    modo_borrar = False

    # Volver al inicio
    fase = "defensor_base"
    elemento_actual = None
    tipo_elemento_actual = None

    cancelar_elemento()
    actualizar_labels()
    crear_botones()
    label_estado.config(text="")
    dibujar_mapa()


def verificar_ganador_partida():
    if victorias_defensor == 2:
        return "defensor"
    if victorias_atacante == 2:
        return "atacante"
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


def terminar_partida(ganador):
    global registro_victorias

    if ganador == "defensor":
        jugador_ganador = defensor
        nombre_ganador = usuario_defensor if usuario_defensor else defensor.nombre
        mensaje = f"¡{nombre_ganador} (Defensor) GANÓ LA PARTIDA!"
    else:
        jugador_ganador = atacante
        nombre_ganador = usuario_atacante if usuario_atacante else atacante.nombre
        mensaje = f"¡{nombre_ganador} (Atacante) GANÓ LA PARTIDA!"

    # Registrar en top_jugadores.txt
    top_jugadores.registrar_victoria(nombre_ganador, jugador_ganador.rol)

    # Registrar en usuarios.json (sistema de login)
    if ganador == "defensor" and usuario_defensor:
        gestor_usuarios.actualizar_victoria(usuario_defensor, "Defensor")
    elif ganador == "atacante" and usuario_atacante:
        gestor_usuarios.actualizar_victoria(usuario_atacante, "Atacante")

    clave = f"{nombre_ganador} ({jugador_ganador.rol})"
    if clave in registro_victorias:
        registro_victorias[clave] += 1
    else:
        registro_victorias[clave] = 1

    historial = "\n".join([f"  • {n}: {w} victoria(s)" for n, w in registro_victorias.items()])
    messagebox.showinfo("¡Partida terminada!",
                        f"{mensaje}\n\n"
                        f"Resultado: Defensor {victorias_defensor} - Atacante {victorias_atacante}\n\n"
                        f"Registro de victorias:\n{historial}")

    jugar_otra = messagebox.askyesno("¿Otra partida?", "¿Quieren jugar una nueva partida?")
    if jugar_otra:
        reiniciar_partida_completa()
    else:
        reiniciar_partida_completa()
        mostrar_pantalla_inicio()


def reiniciar_partida_completa():
    #Reinicia todo para una nueva partida desde cero
    global victorias_defensor, victorias_atacante, resultado_rondas, ronda_actual
    global fase, elemento_actual, tipo_elemento_actual, objetos_en_mapa, matriz
    global turno_combate, log_combate, combate_en_curso, modo_borrar
    global usuario_defensor, usuario_atacante

    victorias_defensor = 0
    victorias_atacante = 0
    resultado_rondas = []
    ronda_actual = 1

    defensor.dinero = 500
    atacante.dinero = 500
    defensor.dinero_por_dano_ronda = 0
    atacante.dinero_por_dano_ronda = 0

    objetos_en_mapa = {}
    for f in range(ALTO):
        for c in range(ANCHO):
            matriz[f][c] = 0

    defensor.base = None
    defensor.defensas = []
    atacante.unidades = []

    turno_combate = 0
    log_combate = []
    combate_en_curso = False
    modo_borrar = False

    usuario_defensor = None
    usuario_atacante = None
    defensor.nombre = "Defensor 1"
    atacante.nombre = "Atacante 1"

    fase = "defensor_base"
    elemento_actual = None
    tipo_elemento_actual = None

    cancelar_elemento()
    actualizar_labels()
    crear_botones()
    label_estado.config(text="¡Nueva partida! El Defensor coloca su Base.")
    dibujar_mapa()


def verificar_ganador_ronda():
    # Atacante gana si destruyó la base
    if defensor.base is None:
        return "atacante"

    # Defensor gana si no quedan unidades enemigas
    if len(atacante.unidades) == 0 and defensor.base is not None:
        return "defensor"

    # Nadie ganó todavía
    return None


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


# ── FASES DE COMBATE ───────────────────────────────────────────

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
                    defensor.ganar_por_dañar_unidad(objetivo.nombre)
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
                        defensor.ganar_por_dañar_unidad(u.nombre)
                        msgs.append(f"{u.nombre}: -{torre.daño} vida ({max(0,u.vida)} restante)")
            else:
                objetivo.vida -= torre.daño
                defensor.ganar_por_dañar_unidad(objetivo.nombre)
                msgs.append(f"Torre Pesada → {objetivo.nombre}: -{torre.daño} vida ({max(0,objetivo.vida)} restante)")

        # Torre Mágica: ataca y cada turnos_habilidad turnos congela
        elif torre.tipo == "torre_magica":
            torre.turnos_restantes += 1
            objetivo.vida -= torre.daño
            defensor.ganar_por_dañar_unidad(objetivo.nombre)
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
                    msgs.append(f"{unidad.nombre} → {objetivo.nombre}: -{daño_real} vida ({max(0,objetivo.vida)} restante)")
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
    global combate_en_curso, turno_combate, log_combate
    #Inicia la fase de combate automático

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
    label_estado.config(text="\n".join(log_combate[-5:]), fg="#e0e0e0")
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
# Fondo oscuro para toda la ventana
BG = "#1a1a1a"
ventana.configure(bg=BG)

# ── PANTALLA DE INICIO ─────────────────────────────────────────

# Frame de la pantalla de inicio (ocupa toda la ventana)
frame_inicio = tk.Frame(ventana, bg=BG)
frame_inicio.pack(fill=tk.BOTH, expand=True)

# Canvas para el fondo de la pantalla de inicio
canvas_inicio = tk.Canvas(frame_inicio, bg=BG, highlightthickness=0)
canvas_inicio.pack(fill=tk.BOTH, expand=True)

# Cargar fondo de la pantalla de inicio desde imagenes/fondo/inicio.png
fondo_inicio_img = None
try:
    ruta_inicio = os.path.join("imagenes", "fondo", "inicio.png")
    if os.path.exists(ruta_inicio):
        fondo_inicio_img = tk.PhotoImage(file=ruta_inicio)
except:
    fondo_inicio_img = None

# Cargar imagen del título desde imagenes/titulo/titulo.png
titulo_img = None
try:
    ruta_titulo = os.path.join("imagenes", "titulo", "titulo.png")
    if os.path.exists(ruta_titulo):
        titulo_img = tk.PhotoImage(file=ruta_titulo)
except:
    titulo_img = None

def mostrar_pantalla_inicio():
    #Muestra la pantalla de inicio y oculta el juego
    frame_juego.pack_forget()
    frame_login.pack_forget()
    frame_inicio.pack(fill=tk.BOTH, expand=True)
    # Forzar que la ventana calcule su tamaño real antes de dibujar
    ventana.update_idletasks()
    _redibujar_inicio()
    # Redibujar si el usuario redimensiona la ventana
    canvas_inicio.bind("<Configure>", lambda e: _redibujar_inicio())

def _redibujar_inicio():
    #Redibuja el contenido del canvas de inicio centrado
    canvas_inicio.delete("all")
    ancho = canvas_inicio.winfo_width() or 1400
    alto = canvas_inicio.winfo_height() or 900

    # Fondo
    if fondo_inicio_img is not None:
        canvas_inicio.create_image(0, 0, anchor="nw", image=fondo_inicio_img)
    else:
        canvas_inicio.create_rectangle(0, 0, ancho, alto, fill=BG, outline="")

    cx = ancho // 2
    # Título: imagen PNG si existe, texto como fallback
    if titulo_img is not None:
        canvas_inicio.create_image(cx, alto // 4, anchor="center", image=titulo_img)
        cy = alto // 2
    else:
        canvas_inicio.create_text(cx, alto // 4,
                                   text="Avgrunnens\nBattle Royale",
                                   font=("Arial", 36, "bold"), fill="white",
                                   justify="center")
        cy = alto // 2

    # Estilo de los botones de inicio
    estilo_btn = {
        "font": ("Arial", 14, "bold"),
        "bg": "#2c2c2c",
        "fg": "white",
        "activebackground": "#444444",
        "activeforeground": "white",
        "relief": tk.FLAT,
        "bd": 0,
        "width": 18,
        "cursor": "hand2",
    }
    btn_jugar = tk.Button(canvas_inicio, text="JUGAR", command=mostrar_pantalla_login, **estilo_btn)
    canvas_inicio.create_window(cx, cy, window=btn_jugar)

    btn_top_inicio = tk.Button(canvas_inicio, text="Top Jugadores",
                               command=mostrar_top_jugadores, **estilo_btn)
    canvas_inicio.create_window(cx, cy + 60, window=btn_top_inicio)

    btn_salir = tk.Button(canvas_inicio, text="Salir",
                          command=lambda: ventana.destroy(), **estilo_btn)
    canvas_inicio.create_window(cx, cy + 120, window=btn_salir)

def iniciar_juego():
    #Oculta el inicio y muestra el juego
    frame_inicio.pack_forget()
    frame_login.pack_forget()
    frame_juego.pack(fill=tk.BOTH, expand=True)
    actualizar_labels()
    crear_botones()
    dibujar_mapa()

# ── PANTALLA DE LOGIN ──────────────────────────────────────────

frame_login = tk.Frame(ventana, bg=BG)
canvas_login = tk.Canvas(frame_login, bg=BG, highlightthickness=0)
canvas_login.pack(fill=tk.BOTH, expand=True)

entry_usuario = tk.Entry(canvas_login, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
entry_password = tk.Entry(canvas_login, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white", show="*")

# ── FRAME DEL JUEGO ────────────────────────────────────────────

# Todo el juego vive dentro de este frame (oculto hasta que se presione Jugar)
frame_juego = tk.Frame(ventana, bg=BG)

# Frame superior con información
frame_info = tk.Frame(frame_juego, bg=BG)
frame_info.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

label_fase = tk.Label(frame_info, text="", font=("Arial", 12, "bold"), fg="#aaaaaa", bg=BG)
label_fase.pack(anchor=tk.W)

label_dinero = tk.Label(frame_info, text="", font=("Arial", 11, "bold"), fg="#cccccc", bg=BG)
label_dinero.pack(anchor=tk.W)

label_estado = tk.Label(frame_info, text="", font=("Arial", 10, "bold"), bg=BG, fg="#e0e0e0")
label_estado.pack(anchor=tk.W)

# Canvas del mapa
canvas = tk.Canvas(
    frame_juego,
    width=ANCHO * TAM_CELDA,
    height=ALTO * TAM_CELDA,
    bg=BG,
    cursor="cross",
    relief=tk.FLAT,
    bd=0
)
canvas.pack(padx=10, pady=10)
canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<Button-3>", on_canvas_right_click)

# Frame inferior con botones
frame_botones = tk.Frame(frame_juego, bg=BG)
frame_botones.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

frame_botones_accion = tk.Frame(frame_botones, bg=BG)
frame_botones_accion.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Frame botones de utilidad
frame_botones_util = tk.Frame(frame_botones, bg=BG)
frame_botones_util.pack(side=tk.RIGHT)

# Estilo monocromático para los botones de la partida
ESTILO_BTN_UTIL = {
    "font": ("Arial", 9, "bold"),
    "bg": "#2c2c2c",
    "fg": "white",
    "activebackground": "#444444",
    "activeforeground": "white",
    "relief": tk.FLAT,
    "bd": 0,
    "width": 12,
    "cursor": "hand2",
}

btn_siguiente = tk.Button(frame_botones_util, text="Siguiente", command=siguiente_fase,
                          font=("Arial", 10, "bold"), bg="#3a3a3a", fg="white",
                          activebackground="#555555", activeforeground="white",
                          relief=tk.FLAT, bd=0, width=12, cursor="hand2")
btn_siguiente.pack(side=tk.LEFT, padx=5)

btn_cancelar = tk.Button(frame_botones_util, text="Cancelar", command=cancelar_elemento,
                         **ESTILO_BTN_UTIL)
btn_cancelar.pack(side=tk.LEFT, padx=2)

btn_borrar = tk.Button(frame_botones_util, text="Borrar", command=activar_borrar,
                       **ESTILO_BTN_UTIL)
btn_borrar.pack(side=tk.LEFT, padx=2)

btn_torres = tk.Button(frame_botones_util, text="Info Torres", command=mostrar_info_torres,
                       **ESTILO_BTN_UTIL)
btn_torres.pack(side=tk.LEFT, padx=2)

btn_unidades = tk.Button(frame_botones_util, text="Info Unidades", command=mostrar_info_unidades,
                         **ESTILO_BTN_UTIL)
btn_unidades.pack(side=tk.LEFT, padx=2)

btn_salir_juego = tk.Button(frame_botones_util, text="Salir",
                            command=lambda: [reiniciar_partida_completa(), mostrar_pantalla_inicio()],
                            **ESTILO_BTN_UTIL)
btn_salir_juego.pack(side=tk.LEFT, padx=2)


# Cargar imágenes desde carpeta
cargar_imagenes()

# Mostrar pantalla de inicio al arrancar
mostrar_pantalla_inicio()

ventana.mainloop()
