#!/usr/bin/env python3
"""
inicializar_bd.py

Crea la base de datos `agua_potable.db` a partir de los archivos
`schema.sql` y `seed.sql` ubicados en el mismo directorio.

Uso:
    python3 inicializar_bd.py

Autor: Angel de Jesús Canela Figueroa
"""

import sqlite3
import sys
from pathlib import Path


DB_NAME = "agua_potable.db"
SCHEMA_FILE = "schema.sql"
SEED_FILE = "seed.sql"


if sys.stdout.isatty():
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
else:
    GREEN = YELLOW = RED = CYAN = BOLD = RESET = ""


def info(msg):
    print(f"{CYAN}[i]{RESET} {msg}")


def ok(msg):
    print(f"{GREEN}[OK]{RESET} {msg}")


def warn(msg):
    print(f"{YELLOW}[!]{RESET} {msg}")


def error(msg):
    print(f"{RED}[X]{RESET} {msg}", file=sys.stderr)


def check_files():
    base = Path(__file__).parent
    schema_path = base / SCHEMA_FILE
    seed_path = base / SEED_FILE

    if not schema_path.exists():
        error(f"No se encontro {SCHEMA_FILE} en {base}")
        sys.exit(1)
    if not seed_path.exists():
        error(f"No se encontro {SEED_FILE} en {base}")
        sys.exit(1)

    return schema_path, seed_path


def init_db(schema_path, seed_path):
    db_path = Path(__file__).parent / DB_NAME

    if db_path.exists():
        warn(f"El archivo {DB_NAME} ya existe.")
        respuesta = input("  Sobrescribir? [s/N]: ").strip().lower()
        if respuesta != "s":
            info("Cancelado. No se modifico ningun archivo.")
            sys.exit(0)
        db_path.unlink()
        info("Archivo anterior eliminado.")

    info(f"Creando base de datos: {DB_NAME}")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        ok("Estructura de tablas y vistas creada correctamente.")

        with open(seed_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        ok("Datos iniciales insertados (categorias de gasto y ofertas anuales).")

        conn.commit()
        ok(f"Base de datos '{DB_NAME}' lista para usarse.")
    except sqlite3.Error as e:
        error(f"Error al ejecutar SQL: {e}")
        sys.exit(1)
    finally:
        conn.close()


def main():
    print(f"{BOLD}Inicializador de la base de datos - Comite de Agua Potable{RESET}")
    print("=" * 60)

    schema_path, seed_path = check_files()
    init_db(schema_path, seed_path)

    print("=" * 60)
    print(f"{BOLD}Siguiente paso:{RESET} abre {DB_NAME} con DB Browser for SQLite")
    print("o ejecuta 'python3 datos_prueba_completos.py' para cargar datos de prueba.")


if __name__ == "__main__":
    main()
