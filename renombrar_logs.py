#!/usr/bin/env python3
"""Script para filtrar y renombrar archivos .log de forma secuencial.

Patrón de salida: nombre_apellido_<numero>.log
Estudiante: Rodrigo Mera R.
Asignatura: Procesos Informáticos (IACC, 2026)
"""

from pathlib import Path
import sys


def renombrar_archivos_log(directorio: str | Path, prefijo: str = "rodrigo_mera") -> list[tuple[Path, Path]]:
    """Filtra los archivos con extensión .log y los renombra secuencialmente.
    
    Args:
        directorio: Ruta a la carpeta que contiene los archivos.
        prefijo: Prefijo con formato nombre_apellido.
        
    Returns:
        Lista de tuplas con (ruta_original, ruta_nueva).
    """
    ruta_dir = Path(directorio).resolve()
    if not ruta_dir.exists() or not ruta_dir.is_dir():
        print(f"Error: El directorio '{ruta_dir}' no existe o no es válido.", file=sys.stderr)
        return []

    # Filtrar únicamente archivos regulares cuya extensión sea .log
    archivos_log = [
        f for f in ruta_dir.iterdir()
        if f.is_file() and f.suffix.lower() == ".log"
    ]

    # Ordenar alfabéticamente para asegurar un orden predecible
    archivos_log.sort(key=lambda x: x.name.lower())

    if not archivos_log:
        print(f"No se encontraron archivos .log en '{ruta_dir}'.")
        return []

    print(f"Directorio de trabajo: {ruta_dir}")
    print(f"Archivos .log encontrados para procesar: {len(archivos_log)}")
    print("-" * 65)

    renombrados = []
    # Renombrado en dos pasos si fuese necesario, o directo con contador 1 a n
    for indice, archivo in enumerate(archivos_log, start=1):
        nuevo_nombre = f"{prefijo}_{indice}.log"
        nueva_ruta = ruta_dir / nuevo_nombre

        # Evitar sobreescritura accidental si el nombre ya existiera y no fuera el mismo archivo
        if nueva_ruta.exists() and nueva_ruta != archivo:
            print(f"Advertencia: '{nuevo_nombre}' ya existe. Se omitirá para evitar colisión.")
            continue

        archivo.rename(nueva_ruta)
        print(f" [OK] {archivo.name:<25} -> {nuevo_nombre}")
        renombrados.append((archivo, nueva_ruta))

    print("-" * 65)
    print(f"Proceso finalizado. Total de archivos renombrados: {len(renombrados)}")
    return renombrados


if __name__ == "__main__":
    carpeta_objetivo = sys.argv[1] if len(sys.argv) > 1 else "."
    renombrar_archivos_log(carpeta_objetivo)
