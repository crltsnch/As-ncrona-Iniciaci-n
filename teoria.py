import asyncio   #para escribir concurrente


async def main():     #Async convierte la función en subrutina
    print('Hola...')
    await asyncio.sleep(1)    #espera 1 segundo antes de imprimir el siguiente print. Imprimirá '...Mundo!' después de 1 segundo.
    print('...Mundo!')

