#!/usr/bin/env python3
"""
MOVETONI - Sistema de precios. Entrada principal.
Uso:
  Modo interactivo: python main.py
  Línea de comandos: python main.py "origen" "destino" [--event 0|1|2]
"""

import argparse
import sys

import config
from core import get_pricing_result


def run_pricing(origin: str, destination: str, event_level: int = 0) -> None:
    """Ejecuta el cálculo de precio y muestra el resultado"""
    print("Obteniendo información de la ruta...")
    result = get_pricing_result(origin, destination, event_level)

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"  Distancia: {result['distance_km']} km, Duración estimada: {result['duration_min']} min")
    print(f"  Tiempo en destino: {result['weather_description']}")

    print()
    print("=" * 40)
    print("Resultado del precio")
    print("=" * 40)
    print(f"  Precio base:     {result['base_price']} €")
    print(f"  Coeficiente dinámico:     {result['surge_multiplier']} (H={result['factors']['H']}, W={result['factors']['W']}, D={result['factors']['D']}, E={result['factors']['E']})")
    print(f"  Precio final:     {result['final_price']} €")
    print("=" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="MOVETONI - Cálculo de precios para motosharing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py                    # Modo interactivo, introducir origen y destino
  python main.py "Madrid Sol" "Madrid Barajas"
  python main.py "Madrid Sol" "Madrid Barajas" --event 1
        """,
    )
    parser.add_argument("origin", nargs="?", help="Dirección de origen (vacío = modo interactivo)")
    parser.add_argument("destination", nargs="?", help="Dirección de destino")
    parser.add_argument(
        "--event",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Nivel de evento especial: 0=none, 1=medio, 2=grave (por defecto 0)",
    )
    args = parser.parse_args()

    if not config.GOOGLE_MAPS_API_KEY:
        print("Error: GOOGLE_MAPS_API_KEY no configurada.")
        print("Copie .env.example a .env e introduzca su API Key.")
        sys.exit(1)

    if args.origin is None:
        # Modo interactivo
        print("\n--- MOVETONI Cálculo de precios (modo interactivo) ---\n")
        origin = input("Introduzca el origen: ").strip()
        if not origin:
            print("Error: El origen no puede estar vacío.")
            sys.exit(1)
        destination = input("Introduzca el destino: ").strip()
        if not destination:
            print("Error: El destino no puede estar vacío.")
            sys.exit(1)
        event_input = input("Nivel de evento especial [0=ninguno/1=medio/2=grave, Enter=0]: ").strip()
        event_level = 0
        if event_input in ("1", "2"):
            event_level = int(event_input)
        run_pricing(origin, destination, event_level)
    else:
        # Modo línea de comandos
        if args.destination is None:
            print("Error: Debe especificar el destino cuando se especifica el origen.")
            sys.exit(1)
        run_pricing(args.origin, args.destination, args.event)


if __name__ == "__main__":
    main()
