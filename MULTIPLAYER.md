# Szüret multiplayer – Cloudflare koordinátor

Ez az ág a többjátékos mód első lépése. A játékosok saját táblán játszanak; a Cloudflare Durable Object csak a közös játékállapotot koordinálja.

## Mi közös?

- birtokok sorrendje
- aktuális birtok
- útkártya-pakli és aktuális útkártya
- sárga lapok száma
- forduló
- READY állapotok
- forduló- és végeredmények

A játékosok saját `Matrix` állapota és az útelhelyezések nem kerülnek a szerverre.

## Szinkronizáció

1. A host létrehoz/választ egy szobakódot, például `BOR2026`.
2. A játékosok ugyanarra a `/room/BOR2026` WebSocket végpontra csatlakoznak.
3. A host `start_game` üzenetet küld.
4. A Durable Object összekeveri a birtokokat és a 42 lapos paklit.
5. Minden játékos ugyanazt az aktuális birtokot és útkártyát kapja.
6. A játékos lokálisan elhelyezi az utat, majd `ready` üzenetet küld.
7. A következő lap csak akkor kerül felfedésre, ha minden játékos READY.
8. A 4. sárga lap után a szerver `round_end` üzenetet küld, és megvárja minden játékos `round_score` üzenetét.
9. Az 5. forduló után minden kliens elküldi a saját teljes `final_score` értékét; a szerver rangsort és győztest küld vissza.

A `peek`/`BIRTOK` válasz csak a kérő WebSocketre érkezik, ezért a következő birtok titkos marad a többi játékos előtt.

## Cloudflare Worker telepítése

Cloudflare account és Node.js szükséges.

```bash
cd cloudflare-worker
npm install
npx wrangler login
npm run typecheck
npm run deploy
```

Deploy után kapsz egy Worker URL-t, például:

```text
https://szuret-multiplayer.<account>.workers.dev
```

Egészségellenőrzés:

```bash
curl https://szuret-multiplayer.<account>.workers.dev/health
```

Várt válasz:

```json
{"ok":true}
```

## Python kliens tesztelése

```bash
pip install -r requirements-multiplayer.txt
```

Host:

```bash
python multiplayer_client.py \
  https://szuret-multiplayer.<account>.workers.dev \
  BOR2026 Miklos --host
```

Másik játékos:

```bash
python multiplayer_client.py \
  https://szuret-multiplayer.<account>.workers.dev \
  BOR2026 Gabor
```

A jelenlegi `multiplayer_client.py` csak a hálózati réteg tesztkliense. A következő fejlesztési lépés a kliens eseményeinek bekötése a `szuret.py` játékhurokba.

## Protokoll

### Kliens → szerver

- `start_game` – host indítja a játékot
- `ready` – a játékos végzett az aktuális lappal
- `peek` – BIRTOK akció
- `round_score` – aktuális forduló pontszáma
- `final_score` – teljes végeredmény

### Szerver → kliens

- `connected`
- `lobby`
- `game_started`
- `farm_revealed`
- `road_revealed`
- `ready_state`
- `peek_result` – csak a kérő játékos kapja
- `round_end`
- `round_results`
- `request_final_score`
- `game_finished`
- `error`
