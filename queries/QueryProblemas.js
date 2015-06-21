//# Acordes com problemas
db.dicionario_acordes.find({$or: {foi_sucesso: false}})
//mongoexport --db=scrapy_tcc --collection=dicionario_acordes  --query="{foi_sucesso:false}" --out=/Users/marcelo/Documents/Ambiente/Projetos/Python/DadosMusicaisScraper/erros/acordes_com_erro.json

// # Musicas que possuem acordes problematicos
db.dicionario_acordes.find({foi_sucesso: false})


// # Inserimos em uma colecao os acordes com sucesso e erro
db.dicionario_acordes.remove({})
var project = {"$project": {"_id": "$foi_sucesso", acorde: "$_id"}};
var group = {"$group": {"_id": "$_id", acordes: {$push: "$acorde"}}};

db.dicionario_acordes.aggregate(project, group).forEach(function (doc) {
    db.acordes_sucesso_erro.insert(doc);
});
// # FIM - Inserimos em uma colecao os acordes com sucesso e erro

// # Separacao das musicas com erros de acorde
// # Saber quantas musicas estao com acordes invalidos para ver se vale a pena tratar ou nao. Separamos as musicas com sucesso e erro em termos de acordes
db.musicas_erro.remove({});
db.musicas_sucesso.remove({});
acordes_erro = db.acordes_sucesso_erro.findOne({_id: false}).acordes;
db.musicas.find({$and: [{seq_acordes_cifraclub: {$exists: 1}}, {$where: "this.seq_acordes_cifraclub.length > 0"}]}, {'_id': true, "seq_acordes_cifraclub": true}).forEach(function (doc) {
    for (i = 0; i < doc.seq_acordes_cifraclub.length; i++) {
        musica_sucesso = true;
        colecao = db.musicas_sucesso;
        if (acordes_erro.indexOf(doc.seq_acordes_cifraclub[i]) > 0) {
            musica_sucesso = false;
            colecao = db.musicas_erro;
            break;
        }
        colecao.insert(doc);
    }
});
// # FIM - Separacao das musicas com erros de acorde

// # Musicas com os acordes traduzidos
db.musicas.find({
    "$and": [{"acordes_unicos_cifraclub": {"$exists": 0}},
        {"seq_acordes_cifraclub": {'$exists': 1}},
        {"$where": "this.seq_acordes_cifraclub.length > 0"}]
}).count()



//# Acordes que nao comecam com [A-G]
db.dicionario_acordes.find({foi_sucesso: true, _id: {$regex: '^[^a-zA-Z]'}}).pretty()


