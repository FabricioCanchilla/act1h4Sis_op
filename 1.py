import threading
import queue
import time
import random

trabajos = queue.Queue()
resultados = {}
registro = []
lock = threading.Lock()

for doc_id in range(1, 25):
    trabajos.put((doc_id, random.randint(1, 5)))


def trabajador(nombre):
    with lock:
        resultados[nombre] = 0

    while True:
        try:
            doc_id, tamano = trabajos.get_nowait()
        except queue.Empty:
            print(f"{nombre}: ya no queda nada")
            break

        print(f"{nombre} esta trabajando en el doc... {doc_id} (tamaño {tamano})")
        time.sleep(tamano * 0.1)

        with lock:
            resultados[nombre] += 1
            registro.append((nombre, doc_id))
        print(f"{nombre} terminó el doc {doc_id}")


nombres = ["Isaac", "Carlos", "Ana", "Maria"]
hilos = []

for nombre in nombres:
    h = threading.Thread(target=trabajador, args=(nombre,))
    hilos.append(h)
    h.start()

for h in hilos:
    h.join()

print("\n los cuatro trabajadores ya terminaron.")

print("\n===== Así quedó el reparto =====")
total = 0
for nombre, cantidad in resultados.items():
    print(f"{nombre} se encargó de {cantidad} documentos")
    total += cantidad

print(f"\nEntre todos procesaron {total} documentos en total.")

if total == 24:
    print("Verificación 1: todo bien, salieron los 24 documentos.")
else:
    print(f"Verificación 1: algo falló, esperaba 24 y salieron {total}.")

ids_procesados = [doc_id for nombre, doc_id in registro]
if len(ids_procesados) == len(set(ids_procesados)) == 24:
    print("Verificación 2: todo bien, ningún documento se procesó dos veces.")
else:
    print("Verificación 2: algo falló, hay documentos repetidos o que faltan.")

if not any(h.is_alive() for h in hilos):
    print("Verificación 3: todo bien, ningún hilo se quedó colgado.")
else:
    print("Verificación 3: algo falló, todavía hay un hilo corriendo.")