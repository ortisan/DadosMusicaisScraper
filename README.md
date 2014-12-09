CifraClubScraper
================

Obtém os dados das cifras do cifraclub e exporta para csv.

Criaçao da base no mongod
-------------------------

1. ``` mongod ```
2. ``` use scrapy ```
3. ``` quit() ```

Scrape dos dados
----------------

1. No diretório do projeto executar: ```python main.py```

Exportação dos dados
--------------------

1. ```mongoexport --db scrapy --collection musicas --csv --fieldFile ./fields.txt --out ./musicas.csv```
