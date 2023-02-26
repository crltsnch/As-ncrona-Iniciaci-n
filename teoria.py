import asyncio   # para escribir asíncrona


async def main():     # Async convierte la función en subrutina
    print('Hola...')
    await asyncio.sleep(1)    # espera 1 segundo antes de imprimir el siguiente print. Imprimirá '...Mundo!' después de 1 segundo.
    print('...Mundo!')

asyncio.run(main())     # ejecutar una corrutina



''''El siguiente fragmento de código imprimirá 'hola' después de esperar 1 segundo
y luego imprimirá 'mundo' después de esperar otros 2 segundos'''

import time    # debemos importar time

async def decir_despues(retrasar, que):
    await asyncio.sleep(retrasar)
    print(que)

async def main():
    # Strftime() devuelve una cadena que representa la fecha y hora especifica, formateada según la especificación que le demos
    # como nosotros queremos la hora, usamos %X.
    print(f"Empieza a {time.strftime('%X')}")

    await decir_despues(1, 'Hola')
    await decir_despues(2, 'Mundo')

    print(f"Acaba a {time.strftime('%X')}")

asyncio.run(main())



'''Aqui modificamos el ejemplo anterior y ejecutamos dos corrutinas decir_despues concurrentemente'''

async def main():
    # create_task() para ejecutar corrutinas concurrentemente como asyncio Tasks.
    task1 = asyncio.create_task(decir_despues(1, 'Hola'))       
    task2 = asyncio.create_task(decir_despues(2, 'mundo'))

    print(f"Empieza a {time.strftime('%X')}")

    # espera hasta que se completen ambas tareas (debe tomar alrededor de 2 segundos)
    await task1
    await task2

    print(f"acaba a {time.strftime('%X')}")

 # en esta función se ejecuta 1 segundo mas rápido que antes


'''Funcion anterior con TaskGroup'''

'''async def main():
    #TaskGroup() para ejecutar corrutinas concurrentemente como asyncio Tasks.
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(decir_despues(1, 'Hola'))
        task2 = tg.create_task(decir_despues(2, 'world'))

        print(f"Empieza a {time.strftime('%X')}")
    
    # el await está implicito cuando usamos el with (context manager)

    print(f"acaba a {time.strftime('%X')}")

asyncio.run(main())'''


'''Decimos que un objeto es un objeto esperable si se puede utilizar en una expresión await. 
Muchas API de asyncio están diseñadas para aceptar los valores esperables.
Hay tres tipos principales de objetos esperables: corrutinas, Tareas y Futures.'''

'''CORRUTINAS: son esperables y por lo tanto se pueden esperar de otras corrutinas'''
async def anidado():
    return 42

async def main():
    anidado()   # esto no devuelve nada, se crea un objeto corrutina pero no devuelve nada
    print(await anidado())   # esto imprime "42", aquí anidado() es un objeto corrutina esperable

asyncio.run(main())

'''TAREAS: se utilizan para ejecutar corrutinas concurrentemente.'''
async def anidado():
    return 42

async def main():
    task = asyncio.create_task(anidado())   # crea una tarea para ejecutar anidado() y la devuelva
    print(await task)   # espera hasta que la tarea se complete y devuelve el valor de return de anidado()

asyncio.run(main())

'''FUTURES: es un objeto esperable especial que representa un resultado eventual de una operación asíncrona.
Cuando un objeto Future es esperado significa que la corrutina esperará hasta que el Future se resuelva en algún otro lugar.'''

#async def main():
#    await funcion_que_devuelve_un_objeto_future():
#    await asyncio.gather(funcion_que_devuelve_un_objeto_future(), alguna_corrutina())  #.gather() agrupa varios objetos esperados juntos

'''ASYNCIO:CREATE_TASK(CORO, *, NAME=None, CONTEST=None)'''
'''Envuelve un acoroutine (coro) en un task y programa su ejecucion. Retorna el objeto tarea'''
# si name es None, se establece como el nombre de la tarea mediante task.set_name()
# get_running_loop() ejecuta la tarea en el bucle retornado

#background_tasks = set()
#for i in range(10):
#    task = asyncio.create_task(some_coro(i))
#    background_tasks.add(task)     #añadimos
#    task.add_done_callback(background_tasks.discard)   #para evitar que queden las referencias de las tareas finalizadas esto hace que cada tarea elimine su propia referencia del conjunto
