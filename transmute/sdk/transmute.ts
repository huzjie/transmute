// TypeScript SDK（fetch，零依赖）
export interface Health { status: string; service: string }
export interface Migration { id: string; status: string; summary: Record<string, number> }

export class TransmuteClient {
  constructor(private baseUrl = "http://127.0.0.1:8000") {}

  async health(): Promise<Health> {
    const r = await fetch(`${this.baseUrl}/health`);
    return r.json();
  }

  async createMigration(config = "config.yaml"): Promise<Migration> {
    const r = await fetch(`${this.baseUrl}/v1/migrations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ config }),
    });
    return r.json();
  }

  async getMigration(id: string): Promise<Migration> {
    const r = await fetch(`${this.baseUrl}/v1/migrations/${id}`);
    return r.json();
  }
}
