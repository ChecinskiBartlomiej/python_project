import unittest
import tempfile
import pandas as pd
from pathlib import Path
from analysis_pkg import analiza

class Testfunkcje(unittest.TestCase):

    def setUp(self):
        #Dane do testowania.
        self.df_area = pd.DataFrame({
            'Nazwa jednostki': ['WOJ. A', 'X', 'WOJ. B'],
            'Pow_ha': [10, 20, 30],
            'Pow_km2': [0.1, 0.2, 0.3]
        })
        self.df_fires = pd.DataFrame({
            'Województwo': ['A', 'A', 'B'],
            'RAZEM Pożar (P)': [1, 2, 3]
        })
        self.df_alcohol = pd.DataFrame({
            'Województwo': ['A', 'B', 'B', 'C']
        })
        self.df_population = pd.DataFrame({
            'Województwo': ['C', 'A', 'B'],
            'Populacja': [300, 100, 200]
        })
    
    def test_wczytaj_dane(self):
        pass
    def test_uporzadkuj_dane(self):

        df_area, _, _, df_population = analiza.uporzadkuj_dane(
            self.df_area.copy(),
            self.df_fires.copy(),
            self.df_alcohol.copy(),
            self.df_population.copy()
        )
        #Sprawdzamy czy Nazwa jednostki zaczyna się od "WOJ" w df_area.
        self.assertTrue(all(df_area['Nazwa jednostki'].str.upper().str.startswith('WOJ.')))
        #Sprawdzamy czy po usunieciu "WOJ" nazwy jednostki sa posortowane alfabetycznie w df_area.
        names = df_area['Nazwa jednostki'].str.replace(r'(?i)^WOJ\.\s*', '', regex=True).tolist()
        self.assertEqual(names, ['A', 'B'])
        #Sprawdzamy czy wojewodztwa sa posortowane alfabetycznie w df_population.
        sorted_pop = sorted(self.df_population['Województwo'].tolist())
        self.assertListEqual(df_population['Województwo'].tolist(), sorted_pop)
    def test_oblicz_statystyki(self):

        df_area = pd.DataFrame({
            'Pow_ha': [10, 20],
            'Pow_km2': [0.1, 0.2]
        })
        df_population = pd.DataFrame({
            'Województwo': ['X', 'Y'],
            'Populacja': [100, 200]
        })
        df_fires = pd.DataFrame({
            'Województwo': ['X', 'Y'],
            'Liczba_pozarow': [5, 10]
        })
        df_alcohol = pd.DataFrame({
            'Województwo': ['X', 'Y'],
            'Liczba_firm': [2, 3]
        })
        #Sprawdzamy czy wszystkie statystyki wystepuja.
        with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp:
            output = Path(tmp.name)
            analiza.oblicz_statystyki(df_area, df_fires, df_alcohol, df_population, output)
            tmp.seek(0) #wskaznik na poczatek pliku tekstowego
            content = tmp.read()
            self.assertIn('=== Powierzchnia województw ===', content)
            self.assertIn('=== Populacja ===', content)
            self.assertIn('=== Liczba pożarów ===', content)
            self.assertIn('=== Liczba firm ===', content)
            self.assertIn('count', content)
            self.assertIn('std', content)
            self.assertIn('min', content)
            self.assertIn('25%', content)
            self.assertIn('50%', content)
            self.assertIn('75%', content)
            self.assertIn('max', content)

    def test_hipotezy(self):

        df_area = pd.DataFrame({
            'Województwo': ['X', 'Y'],
            'Powierzchnia_km2': [0.1, 0.2]
        })
        df_fires = pd.DataFrame({
            'Województwo': ['X', 'Y'],
            'Liczba_pozarow': [5, 10]
        })
        df_alcohol = pd.DataFrame({
            'Województwo': ['X', 'Y'],
            'Liczba_firm': [2, 3]
        })
        df_population = pd.DataFrame({
            'Województwo': ['X', 'Y'],
            'Populacja': [100, 200]
        })
        #Sprawdzamy czy wystepuje konkretny napis ktory powinien wystapic.
        with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp:
            output = Path(tmp.name)
            analiza.hipotezy(
                df_area, df_fires, df_alcohol, df_population, output
            )
            tmp.seek(0) 
            content = tmp.read()
            self.assertIn('Korelacja Pearsona między liczbą mieszkańców a liczbą pożarów: 1.000', content)

#python3 -m unittest tests.py