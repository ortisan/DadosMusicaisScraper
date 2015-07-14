DadosMusicaisScraper
====================

O objetivo desse projeto é obter os dados musicais do Cifraclub, Youtube, Lastfm e Spotify. Tendo esses dados, o objetivo é analisá-los.


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
1. Executar o comando Mongo ```mongo```.
1. Criar a base de dados ```use scrapy```.
1. Sair ``` quit() ```.


Scrape dos dados
----------------
1. No diretório do projeto executar: ```python main.py -s MusicasEchordSpider```. Esse Spider, obtém as músicas de acordo com os estilos da url [http://www.cifraclub.com.br/estilos/](http://www.cifraclub.com.br/estilos/)
1. No diretório do projeto executar: ```python main.py -s MusicasPorEstiloCifraClubSpider```. Esse Spider, obtém as músicas de acordo com os estilos da url [http://www.cifraclub.com.br/estilos/](http://www.cifraclub.com.br/estilos/)
1. No diretório do projeto executar: ```python main.py -s MusicasPorArtistaCifraClubSpider```. Obtém todas as músicas dos artistas já separados por estilo (passo 1).
1. No diretório do projeto executar: ```python main.py -s RatingsYoutubeSpider```. Obtém os ratings das músicas obtidas no passo 1 e 2.
1. Caso queira os dados de duração e qtd de audições do Lastfm, configure no settings.py as variáveis: LASTFM_API_KEY, LASTFM_API_SECRET, LASTFM_USERNAME e LASTFM_PASSWORD. No diretório do projeto executar: ```python AtualizadorDadosLastFM.py```.
1. Caso queira os dados de duração e e popularidade do spotify, configure no settings.py as variáveis: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET. No diretório do projeto executar: ```python AtualizadorDadosSpotify.py```.


Preparação da base de dadoa para Analytical Base Table (ATB)
------------------------------------------------------------



Exportação dos dados
--------------------

1. ```mongoexport  -q '{ $query: {qtd_exibicoes_youtube: {$gt: 0}}}' -d scrapy -c musicas --csv --fieldFile ./fields.txt --out ./musicas.csv```


OBSERVAÇÕES
-----------

* Na bilioteca music21, os bemois ("b"), são traduzidos para "-" ex: Bb == B-.
* Tudo entre parêntesis, são notas acrescentadas, ex: Am(7M) == Am com 7 maior.


TODO:
====

Criar uma variável para quantidade de acordes.
Criar uma variavel para quantidade de acordes que nao pertencem ao tom.



