//BACKUP DA BASE
//mongodump -d scrapy_tcc --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/backup_bases/base_scrapy
//mongorestore --db scrapy_tcc_restore /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/backup_bases/base_scrapy_0607

// Musicas que nao possuem acordes cifraclub
db.musicas.find({$where: "this.seq_acordes_cifraclub.length > 0"});
// Musicas que nao possuem dados youtube
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
}).forEach(function (doc) {
    db.musicas.update({_id: doc._id}, {
        url_busca_youtube: doc.url_busca_youtube,
        url_video_youtube: doc.url_video_youtube,
        qtd_exibicoes_youtube: doc.qtd_exibicoes_youtube,
        qtd_gostei_youtube: doc.qtd_gostei_youtube,
        qtd_nao_gostei_youtube: doc.qtd_nao_gostei_youtube,
        dt_publicacao_youtube: doc.dt_publicacao_youtube,
        dias_desde_publicacao_youtube: doc.dias_desde_publicacao_youtube
    })
})

db.musicas.find({"$or": [{"duracao_lastfm": {'$exists': 0}}, {"duracao_lastfm": -1}]}, {
    '_id': true,
    "artista": true,
    "nome": true
})

db.musicas.find({"$or": [{"duracao_spotify": {"$exists": 0}}, {"duracao_spotify": -1}]}, {
    '_id': true,
    "artista": true,
    "nome": true
})

db.dicionario_acordes.find({"$or": [{"foi_sucesso": {"$exists": 0}}, {"foi_sucesso": false}]})

// Verificamos se a base possui dados do lastfm
qtd_registros = db.musicas.find({"duracao_lastfm": {"$exists": 0}}, {
    '_id': true,
    "artista": true,
    "nome": true
}).count()


db.dicionario_acordes.update(
    {_id:{$exists: 1}},
    {$set:{lista_notas: []}},
    {multi:true}
)

db.musicas.update(
    {_id:{$exists: 1}},
    {$set:{tonicas_cifraclub: [], acordes_unicos_cifraclub: [], baixos_cifraclub: [], modos_cifraclub: []}},
    {multi:true}
)

/* ### Preparacao do dicionario de acordes ### */

// PROJECT Retorna somente as colunas que eu quero ou cria novas,
// UNWIND Desagrega o array com x elementos em x registros

var bulk = db.dicionario_acordes.initializeUnorderedBulkOp();

var max_elements_bulk = 100;
var i = 0;

var project = {"$project": {"seq_acordes_cifraclub": "$seq_acordes_cifraclub"}};
var unwind = {$unwind: "$seq_acordes_cifraclub"};

