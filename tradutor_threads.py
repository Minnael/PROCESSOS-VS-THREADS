import re
import threading
import time
from colorama import init, Fore, Back
from deep_translator import GoogleTranslator

start_time = time.time()

init(autoreset=True)
tradutor = GoogleTranslator(source="en", target="pt")

def traduzir_legenda(inicio, fim, linhas, resultados, thread_index):
    for i in range(inicio, fim):
        palavra = linhas[i]
        tem_numeros = bool(re.search(r'\d', palavra))
        if not tem_numeros and palavra.strip() != "":
            traducao = tradutor.translate(palavra)
            resultados[i] = traducao + '\n'
            print(f"TRADUZINDO... LINHA {i}/{len(linhas)}")

def main():
    with open('Game.of.Thrones.S06E07.1080p.HBO.WEB-DL.DD2.0.H.264-PiA.srt', 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    num_threads = 12
    linhas_por_thread = len(linhas) // num_threads
    threads = []
    resultados = linhas.copy()

    for i in range(num_threads):
        inicio = i * linhas_por_thread
        fim = (i + 1) * linhas_por_thread if i != num_threads - 1 else len(linhas)
        thread = threading.Thread(target=traduzir_legenda, args=(inicio, fim, linhas, resultados, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    with open('Game.of.Thrones.S06E07.1080p.HBO.WEB-DL.DD2.0.H.264-PiA.srt', 'w', encoding='utf-8') as file:
        file.writelines(resultados)


main()

end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")