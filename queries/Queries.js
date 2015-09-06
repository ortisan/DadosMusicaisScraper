//BACKUP DA BASE
//mongodump -d scrapy_tcc --out /Users/marcelo/Documents/Ambiente/workspace-py/DadosMusicaisScraper/base_scrapy_antes_correcao_acordes_14_07
//mongorestore --db scrapy_tcc_restore /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/backup_bases/base_scrapy_0607
//mongodump -d scrapy_tcc --out /Users/marcelo/Documents/Ambiente/workspace-py/DadosMusicaisScraper/backup_bases/base_scrapy_estilos_tons_separados_30_08

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
    {_id: {$exists: 1}},
    {$set: {lista_notas: []}},
    {multi: true}
)

db.dicionario_acordes.find({$where: "this.lista_notas.length > 1"})

db.musicas.update(
    {_id: {$exists: 1}},
    {$set: {tonicas_cifraclub: [], acordes_unicos_cifraclub: [], baixos_cifraclub: [], modos_cifraclub: []}},
    {multi: true}
)

// Limpar os acordes dando um trim()
db.musicas.find({seq_acordes_cifraclub: {$exists: 1}}).forEach(function (document) {
    var acordes_trim = [];
    for (var i = 0; i < document.seq_acordes_cifraclub.length; i++) {
        acordes_trim[i] = document.seq_acordes_cifraclub[i].trim();
    }
    db.musicas.update({_id: document._id}, {$set: {seq_acordes_cifraclub: acordes_trim}});
});


db.musicas.find({$where: "this.tonicas_cifraclub.length > 1"})

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

//mongoexport - d scrapy_tcc - c dicionario_acordes --type=csv --fieldFile./fields_dicionario_acordes.txt --out ./dicionario_acordes.csv


/* ### FIM - Preparacao do dicionario de acordes ### */


/* ### Preparacao da base ADB ### */

// Criacao da base ADB
db.musicas_pre_adb.remove({});
// Backup dos registros
db.musicas.find({}).forEach(function (doc) {
    db.musicas_pre_adb.insert(doc);
});

db.musicas_pre_adb.count()

db.modos_acordes.remove({})

// Saber os modos
var bulk = db.modos_acordes.initializeUnorderedBulkOp();

var max_elements_bulk = 100;

var i = 0;

var project = {"$project": {"modos_cifraclub": "$modos_cifraclub"}};

var unwind = {"$unwind": "$modos_cifraclub"};

