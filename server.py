#!/usr/bin/env python3
"""
TCP to HTTP Bridge Server - Gateway TS-RF
Basado en el servidor AWS de OnesilverM
Recibe datos TCP del Gateway serial y los reenvía a tu hosting vía HTTP POST
"""

import socket
import requests
import time
from datetime import datetime

# Configuración
TCP_HOST = '0.0.0.0'  # Escuchar en todas las interfaces
TCP_PORT = 22222      # Puerto donde el gateway se conectará
TARGET_URL = 'https://silvercastlesoft.com/ts/ts-rf_receive.php'

def iniciar_servidor():
    """Inicia el servidor TCP con reinicio automático"""
    while True:
        try:
            # Crear un socket TCP/IP
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Asignar IP y puerto
            servidor.bind((TCP_HOST, TCP_PORT))

            # Escuchar conexiones entrantes
            servidor.listen(1)
            print(f"[{datetime.now()}] ✓ Servidor TCP iniciado")
            print(f"[{datetime.now()}] ✓ Esperando conexiones en {TCP_HOST}:{TCP_PORT}...")
            print(f"[{datetime.now()}] ✓ Reenviando datos a: {TARGET_URL}")

            # Aceptar una conexión
            conexion, direccion = servidor.accept()
            print(f"[{datetime.now()}] ✓ Conexión establecida desde {direccion}")

            while True:
                try:
                    # Recibir datos (hasta 1024 bytes a la vez)
                    datos = conexion.recv(1024)

                    # Si no hay más datos, salir del bucle interno
                    if not datos:
                        print(f"[{datetime.now()}] La conexión ha sido cerrada.")
                        break

                    # Decodificar datos (intentar UTF-8, si falla usar latin-1)
                    try:
                        mensaje = datos.decode('utf-8')
                    except:
                        mensaje = datos.decode('latin-1')
                    
                    print(f"[{datetime.now()}] Datos recibidos ({len(datos)} bytes): {mensaje[:100]}")
                    print(f"[{datetime.now()}] Datos HEX: {datos.hex()[:100]}...")

                    # Enviar datos a tu servidor PHP
                    try:
                        response = requests.post(
                            TARGET_URL,
                            params={'data': mensaje},
                            data=datos,
                            headers={'Content-Type': 'application/octet-stream'},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            print(f"[{datetime.now()}] ✓ Datos enviados exitosamente al servidor PHP")
                        else:
                            print(f"[{datetime.now()}] ✗ Error al enviar datos: {response.status_code}")
                    
                    except Exception as e:
                        print(f"[{datetime.now()}] ✗ Error en solicitud POST: {e}")

                except Exception as e:
                    print(f"[{datetime.now()}] ✗ Error al procesar datos: {e}")
                    break  # Salir del bucle interno para reconectar
        
        except Exception as e:
            print(f"[{datetime.now()}] ✗ Error en el servidor: {e}")
            print(f"[{datetime.now()}] Reiniciando en 5 segundos...")
            time.sleep(5)  # Esperar 5 segundos antes de reiniciar

        finally:
            # Cerrar la conexión si está abierta
            try:
                conexion.close()
                servidor.close()
            except:
                pass

if __name__ == '__main__':
    print("=" * 70)
    print("TCP to HTTP Bridge Server - Gateway TS-RF")
    print("Basado en servidor AWS OnesilverM")
    print("=" * 70)
    iniciar_servidor()
