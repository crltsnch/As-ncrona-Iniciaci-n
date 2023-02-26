import asyncio   # para escribir asíncrona


async def main():     # Async convierte la función en subrutina
    print('Hola...')
    await asyncio.sleep(1)    # espera 1 segundo antes de imprimir el siguiente print. Imprimirá '...Mundo!' después de 1 segundo.
    print('...Mundo!')

asyncio.run(main())     # ejecutar una corrutina



# El siguiente fragmento de código imprimirá 'hola' después de esperar 1 segundo
# y luego imprimirá 'mundo' después de esperar otros 2 segundos

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



#Aqui modificamos el ejemplo anterior y ejecutamos dos corrutinas decir_despues concurrentemente

async def main():
    # create_task() para ejecutar corrutinas concurrentemente como asyncio Tasks.
    task1 = asyncio.create_task(decir_despues(1, 'Hola'))       
    task2 = asyncio.create_task(decir_despues(2, 'mundo'))

    print(f"Empieza a {time.strftime('%X')}")

    # espera hasta que se completen ambas tareas (debe tomar alrededor de 2 segundos)
    await task1
    await task2

