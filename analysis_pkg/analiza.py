import pandas as pd
from pathlib import Path

def wczytaj_dane(data_dir: Path):

    #Wczytujemy pliki, używając data_dir / nazwa_pliku.
    df_area = pd.read_excel(
        data_dir / 'wykaz_powierzchni_wg_stanu.xlsx',
        engine='openpyxl',
        usecols=[1,2,3],
        names=['Nazwa jednostki','Pow_ha','Pow_km2'],
        header=0
    )
    df_fires = pd.read_csv(data_dir / 'pozary.csv')
    df_alcohol = pd.read_csv(data_dir / 'raport_zezwolen_alkoholowych.csv')
    df_population = pd.read_excel(
        data_dir / 'tabela02.xls',
        skiprows=[0,1,2,3,4,5,7,8],
        usecols=[0,1],
        engine='xlrd',
        names=['Województwo','Populacja'],
        header=0
    )
    return df_area, df_fires, df_alcohol, df_population

def uporzadkuj_dane(df_area, df_fires, df_alcohol, df_population):

    #Uporzadkowanie danych.
    mask = df_area['Nazwa jednostki'].astype(str).str.strip().str.upper().str.startswith('WOJ.')
    df_area = df_area[mask].reset_index(drop=True)
    df_area = df_area.sort_values(
    by='Nazwa jednostki',
    key=lambda col: col.str.replace(r'(?i)^WOJ\.\s*', '', regex=True)
    ).reset_index(drop=True)

    df_fires = (
    df_fires
    .groupby('Województwo', as_index=False)['RAZEM Pożar (P)']
    .sum()
    .rename(columns={'RAZEM Pożar (P)': 'Liczba_pozarow'})
    .sort_values('Województwo')      
    .reset_index(drop=True)
    )

    df_alcohol = (
    df_alcohol
    .groupby('Województwo', as_index=False)   
    .size()                                   
    .rename(columns={'size': 'Liczba_firm'})
    .sort_values('Województwo')               
    .reset_index(drop=True)
    )
    
    df_population = (
    df_population
    .sort_values("Województwo")
    .reset_index(drop=True)
    )
    return df_area, df_fires, df_alcohol, df_population

def oblicz_statystyki(df_area, df_fires, df_alcohol, df_population, output_file: Path):

    # Obliczenie statystyk.
    stats_area  = df_area[['Pow_ha','Pow_km2']].describe()
    stats_pop   = df_population['Populacja'].describe()
    stats_fires = df_fires['Liczba_pozarow'].describe()
    stats_firms = df_alcohol['Liczba_firm'].describe()

    #Zapisanie do pliku.
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== Powierzchnia województw ===\n")
        f.write(stats_area.to_string())
        f.write("\n\n=== Populacja ===\n")
        f.write(stats_pop.to_string())
        f.write("\n\n=== Liczba pożarów ===\n")
        f.write(stats_fires.to_string())
        f.write("\n\n=== Liczba firm ===\n")
        f.write(stats_firms.to_string())
        f.write("\n")

def hipotezy(df_area, df_fires, df_alcohol, df_population, output_file: Path):

    #Nowa ramka danych do hipotez.
    new_df = pd.DataFrame({
    'Województwo':         df_population.iloc[:, 0],
    'Liczba_mieszkancow':  df_population.iloc[:, 1],
    'Liczba_pozarow':      df_fires.iloc[:, 1],
    'Liczba_firm':         df_alcohol.iloc[:, 1],
    'Powierzchnia_km2':    df_area.iloc[:, 1],
    })
    
    # Hipoteza 1 Czym wiecej ludzi tym wiecej pozarow.
    corr1 = new_df['Liczba_mieszkancow'].corr(new_df['Liczba_pozarow'])

    # Hipoteza 2 Czym wiecej ludzi tym wiecej firm.
    corr2 = new_df['Liczba_mieszkancow'].corr(new_df['Liczba_firm'])
    
    # Hipoteza 3 Czym wiecej firm alkoholowych tym wiecej pozarow.
    corr3 = new_df['Liczba_firm'].corr(new_df['Liczba_pozarow'])
    
    # Hipoteza 4 Czym większa powierzchnia tym więcej ludzi.
    corr4 = new_df['Powierzchnia_km2'].corr(new_df['Liczba_mieszkancow'])

    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"Hipoteza 1: liczba mieszkańców jest pozytywnie skorelowana z liczbą pożarów\n")
        f.write(f"Korelacja Pearsona między liczbą mieszkańców a liczbą pożarów: {corr1:.3f}\n")
        f.write(f"Hipoteza 2: Liczba mieszkańców jest pozytywnie skorelowana z liczbą przedsiębiorstw mających zezwolenie na handel hurtowy napojami alkoholowymi\n")
        f.write(f"Korelacja Pearsona między liczbą mieszkańców a liczbą firm: {corr2:.3f}\n")
        f.write(f"Hipoteza 3: Liczba pożarów jest pozytywnie skorelowana z liczbą przedsiębiorstw mających zezwolenie na handel hurtowy napojami alkoholowymi\n")
        f.write(f"Korelacja Pearsona między liczbą firm a liczbą pożarów: {corr3:.3f}\n")
        f.write(f"Hipoteza 4: Powierzchnia jest pozytywnie skorelowana z liczbą mieszkańców\n")
        f.write(f"Korelacja Pearsona między powierzchnią a liczbą mieszkańców: {corr4:.3f}\n")






