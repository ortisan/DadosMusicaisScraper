//mongodump --collection musicas --db scrapy --out /Users/marcelo/Documents/Ambiente/backups/mongodb
//mongorestore /Users/marcelo/Documents/Ambiente/backups/mongodb -d test -c musics
// mongorestore --host localhost --db test --collection musics /Users/marcelo/Documents/Ambiente/backups/mongodb/20150221


//EXPORTAMOS, TRADUZIMOS E REIMPORTAMOS OS DADOS DA SUBSTITUICAO DOS ACORDES

//mongoexport -d scrapy -c substituicao_acordes --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/traducao.json
//mongoimport -d scrapy -c substituicao_acordes /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/traducao.json

// EXPORTAMOS E IMPORTAMOS A COLECAO DE MUSICAS
//mongoexport -d scrapy -c musicas --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas.json
//mongoimport -d scrapy -c musicas /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas.json

//EXPORTAMOS E IMPORTAMOS A COLECAO DE MUSICAS COM ERRO

//mongoexport -d scrapy -c musicas_erro_acordes --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas_erro_acordes.json
//mongoimport -d scrapy -c musicas_erro_acordes2 /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas_erro_acordes.json


//mongoimport -d scrapy -c musicas2 /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas.json

//mongoexport -d scrapy -c acordes_estilos --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/acordes_estilos.json
//mongoimport -d scrapy -c acordes_estilos2 /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/acordes_estilos.json


db.musicas.update({}, {
    $rename: {
        "estilo": "estilo_cifraclub",
        "tom": "tom_cifraclub",
        "seq_acordes": "seq_acordes_cifraclub",
        "acordes": "acordes_cifraclub",
        "tonicas": "tonicas_cifraclub",
        "modos": "modos_cifraclub",
        "inversoes": "inversoes_cifraclub",
        "possui_tabs": "possui_tabs_cifraclub",
        "capo:cifraclub": "capo_cifraclub"
    }
}, {multi: true})

db.musicas.update({}, {$unset: {"qtd_exibicoes_cifraclub": ""}}, {multi: true})

db.musicas.find({qtd_acordes_cifraclub: {$exists: 0}}).count()

//Busca as musicas que tem mais de 3 acordes e tem duracao na lastfm e possui mais de uma visualizacao no youtube
db.musicas.find({qtd_acordes_cifraclub: {$gt: 3}, duracao_lastfm: {$gt: 0}, qtd_exibicoes_youtube: {$gt: 0}}).count()
db.musicas.find({duracao_lastfm: {$exists: 0}}).count()

db.musicas.find({seq_acordes_cifraclub: {$in: [')']}})


db.musicas.aggregate(unwind);
db.musicas.aggregate(project);

var unwind = {"$unwind": "$seq_acordes_cifraclub"};

var project = {
    "$project": {
        "seq_acordes_cifraclub": 1, "estilo_cifraclub": 1
    }
};


var group = {"$group": {"_id": "$estilo", "acordes": {"$push": "$seq_acordes_cifraclub"}}};

var project = {
    "$project": {
        "seq_acordes_cifraclub": 1, "estilo_cifraclub": 1
    }
};

var unwind = {"$unwind": "$seq_acordes_cifraclub"};

var skip = {$skip: 0}
var limit = {$limit: 30000};

var group = {"$group": {"_id": "$estilo", "acordes": {"$push": "$seq_acordes_cifraclub"}}};

db.musicas.aggregate(skip, limit, project, unwind).forEach(function (doc) {
    db.acordes_estilos.insert({_id: doc.seq_acordes_cifraclub});
});

db.musicas.aggregate(skip, limit, project, unwind, group).forEach(function (doc) {
    db.acordes_estilos.insert(doc);
});


db.musicas.aggregate(project)


var group1 = {
    "$group": {
        "_id": "$estilo_cifraclub",
        "acordes": {$addToSet: "$seq_acordes_cifraclub"}
    }
};

