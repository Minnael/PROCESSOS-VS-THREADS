import os
import time
import subprocess

start_time = time.time()

#DEFININDO ARQUIVO
arquivo = 'Game.of.Thrones.S06E07.1080p.HBO.WEB-DL.DD2.0.H.264-PiA'
nome_arquivo_completo = f'{arquivo}.srt'

#DEFININDO LINHAS DA LEGENDA E PARTICIONANDO INTERVALOS
with open(f'{arquivo}.srt', 'r', encoding='utf-8') as file:
   legenda = file.readlines()

#FUNÇÕES BASE PARA DIVIDIR E MONTAR
def dividir_arquivo_srt(caminho_arquivo, num_partes=12):
   with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
      linhas = arquivo.readlines()
        
   tamanho = len(linhas)
   partes = [linhas[i*tamanho // num_partes : (i+1)*tamanho // num_partes] for i in range(num_partes)]
    
   for i, parte in enumerate(partes):
      with open(f"{caminho_arquivo.rsplit('.', 1)[0]}_parte{i+1}.srt", 'w', encoding='utf-8') as arquivo_parte:
         arquivo_parte.writelines(parte)

def remontar_arquivos_srt(arquivos_partes, arquivo_saida):
   with open(arquivo_saida, 'w', encoding='utf-8') as saida:
      for arquivo_parte in arquivos_partes:
         with open(arquivo_parte, 'r', encoding='utf-8') as parte:
            saida.writelines(parte.readlines())


#DIVIDINDO ARQUIVO DE LEGENDA E EM SEGUIDA APAGANDO O ARQUIVO DE LEGENDA
dividir_arquivo_srt(nome_arquivo_completo)

#CÓDIGO DOS PROGRAMAS QUE SERÃO GERADOS:
codigo_gerado = """import os
import re
import sys
from deep_translator import GoogleTranslator

tradutor = GoogleTranslator(source="en", target="pt")

#DEFININDO NOSSA LEGENDA
arquivo = 'Game.of.Thrones.S06E07.1080p.HBO.WEB-DL.DD2.0.H.264-PiA' + sys.argv[1]
with open(arquivo, 'r+', encoding='utf-8') as file:
   legenda = file.readlines()

   for i in range(len(legenda)):
      palavra = legenda[i] 
      tem_numeros = bool(re.search(r'\d', palavra))
      if not tem_numeros and palavra.strip() != "":
         traducao = tradutor.translate(palavra)
         legenda[i] = traducao + '\\n'
         print(f"TRADUZINDO... LINHA {i}/{len(legenda)}")

   file.seek(0)
   file.writelines(legenda)  
   file.truncate()      

#REMOVENDO PROCESSO...
processo = sys.argv[0]
print(f'{processo} ENCERRADO!')
os.remove(processo)
"""

#NOME DOS ARQUIVOS QUE SERÃO GERADO:
processos = ["processo1.py", "processo2.py", "processo3.py", "processo4.py", "processo5.py", "processo6.py", "processo7.py", "processo8.py", "processo9.py", "processo10.py", "processo11.py", "processo12.py"]
parametros = [["_parte1.srt"], ["_parte2.srt"], ["_parte3.srt"], ["_parte4.srt"], ["_parte5.srt"], ["_parte6.srt"], ["_parte7.srt"], ["_parte8.srt"], ["_parte9.srt"], ["_parte10.srt"], ["_parte11.srt"], ["_parte12.srt"]]
particoes = [f'{arquivo}_parte1.srt', f'{arquivo}_parte2.srt', f'{arquivo}_parte3.srt', f'{arquivo}_parte4.srt', f'{arquivo}_parte5.srt', f'{arquivo}_parte6.srt', f'{arquivo}_parte7.srt', f'{arquivo}_parte8.srt', f'{arquivo}_parte9.srt', f'{arquivo}_parte10.srt', f'{arquivo}_parte11.srt', f'{arquivo}_parte12.srt'] 

#CRIANDO ARQUIVOS E ESCREVENDO CÓDIGO NELES:
for processo in processos:
   with open(processo, "w") as arquivo:
      arquivo.write(codigo_gerado)

processos_filhos = []

#PASSANDO OS PARAMETROS E ABRINDO OS ARQUIVOS:
for indice, processo in enumerate(processos):
   processo_filho = subprocess.Popen(["python", processo] + [str(param) for param in parametros[indice]])
   processos_filhos.append(processo_filho)

#MONITORANDO PROCESSOS ATIVOS 
for processo_filho in processos_filhos:
   processo_filho.wait()  
   print(f"Processo {processo_filho.pid} foi encerrado.")

os.remove(nome_arquivo_completo)

#REMONTANDO LEGENDA...
arquivo_traduzido = nome_arquivo_completo
remontar_arquivos_srt(particoes, arquivo_traduzido)

#APAGANDO PARTIÇÕES
for particao in particoes:
   os.remove(particao)

end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time} segundos")