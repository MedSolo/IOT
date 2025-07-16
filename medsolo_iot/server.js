const express = require('express');
const app = express();
const port = 3000;

app.use(express.json()); // Permite receber JSON

let ultimoDado = {
    Aplication: "IoT",
    Temperatura: null,
    Umidade: null
};

// Rota para receber os dados da placa
app.post('/dados', (req, res) => {
    const { temperatura, umidade } = req.body;
    if (temperatura != null && umidade != null) {
        ultimoDado.Temperatura = temperatura;
        ultimoDado.Umidade = umidade;
        console.log("Dados recebidos:", ultimoDado);
        res.status(200).send("Dados recebidos com sucesso.");
    } else {
        res.status(400).send("Dados incompletos.");
    }
});

// Rota para exibir os últimos dados
app.get('/', (req, res) => {
    res.json(ultimoDado);
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
