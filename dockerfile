# Use a imagem base do Python
FROM python:3.9

# Sete o diretório de trabalho para /app
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install -r requirements.txt

# Copie o código da sua aplicação para o diretório de trabalho
COPY . .

# Exponha a porta 8000 para permitir conexões
EXPOSE 8000

# Execute o comando de inicialização do Django
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]