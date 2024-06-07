# Usa a imagem base do Python 3.11
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


# Expondo a porta 5000 (porta padrão do Flask)
EXPOSE 5000

# Comando de execução do Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "5000:5000", "run:app"]