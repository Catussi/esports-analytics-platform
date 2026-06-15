import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { MatchStatsListResponse } from '../models/match-stats.model';
import { Player, PlayerListResponse } from '../models/player.model';

@Injectable({ providedIn: 'root' })
export class PlayerService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/players`;

  listPlayers(skip = 0, limit = 50): Observable<PlayerListResponse> {
    const params = new HttpParams()
      .set('skip', skip)
      .set('limit', limit);

    return this.http.get<PlayerListResponse>(this.baseUrl, { params });
  }

  getPlayer(playerId: number): Observable<Player> {
    return this.http.get<Player>(`${this.baseUrl}/${playerId}`);
  }

  getPlayerStats(playerId: number, skip = 0, limit = 20): Observable<MatchStatsListResponse> {
    const params = new HttpParams()
      .set('skip', skip)
      .set('limit', limit);

    return this.http.get<MatchStatsListResponse>(`${this.baseUrl}/${playerId}/stats`, { params });
  }
}
