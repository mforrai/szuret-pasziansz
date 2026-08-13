# Szüret-CLI

A **Szüret** (Kiadó: Granna) című társasjáték ASCII-alapú Python-verziója.

## Verziók

- **v2.1** – Windows terminal fix
- **v2.0** – Multiplayer
- **v1.35** – Bugfix (ChatGPT code review)
- **v1.3** – Egyjátékos mód

## Futtatáshoz szükséges Python-környezet

A játék Python 3-mal fut. Javasolt külön virtuális környezetet használni.

### 1. Repository klónozása

```bash
git clone https://github.com/mforrai/szuret-cli.git
cd szuret-cli
```

### 2. Virtuális környezet létrehozása

Linux / macOS:

```bash
python3 -m venv venv-szuret-cli
source venv-szuret-cli/bin/activate
```

Windows PowerShell:

```powershell
py -m venv venv-szuret-cli
.\venv-szuret-cli\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
py -m venv venv-szuret-cli
venv-szuret-cli\Scripts\activate.bat
```

### 3. Python-függőségek telepítése

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

A `requirements.txt` jelenleg ezeket a külső csomagokat telepíti:

- `requests`
- `websocket-client`

### 4. Játék indítása

```bash
python main.py
```

Indítás után kiválasztható:

```text
1. Single player
2. Multiplayer
```

A multiplayer módhoz internetkapcsolat szükséges, mert a játék közös állapotát Cloudflare Worker / Durable Object koordinálja.

## Frissítés

Ha a repository már le van klónozva:

```bash
git switch main
git pull
```

A függőségek frissítéséhez vagy új dependency hozzáadása után érdemes újra futtatni:

```bash
python -m pip install -r requirements.txt
```
