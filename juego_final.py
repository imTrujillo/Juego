import pygame  # Importa la biblioteca pygame para manejar gráficos y sonido.
import sys     # Importa sys para manejar la salida del programa.
import random  # Importa random para generar posiciones aleatorias para los enemigos.

# Constantes
ANCHO = 800                     # Ancho de la ventana del juego.
ALTO = 600                      # Alto de la ventana del juego.
color_negro = (0, 0, 0)         # Definición del color negro en RGB.
color_blanco = (255, 255, 255)  # Definición del color blanco en RGB.
puntaje = 0                     # Inicialización del puntaje del jugador.
game_over = False               # Estado inicial del juego (no ha terminado).

# Inicializar pygame
pygame.init()        # Inicializa todos los módulos de Pygame.
pygame.mixer.init()  # Inicializa el módulo de mezcla de sonido de Pygame.

# Función para introducir el nombre del jugador
def introducir_nombre():
    nombre = input("Introduce tu nombre: ")  # Pide al usuario que introduzca su nombre.
    return nombre                            # Devuelve el nombre introducido.

# Clase para el usuario
class User:
    def __init__(self, name):
        self.name = name                    # Guarda el nombre del usuario.
        self.record = self.cargar_record()  # Carga el récord del usuario.

    def actualizar_record(self, nuevo_record):
        if nuevo_record > self.record:  # Si el nuevo récord es mayor que el récord actual,
            self.record = nuevo_record  # actualiza el récord.
            self.guardar_record()       # Guarda el nuevo récord en un archivo.

    def cargar_record(self):
        try:
            with open(f"{self.name}_record.txt", "r") as file:   # Intenta abrir el archivo del récord.
                record = int(file.read())                        # Lee el récord del archivo.
                return record                                    # Devuelve el récord.
        except FileNotFoundError:                                # Si el archivo no existe,
            return 0  # devuelve 0.

    def guardar_record(self):
        with open(f"{self.name}_record.txt", "w") as file:  # Abre el archivo del récord en modo escritura.
            file.write(str(self.record))                    # Escribe el récord en el archivo.

# Función para cargar y reproducir sonidos
def play_sound(sound_file):
    pygame.mixer.Sound(sound_file).play()  # Reproduce el archivo de sonido.

# Función para guardar el puntaje del usuario
def guardar_puntaje(nombre, puntaje):
    with open(f"{nombre}_puntajes.txt", "a") as file:  # Abre el archivo de puntajes en modo adjuntar.
        file.write(f"{puntaje}\n")                     # Escribe el puntaje en el archivo.

# Función para cargar los puntajes del usuario
def cargar_puntajes(nombre):
    try:
        with open(f"{nombre}_puntajes.txt", "r") as file:    # Intenta abrir el archivo de puntajes.
            puntajes = [int(line.strip()) for line in file]  # Lee los puntajes del archivo.
            return puntajes                                  # Devuelve la lista de puntajes.
    except FileNotFoundError:                                # Si el archivo no existe,
        return []                                            # devuelve una lista vacía.

# Obtener el nombre del jugador
def nuevo_jugador():
    global usuario, nombre_jugador
    nombre_jugador = introducir_nombre()  # Pide al usuario que introduzca su nombre.
    usuario = User(nombre_jugador)        # Crea un nuevo objeto usuario con el nombre introducido.
    reiniciar_juego()                     # Reinicia el juego.

# Configuración de la ventana del juego
ventana = pygame.display.set_mode((ANCHO, ALTO))      # Establece el tamaño de la ventana.
pygame.display.set_caption("¡Space Wars!")  # Establece el título de la ventana.

# Configuración del jugador y el enemigo
jugador_size = 50                                           # Tamaño del jugador.
jugador_pos = [ANCHO / 2, ALTO - jugador_size * 2]          # Posición inicial del jugador.
enemigo_size = 50                                           # Tamaño del enemigo.
enemigo_pos = [random.randint(0, ANCHO - enemigo_size), 0]  # Posición inicial del enemigo.

# Cargar imágenes
jugador_img = pygame.image.load("assets/jugador.gif")      # Carga la imagen del jugador.
jugador_img = pygame.transform.scale(jugador_img, (jugador_size, jugador_size))  # Escala la imagen del jugador.
enemigo_img = pygame.image.load("assets/enemigo.gif")      # Carga la imagen del enemigo.
enemigo_img = pygame.transform.scale(enemigo_img, (enemigo_size, enemigo_size))  # Escala la imagen del enemigo.

clock = pygame.time.Clock()  # Crea un objeto Clock para controlar la velocidad del juego.

# Función para reiniciar el juego
def reiniciar_juego():
    global game_over, puntaje, jugador_pos, enemigo_pos
    puntaje = 0                                                 # Reinicia el puntaje.
    jugador_pos = [ANCHO / 2, ALTO - jugador_size * 2]          # Reinicia la posición del jugador.
    enemigo_pos = [random.randint(0, ANCHO - enemigo_size), 0]  # Reinicia la posición del enemigo.
    game_over = False                                           # Establece que el juego no ha terminado.

# Función para detectar colisión
def detectar_colision(jugador_pos, enemigo_pos):
    jx = jugador_pos[0]
    jy = jugador_pos[1]
    ex = enemigo_pos[0]
    ey = enemigo_pos[1]

    if (ex >= jx and ex < (jx + jugador_size)) or (jx >= ex and jx < (ex + enemigo_size)):
        if (ey >= jy and ey < (jy + jugador_size)) or (jy >= ey and jy < (ey + enemigo_size)):
            return True  # Si las coordenadas del jugador y el enemigo se superponen, hay una colisión.
    return False         # Si no, no hay colisión.

