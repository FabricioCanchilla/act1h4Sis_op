# Practica: clasificacion de documentos con 4 hilos

Es un programa en Python con cuatro trabajadores (Isaac, Carlos, Ana y Maria) que sacan documentos de una cola compartida y los procesan al mismo tiempo. Al final muestra cuantos documentos se procesaron en total y cuantos hizo cada uno.

Para correrlo: `python 1.py`

## 1. ¿Por que use `queue.Queue` para repartir los trabajos?

Porque `Queue` ya viene lista para que varios hilos la usen a la vez, asi que no me toco armar un lock aparte para sacar documentos. Con `get_nowait()` el hilo revisa y saca el documento de una sola vez, y por eso dos trabajadores nunca agarran el mismo ni se pierde ninguno. Cada documento se procesa una sola vez.

## 2. ¿Que protege el `Lock` y que pasaria sin el?

Protege lo que comparten todos los hilos: el diccionario `resultados` y la lista `registro`. Con `with lock:` solo un hilo a la vez puede modificarlos.

Sin el lock habria una condicion de carrera. `resultados[nombre] += 1` parece una sola operacion, pero son tres: Python lee el valor, le suma 1 y lo guarda. Si dos hilos lo hacen justo al mismo tiempo, uno pisa lo del otro y se pierde una cuenta. El resumen saldria con menos de 24 documentos aunque todos se hayan procesado. Y lo peor es que cambiaria en cada ejecucion, asi que seria un error bien dificil de encontrar.

## 3. ¿Que cambiaria si cada documento se guardara en un archivo real?

- Cambiaria el `time.sleep()` por la escritura real del archivo, usando `with open(...)` para que siempre se cierre bien.
- Haria que cada documento vaya a su propio archivo (por ejemplo, uno por ID), asi dos hilos nunca escriben en el mismo y no se mezcla nada. Si todos tuvieran que escribir en un solo archivo, ahi si necesitaria otro lock.
- Le pondria un `try/except` por si falla el disco o el archivo, para que un error con un documento no deje el hilo colgado ni se pierda sin avisar.
- Los hilos seguirian siendo buena opcion: escribir en disco es entrada/salida, y mientras un hilo espera al disco, los demas pueden seguir trabajando.