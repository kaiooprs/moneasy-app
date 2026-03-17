💰 Moneasy

    Gestão financeira pessoal de forma simples, inteligente e visual.

O Moneasy é um Progressive Web App (PWA) focado em dar clareza ao seu dinheiro. Diferente de planilhas complexas, ele organiza seus gastos, prevê suas contas fixas e te ajuda a construir sua reserva de emergência com uma interface moderna e intuitiva.
🚀 Funcionalidades Principais

    📊 Inteligência Financeira: Gráficos interativos de despesas por categoria e resumo mensal de entradas/saídas.

    🛡️ Reserva de Emergência: Controle específico para carteiras de poupança com barra de progresso baseada em metas.

    📅 Contas Fixas & Assinaturas: Gerencie gastos recorrentes (Netflix, Aluguel, Academia) e dê "baixa" neles com um clique, integrando o pagamento direto às suas carteiras.

    💳 Gestão de Carteiras: Separação entre Contas Correntes (saldo disponível) e Contas de Reserva (investimentos/poupança).

    🏷️ Categorias Customizáveis: Organize seus lançamentos com ícones (emojis) e cores personalizadas.

    🔒 Segurança: Autenticação robusta utilizando JWT (JSON Web Tokens).

🛠️ Tech Stack
Camada	Tecnologias
Frontend	Vue.js 3, Tailwind CSS, Chart.js, Lucide Icons
Backend	Python, FastAPI, Beanie (ODM para MongoDB)
Banco de Dados	MongoDB (Atlas)
Segurança	OAuth2 com JWT (Passlib & Jose)
📦 Como rodar o projeto
1. Requisitos

    Python 3.10+

    Node.js 18+

    Instância do MongoDB (Local ou Atlas)

2. Backend
Bash

# Entre na pasta do backend
cd backend

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o .env (veja abaixo) e inicie
uvicorn app.main:app --reload

3. Frontend
Bash

# Entre na pasta do frontend
cd frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev

⚙️ Variáveis de Ambiente (.env)

Crie um arquivo .env na raiz do backend:
Snippet de código

DATABASE_URL=mongodb+srv://...
SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

📱 Visual do App

    [!TIP]
    O Moneasy foi desenhado com foco em Mobile First, garantindo uma experiência fluida tanto no celular quanto no desktop.

📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.