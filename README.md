# Narzedzie do asynchronicznej enumeracji zawartosci serwisu webowego

## autor
Kacper Wielechowski

## Budowa srodowiska

### Linux

```bash
./build.sh
```

### Windows

```powershell
powershell.exe build.ps1
```


## przykladowe uzycie aplikacji
Aplikacja uzywa stringa 'ZPR' aby wskazac miejsce w URLu do ktorego przekazywane beda slowa ze slownika wskazanego przez uzytkownika

### enumeracja katalogow/plikow
```bash
python3 main.py --threads 8 --url https://{domena}/ZPR --wordlist wordlist.txt
```

### enumeracja subdomen
```bash
python3 main.py --threads 8 --url https://ZPR.{domena}/ --wordlist wordlist.txt
```


## sekcja help

Usage: main.py [OPTIONS]

```
Options:
  --threads INTEGER  Number of threads or subprocesses to be used.  [required]
  --url TEXT         The URL that will be enumerated.  [required]
  --wordlist PATH    Path to the file that contains words which will be used
                     for enumeration.  [required]
  --verbose          Print information about errors if set.
  --help             Show this message and exit.
```
## ciekawostki wydajnosciowe

### czas wykonania programu przy uzyciu tego samego slownika, ale roznej liczby watkow

### 1 watek -> 45 sekund
### 4 watki -> 14 sekund
### 8 watkow -> 9.5 sekundy