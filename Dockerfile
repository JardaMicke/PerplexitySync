# Dockerfile pro lokální nasazení PerplexitySync
FROM python:3.10-slim

# Nastavení pracovního adresáře
WORKDIR /app

# Zkopírování requirements a instalace závislostí
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Instalace dalších systémových závislostí (pro pywin32, GUI, atd.)
RUN apt-get update && apt-get install -y \
    git \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Zkopírování celého projektu
COPY . .

# Nastavení proměnných prostředí pro správnou komunikaci
ENV MCP_CONFIG_PATH=/app/mcp_server/config.json
ENV OLLAMA_API_URL=http://host.docker.internal:11434/api/generate
ENV APPDATA=/app/appdata

# Vytvoření adresáře pro data a logy
RUN mkdir -p /app/appdata/PerplexitySync

# Exponování portů MCP serveru
EXPOSE 3000

# Výchozí příkaz: spuštění MCP serveru
CMD ["uvicorn", "mcp_server.server:app", "--host", "0.0.0.0", "--port", "3000"]
