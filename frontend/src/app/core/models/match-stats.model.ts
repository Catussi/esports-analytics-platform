export interface MatchStats {
  id: number;
  player_id: number;
  map_name: string;
  team_side: string | null;
  match_external_id: number | null;
  kills: number;
  deaths: number;
  assists: number;
  headshots: number;
  adr: number;
  kast: number;
  rating: number;
  flank_kills: number;
  avg_kill_distance: number | null;
  time_alive: number | null;
  travelled_distance: number | null;
  played_at: string | null;
  created_at: string;
}

export interface MatchStatsListResponse {
  total: number;
  items: MatchStats[];
}
