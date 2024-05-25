import click
import subprocess
import os
import threading
from queue import Queue
from colorama import Fore, Style, init

init(autoreset=True)

@click.command()
@click.option('--threads', type=int, required=True, help='Number of threads to be used.')
@click.option('--url', type=str, required=True, help='The URL that will be enumerated.')
@click.option('--wordlist', type=click.Path(exists=True), required=True, help='Path to the file that contains words which will be used for enumeration.')
@click.option('--verbose', is_flag=True, help='Print information about errors if set.')
def run_enum(threads, url, wordlist, verbose):
    with open(wordlist, 'r') as f:
        words = [line.strip() for line in f.readlines()]

    queue = Queue()
    for word in words:
        queue.put(word)

    def worker():
        while not queue.empty():
            word = queue.get()
            run_rust_enum(url, word, verbose)
            queue.task_done()

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.start()
        threads_list.append(t)

    for t in threads_list:
        t.join()

def run_rust_enum(url, word, verbose):
    result = subprocess.run(
        ['cargo', 'run', '--release', '--', url, word, '--verbose' if verbose else '--no-verbose'],
        cwd='./content_enum',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in result.stdout.splitlines():
        if line.startswith("[+]"):
            print(Fore.GREEN + line)
        elif verbose:
            print(Fore.RED + "[-] " + line)

if __name__ == '__main__':
    run_enum()
