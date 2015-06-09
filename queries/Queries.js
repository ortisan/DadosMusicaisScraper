//BACKUP DA BASE
//mongodump -d scrapy_tcc --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/backup_bases/base_scrapy
//mongorestore --db scrapy_tcc_restore /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/backup_bases/base_scrapy_0607

// MUSICAS QUE NAO POSSUEM ACORDES CIFRACLUB
db.musicas.find( { $where: "this.seq_acordes_cifraclub.length > 0" } );
// MUSICAS QUE NAO POSSUEM DADOS YOUTUBE
db.musicas.find({'qtd_exibicoes_youtube': {'$exists': 0}}, {"artista": 1, "nome": 1}).count()
// Merge da base antiga
db.musicas.find({'qtd_exibicoes_youtube': {'$exists': 1}}, {
    _id: 1,
    url_busca_youtube: 1,
    url_video_youtube: 1,
    qtd_exibicoes_youtube: 1,
    qtd_gostei_youtube: 1,
    qtd_nao_gostei_youtube: 1,
    dt_publicacao_youtube: 1,
    dias_desde_publicacao_youtube: 1
}).forEach(function(doc){
    db.musicas.update({_id: doc._id}, {
        url_busca_youtube: doc.url_busca_youtube,
        url_video_youtube: doc.url_video_youtube,
        qtd_exibicoes_youtube: doc.qtd_exibicoes_youtube,
        qtd_gostei_youtube: doc.qtd_gostei_youtube,
        qtd_nao_gostei_youtube: doc.qtd_nao_gostei_youtube,
        dt_publicacao_youtube: doc.dt_publicacao_youtube,
        dias_desde_publicacao_youtube: doc.dias_desde_publicacao_youtube})
})

db.musicas.find({"$or": [{"duracao_lastfm": {'$exists': 0}}, {"duracao_lastfm": -1}]}, {'_id': true, "artista": true, "nome": true})
db.musicas.find({"$or": [{"duracao_spotify": {"$exists": 0}}, {"duracao_spotify": -1}]}, {'_id': true, "artista": true, "nome": true})

db.dicionario_acordes.find({"$or": [{"foi_sucesso": {"$exists": 0}}, {"foi_sucesso": false}]})


// VERIFICAMOS SE A BASE POSSUI DADOS DO LASTFM
qtd_registros = db.musicas.find({"duracao_lastfm": {"$exists": 0}}, {'_id': true, "artista": true, "nome": true}).count()

/* ### PREPARACAO DO DICIONARIO DE ACORDES ### */

// PROJECT RETORNA SOMENTE AS COLUNAS QUE EU QUERO,
// UNWIND DESAGREGA O ARRAY COM X ELEMENTOS EM X REGISTROS

var bulk = db.dicionario_acordes.initializeUnorderedBulkOp();

var max_elements_bulk = 100;
var i = 0;

db.musicas.aggregate({"$project" : {"seq_acordes_cifraclub" : "$seq_acordes_cifraclub"}}, {$unwind: "$seq_acordes_cifraclub"}).forEach(function(doc){
    var acorde = doc.seq_acordes_cifraclub;
    if (i < max_elements_bulk) {
        bulk.find({_id: acorde}).upsert().replaceOne({_id: acorde});
    } else {
        bulk.execute();
        i = 0;
        bulk = db.dicionario_acordes.initializeUnorderedBulkOp();
    }

    i++;
});

/* ### FIM - PREPARACAO DO DICIONARIO DE ACORDES ### */

// ### INSERIMOS EM UMA COLECAO OS ACORDES COM SUCESSO E ERRO
var project = {"$project": {"_id": "$foi_sucesso", acorde: "$_id"}};
var group = {"$group": {"_id": "$_id", acordes: {$push: "$acorde"}}};

db.dicionario_acordes.aggregate(project, group).forEach(function (doc) {
    db.acordes_sucesso_erro.insert(doc);
});
// ### FIM - INSERIMOS EM UMA COLECAO OS ACORDES COM SUCESSO E ERRO


// EXPORTAMOS OS ACORDES COM ERRO
//mongoexport -d scrapy_tcc -c acordes_sucesso_erro -q {_id:false} --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/result_queries/acordes_erro.json

// ### PRECISO SABER QUANTAS MUSICAS ESTAO COM ACORDES INVALIDOS PARA VER SE VALE A PENA TRATAR OU NAO
// MUSICAS QUE NAO POSSUEM CIFRAS
db.musicas.find({seq_acordes_cifraclub: {$exists:0}})
acordes_erro = db.acordes_sucesso_erro.findOne({_id: false}).acordes;
db.musicas.find({$and: [{seq_acordes_cifraclub: {$exists:1}}, {$where : "this.seq_acordes_cifraclub.length > 0"}]}).forEach(function(doc) {
    for (i = 0; i < doc.seq_acordes_cifraclub.length; i++) {
        if (acordes_erro.indexOf(doc.seq_acordes_cifraclub[i]) > 0) {
            db.musicas_erro.insert({ _id: doc._id,  acorde_erro: doc.seq_acordes_cifraclub[i]});
            break;
        }
    }
});

