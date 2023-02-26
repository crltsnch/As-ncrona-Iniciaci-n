import asyncio   # para escribir asíncrona


async def main():     # Async convierte la función en subrutina
    print('Hola...')
    await asyncio.sleep(1)    # espera 1 segundo antes de imprimir el siguiente print. Imprimirá '...Mundo!' después de 1 segundo.
    print('...Mundo!')

asyncio.run(main())     # ejecutar una corrutina
main()


# El siguiente fragmento de código imprimirá 'hola' después de esperar 1 segundo
# y luego imprimirá 'mundo' después de esperar otros 2 segundos

import time    # debemos importar time

async def decir_despues(retrasar, que):
    await asyncio.sleep(retrasar)
    print(que)
    