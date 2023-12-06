import websockets
import asyncio
import ssl
import json
import vgamepad as vg
import websockets.exceptions
from time import sleep
import pyautogui
import pydirectinput

stick_max = 32768
gamepad = vg.VX360Gamepad()

def processingMessage(message):
    try:
        message = float(message)
    except:
        pass

    if isinstance(message, float):
        tilt = (stick_max *(abs(message) / 10))
        
        if message < 0:
            #LEFT
            gamepad.left_joystick(x_value=int(tilt), y_value=0)
        
        else:
            gamepad.left_joystick(x_value=-int(tilt), y_value=0)
        
        gamepad.update()
    else:
        if message[0] == "a":
            tiltBreak = ((int(message[1:]) *2.55))
            gamepad.left_trigger(value=int(tiltBreak))
            gamepad.update()
            print(tiltBreak)

        elif message[0] == "b":
            tiltGas = ((int(message[1:]) *2.55))
            gamepad.right_trigger(value=int(tiltGas))
            gamepad.update()
            print(tiltGas)
        
        elif message[0] == "f":
            fovsl = float(message[1:])
            
            if fovsl == 1:
                pydirectinput.keyUp("num6")
                pydirectinput.keyUp("num5")
                pydirectinput.keyDown("num4")
            elif fovsl == 100:
                pydirectinput.keyUp("num4")
                pydirectinput.keyUp("num5")
                pydirectinput.keyDown("num6")
            else:
                pydirectinput.keyUp("num4")
                pydirectinput.keyUp("num6")
                pydirectinput.keyDown("num5")

            gamepad.update()

        elif message == "lookLeft":
            pydirectinput.keyDown("[")
            pydirectinput.keyUp("[")
            print("dasdas")
        elif message == "lookRight":
            pydirectinput.keyDown("]")
            pydirectinput.keyUp("]")

        elif message == "T":
            pydirectinput.keyDown("t")
            pydirectinput.keyUp("t")

        elif message == "F1":
            pydirectinput.keyDown("f1")
            pydirectinput.keyUp("f1")






ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# Generate with Lets Encrypt, copied to this location, chown to current user and 400 permissions
ssl_cert = "C:/cert.pem"
ssl_key = "C:/key.pem"

ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)

all_clients = []

async def send_message(message: str):
    for client in all_clients:
        try:
            await client.send(message)
        except:
            loop = asyncio.get_running_loop()
            loop.stop()
STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(client_socket: websockets.WebSocketClientProtocol, path: str):
    # register(websocket) sends user_event() to websocket
    print("new Client Connected")
    all_clients.append(client_socket)
    while True:
        try:
            new_message = await client_socket.recv()
        except:
            loop = asyncio.get_running_loop()
            loop.stop()
        processingMessage(new_message)
        await send_message(message=new_message)






start_server = websockets.serve(counter, "HOST IP", 12345, ssl=ssl_context)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
