import click
import subprocess
import threading
import time
from queue import Queue
from colorama import Fore, Style, init

init(autoreset=True)

# biblioteka click odpowiada za obsluzenie argumentow wejsciowych podanych przez uzytkownika
@click.command()
@click.option('--threads', type=int, required=True, help='Liczba wątków do użycia.')
@click.option('--url', type=str, required=True, help='URL, który będzie enumerowany.')
@click.option('--wordlist', type=click.Path(exists=True), required=True, help='Ścieżka do pliku zawierającego słowa do enumeracji.')
@click.option('--verbose', is_flag=True, help='Wyświetlaj informacje o błędach, jeśli ustawione.')
@click.option('--clock', is_flag=True, help='Mierz i wyświetl czas wykonania aplikacji.')
def run_enum(threads, url, wordlist, verbose, clock):

    if clock:
        start_time = time.time()

    # wczytanie danych z pliku
    with open(wordlist, 'r') as f:
        words = [line.strip() for line in f.readlines()]

    # kolejka przechowująca słowa do enumeracji, dostepna dla wszystkich wątków
    queue = Queue()
    for word in words:
        queue.put(word)

    # funkcja wątkowa, która pobiera słowo z kolejki i wywoluje funkcje run_rust_enum
    def worker():
        while not queue.empty():
            word = queue.get()
            run_rust_enum(url, word, verbose)
            queue.task_done()

    # stworzenie listy wątków i uruchomienie ich
    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.start()
        threads_list.append(t)

    # oczekiwanie na zakończenie pracy przez kazdy z watkow
    for t in threads_list:
        t.join()

    # jesli uzytkownik wybral opcje --clock, wyswietlony zostanie czas w ktrym skrypt zostal wykonany
    if clock:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(Fore.CYAN + f"Total time taken: {elapsed_time:.2f} seconds")


def run_rust_enum(url, word, verbose):
    # w subprocessie uruchimiony zostaje program Rust z odpowiednimi argumentami
    result = subprocess.run(
        ['cargo', 'run', '--release', '--', url, word, '--verbose' if verbose else '--no-verbose'],
        cwd='./content_enum',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # przetworzenie danych zwroconych na standardowe wyjscie przez program Rust
    # output jest kolorowany aby polepszyc czytelnosc
    for line in result.stdout.splitlines():
        if line.startswith("[+]"):
            print(Fore.GREEN + line)
        elif verbose:
            print(Fore.RED + line)

if __name__ == '__main__':
    run_enum()
