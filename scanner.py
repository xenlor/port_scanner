import socket
import argparse
import concurrent.futures
from datetime import datetime
import sys

# Puertos comunes para escanear por defecto
POPULAR_PORTS = [
    20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 
    993, 995, 1433, 3306, 3389, 5432, 5900, 8080
]

def scan_port(target, port, timeout):
    """
    Intenta conectar a un puerto específico en el objetivo.
    Retorna una tupla: (puerto, estado).
    """
    try:
        # Crear objeto socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establecer tiempo de espera (timeout)
        s.settimeout(timeout)
        # Intentar conectar. connect_ex retorna 0 si tiene éxito.
        result = s.connect_ex((target, port))
        s.close()
        
        if result == 0:
            return port, "ABIERTO"
        elif result == 10035: # Código de error para operación que bloquearía (EWOULDBLOCK)
            return port, "TIEMPO_AGOTADO"
        else:
            return port, "CERRADO"
    except socket.timeout:
        return port, "TIEMPO_AGOTADO"
    except Exception as e:
        return port, f"ERROR: {e}"

def run_scanner(target, ports, threads, timeout, verbose):
    print(f"-" * 50)
    print(f"Escaneando Objetivo: {target}")
    if len(ports) > 20:
        print(f"Escaneando {len(ports)} puertos (Rango o Lista larga)")
    else:
        print(f"Escaneando Puertos: {ports}")
    print(f"Hilos: {threads}, Tiempo de espera: {timeout}s, Detallado: {verbose}")
    print(f"Inicio: {datetime.now()}")
    print(f"-" * 50)

    open_ports = []
    
    # Usar ThreadPoolExecutor para escaneo concurrente (varios puertos a la vez)
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        # Crear un diccionario que mapea la ejecución futura al número de puerto
        future_to_port = {
            executor.submit(scan_port, target, port, timeout): port 
            for port in ports
        }
        
        # Procesar los resultados a medida que se completan
        for future in concurrent.futures.as_completed(future_to_port):
            port, status = future.result()
            if status == "ABIERTO":
                print(f"Puerto {port} está ABIERTO")
                open_ports.append(port)
            elif verbose:
                print(f"Puerto {port} está {status}")

    # Ordenar la lista de puertos encontrados
    open_ports.sort()
    
    print(f"-" * 50)
    print(f"Escaneo completado. Se encontraron {len(open_ports)} puertos abiertos.")
    print(f"Puertos Abiertos: {open_ports}")
    print(f"Fin: {datetime.now()}")

def parse_ports(port_arg):
    """
    Parsea un string de puertos (ej: "80,443,1000-2000") y retorna una lista de enteros.
    """
    ports = set()
    parts = port_arg.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            except ValueError:
                print(f"[!] Advertencia: Rango inválido ignorado: {part}")
        else:
            try:
                ports.add(int(part))
            except ValueError:
                print(f"[!] Advertencia: Puerto inválido ignorado: {part}")
    return sorted(list(ports))

def main():
    # Configuración de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Escáner de Puertos en Python (Multi-hilo)")
    parser.add_argument("target", help="Dirección IP o nombre de host a escanear")
    parser.add_argument("-p", "--ports", help="Puertos a escanear (ej: 22,80,1000-2000)")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Número de hilos (por defecto: 1)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Tiempo de espera del socket en segundos (por defecto: 1.0)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar todos los resultados (cerrados/tiempo agotado)")
    
    args = parser.parse_args()
    
    # Resolver nombre de host a IP si es necesario
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"Error: No se pudo resolver el nombre de host {args.target}")
        return

    # Determinar qué puertos escanear
    if args.ports:
        ports_to_scan = parse_ports(args.ports)
        if not ports_to_scan:
            print("Error: No se especificaron puertos válidos.")
            return
    else:
        # Por defecto usar puertos populares
        print("[*] No se especificaron puertos (-p). Escaneando puertos populares por defecto.")
        ports_to_scan = POPULAR_PORTS

    # Ejecutar el escáner manejando la interrupción del usuario (Ctrl+C)
    try:
        run_scanner(target_ip, ports_to_scan, args.threads, args.timeout, args.verbose)
    except KeyboardInterrupt:
        print("\n[!] Escaneo interrumpido por el usuario.")
        sys.exit(0)

if __name__ == "__main__":
    main()