db.musicas_pre_adb.aggregate(project, unwind).forEach(function (doc) {
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


var map_modos = {};
db.modos_acordes.find().forEach(function (doc) {
    map_modos[doc._id] = 0;
});

// Pegar esses modos e incluir no map_modos abaixo
map_modos

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
    var map_modos = {
        "major triad": 0,
        "minor triad": 0,
        "dominant seventh chord": 0,
        "major seventh chord": 0,
        "minor seventh chord": 0,
        "interval class 5": 0,
        "incomplete minor-seventh chord": 0,
        "quartal trichord": 0,
        "incomplete dominant-seventh chord": 0,
        "half-diminished seventh chord": 0,
        "diminished seventh chord": 0,
        "quartal tetramirror": 0,
        "major-second major tetrachord": 0,
        "perfect-fourth major tetrachord": 0,
        "lydian tetrachord": 0,
        "minor-diminished ninth chord": 0,
        "major-second minor tetrachord": 0,
        "whole-tone tetramirror": 0,
        "flat-ninth pentachord": 0,
        "augmented seventh chord": 0,
        "phrygian tetrachord": 0,
        "harmonic minor tetrachord": 0,
        "all-interval tetrachord": 0,
        "major-diminished tetrachord": 0,
        "Messiaen's truncated mode 6": 0,
        "major pentatonic": 0,
        "minor-augmented tetrachord": 0,
        "augmented triad": 0,
        "minor-second quartal tetrachord": 0,
        "major-ninth chord": 0,
        "major pentachord": 0,
        "minor-second diminished tetrachord": 0,
        "perfect-fourth minor tetrachord": 0,
        "tritone quartal tetrachord": 0,
        "center-cluster pentamirror": 0,
        "augmented major tetrachord": 0,
        "dominant-ninth": 0,
        "Neapolitan pentachord": 0,
        "major-minor tetramirror": 0,
        "diminished-augmented ninth chord": 0,
        "phrygian pentachord": 0,
        "Javanese pentatonic": 0,
        "perfect-fourth diminished tetrachord": 0,
        "whole-tone pentachord": 0,
        "Kumoi pentachord": 0,
        "diminished-major ninth chord": 0,
        "diminished triad": 0,
        "incomplete half-diminished seventh chord": 0,
        "minor-ninth chord": 0,
        "C all combinatorial (P6, I3, RI9)": 0,
        "augmented-sixth pentachord": 0,
        "alternating tetramirror": 0,
        "minor-major ninth chord": 0,
        "incomplete major-seventh chord": 0,
        "lydian pentachord": 0,
        "tritone-fourth": 0,
        "minor-diminished tetrachord": 0,
        "dorian pentachord": 0,
        "whole-tone trichord": 0,
        "dominant-eleventh": 0,
        "diminished pentacluster": 0,
        "enigmatic pentachord": 0,
        "augmented-diminished ninth chord": 0,
        "Balinese Pelog pentatonic": 0,
        "major-augmented ninth chord": 0,
        "combinatorial RI (RI1)": 0,
        "double-fourth tetramirror": 0,
        "diminished minor-ninth chord": 0,
        "major-minor diminished pentachord": 0,
        "phrygian hexamirror": 0,
        "Persian pentamirror": 0,
        "minor-seventh pentacluster": 0,
        "Lebanese pentachord": 0,
        "Hirajoshi pentatonic": 0,
        "locrian hexachord": 0,
        "minor hexachord": 0
    };


    var tonicas = this.tonicas_cifraclub;
    var baixos = this.baixos_cifraclub;
    var modos = this.modos_cifraclub;

    if (tonicas) {
        for (i = 0; i < tonicas.length; i++) {
            var tonica = tonicas[i];
            var baixo = baixos[i];
            var modo = modos[i];

            if (tonica in map_tonicas) {
                var count_t = 1;
                var count_tonica = map_tonicas[tonica];
                if (count_tonica) {
                    count_t = count_tonica + 1;
                }
                map_tonicas[tonica] = count_t;
            }

            if (baixo in map_baixos) {
                var count_b = 1;
                var count_baixo = map_baixos[baixo];
                if (count_baixo) {
                    count_b = count_baixo + 1;
                }
                map_baixos[baixo] = count_b;
            }

            if (modo in map_modos) {
                var count_m = 1;
                var count_modos = map_modos[modo];
                if (count_modos) {
                    count_m = count_modos + 1;
                }
                map_modos[modo] = count_m;
            }

        }
    }
    emit(this._id, {cont_tonicas: map_tonicas, cont_baixos: map_baixos, cont_modos: map_modos});
};

var reduce = function (key, values) {
    return values.length;
};

query_map_reduce = {
    "$and": [{"tonicas_cifraclub": {'$exists': 1}},
        {"$where": "this.tonicas_cifraclub.length > 0"}]
}

db.musicas_pre_adb.mapReduce(map_contadores, reduce, {query: query_map_reduce, out: "cont"});

// Atualizamos a colecao com as tonicas, os baixos e os modos.
db.cont.find({}).forEach(function (doc) {
    var fields_set = {};
    var cont_tonicas = doc.value.cont_tonicas;
    for (var field in cont_tonicas) {
        var field_replace = field.replace(/\#/g, "sus");
        var field_replace = field_replace.replace(/\-/g, "b");
        fields_set["T_" + field_replace] = cont_tonicas[field];
    }

    var cont_baixos = doc.value.cont_baixos;
    for (var field in cont_baixos) {
        var field_replace = field.replace(/\#/g, "sus");
        var field_replace = field_replace.replace(/\-/g, "b");
        fields_set["B_" + field_replace] = cont_baixos[field];
    }

    var cont_modos = doc.value.cont_modos;
    for (var field in cont_modos) {
        var field_replace = field.replace(/(\W+)/g, "_");
        fields_set["M_" + field_replace] = cont_modos[field];
    }
    db.musicas_pre_adb.update({_id: doc._id}, {$set: fields_set});
});

// Cria-se a variavel com a quantidade de acordes unicos
db.musicas_pre_adb.find({acordes_unicos_cifraclub: {$exists: 1}}).forEach(function (document) {
    var qtd_acordes_unicos_cifraclub = document.acordes_unicos_cifraclub.length;
    db.musicas_pre_adb.update({_id: document._id}, {$set: {qtd_acordes_unicos_cifraclub: qtd_acordes_unicos_cifraclub}});
});


db.musicas_pre_adb.find({}).forEach(function (doc) {
    var nome = doc.nome.replace(/,/g, '');
    var artista = doc.nome.replace(/,/g, '');
    var estilo_cifraclub = doc.nome.replace(/,/g, '');
});

// media de visualizacoes
db.musicas_pre_adb.find({qtd_exibicoes_youtube: {$exists:1}, dias_desde_publicacao_youtube: {$exists:1}}).forEach(function (doc) {
    var qtd_exibicoes = doc.qtd_exibicoes_youtube;
    var qtd_dias = doc.dias_desde_publicacao_youtube;
    var media = qtd_exibicoes / qtd_dias;
    var dict_update = {calc_media_exibicoes_dia_youtube_1: media};

    db.musicas_pre_adb.update(
        {_id: doc._id},
        {$set: dict_update},
        {multi: true}
    )
});


// Separo os estilos de acordo com a coluna
function remover_caracteres_invalidos(valor) {
  var string = valor;
	var mapaAcentosHex = {
        a : /[\xE0-\xE6]/g,
        A : /[\xC0-\xC6]/g,
        e : /[\xE8-\xEB]/g,
        E : /[\xC8-\xCB]/g,
        i : /[\xEC-\xEF]/g,
        I : /[\xCC-\xCF]/g,
        o : /[\xF2-\xF6]/g,
        O : /[\xD2-\xD6]/g,
        u : /[\xF9-\xFC]/g,
        U : /[\xD9-\xDC]/g,
        c : /\xE7/g,
        C : /\xC7/g,
        n : /\xF1/g,
        N : /\xD1/g,
        _e_ : /\&/g,
        sus : /\#/g,
        _ : /\W/g,
	};

	for (var letra in mapaAcentosHex) {
            var expressaoRegular = mapaAcentosHex[letra];
            string = string.replace(expressaoRegular, letra);
	}
    return string.toLowerCase();
}

var estilos = [];
var tons = [];
var query = {estilo_cifraclub: {$exists: true, $nin: [null]}, tom_cifraclub: {$exists:true, $nin: [null]}};
var fields = {_id: 1, estilo_cifraclub: 1, tom_cifraclub:1};
db.musicas_pre_adb.find(query, fields).forEach(function (doc) {
    var estilo_normalizado = remover_caracteres_invalidos(doc.estilo_cifraclub);
    if (estilos.indexOf(estilo_normalizado) < 0) {
        estilos.push(estilo_normalizado);
    }

    print(doc._d + doc.tom_cifraclub);

    var tom_normalizado = remover_caracteres_invalidos(doc.tom_cifraclub);
    tom_normalizado = tom_normalizado.toUpperCase();
    tom_normalizado = tom_normalizado.replace('SUS', 'sus');
    if (tons.indexOf(tom_normalizado) < 0) {
        tons.push(tom_normalizado);
    }
});

estilos = estilos.sort();
tons = tons.sort();

var map_estilos = {};
for (var i = 0; i < estilos.length; i++) {
    map_estilos['E_' + estilos[i]] = 0;
}

var map_tons = {};
for (var i = 0; i < tons.length; i++) {
    map_tons['TOM_' + tons[i]] = 0;
}

db.musicas_pre_adb.update(
    {_id: {$exists: 1}},
    {$set: map_estilos},
    {multi: true}
)

db.musicas_pre_adb.update(
    {_id: {$exists: 1}},
    {$set: map_tons},
    {multi: true}
)

var query = {estilo_cifraclub: {$exists: true, $nin: [null]}, tom_cifraclub: {$exists:true, $nin: [null]}};
var fields = {_id: 1, estilo_cifraclub: 1, tom_cifraclub:1};
db.musicas_pre_adb.find(query, fields).forEach(function(doc) {
    var estilo_normalizado = remover_caracteres_invalidos(doc.estilo_cifraclub);
    var tom_normalizado = remover_caracteres_invalidos(doc.tom_cifraclub);
    tom_normalizado = tom_normalizado.toUpperCase();
    tom_normalizado = tom_normalizado.replace('SUS', 'sus');

    var map_estilos_tons = {};
    map_estilos_tons['E_' + estilo_normalizado] = 1;
    map_estilos_tons['TOM_' + tom_normalizado] = 1;

    db.musicas_pre_adb.update(
        {_id: doc._id},
        {$set: map_estilos_tons},
        {multi: true}
    )
});


// Base para cesto de compras
db.musicas_basket.remove({});
db.musicas_pre_adb.find({tonicas_cifraclub: {$exists: 1}, $where: "this.tonicas_cifraclub.length > 0", qtd_exibicoes_youtube: {$exists:1}, dias_desde_publicacao_youtube: {$exists:1}}).forEach(function(doc){
        for (var i = 0; i < doc.seq_acordes_cifraclub.length; i++) {
        var acorde = doc.seq_acordes_cifraclub[i];
        var id = doc._id + "_" + acorde;
        db.musicas_basket.update(
                { _id: id },
                {
                    id_musica: doc._id,
                    acorde: acorde,
                    tom_cifraclub: doc.tom_cifraclub,
                    qtd_exibicoes_youtube: doc.qtd_exibicoes_youtube,
                    dias_desde_publicacao_youtube: doc.dias_desde_publicacao_youtube
                },
                { upsert: true }
        );
    }

});


// Obter os campos da tabela
mr = db.runCommand({
    "mapreduce": "musicas_pre_adb",
    "map": function () {
        for (var key in this) {
            emit(key, null);
        }
    },
    "reduce": function (key, stuff) {
        return null;
    },
    "out": "musicas_pre_adb" + "_keys"
})

db[mr.result].distinct("_id")


// Obter os campos da colecao basket
mr = db.runCommand({
    "mapreduce": "musicas_basket",
    "map": function () {
        for (var key in this) {
            emit(key, null);
        }
    },
    "reduce": function (key, stuff) {
        return null;
    },
    "out": "musicas_basket" + "_keys"
})

db[mr.result].distinct("_id")

//COLAR NO ARQUIVO fields.txt E REMOVER COM O REGEX DAS LINHAS AS ASPAS E O VIRG. "|,

{
    $and: [{tonicas_cifraclub: {$exists: 1}}, {$where: this.tonicas_cifraclub.length > 0}]
}


//mongoexport -d scrapy_tcc -c musicas_pre_adb --type=csv --query '{"tonicas_cifraclub": {"$exists": "1"}, "$where": "this.tonicas_cifraclub.length > 0"}' --fieldFile ./fields.txt --out ./base_adb5.csv
//mongoexport -d scrapy_tcc -c musicas_pre_adb --query '{"tonicas_cifraclub": {"$exists": "1"}, "$where": "this.tonicas_cifraclub.length > 0"}' --fieldFile ./fields.txt --out ./base_adb1.json --jsonArray
//mongoexport -d scrapy_tcc -c musicas_pre_adb --type=csv --query '{"tonicas_cifraclub": {"$exists": "1"}, "$where": "this.tonicas_cifraclub.length > 0"}' --fieldFile ./fields.txt --out ./base_adb.csv
//mongoexport -d scrapy_tcc -c musicas_pre_adb --type=csv --query '{"tonicas_cifraclub": {"$exists": "1"}, "$where": "this.tonicas_cifraclub.length > 0"}' --fieldFile ./fields.txt --out ./base_adb0831.csv
//EXPORTACAO BASE CESTO DE COMPRAS
//mongoexport -d scrapy_tcc -c musicas_basket --type=csv --fieldFile ./fields_basket.txt --out ./base_basket.csv

// ENCONTRA OS ACORDES DE ACORDO COM SEU DESENHO
dict_dicionario = {};

db.dicionario_acordes.find({foi_sucesso:true}).forEach(function(doc){
    var desenho_acorde = doc.desenho_acorde;
    var acorde = doc._id;
    if (!dict_dicionario[desenho_acorde])
        dict_dicionario[desenho_acorde] = [];
    dict_dicionario[desenho_acorde].push(acorde);
});

dict_dicionario

"{"
"A"
":0,"
"A#"
":0,"
"A-"
":0,"
"B"
":0,"
"B-"
":1,"
"C"
":2,"
"C#"
":0,"
"D"
":1,"
"D#"
":1,"
"D-"
":0,"
"E"
":0,"
"E-"
":0,"
"F"
":1,"
"F#"
":0,"
"G"
":1,"
"G#"
":0,"
"G-"
":0}", "{"
"A"
":0,"
"A#"
":0,"
"A-"
":0,"
"B"
":0,"
"B-"
":1,"
"C"
":2,"
"C#"
":0,"
"D"
":1,"
"D#"
":1,"
"D-"
":0,"
"E"
":0,"
"E-"
":0,"
"F"
":1,"
"F#"
":0,"
"G"
":1,"
"G#"
":0,"
"G-"
":0}", "{"
"Balinese Pelog pentatonic"
":0,"
"C all combinatorial (P6, I3, RI9)"
":0,"
"Hirajoshi pentatonic"
":0,"
"Javanese pentatonic"
":0,"
"Kumoi pentachord"
":0,"
"Lebanese pentachord"
":0,"
"Messiaen's truncated mode 6"
":0,"
"Neapolitan pentachord"
":0,"
"Persian pentamirror"
":0,"
"all-interval tetrachord"
":0,"
"alternating tetramirror"
":0,"
"augmented major tetrachord"
":0,"
"augmented seventh chord"
":0,"
"augmented triad"
":0,"
"augmented-diminished ninth chord"
":0,"
"augmented-sixth pentachord"
":0,"
"center-cluster pentamirror"
":0,"
"combinatorial RI (RI1)"
":0,"
"diminished minor-ninth chord"
":0,"
"diminished pentacluster"
":0,"
"diminished seventh chord"
":0,"
"diminished triad"
":0,"
"diminished-augmented ninth chord"
":0,"
"diminished-major ninth chord"
":0,"
"dominant seventh chord"
":0,"
"dominant-eleventh"
":0,"
"dominant-ninth"
":0,"
"dorian pentachord"
":0,"
"double-fourth tetramirror"
":0,"
"enigmatic pentachord"
":0,"
"flat-ninth pentachord"
":0,"
"half-diminished seventh chord"
":0,"
"harmonic minor tetrachord"
":0,"
"incomplete dominant-seventh chord"
":0,"
"incomplete half-diminished seventh chord"
":0,"
"incomplete major-seventh chord"
":0,"
"incomplete minor-seventh chord"
":0,"
"interval class 5"
":0,"
"locrian hexachord"
":0,"
"lydian pentachord"
":0,"
"lydian tetrachord"
":0,"
"major pentachord"
":0,"
"major pentatonic"
":0,"
"major seventh chord"
":0,"
"major triad"
":5,"
"major-augmented ninth chord"
":0,"
"major-diminished tetrachord"
":0,"
"major-minor diminished pentachord"
":0,"
"major-minor tetramirror"
":0,"
"major-ninth chord"
":0,"
"major-second major tetrachord"
":0,"
"major-second minor tetrachord"
":0,"
"minor hexachord"
":0,"
"minor seventh chord"
":0,"
"minor triad"
":2,"
"minor-augmented tetrachord"
":0,"
"minor-diminished ninth chord"
":0,"
"minor-diminished tetrachord"
":0,"
"minor-major ninth chord"
":0,"
"minor-ninth chord"
":0,"
"minor-second diminished tetrachord"
":0,"
"minor-second quartal tetrachord"
":0,"
"minor-seventh pentacluster"
":0,"
"perfect-fourth diminished tetrachord"
":0,"
"perfect-fourth major tetrachord"
":0,"
"perfect-fourth minor tetrachord"
":0,"
"phrygian hexamirror"
":0,"
"phrygian pentachord"
":0,"
"phrygian tetrachord"
":0,"
"quartal tetramirror"
":0,"
"quartal trichord"
":0,"
"tritone quartal tetrachord"
":0,"
"tritone-fourth"
":0,"
"whole-tone pentachord"
":0,"
"whole-tone tetramirror"
":0,"
"whole-tone trichord"
":0}"


// TODO PREPARAR UMA BASE PARA A ANALISE DE ASSOCIACAO

//  (\"{2})(.{1,}?)(\"{2})\:\d+ // Separa as tonicas, baixos e modos dos contadore
//  Usar no replace o $2

//  T_A,T_A#,T_A-,T_B,T_B-,T_C,T_C#,T_D,T_D#,T_D-,T_E,T_E-,T_F,T_F#,T_G,T_G#,T_G-,B_A,B_A#,B_A-,B_B,B_B-,B_C,B_C#,B_D,B_D#,B_D-,B_E,B_E-,B_F,B_F#,B_G,B_G#,B_G-

//  Normalizo as strings dos modos
//  [^a-z1-9\,]

M_balinese_pelog_pentatonic, M_c_all_combinatorial_p6_i3_ri9, M_hirajoshi_pentatonic, M_javanese_pentatonic, M_kumoi_pentachord, M_lebanese_pentachord, M_messiaen_s_truncated_mode_6, M_neapolitan_pentachord, M_persian_pentamirror, M_all_interval_tetrachord, M_alternating_tetramirror, M_augmented_major_tetrachord, M_augmented_seventh_chord, M_augmented_triad, M_augmented_diminished_ninth_chord, M_augmented_sixth_pentachord, M_center_cluster_pentamirror, M_combinatorial_ri_ri1, M_diminished_minor_ninth_chord, M_diminished_pentacluster, M_diminished_seventh_chord, M_diminished_triad, M_diminished_augmented_ninth_chord, M_diminished_major_ninth_chord, M_dominant_seventh_chord, M_dominant_eleventh, M_dominant_ninth, M_dorian_pentachord, M_double_fourth_tetramirror, M_enigmatic_pentachord, M_flat_ninth_pentachord, M_half_diminished_seventh_chord, M_harmonic_minor_tetrachord, M_incomplete_dominant_seventh_chord, M_incomplete_half_diminished_seventh_chord, M_incomplete_major_seventh_chord, M_incomplete_minor_seventh_chord, M_interval_class_5, M_locrian_hexachord, M_lydian_pentachord, M_lydian_tetrachord, M_major_pentachord, M_major_pentatonic, M_major_seventh_chord, M_major_triad, M_major_augmented_ninth_chord, M_major_diminished_tetrachord, M_major_minor_diminished_pentachord, M_major_minor_tetramirror, M_major_ninth_chord, M_major_second_major_tetrachord, M_major_second_minor_tetrachord, M_minor_hexachord, M_minor_seventh_chord, M_minor_triad, M_minor_augmented_tetrachord, M_minor_diminished_ninth_chord, M_minor_diminished_tetrachord, M_minor_major_ninth_chord, M_minor_ninth_chord, M_minor_second_diminished_tetrachord, M_minor_second_quartal_tetrachord, M_minor_seventh_pentacluster, M_perfect_fourth_diminished_tetrachord, M_perfect_fourth_major_tetrachord, M_perfect_fourth_minor_tetrachord, M_phrygian_hexamirror, M_phrygian_pentachord, M_phrygian_tetrachord, M_quartal_tetramirror, M_quartal_trichord, M_tritone_quartal_tetrachord, M_tritone_fourth, M_whole_tone_pentachord, M_whole_tone_tetramirror, M_whole_tone_trichord


//  T_A,T_A#,T_A-,T_B,T_B-,T_C,T_C#,T_D,T_D#,T_D-,T_E,  T_E-,T_F,T_F#,T_G,T_G#,T_G-,B_A,B_A#,B_A-,B_B,B_B-,B_C,B_C#,B_D,B_D#,B_D-,B_E,B_E-,B_F,B_F#,B_G,B_G#,B_G-

//  T_A,T_A#,T_A-,T_B,T_B-,T_C,T_C#,T_D,T_D#,T_D-,T_E,T_E-,T_F,T_F#,T_G,T_G#,T_G-,B_A,B_A#,B_A-,B_B,B_B-,B_C,B_C#,B_D,B_D#,B_D-,B_E,B_E-,B_F,B_F#,B_G,B_G#,B_G-,M_balinese_pelog_pentatonic,M_c_all_combinatorial_p6_i3_ri9,M_hirajoshi_pentatonic,M_javanese_pentatonic,M_kumoi_pentachord,M_lebanese_pentachord,M_messiaen_s_truncated_mode_6,M_neapolitan_pentachord,M_persian_pentamirror,M_all_interval_tetrachord,M_alternating_tetramirror,M_augmented_major_tetrachord,M_augmented_seventh_chord,M_augmented_triad,M_augmented_diminished_ninth_chord,M_augmented_sixth_pentachord,M_center_cluster_pentamirror,M_combinatorial_ri_ri1,M_diminished_minor_ninth_chord,M_diminished_pentacluster,M_diminished_seventh_chord,M_diminished_triad,M_diminished_augmented_ninth_chord,M_diminished_major_ninth_chord,M_dominant_seventh_chord,M_dominant_eleventh,M_dominant_ninth,M_dorian_pentachord,M_double_fourth_tetramirror,M_enigmatic_pentachord,M_flat_ninth_pentachord,M_half_diminished_seventh_chord,M_harmonic_minor_tetrachord,M_incomplete_dominant_seventh_chord,M_incomplete_half_diminished_seventh_chord,M_incomplete_major_seventh_chord,M_incomplete_minor_seventh_chord,M_interval_class_5,M_locrian_hexachord,M_lydian_pentachord,M_lydian_tetrachord,M_major_pentachord,M_major_pentatonic,M_major_seventh_chord,M_major_triad,M_major_augmented_ninth_chord,M_major_diminished_tetrachord,M_major_minor_diminished_pentachord,M_major_minor_tetramirror,M_major_ninth_chord,M_major_second_major_tetrachord,M_major_second_minor_tetrachord,M_minor_hexachord,M_minor_seventh_chord,M_minor_triad,M_minor_augmented_tetrachord,M_minor_diminished_ninth_chord,M_minor_diminished_tetrachord,M_minor_major_ninth_chord,M_minor_ninth_chord,M_minor_second_diminished_tetrachord,M_minor_second_quartal_tetrachord,M_minor_seventh_pentacluster,M_perfect_fourth_diminished_tetrachord,M_perfect_fourth_major_tetrachord,M_perfect_fourth_minor_tetrachord,M_phrygian_hexamirror,M_phrygian_pentachord,M_phrygian_tetrachord,M_quartal_tetramirror,M_quartal_trichord,M_tritone_quartal_tetrachord,M_tritone_fourth,M_whole_tone_pentachord,M_whole_tone_tetramirror,M_whole_tone_trichord


//_id,artista,nome,estilo_cifraclub,tom_cifraclub,capo_cifraclub,dt_insercao,duracao_lastfm,qtd_audicoes_lastfm,duracao_spotify,popularidade_spotify,possui_capo_cifraclub,possui_tabs_cifraclub,qtd_exibicoes_cifraclub,qtd_exibicoes_youtube,qtd_gostei_youtube,qtd_nao_gostei_youtube,dt_publicacao_youtube,dias_desde_publicacao_youtube,cont_tonicas,cont_baixos,cont_modos


// NAS LINHAS USO O REGEX (\"{2})(.{1,}?)(\"{2})\:(\d+\.\d+) SUBSTITUINDO O $4


db.musicas_pre_adb.aggregate([{
    $project: {
        _id: 0,
        cont_tonicas: 1,
        cont_modos: 1
    }
}, {
    $unwind: "cont_tonicas"
}, {
    $out: "forcsv"
}]);


T_A, T_Asus, T_Ab, T_B, T_Bb, T_C, T_Csus, T_D, T_Dsus, T_Db, T_E, T_Eb, T_F, T_Fsus, T_G, T_Gsus, T_Gb, B_A, B_Asus, B_Ab, B_B, B_Bb, B_C, B_Csus, B_D, B_Dsus, B_Db, B_E, B_Eb, B_F, B_Fsus, B_G, B_Gsus, B_Gb





// PREPARACAO DA BASE DE SNA


{calc_media_exibicoes_dia_youtube_1: {$gt:65}}


//mongoexport -d scrapy_tcc -c musicas_pre_adb --type=csv --query '{"seq_acordes_cifraclub": {"$exists": "1"}, "$where": "this.seq_acordes_cifraclub.length > 0", "calc_media_exibicoes_dia_youtube_1": {"$gt": 65}}' --fieldFile ./fields_sna.txt --out ./base_sna_pop.csv
//mongoexport -d scrapy_tcc -c musicas_pre_adb --type=csv --query '{"seq_acordes_cifraclub": {"$exists": "1"}, "$where": "this.seq_acordes_cifraclub.length > 0", "calc_media_exibicoes_dia_youtube_1": {"$lt": 65}}' --fieldFile ./fields_sna.txt --out ./base_sna_impop.csv




/* ### FIM - Preparacao da base ### */








// TODO:

Remover
espacos
dos
acordes
Criar
variavel
para
saber as inversoes
Criar
variavel
para
saber as cadencias








