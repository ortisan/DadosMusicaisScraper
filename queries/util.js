//mongodump --collection musicas --db scrapy --out /Users/marcelo/Documents/Ambiente/backups/mongodb
//mongorestore /Users/marcelo/Documents/Ambiente/backups/mongodb -d test -c musics
// mongorestore --host localhost --db test --collection musics /Users/marcelo/Documents/Ambiente/backups/mongodb/20150221


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


db.messages.insert([{"Category": 1, "Messages": ["Msg1", "Msg2"], "Value": 1},
    {"Category": 1, "Messages": [], "Value": 10},
    {"Category": 1, "Messages": ["Msg1", "Msg3"], "Value": 100},
    {"Category": 2, "Messages": ["Msg4"], "Value": 1000},
    {"Category": 2, "Messages": ["Msg5"], "Value": 10000},
    {"Category": 3, "Messages": [], "Value": 100000}])


var group1 = {
    "$group": {
        "_id": "$Category",
        "Value": {"$sum": "$Value"},
        "Messages": {"$push": "$Messages"}
    }
};

var project1 = {
    "$project": {
        "Value": 1, "Messages": {
            "$cond": [{"$eq": ["$Messages", [[]]]},
                [[null]],
                "$Messages"
            ]
        }
    }
};

db.messages.aggregate(group1, project1, unwind, unwind)

db.messages.aggregate(unwind, unwind)


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

db.acordes_estilos.find({$or: [{"foi_sucesso": {$exists: 0}}, {"foi_sucesso": false}]});

db.acordes_estilos.find({_id: "F7M(9)/C"});

//mongoexport -d scrapy -c substituicao_acordes --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/traducao.json
//mongoimport -d scrapy -c substituicao_acordes /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/traducao.json
//mongoexport -d scrapy -c musicas --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas.json
//mongoimport -d scrapy -c musicas /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas.json

//mongoexport -d scrapy -c musicas_erro_acordes --out /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas_erro_acordes.json
//mongoimport -d scrapy -c musicas_erro_acordes2 /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas_erro_acordes.json

musicas_erro_acordes

//mongoimport -d scrapy -c musicas2 /Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/musicas.json

var depara = {};

db.substituicao_acordes.find({para: {$exists: 1}}).forEach(function (doc) {
    depara[doc._id] = doc.para;
});


db.musicas_erro_acordes.find().forEach(function (doc) {
    var doc_musica = db.musicas2.findOne({_id: doc._id});
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
    db.musicas2.update({_id: doc._id}, {$set: {novo_seq_acordes_cifraclub: novo_seq_acordes}});
});

db.musicas_erro_acordes.find({_id: "Alejandro Sanz - Questa Storia É Finita"});
db.musicas2.find({_id: "Alejandro Sanz - Questa Storia É Finita"}, {novo_seq_acordes_cifraclub: 1});

db.musicas2.find({novo_seq_acordes_cifraclub: {$exists: 0}}, {novo_seq_acordes_cifraclub: 1});
