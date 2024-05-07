# Use uma imagem base Python
FROM python:3.11

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários para o contêiner
COPY . .

# Instala o Gunicorn
RUN pip install gunicorn

# Instala o Poetry
RUN pip install poetry

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Expõe a porta 5000 para acesso externo
EXPOSE 5000

# Define o comando para iniciar a aplicação com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]

