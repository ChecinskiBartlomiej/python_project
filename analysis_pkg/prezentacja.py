import parser
import analiza
from pathlib import Path
import cProfile
import pstats

def run(data_dir: Path, output_file: Path):
    df_area, df_fires, df_alcohol, df_population = analiza.wczytaj_dane(data_dir)
    df_area, df_fires, df_alcohol, df_population = analiza.uporzadkuj_dane(df_area, df_fires, df_alcohol, df_population)
    analiza.oblicz_statystyki(df_area, df_fires, df_alcohol, df_population, output_file)
    analiza.hipotezy(df_area, df_fires, df_alcohol, df_population, output_file)

def main():
    args = parser.create_parser().parse_args()
    data_dir      = args.data_dir
    output_file   = args.output
    profile_file  = args.profile_output

    if not data_dir.is_dir():
        raise SystemExit(f"Katalog nie istnieje")

    #Uruchomienie kodu profilerem cProfile.
    cProfile.runctx(
        'run(data_dir, output_file)',
        globals(), locals(),
        filename=str(profile_file)
    )

    #Wczytanie i przeanalizowanie wyników profilowania za pomocą pstats.
    stats = pstats.Stats(str(profile_file))
    stats.strip_dirs().sort_stats('cumtime')

    #Wypisanie 20 najwolniejszych funkcji na standardowe wyjście.
    print("\nTop 20 najwolniejszych funkcji wg czasu kumulatywnego:")
    stats.print_stats(20)

    #Zapisanie raportu profilowania do osobnego pliku tekstowego.
    report_path = profile_file.with_suffix('.txt')
    with report_path.open('w', encoding='utf-8') as pf:
        stats_txt = pstats.Stats(str(profile_file), stream=pf)
        stats_txt.strip_dirs().sort_stats('cumtime').print_stats(20)
    print(f"Profiling zapisany do {report_path}\n")

    #Wyświetlenie raportu analizy.
    report = Path(output_file).read_text(encoding='utf-8')
    print("Analiza danych:\n", report)

if __name__ == '__main__':
    main()
    
#python3 prezentacja.py -d ./data/raw -o wyniki.txt -p profile.stats



