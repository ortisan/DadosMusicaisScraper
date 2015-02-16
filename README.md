DadosMusicaisScraper
================

Obtém os dados musicais através do Cifraclub (acordes, tom, etc) e Youtube (Ratings) e exporta para csv.

Pré-requisitos
--------------
1. Ter o python 2.7 e o pip instalados. Teste com os comandos ```python -V``` e ```pip -V```.
2. Ter o mongodb instalado. Teste com o comando ```mongo -version```.

Instalação dos pacotes python
-----------------------------
1. No diretório do projeto executar: ```pip install -r requirements.txt```

Criação da base no MongoDB
-------------------------

1. Inicializar o serviço ```mongod```.
2. Executar o comando Mongo ```mongo```.
3. Criar a base de dados ```use scrapy```.
4. Sair ``` quit() ```.

Scrape dos dados
----------------

1. No diretório do projeto executar: ```python main.py -s MusicasPorEstiloCifraClubSpider```. Esse Spider, obtém as músicas de acordo com os estilos da url [http://www.cifraclub.com.br/estilos/](http://www.cifraclub.com.br/estilos/)
2. No diretório do projeto executar: ```python main.py -s MusicasPorArtistaCifraClubSpider```. Obtém todas as músicas dos artistas já separados por estilo (passo 1).
3. No diretório do projeto executar: ```python main.py -s RatingsYoutubeSpider```. Obtém os ratings das músicas obtidas no passo 1 e 2.

Exportação dos dados
--------------------

1. ```mongoexport --db scrapy --collection musicas --csv --fieldFile ./fields.txt --out ./musicas.csv```

OBSERVAÇÕES
-----------

* Na bilioteca music21, os bemois ("b"), são traduzidos para "-" ex: Bb == B-.
* Tudo entre parêntesis, são notas acrescentadas, ex: Am(7M) == Am com 7 maior.

