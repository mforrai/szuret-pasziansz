import { DurableObject } from "cloudflare:workers";

type Card = [number, number, number, number, 11 | 99];

type PlayerState = {
  id: string;
  name: string;
  host: boolean;
  ready: boolean;
  peekUsed: boolean;
  roundScore?: number;
  finalScore?: number;
};

type RoomState = {
  started: boolean;
  finished: boolean;
  round: number;
  yellowCount: number;
  cardIndex: number;
  currentFarm?: string;
  currentCard?: Card;
  farms: string[];
  deck: Card[];
  players: Record<string, PlayerState>;
};

type Env = {
  GAME_ROOMS: DurableObjectNamespace<GameRoom>;
};

const EMPTY_STATE: RoomState = {
  started: false,
  finished: false,
  round: 0,
  yellowCount: 0,
  cardIndex: 0,
  farms: [],
  deck: [],
  players: {},
};

function shuffle<T>(items: T[]): T[] {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const a = new Uint32Array(1);
    crypto.getRandomValues(a);
    const j = a[0] % (i + 1);
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function makeDeck(): Card[] {
  const grey: Card[] = [
    [1, 0, 0, 1, 11],
    [1, 1, 0, 0, 11],
    [0, 1, 1, 0, 11],
    [0, 0, 1, 1, 11],
    [0, 1, 0, 1, 11],
    [1, 0, 1, 0, 11],
  ];
  const yellow: Card[] = grey.map((c) => [c[0], c[1], c[2], c[3], 99] as Card);
  return shuffle([
    ...Array(3).fill(grey[0]),
    ...Array(3).fill(grey[1]),
    ...Array(3).fill(grey[2]),
    ...Array(3).fill(grey[3]),
    ...Array(4).fill(grey[4]),
    ...Array(4).fill(grey[5]),
    ...Array(4).fill(yellow[0]),
    ...Array(4).fill(yellow[1]),
    ...Array(4).fill(yellow[2]),
    ...Array(4).fill(yellow[3]),
    ...Array(3).fill(yellow[4]),
    ...Array(3).fill(yellow[5]),
  ]);
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return Response.json({ ok: true });
    }

    const match = url.pathname.match(/^\/room\/([A-Za-z0-9_-]{3,32})$/);
    if (!match) {
      return new Response("Use /room/<code>?name=<name>&host=1", { status: 404 });
    }

    const id = env.GAME_ROOMS.idFromName(match[1].toUpperCase());
    return env.GAME_ROOMS.get(id).fetch(request);
  },
};

export class GameRoom extends DurableObject<Env> {
  async fetch(request: Request): Promise<Response> {
    if (request.headers.get("Upgrade") !== "websocket") {
      return new Response("WebSocket required", { status: 426 });
    }

    const url = new URL(request.url);
    const name = (url.searchParams.get("name") || "Játékos").slice(0, 32);
    const wantsHost = url.searchParams.get("host") === "1";

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);
    const playerId = crypto.randomUUID();

    let state = await this.loadState();
    const hasHost = Object.values(state.players).some((p) => p.host);
    const host = wantsHost && !hasHost;

    state.players[playerId] = {
      id: playerId,
      name,
      host,
      ready: false,
      peekUsed: false,
    };
    await this.saveState(state);

    server.serializeAttachment({ playerId });
    this.ctx.acceptWebSocket(server);

