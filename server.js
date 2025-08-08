const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(express.json({ limit: '10mb' })); 
app.use(cors());

// Variavel para armazenar o ultimo dado recebido
let ultimoDado = {
    aplicacao: "MedSolo IoT",
    temperatura: null,
    solo: null,
    timestamp: null,
    status: "Aguardando dados..."
};

// --- Rota para receber os dados da placa (POST) ---
app.post('/dados', (req, res) => {
    try {
        console.log('Dados recebidos:', req.body);
        
        // Desestrutura os dados de temperatura e solo
        const { temperatura, solo } = req.body;
        
        // Validar dados obrigatorios (simples)
        if (temperatura == null || solo == null) {
            return res.status(400).json({
                erro: "Dados incompletos. Esperado: temperatura, solo",
                recebido: req.body
            });
        }
        
        // Atualiza o ultimo dado recebido
        const timestamp = new Date();
        ultimoDado = {
            aplicacao: "MedSolo IoT",
            temperatura: temperatura,
            solo: solo,
            timestamp: timestamp.toISOString(),
            status: "Online"
        };
        
        console.log(` Dados salvos - Temp: ${temperatura}C, Solo: ${solo}%`);
        
        res.status(200).json({
            mensagem: "Dados recebidos com sucesso",
            dados: ultimoDado
        });
        
    } catch (error) {
        console.error('Erro ao processar dados:', error);
        res.status(500).json({
            erro: "Erro interno do servidor",
            detalhes: error.message
        });
    }
});

// --- Rota para exibir os ultimos dados (GET) ---
app.get('/', (req, res) => {
    try {
        // Verifica se os dados sao recentes (ultimos 30 segundos)
        if (ultimoDado.timestamp) {
            const agora = new Date();
            const ultimaLeitura = new Date(ultimoDado.timestamp);
            const diferencaMs = agora - ultimaLeitura;
            
            if (diferencaMs > 30000) { // Se a ultima leitura for mais de 30 segundos atras
                ultimoDado.status = "Offline - ultima leitura ha " + Math.round(diferencaMs / 1000) + "s";
            } else {
                ultimoDado.status = "Online"; // Se estiver dentro do tempo, garanta que o status e online
            }
        }
        
        res.json(ultimoDado);
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        res.status(500).json({
            erro: "Erro interno do servidor"
        });
    }
});

// Middleware para rotas nao encontradas (404)
app.use((req, res) => {
    res.status(404).json({
        erro: "Rota nao encontrada",
        rotas_disponiveis: [
            "GET / - ultimos dados dos sensores",
            "POST /dados - Enviar dados dos sensores"
        ]
    });
});

// Iniciar servidor
app.listen(port, '0.0.0.0', () => {
    console.log(`=== MedSolo IoT Server Simplificado ===`);
    console.log(`Acesse tambem via http://localhost:${port}`);
    console.log(`Sensores monitorados: Temperatura, Umidade do Solo`);
    console.log(`Timestamp inicial: ${new Date().toISOString()}`);
});