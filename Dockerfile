FROM python:3.11.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Node.js и pyright
RUN apt-get update \ 
 && apt-get install -y curl gnupg ca-certificates \ 
 && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \ 
 && apt-get install -y nodejs \ 
 && npm install -g pyright \ 
 && apt-get clean \ 
 && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["sh", "-c", "alembic upgrade head && python src/main.py"]