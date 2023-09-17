# programa que llama al pai de telegram para pedir actualizaciones dentro de un bucle infinito
# y que llama a la funcion que procesa las actualizaciones sin usar ninguna librería externa de telegram

import time
import httpx
import json
import random
import string

token = 'your_token'
url_base = f'https://api.telegram.org/bot{token}/'

def generatePassword(num=10):
    # Generamos una contraseña aleatoria de num caracteres
    letras = string.ascii_letters + string.digits
    password = ''.join(random.choice(letras) for i in range(num))
    return password

# Llamamos a deleteWebhook para que no haya un webhook activo
r = httpx.get(url_base + 'deleteWebhook')
offset = 0

while True:
    # Llamamos a getUpdates para pedir actualizaciones
    # con offset+1 para que no nos devuelva las actualizaciones que ya hemos procesado
    r = httpx.get(url_base + 'getUpdates', params={'offset': offset+1})
    if r.status_code != 200:
        print('Error en la petición')
        print(r.text)
        time.sleep(1)
        continue
    updates = r.json()['result']
    for update in updates:
        offset = update['update_id']
        if 'message' in update:
            message = update['message']
            if 'text' in message:
                text = message['text']
                if 'from' in update['message']:
                    user = update['message']['from']
                    # Si text contiene la palabra password, respondemos con un mensaje
                    if 'password' in text:
                        respuesta = 'La contraseña es ' + generatePassword(10)
                    else:
                        respuesta = 'No se lo que quieres'
                    r = httpx.post(url_base + 'sendMessage', data={'chat_id': user['id'], 'text': respuesta})
                else:
                    continue #Solo respondemos a mensajes de usuarios
    time.sleep(1) # Esperamos un segundo antes de volver a pedir actualizaciones
                