    server.send(JSON.stringify({
      type: "connected",
      playerId,
      host,
      room: url.pathname.split("/").pop(),
    }));
    this.broadcastLobby(state);

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer): Promise<void> {
    const attachment = ws.deserializeAttachment() as { playerId?: string } | null;
    const playerId = attachment?.playerId;
    if (!playerId || typeof message !== "string") return;

    let data: any;
    try {
      data = JSON.parse(message);
    } catch {
      this.send(ws, { type: "error", message: "Invalid JSON" });
      return;
    }

    let state = await this.loadState();
    const player = state.players[playerId];
    if (!player) return;

    switch (data.type) {
      case "start_game":
        if (!player.host || state.started) return;
        state.started = true;
        state.round = 1;
        state.yellowCount = 0;
        state.cardIndex = 0;
        state.farms = shuffle(["A", "B", "C", "D", "E", "F"]);
        state.deck = makeDeck();
        state.currentFarm = state.farms[0];
        this.resetPlayersForRound(state);
        await this.saveState(state);
        this.broadcast({ type: "game_started", round: 1, farm: state.currentFarm, players: this.publicPlayers(state) });
        await this.revealNextCard(state);
        break;

      case "ready":
        if (!state.started || state.finished || !state.currentCard) return;
        player.ready = true;
        await this.saveState(state);
        this.broadcast({ type: "ready_state", ready: this.readyNames(state), total: Object.keys(state.players).length });
        if (this.allPlayersReady(state)) {
          if (state.yellowCount >= 4) {
            for (const p of Object.values(state.players)) p.ready = false;
            await this.saveState(state);
            this.broadcast({ type: "round_end", round: state.round, farm: state.currentFarm });
          } else {
            for (const p of Object.values(state.players)) p.ready = false;
            await this.saveState(state);
            await this.revealNextCard(state);
          }
        }
        break;

      case "peek":
        if (!state.started || state.finished || player.peekUsed) return;
        if (state.round < 5) {
          player.peekUsed = true;
          await this.saveState(state);
          this.send(ws, { type: "peek_result", farm: state.farms[state.round] });
        } else {
          player.peekUsed = true;
          await this.saveState(state);
          this.send(ws, { type: "peek_result", farm: state.farms[5] });
        }
        break;

      case "round_score":
        if (!state.started || state.finished || typeof data.score !== "number") return;
        player.roundScore = Math.trunc(data.score);
        await this.saveState(state);
        if (Object.values(state.players).every((p) => p.roundScore !== undefined)) {
          this.broadcast({
            type: "round_results",
            round: state.round,
            scores: Object.values(state.players).map((p) => ({ name: p.name, score: p.roundScore })),
          });
          if (state.round >= 5) {
            this.broadcast({ type: "request_final_score" });
          } else {
            state.round += 1;
            state.yellowCount = 0;
            state.currentFarm = state.farms[state.round - 1];
            this.resetPlayersForRound(state);
            await this.saveState(state);
            this.broadcast({ type: "farm_revealed", round: state.round, farm: state.currentFarm });
            await this.revealNextCard(state);
          }
        }
        break;

      case "final_score":
        if (typeof data.score !== "number") return;
        player.finalScore = Math.trunc(data.score);
        await this.saveState(state);
        if (Object.values(state.players).every((p) => p.finalScore !== undefined)) {
          state.finished = true;
          await this.saveState(state);
          const ranking = Object.values(state.players)
            .map((p) => ({ name: p.name, score: p.finalScore as number }))
            .sort((a, b) => b.score - a.score);
          const best = ranking[0]?.score;
          this.broadcast({
            type: "game_finished",
            ranking,
            winners: ranking.filter((p) => p.score === best).map((p) => p.name),
          });
        }
        break;
    }
  }

  async webSocketClose(ws: WebSocket): Promise<void> {
    const attachment = ws.deserializeAttachment() as { playerId?: string } | null;
    const playerId = attachment?.playerId;
    if (!playerId) return;
    const state = await this.loadState();
    delete state.players[playerId];
    await this.saveState(state);
    this.broadcastLobby(state);
  }

  private async revealNextCard(state: RoomState): Promise<void> {
    const card = state.deck[state.cardIndex++];
    if (!card) {
      this.broadcast({ type: "error", message: "Deck exhausted" });
      return;
    }
    state.currentCard = card;
    if (card[4] === 99) state.yellowCount += 1;
    await this.saveState(state);
    this.broadcast({
      type: "road_revealed",
      round: state.round,
      cardIndex: state.cardIndex,
      card,
      yellowCount: state.yellowCount,
    });
  }

  private resetPlayersForRound(state: RoomState): void {
    for (const p of Object.values(state.players)) {
      p.ready = false;
      p.peekUsed = false;
      p.roundScore = undefined;
    }
  }

  private allPlayersReady(state: RoomState): boolean {
    const players = Object.values(state.players);
    return players.length > 0 && players.every((p) => p.ready);
  }

  private readyNames(state: RoomState): string[] {
    return Object.values(state.players).filter((p) => p.ready).map((p) => p.name);
  }

  private publicPlayers(state: RoomState) {
    return Object.values(state.players).map((p) => ({ id: p.id, name: p.name, host: p.host }));
  }

  private broadcastLobby(state: RoomState): void {
    this.broadcast({ type: "lobby", players: this.publicPlayers(state), started: state.started });
  }

  private broadcast(payload: unknown): void {
    const text = JSON.stringify(payload);
    for (const ws of this.ctx.getWebSockets()) {
      try { ws.send(text); } catch { /* disconnected socket */ }
    }
  }

  private send(ws: WebSocket, payload: unknown): void {
    try { ws.send(JSON.stringify(payload)); } catch { /* disconnected socket */ }
  }

  private async loadState(): Promise<RoomState> {
    return (await this.ctx.storage.get<RoomState>("state")) ?? structuredClone(EMPTY_STATE);
  }

  private async saveState(state: RoomState): Promise<void> {
    await this.ctx.storage.put("state", state);
  }
}