db.musicas.aggregate(unwind).forEach(function (doc) {
    db.acordes_estilos.insert(doc);
});


db.acordes_estilos.aggregate(
    [

        {$unwind: "$acordes"},
    ]
)


var group1 = {
    "$group": {
        "_id": "$_id",
        "acordes": {"$push": "$acordes"}
    }
};


db.acordes_estilos.find()

x = ["\nAnd I'm just trying to make you see\n**********************************************************\n\n("]

db.musicas.find({seq_acordes_cifraclub: {$in: x}})


var project1 = {"$project": {"_id": "$foi_sucesso", acorde: "$_id"}};
var group1 = {"$group": {"_id": "$_id", acordes: {$push: "$acorde"}}};
db.acordes_estilos.aggregate(project1, group1).forEach(function (doc) {
    db.acordes_sucesso_erro.insert(doc);
});

erros = db.acordes_sucesso_erro.findOne({_id: false}).acordes;
db.musicas.find({seq_acordes_cifraclub: {$in: erros}})

db.musicas.find({seq_acordes_cifraclub: {$in: erros}}, {qtd_exibicoes_youtube: 1}).sort({qtd_exibicoes_youtube: -1})


// GRAVA OS ACORDES COM AS RESPECTIVAS NOTAS E DESENHOS.
var project = {
    "$project": {
        "seq_acordes_cifraclub": 1, "estilo_cifraclub": 1
    }
};

var unwind = {"$unwind": "$seq_acordes_cifraclub"};

var skip = {$skip: 0};
var limit = {$limit: 35000};

var group = {"$group": {"_id": "$estilo", "acordes": {"$push": "$seq_acordes_cifraclub"}}};

db.musicas.aggregate(skip, limit, project, unwind).forEach(function (doc) {
    db.acordes_estilos.insert({_id: doc.seq_acordes_cifraclub});
});

var skip = {$skip: 35000};

db.musicas.aggregate(skip, limit, project, unwind).forEach(function (doc) {
    db.acordes_estilos.insert({_id: doc.seq_acordes_cifraclub});
});


// ACORDES NAO ENCONTRADOS POR MUSICA
var erros = db.acordes_sucesso_erro.findOne({_id: false}).acordes;
db.musicas.find({seq_acordes_cifraclub: {$in: erros}}, {
    seq_acordes_cifraclub: 1,
    qtd_exibicoes_youtube: 1
}).sort({qtd_exibicoes_youtube: -1}).forEach(
    function (doc) {
        var seq_acordes = doc.seq_acordes_cifraclub;
        var acordes_com_erros = [];
        seq_acordes.forEach(function (acorde) {
            if (erros.indexOf(acorde) > 0) {
                acordes_com_erros.push(acorde);
            }
        });

        db.musicas_erro_acordes.insert({
            _id: doc._id,
            acordes_com_erros: acordes_com_erros,
            qtd_exibicoes_youtube: doc.qtd_exibicoes_youtube
        });
    });

db.musicas_erro_acordes.find().sort({qtd_exibicoes_youtube: -1}).pretty()


// SUBSTITUICAO DOS ACORDES
// PREPARAMOS A COLECAO PARA FAZER O DE -> PARA
db.musicas_erro_acordes.find().forEach(function (doc) {
    acordes_com_erros = doc.acordes_com_erros;
    acordes_com_erros.forEach(function (acorde) {
        db.substituicao_acordes.insert({_id: acorde, de: acorde, para: ''});
    });
});


// GRAVO OS ACORDES "PARA:" PARA OBTERMOS OS DESENHOS
db.substituicao_acordes.find({$where: "this.para.length > 0"}).forEach(function (doc) {
    db.acordes_estilos.insert({_id: doc.para})
});
db.acordes_estilos.find({"foi_sucesso": {$exists: 0}});
db.acordes_estilos.find({$or: [{"foi_sucesso": {$exists: 0}}, {"foi_sucesso": false}]});

db.acordes_estilos.find({_id: "F7M(9)/C"});


var depara = {};

