# Avgrunnens Battle Royale

> Juego de estrategia por turnos para dos jugadores — Python + Tkinter

---

## ¿Qué es este juego?

Avgrunnens Battle Royale es un juego de estrategia en el que dos jugadores se enfrentan en la misma computadora. Uno defiende su base usando torres y muros, y el otro intenta destruirla enviando unidades al ataque. El combate ocurre automáticamente turno a turno.

---

## Requisitos

| Requisito | Versión mínima |
|-----------|---------------|
| Python | 3.8 o superior |
| tkinter | Incluido con Python |
| Sistema operativo | Windows, macOS o Linux |

> **No se necesitan librerías externas.** El juego usa únicamente módulos estándar de Python: `tkinter`, `os` y `json`.

Para verificar que tienes Python instalado, abre una terminal y ejecuta:

```bash
python --version
```

---

## Estructura de archivos

```
avgrunnens_battle_royale_v6.py   ← Archivo principal del juego
usuarios.json                    ← Se crea automáticamente al registrar el primer usuario
top_jugadores.txt                ← Se crea automáticamente al registrar la primera victoria
imagenes/                        ← Carpeta opcional de recursos visuales
├── fondo/
│   ├── inicio.png               ← Fondo de la pantalla principal
│   └── fondo.png                ← Fondo del tablero de juego
├── titulo/
│   └── titulo.png               ← Imagen del título en la pantalla de inicio
└── elementos/
    ├── muro.png
    ├── torre_basica.png
    ├── torre_pesada.png
    ├── torre_magica.png
    ├── soldado.png
    ├── arquero.png
    ├── mago.png
    ├── base.png
    ├── oscuro/                  ← Sprites alternativos para la facción Oscuro
    │   └── (mismos nombres)
    └── naturaleza/              ← Sprites alternativos para la facción Naturaleza
        └── (mismos nombres)
```

> La carpeta `imagenes/` es **completamente opcional**. Si no existe o le faltan imágenes, el juego dibuja los elementos usando colores sólidos según la facción de cada jugador.

---

## Instrucciones de ejecución

### 1. Descarga el archivo

Copia el archivo `avgrunnens_battle_royale_v6.py` a una carpeta de tu elección.

### 2. (Opcional) Agrega las imágenes

Si tienes los recursos visuales, crea la carpeta `imagenes/` con la estructura indicada arriba dentro de la misma carpeta donde está el archivo `.py`.

### 3. Abre una terminal en esa carpeta

**Windows:**
```
Clic derecho en la carpeta → "Abrir en Terminal"
  o bien:
Win + R → cmd → cd ruta\de\la\carpeta
```

**macOS / Linux:**
```bash
cd /ruta/de/la/carpeta
```

### 4. Ejecuta el juego

```bash
python avgrunnens_battle_royale_v6.py
```

En algunos sistemas puede ser necesario usar `python3`:

```bash
python3 avgrunnens_battle_royale_v6.py
```

La ventana del juego se abrirá automáticamente en pantalla completa.

---

## Primer uso: crear cuentas

Antes de jugar, ambos jugadores necesitan registrarse. Desde la pantalla principal:

1. Haz clic en **JUGAR**.
2. El primer jugador escribe su nombre de usuario y contraseña → clic en **Registrarse**.
3. Repite con el segundo jugador (con un usuario diferente).
4. Una vez ambos tienen cuenta, inician sesión uno tras otro en la misma pantalla.

---

## Cómo jugar (resumen)

```
1. Ambos jugadores inician sesión
        ↓
2. Cada uno elige una facción diferente (Medieval / Oscuro / Naturaleza)
        ↓
3. El Defensor coloca su BASE en el tablero → clic en Siguiente
        ↓
4. El Defensor coloca MUROS y TORRES con su dinero ($500 + bonos) → clic en Siguiente
        ↓
5. El Atacante coloca sus UNIDADES con su dinero → clic en Siguiente
        ↓
6. Fase de COMBATE automático → clic en "Iniciar Combate"
        ↓
7. Se decide el ganador de la ronda y comienza la siguiente
```

---

## Elementos del juego

### Torres (Defensor)

| Torre | Costo | Vida | Daño | Alcance | Habilidad |
|-------|-------|------|------|---------|-----------|
| Torre Básica | $100 | 60 | 20 | 3 casillas | Disparo Doble cada 3 turnos |
| Torre Pesada | $200 | 150 | 35 | 2 casillas | Daño en Área cada 4 turnos |
| Torre Mágica | $150 | 100 | 15 | 4 casillas | Congela por 2 turnos cada 2 turnos |
| Muro | $50 | 75 | — | — | Obstáculo sin ataque |

### Unidades (Atacante)

| Unidad | Costo | Vida | Daño | Velocidad | Habilidad |
|--------|-------|------|------|-----------|-----------|
| Soldado | $75 | 120 | 35 | 2/turno | Ataque Doble cada 3 turnos |
| Arquero | $100 | 100 | 25 | 3/turno | +50% daño vs torres cada 2 ataques |
| Mago | $120 | 80 | 20 | 2/turno | Cura +40 vida a un aliado cada 3 turnos |

---

## Sistema de dinero

- Cada jugador comienza con **$500** por ronda.
- Al inicio de cada nueva ronda reciben **+$100** de bono.
- El dinero ganado durante el combate (por dañar/destruir elementos enemigos) se acumula y se suma en la siguiente ronda.
- El combate termina a los **40 turnos** si la base sigue en pie → gana el Defensor.

---

## Archivos generados automáticamente

| Archivo | Descripción |
|---------|-------------|
| `usuarios.json` | Cuentas de usuario con contraseñas y conteo de victorias. Se crea al registrar el primer usuario. |
| `top_jugadores.txt` | Historial de victorias de todos los jugadores. Se actualiza al final de cada ronda. |

Estos archivos no deben borrarse si quieres conservar el historial de partidas y cuentas registradas.

---

## Solución de problemas

**El juego no abre / error al ejecutar**
- Verifica que Python esté instalado: `python --version`
- Asegúrate de estar en la carpeta correcta antes de ejecutar el comando.

**Error: "No module named tkinter"**
- En Linux puede ser necesario instalarlo: `sudo apt-get install python3-tk`
- En macOS y Windows viene incluido con Python.

**Las imágenes no aparecen**
- Verifica que la carpeta `imagenes/` esté en la misma carpeta que el archivo `.py`.
- Los nombres de los archivos PNG deben ser exactamente como se indica en la estructura de arriba.
- Si no tienes imágenes, el juego funciona igual con colores.

**Error de usuario o contraseña**
- Los datos son sensibles a mayúsculas. "Juan" y "juan" son usuarios diferentes.
- No hay forma de recuperar contraseña; en ese caso, crea una cuenta nueva.

---

## Créditos

Desarrollado como proyecto del curso de Programación — 2025.

**Stephano Thomas Jarquín Quesada - 2026086055**
**Jeffry Leonardo Rojas Arias - 2023800057**