db.musicas.aggregate(project, unwind).forEach(function (doc) {
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

/* ### FIM - Preparacao do dicionario de acordes ### */


/* ### Preparacao da base ### */

// Saber os modos
var bulk = db.modos_acordes.initializeUnorderedBulkOp();

var max_elements_bulk = 100;

var i = 0;

var project = {"$project": {"modos_cifraclub": "$modos_cifraclub"}};

var unwind = {"$unwind": "$modos_cifraclub"};

db.musicas.aggregate(project, unwind).forEach(function (doc) {
    var modo_cifraclub = doc.modos_cifraclub;
    if (i < max_elements_bulk) {
        bulk.find({_id: modo_cifraclub}).upsert().replaceOne({_id: modo_cifraclub});
    } else {
        bulk.execute();
        i = 0;
        bulk = db.modos_acordes.initializeUnorderedBulkOp();
    }
    i++;
});

// Criacao da base ADB
db.musicas_pre_adb.remove({});
// Backup dos registros
db.musicas.find({}).forEach(function(doc){
   db.musicas_pre_adb.insert(doc);
});

db.musicas_pre_adb.count()

var map_contadores = function () {

    var map_tonicas = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
        "F": 0,
        "G": 0,
        "A#": 0,
        "C#": 0,
        "D#": 0,
        "F#": 0,
        "G#": 0,
        "B-": 0,
        "D-": 0,
        "E-": 0,
        "G-": 0,
        "A-": 0
    };
    var map_baixos = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
        "F": 0,
        "G": 0,
        "A#": 0,
        "C#": 0,
        "D#": 0,
        "F#": 0,
        "G#": 0,
        "B-": 0,
        "D-": 0,
        "E-": 0,
        "G-": 0,
        "A-": 0
    };

    // TODO Fazer os modos
    var map_modos = { "Balinese Pelog pentatonic": 0, "C all combinatorial (P6, I3, RI9)": 0, "Hirajoshi pentatonic": 0, "Javanese pentatonic": 0, "Kumoi pentachord": 0, "Messiaen's truncated mode 6": 0, "Neapolitan pentachord": 0, "all-interval tetrachord": 0, "alternating tetramirror": 0, "augmented major tetrachord": 0, "augmented seventh chord": 0, "augmented triad": 0, "augmented-diminished ninth chord": 0, "augmented-eleventh": 0, "augmented-sixth pentachord": 0, "center-cluster pentamirror": 0, "combinatorial RI (RI1)": 0, "combinatorial RI (RI9)": 0, "diminished minor-ninth chord": 0, "diminished pentacluster": 0, "diminished seventh chord": 0, "diminished triad": 0, "diminished-augmented ninth chord": 0, "diminished-major ninth chord": 0, "dominant seventh chord": 0, "dominant-eleventh": 0, "dominant-ninth": 0, "dorian hexachord": 0, "dorian pentachord": 0, "double-fourth tetramirror": 0, "enigmatic pentachord": 0, "flat-ninth pentachord": 0, "half-diminished seventh chord": 0, "harmonic minor tetrachord": 0, "incomplete dominant-seventh chord": 0, "incomplete half-diminished seventh chord": 0, "incomplete major-seventh chord": 0, "incomplete minor-seventh chord": 0, "interval class 5": 0, "locrian hexachord": 0, "lydian pentachord": 0, "lydian tetrachord": 0, "major pentachord": 0, "major pentatonic": 0, "major seventh chord": 0, "major triad": 0, "major-augmented ninth chord": 0, "major-diminished tetrachord": 0, "major-minor tetramirror": 0, "major-ninth chord": 0, "major-second major tetrachord": 0, "major-second minor tetrachord": 0, "minor hexachord": 0, "minor seventh chord": 0, "minor triad": 0, "minor-augmented tetrachord": 0, "minor-diminished ninth chord": 0, "minor-diminished tetrachord": 0, "minor-major ninth chord": 0, "minor-ninth chord": 0, "minor-second diminished tetrachord": 0, "minor-second quartal tetrachord": 0, "perfect-fourth diminished tetrachord": 0, "perfect-fourth major tetrachord": 0, "perfect-fourth minor tetrachord": 0, "phrygian hexamirror": 0, "phrygian pentachord": 0, "phrygian tetrachord": 0, "quartal tetramirror": 0, "quartal trichord": 0, "tritone quartal tetrachord": 0, "tritone-fourth": 0, "whole-tone pentachord": 0, "whole-tone tetramirror": 0, "whole-tone trichord": 0};

    var tonicas = this.tonicas_cifraclub;
    var baixos = this.baixos_cifraclub;
    var modos = this.modos_cifraclub;

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
db.musicas_pre_adb.mapReduce(map_contadores, reduce, {query: {"acordes_unicos_cifraclub": {"$exists": 1}}, out: "cont"});

var map_modos = function () {

    var modos = this.modos_music21;
    if (modos) {
        for (i = 0; i < modos.length; i++) {
            emit(modos[i], 1);
        }
    }
};


db.count_modos.find()
db.musicas_adb.mapReduce(map_modos, reduce, {query: {foi_sucesso_music21: true}, out: "cont_modos"});



/* ### FIM - Preparacao da base ### */