db.substituicao_acordes.find({para: {$exists: 1}}).forEach(function (doc) {
    depara[doc._id] = doc.para;
});

db.musicas_erro_acordes.find().forEach(function (doc) {
    // SEMPRE USAMOS A COLECAO ORIGINAL PARA NAO POLUIR OS DADOS
    var doc_musica = db.musicas.findOne({_id: doc._id});
    var seq_acordes = doc_musica.seq_acordes_cifraclub;
    var novo_seq_acordes = [];
    seq_acordes.forEach(function (acorde) {
        print(acorde);
        // SE ACORDE FAZ PARTE DOS ERROS,
        if (doc.acordes_com_erros.indexOf(acorde) >= 0) {
            var acorde_para = depara[acorde];
            print("acorde_para:" + acorde_para);
            if (acorde_para.length > 0) {
                acorde = acorde_para;
            }
        }
        novo_seq_acordes.push(acorde);
    });
    db.musicas2.update({_id: doc._id}, {$set: {seq_acordes_cifraclub: novo_seq_acordes}});
});

//Quero saber quantas musicas existem com dados ok e dados nao ok
db.musicas2.find({foi_sucesso_music21: true})


// Quero saber as notas com mais ocorrencia por tonicas
db.musicas2.find({foi_sucesso_music21: true})
var unwind = {"$unwind": "$tonicas_music21"};

var skip = {$skip: 0};
var limit = {$limit: 35000};

var group = {"$group": {"_id": "$estilo", "acordes": {"$push": "$seq_acordes_cifraclub"}}};

db.musicas.aggregate(skip, limit, project, unwind).forEach(function (doc) {
    db.acordes_estilos.insert({_id: doc.seq_acordes_cifraclub});
});

var skip = {$skip: 35000};

db.musicas.aggregate(skip, limit, project, unwind).forEach(function (doc) {
    db.acordes_estilos.insert({_id: doc.seq_acordes_cifraclub});
});

