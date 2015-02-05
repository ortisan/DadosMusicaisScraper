DadosMusicaisScraper
================

Obtém os dados musicais através do Cifraclub(acordes, tom, etc) e Youtube (Rating) e exporta para csv.

Pré-requisitos
--------------
1. Ter o python 2.7 e o pip instalados. Teste com os comandos ```python -V``` e ```pip -V```.
2. Ter o mongodb instalado. Teste com o comando ```mongo -version```.

Instalação dos pacotes python
-----------------------------
1. No diretório do projeto executar: ```pip install -r requirements.py```

Criação da base no mongod
-------------------------

1. Inicializar o serviço ```mongod```.
2. Executar o comando mongo ```mongo```.
3. Criar a base de dados ```use scrapy```.
4. Sair ``` quit() ```.

Scrape dos dados
----------------

1. No diretório do projeto executar: ```python main.py```
2. No diretório do projeto executar: ```python RatingsYoutube.py``` (APÓS O PASSO 1 TERMINAR)

Exportação dos dados
--------------------

1. ```mongoexport --db scrapy --collection musicas --csv --fieldFile ./fields.txt --out ./musicas.csv```