# Función para mostrar puntaje y récord
def mostrar_puntajes():
    font = pygame.font.SysFont(None, 40)                                         # Configura la fuente.
    texto_puntaje = font.render(f"Puntaje: {puntaje}", True, color_blanco)       # Renderiza el texto del puntaje.
    ventana.blit(texto_puntaje, (10, 10))                                        # Muestra el puntaje en la pantalla.
    texto_record = font.render(f"Récord: {usuario.record}", True, color_blanco)  # Renderiza el texto del récord.
    ventana.blit(texto_record, (10, 50)) 
    texto_nombre = font.render(f"Jugador: {nombre_jugador}", True, color_blanco) # Renderiza el nombre del jugador.
    ventana.blit(texto_nombre, (10, 90))                                         # Muestra el nombre del jugador en la pantalla.                                        # Muestra el récord en la pantalla.

# Iniciar el primer jugador
nuevo_jugador()

# Bucle principal del juego
while True:
    ventana.fill(color_negro)  # Limpia la pantalla con el color negro.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # Si se cierra la ventana,
            pygame.quit()                   # cierra Pygame.
            sys.exit()                      # cierra el programa.
        if event.type == pygame.KEYDOWN:                           # Si se presiona una tecla,
            if game_over:                                          # Si el juego ha terminado,
                if event.key == pygame.K_r:                        # y se presiona 'R',
                    reiniciar_juego()                              # reinicia el juego.
                    puntajes = cargar_puntajes(nombre_jugador)     # Carga los puntajes del jugador.
                    if puntajes:                                   # Si hay puntajes,
                        usuario.actualizar_record(max(puntajes))   # actualiza el récord.
                elif event.key == pygame.K_n:                      # y se presiona 'N',
                    nuevo_jugador()                                # inicia un nuevo jugador.
            else:                                                  # Si el juego no ha terminado,
                x = jugador_pos[0]
                if event.key == pygame.K_LEFT:                     # y se presiona la flecha izquierda,
                    x -= jugador_size                              # mueve el jugador a la izquierda.
                if event.key == pygame.K_RIGHT:                    # y se presiona la flecha derecha,
                    x += jugador_size                              # mueve el jugador a la derecha.

                if x < 0:                                          # Si el jugador se sale de la ventana por la izquierda,
                    x = 0                                          # lo coloca en el borde izquierdo.
                if x > ANCHO - jugador_size:                       # Si el jugador se sale de la ventana por la derecha,
                    x = ANCHO - jugador_size                       # lo coloca en el borde derecho.

                jugador_pos[0] = x  # Actualiza la posición del jugador.

    if not game_over:                                                 # Si el juego no ha terminado,
        if enemigo_pos[1] >= 0 and enemigo_pos[1] < ALTO:             # y el enemigo está dentro de la pantalla,
            enemigo_pos[1] += 30                                      # mueve el enemigo hacia abajo.
        else:                                                         # Si el enemigo sale de la pantalla,
            enemigo_pos[0] = random.randint(0, ANCHO - enemigo_size)  # lo reposiciona horizontalmente.
            enemigo_pos[1] = 0                                        # lo reposiciona verticalmente.
            puntaje += 1           # Aumenta el puntaje.

        if detectar_colision(jugador_pos, enemigo_pos):               # Si hay una colisión,
            play_sound("assets/impacto.wav")    # reproduce el sonido de impacto.
            guardar_puntaje(nombre_jugador, puntaje)                  # Guarda el puntaje del jugador.
            usuario.actualizar_record(puntaje)                        # Actualiza el récord del jugador.
            game_over = True                                          # Establece que el juego ha terminado.

        ventana.blit(enemigo_img, (enemigo_pos[0], enemigo_pos[1]))   # Dibuja el enemigo en la pantalla.
        ventana.blit(jugador_img, (jugador_pos[0], jugador_pos[1]))   # Dibuja el jugador en la pantalla.

        mostrar_puntajes()  # Muestra los puntajes en la pantalla.

    else:  # Si el juego ha terminado,
        font = pygame.font.SysFont(None, 60)                                                          # Configura la fuente.
        texto = font.render(f"Fin del juego, Puntaje: {puntaje}", True, color_blanco)                 # Renderiza el texto del fin del juego.
        ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 100))                         # Muestra el texto del fin del juego en la pantalla.
        nombre_superficie = font.render(f"Jugador: {nombre_jugador}", True, color_blanco)             # Renderiza el nombre del jugador.
        ventana.blit(nombre_superficie, (ANCHO//2 - nombre_superficie.get_width()//2, ALTO//2 - 30))  # Muestra el nombre del jugador en la pantalla.
        font = pygame.font.SysFont(None, 40)                                                                       # Configura la fuente.
        texto_reiniciar = font.render("Presiona 'R' para reiniciar o 'N' para nuevo jugador", True, color_blanco)  # Renderiza el texto para reiniciar el juego o cambiar de jugador.
        ventana.blit(texto_reiniciar, (ANCHO//2 - texto_reiniciar.get_width()//2, ALTO//2 + 90))                   # Muestra el texto para reiniciar el juego o cambiar de jugador en la pantalla.

    pygame.display.flip()  # Actualiza la pantalla.
    clock.tick(30)         # Controla la velocidad del bucle principal del juego.