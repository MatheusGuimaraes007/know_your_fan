
# 📊 Know Your Fan – Sistema de Análise e Validação de Fãs de eSports

O **Know Your Fan** é uma solução interativa desenvolvida em Python com Streamlit, que coleta, valida e analisa dados de fãs de e-sports da Furia para fins de personalização de experiências e segmentação inteligente. A aplicação permite que fãs enviem seus dados, comprovem identidade com upload de documentos e sejam analisados com auxílio de inteligência artificial.

---

## 🎯 Objetivo

Conhecer profundamente o fã de e-sports, centralizando dados relevantes como:

- Informações básicas (nome, CPF, endereço, interesses)
- Eventos, compras e atividades recentes no universo e-sports
- Validação automática de identidade via RG com OCR e AI
- Análise de comportamento e perfil através de gráficos e IA
- Vinculação e verificação de relevância de redes sociais (Fase futura)

---

## 🧠 Tecnologias Utilizadas

- **Python 3.11+**
- **Streamlit** – Interface interativa
- **SQLite** – Armazenamento local dos dados
- **EasyOCR** – Leitura e validação de documentos de identidade (RG)
- **OpenAI API** – Análise de perfis e respostas personalizadas
- **Pandas & Matplotlib** – Manipulação e visualização dos dados
- **Tqdm, Requests, JSON, OS** – Utilitários para processamento

---

## 🚀 Como Executar Localmente

1. Clone o repositório:

```
git clone https://github.com/MatheusGuimaraes007/know_your_fan
cd know_your_fan
```

2. Instale as dependências:

```
pip install -r requirements.txt
```

3. Execute o app:

```
streamlit run app.py
```

---

## 🗂️ Estrutura do Projeto

```
know_your_fan/
├── app.py                  # Arquivo principal do Streamlit
├── ocr_utils.py           # Funções de OCR com EasyOCR
├── database.db            # Banco SQLite com registros
├── requirements.txt       # Bibliotecas do projeto
├── uploads/               # Pasta de upload dos documentos
├── analysis/              # Lógica de geração de gráficos
└── README.md
```

---

## 🔍 Funcionalidades

- **📥 Coleta de Dados:**  
  Formulário para preenchimento de dados pessoais e esportivos.

- **🧾 Upload de RG:**  
  Envio de imagem/documento para validação da identidade do fã com EasyOCR.

- **✅ Verificação com AI:**  
  A IA interpreta e confirma se o documento corresponde aos dados inseridos.

- **📊 Análise Geral:**  
  Geração automática de gráficos com o perfil de todos os inscritos.

---

## 💾 Armazenamento

Todos os dados são armazenados em um banco SQLite local (`database.db`).  

---

## 🧠 Inteligência Artificial Aplicada

- **EasyOCR**: para extrair texto da imagem do RG.
- **OpenAI GPT**: para análise e avaliação textual personalizada dos perfis e respostas interpretativas.

---

## 👨‍💻 Autor

Desenvolvido por **Matheus Guimarães**  
GitHub: [https://github.com/MatheusGuimaraes007](https://github.com/MatheusGuimaraes007)
