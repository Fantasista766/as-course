FROM python:3.11.11

# Node.js и pyright
RUN apt-get update \ 
 && apt-get install -y curl gnupg ca-certificates \ 
 && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \ 
 && apt-get install -y nodejs \ 
 && npm install -g pyright
#  && apt-get clean \ 
#  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["alembic", "upgrade", "head"]

CMD ["python", "src/main.py"]