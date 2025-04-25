# PerplexitySync

**PerplexitySync** je desktopová aplikace pro správu projektů a synchronizaci mezi Perplexity AI, lokálním souborovým systémem a Ollama AI, s bezpečným MCP serverem a GUI vrstvou.

![Build Status](https://github.com/JardaMicke/PerplexitySync/actions/workflows/python-ci.yml/badge.svg)

## Lokální nasazení v Dockeru

### 1. Požadavky
- Docker Desktop (Windows, Linux, Mac)

### 2. Sestavení a spuštění kontejneru
```bash
git clone https://github.com/JardaMicke/PerplexitySync.git
cd Longin_perplexity
docker build -t perplexitysync .
docker run -it -p 3000:3000 -v %cd%/appdata:/app/appdata perplexitysync
```
- MCP server poběží na `http://localhost:3000`
- GUI a ostatní komponenty komunikují přes API a sdílený objem `/app/appdata`

### 3. Proměnné prostředí
- `MCP_CONFIG_PATH` – cesta ke konfiguraci MCP serveru
- `OLLAMA_API_URL` – adresa Ollama API (propojeno s hostem)
- `APPDATA` – složka pro cache, šifrované konfigurace, logy

### 4. Komunikace a bezpečnost
- Všechny API endpointy jsou dostupné pouze z hosta (není vystaveno veřejně)
- Spouštění příkazů je whitelisted a auditováno
- Veškerá citlivá data (cesty, klíče) jsou šifrována (DPAPI)

### 5. Typické workflow
- Tray aplikace umožní výběr projektu, autostart, notifikace
- Při dotazu v Perplexity je automaticky přidán aktuální stav codebase
- Synchronizace a exekuce příkazů probíhá přes MCP server

### 6. Testování
```bash
docker run -it perplexitysync python -m unittest discover -s tests
```

---

## Architektura
- **MCP server**: REST API pro správu souborů, exec, audit, bezpečnost
- **Ollama integration**: generování kódu, prompt engineering
- **GUI**: tray, dialogy, notifikace, autostart
- **Synchronizační engine**: sliding window, batch, cache
- **Konfigurační management**: šifrování, .psync, validace

## CI/CD
- Každý push a pull request na `main` automaticky spustí testy (GitHub Actions)

## Release
- Pro stabilní verzi vytvořte nový tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

## Branch protection
- Doporučeno nastavit v GitHub repozitáři: Settings > Branches > Add rule > Require status checks to pass before merging

---

## Poznámky
- Pro enterprise rozšíření (SAML/OAuth, cluster, compliance) kontaktujte autora.
