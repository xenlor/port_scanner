# Python Port Scanner

Un escáner de puertos de línea de comandos rápido y flexible escrito en Python. Diseñado para ser simple de usar pero potente, con soporte para escaneo concurrente (multi-hilo).

## Características

*   **Rápido:** Utiliza `concurrent.futures` para escanear múltiples puertos simultáneamente.
*   **Flexible:** Permite especificar puertos individuales, rangos o listas combinadas (ej: `22,80,1000-2000`).
*   **Inteligente:** Si no se especifican puertos, escanea automáticamente los puertos más populares/comunes.
*   **Configurable:** Control total sobre el número de hilos (`threads`) y el tiempo de espera (`timeout`).
*   **Modo Verbose:** Opción `-v` para ver qué puertos están cerrados o dan timeout, útil para depuración.

## Requisitos

*   Python 3.x
*   No requiere librerías externas (usa solo la librería estándar).

## Uso

La sintaxis básica es:

```bash
python scanner.py <objetivo> [opciones]
```

### Ejemplos

**1. Escaneo rápido de puertos populares (por defecto):**
```bash
python scanner.py google.com
```

**2. Escanear un puerto específico:**
```bash
python scanner.py 192.168.1.1 -p 22
```

**3. Escanear un rango de puertos:**
```bash
python scanner.py localhost -p 1-100
```

**4. Escanear una lista compleja de puertos y rangos:**
```bash
python scanner.py mi-servidor.com -p 22,80,443,8000-8080
```

**5. Escaneo lento y seguro (para evitar firewalls):**
Usa 1 solo hilo y un timeout mayor.
```bash
python scanner.py scanme.nmap.org -t 1 --timeout 2.0
```

### Argumentos Disponibles

| Argumento | Descripción |
| :--- | :--- |
| `target` | **Requerido.** IP o dominio a escanear. |
| `-p`, `--ports` | Puertos a escanear. Soporta listas y rangos (ej: `22,80-100`). Si se omite, usa puertos populares. |
| `-t`, `--threads` | Número de hilos simultáneos. Por defecto: `1` (para mayor estabilidad). |
| `--timeout` | Tiempo de espera por puerto en segundos. Por defecto: `1.0`. |
| `-v`, `--verbose` | Muestra todos los resultados, incluyendo puertos cerrados o con timeout. |

## Disclaimer

Esta herramienta ha sido creada con fines educativos y de administración de redes. El escaneo de puertos en servidores ajenos sin autorización puede ser ilegal o violar los términos de servicio de tu proveedor de internet. Úsala responsablemente.