var map_contadores = function () {

    var map_tonicas = {
        "A": 0,
        "A#": 0,
        "B": 0,
        "C": 0,
        "C#": 0,
        "D": 0,
        "D#": 0,
        "E": 0,
        "F": 0,
        "F#": 0,
        "G": 0,
        "G#": 0,
        "A": 0,
        "B-": 0,
        "B": 0,
        "C": 0,
        "D-": 0,
        "D": 0,
        "E-": 0,
        "E": 0,
        "F": 0,
        "G-": 0,
        "G": 0,
        "A-": 0
    };
    var map_baixos = {
        "A": 0,
        "A#": 0,
        "B": 0,
        "C": 0,
        "C#": 0,
        "D": 0,
        "D#": 0,
        "E": 0,
        "F": 0,
        "F#": 0,
        "G": 0,
        "G#": 0,
        "A": 0,
        "B-": 0,
        "B": 0,
        "C": 0,
        "D-": 0,
        "D": 0,
        "E-": 0,
        "E": 0,
        "F": 0,
        "G-": 0,
        "G": 0,
        "A-": 0
    };

    var map_modos = { "Balinese Pelog pentatonic": 0, "C all combinatorial (P6, I3, RI9)": 0, "Hirajoshi pentatonic": 0, "Javanese pentatonic": 0, "Kumoi pentachord": 0, "Messiaen's truncated mode 6": 0, "Neapolitan pentachord": 0, "all-interval tetrachord": 0, "alternating tetramirror": 0, "augmented major tetrachord": 0, "augmented seventh chord": 0, "augmented triad": 0, "augmented-diminished ninth chord": 0, "augmented-eleventh": 0, "augmented-sixth pentachord": 0, "center-cluster pentamirror": 0, "combinatorial RI (RI1)": 0, "combinatorial RI (RI9)": 0, "diminished minor-ninth chord": 0, "diminished pentacluster": 0, "diminished seventh chord": 0, "diminished triad": 0, "diminished-augmented ninth chord": 0, "diminished-major ninth chord": 0, "dominant seventh chord": 0, "dominant-eleventh": 0, "dominant-ninth": 0, "dorian hexachord": 0, "dorian pentachord": 0, "double-fourth tetramirror": 0, "enigmatic pentachord": 0, "flat-ninth pentachord": 0, "half-diminished seventh chord": 0, "harmonic minor tetrachord": 0, "incomplete dominant-seventh chord": 0, "incomplete half-diminished seventh chord": 0, "incomplete major-seventh chord": 0, "incomplete minor-seventh chord": 0, "interval class 5": 0, "locrian hexachord": 0, "lydian pentachord": 0, "lydian tetrachord": 0, "major pentachord": 0, "major pentatonic": 0, "major seventh chord": 0, "major triad": 0, "major-augmented ninth chord": 0, "major-diminished tetrachord": 0, "major-minor tetramirror": 0, "major-ninth chord": 0, "major-second major tetrachord": 0, "major-second minor tetrachord": 0, "minor hexachord": 0, "minor seventh chord": 0, "minor triad": 0, "minor-augmented tetrachord": 0, "minor-diminished ninth chord": 0, "minor-diminished tetrachord": 0, "minor-major ninth chord": 0, "minor-ninth chord": 0, "minor-second diminished tetrachord": 0, "minor-second quartal tetrachord": 0, "perfect-fourth diminished tetrachord": 0, "perfect-fourth major tetrachord": 0, "perfect-fourth minor tetrachord": 0, "phrygian hexamirror": 0, "phrygian pentachord": 0, "phrygian tetrachord": 0, "quartal tetramirror": 0, "quartal trichord": 0, "tritone quartal tetrachord": 0, "tritone-fourth": 0, "whole-tone pentachord": 0, "whole-tone tetramirror": 0, "whole-tone trichord": 0};

    var tonicas = this.tonicas_music21;
    var baixos = this.baixos_music21;
    var modos = this.modos_music21;

    if (tonicas) {
        for (i = 0; i < tonicas.length; i++) {
            var tonica = tonicas[i];
            var baixo = baixos[i];
            var modo = modos[i];

            var count_t = 1;
            var count_tonica = map_tonicas[tonica];
            if (count_tonica) {
                count_t = count_tonica + 1;
            }
            map_tonicas[tonica] = count_t;

            var count_b = 1;
            var count_baixo = map_baixos[baixo];
            if (count_baixo) {
                count_b = count_baixo + 1;
            }
            map_baixos[baixo] = count_b;

            var count_m = 1;
            var count_modos = map_modos[modo];
            if (count_modos) {
                count_m = count_modos + 1;
            }
            map_modos[modo] = count_m;
        }
    }
    emit(this._id, {cont_tonicas: map_tonicas, cont_baixos: map_baixos, cont_modos: map_modos});
};

var reduce = function (key, values) {

    return values.length;

};

var map_modos = function () {
    var modos = this.modos_music21;

    if (modos) {
        for (i = 0; i < modos.length; i++) {
            emit(modos[i], 1);
        }
    }
};

db.count_modos.find()

db.musicas2.mapReduce(map_contadores, reduce, {query: {foi_sucesso_music21:true}, out: "cont"});
db.musicas2.mapReduce(map_modos, reduce, {query: {foi_sucesso_music21: true}, out: "cont_modos"});

//mongoexport -d scrapy -c musicas2 --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas2.json


//mongoexport -d scrapy -c musicas3 -q "{foi_sucesso_music21: true}" --csv --fieldFile ./fields.txt --out ./musicas3.csv

//mongoexport -d scrapy -c cont_modos --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/modos.json
//mongoimport -d scrapy -c musicas3 /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas2.json


db.cont.find().forEach(function(doc){
   db.musicas3.update({_id: doc._id}, {$set: {cont_tonicas: doc.value.cont_tonicas, cont_baixos: doc.value.cont_baixos, cont_modos: doc.value.cont_modos}});
});

db.musicas3.find({"_id": "007 - Another Way To Die"});