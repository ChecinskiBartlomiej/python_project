import argparse
from pathlib import Path

def create_parser():
    parser = argparse.ArgumentParser(description="Analiza danych PSP, JST, zezwoleń alkoholowych i populacji") 

    # argument 1: nazwa pliku wyjściowego
    parser.add_argument(
        '-o', '--output',
        type=Path,
        required=True,
        help='Ścieżka i nazwa pliku, do którego zapisane zostaną wyniki analizy (np. wyniki.csv)'
    )

    # argument 2: katalog z danymi
    parser.add_argument(
        '-d', '--data-dir',
        type=Path,
        required=True,
        help='Ścieżka do katalogu zawierającego wszystkie pliki danych (.csv, .xls, .xlsx)'
    )

    #argument 3:
    parser.add_argument(
        '-p', '--profile-output',
        type=Path,
        required=True,
        help="Ścieżka do katalogu zawierającego profilingu"
    )

    return parser



#python3 parser.py -d ./data/raw -o wyniki.txt -p profile.stats

