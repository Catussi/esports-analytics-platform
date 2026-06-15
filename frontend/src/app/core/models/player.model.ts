export interface Player {
  id: number;
  steam_id: string;
  nickname: string | null;
  team: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface PlayerListResponse {
  total: number;
  items: Player[];
}

export interface PlayerUpdateRequest {
  nickname?: string | null;
  team?: string | null;
  is_active?: boolean;
}
