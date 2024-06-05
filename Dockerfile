# Use a imagem base do Python 3.11
FROM python:3.11

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários para o contêiner
COPY . .

# Instala o Pyenv
RUN curl https://pyenv.run | bash

# Instala o Python 3.11.1 com o Pyenv
RUN /root/.pyenv/bin/pyenv install 3.11.1 && \
    /root/.pyenv/bin/pyenv global 3.11.1

# Instala as dependências usando Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


# Comando para iniciar a sua aplicação FastAPI
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "5000"]