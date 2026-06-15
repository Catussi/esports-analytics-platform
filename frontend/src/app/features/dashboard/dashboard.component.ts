import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

import { environment } from '../../../environments/environment';
import { MatchStats } from '../../core/models/match-stats.model';
import { Player } from '../../core/models/player.model';
import { PredictionResponse } from '../../core/models/prediction.model';
import { AnalyticsService } from '../../core/services/analytics.service';
import { PlayerService } from '../../core/services/player.service';
import { MatchHistoryComponent } from './components/match-history/match-history.component';
import { PerformanceChartComponent } from './components/performance-chart/performance-chart.component';
import { PlayerTableComponent } from './components/player-table/player-table.component';
import { PredictionPanelComponent } from './components/prediction-panel/prediction-panel.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    PlayerTableComponent,
    PredictionPanelComponent,
    MatchHistoryComponent,
    PerformanceChartComponent,
  ],
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  private readonly playerService = inject(PlayerService);
  private readonly analyticsService = inject(AnalyticsService);
  private readonly http = inject(HttpClient);

  readonly pageSize = 25;
  readonly statsPageSize = 20;

  readonly players = signal<Player[]>([]);
  readonly playersTotal = signal(0);
  readonly playersPage = signal(0);
  readonly playersLoading = signal(true);

  readonly selectedPlayer = signal<Player | null>(null);
  readonly matchStats = signal<MatchStats[]>([]);
  readonly matchStatsTotal = signal(0);
  readonly statsLoading = signal(false);

  readonly prediction = signal<PredictionResponse | null>(null);
  readonly predictionLoading = signal(false);
  readonly predictionError = signal<string | null>(null);

  readonly apiOnline = signal(false);

  ngOnInit(): void {
    this.checkApiHealth();
    this.loadPlayers(0, true);
  }

  private checkApiHealth(): void {
    this.http.get<{ status: string }>(environment.apiHealthUrl).subscribe({
      next: () => this.apiOnline.set(true),
      error: () => this.apiOnline.set(false),
    });
  }

  loadPlayers(page: number, selectFirst = false): void {
    this.playersLoading.set(true);
    this.playersPage.set(page);

    const skip = page * this.pageSize;
    this.playerService.listPlayers(skip, this.pageSize).subscribe({
      next: (response) => {
        this.players.set(response.items);
        this.playersTotal.set(response.total);
        this.playersLoading.set(false);

        const selected = this.selectedPlayer();
        const selectedStillVisible = selected
          ? response.items.some((player) => player.id === selected.id)
          : false;

        if (selectFirst && response.items.length > 0) {
          this.onPlayerSelected(response.items[0]);
        } else if (!selectedStillVisible && response.items.length > 0) {
          this.onPlayerSelected(response.items[0]);
        } else if (!response.items.length) {
          this.selectedPlayer.set(null);
          this.matchStats.set([]);
        }
      },
      error: () => this.playersLoading.set(false),
    });
  }

  onPlayersPageChange(page: number): void {
    this.loadPlayers(page);
  }

  onPlayerSelected(player: Player): void {
    this.selectedPlayer.set(player);
    this.prediction.set(null);
    this.predictionError.set(null);
    this.loadPlayerStats(player.id);
  }

  private loadPlayerStats(playerId: number): void {
    this.statsLoading.set(true);
    this.playerService.getPlayerStats(playerId, 0, this.statsPageSize).subscribe({
      next: (response) => {
        this.matchStats.set(response.items);
        this.matchStatsTotal.set(response.total);
        this.statsLoading.set(false);
      },
      error: () => {
        this.matchStats.set([]);
        this.matchStatsTotal.set(0);
        this.statsLoading.set(false);
      },
    });
  }

  onPredict(metrics: {
    kills: number;
    deaths: number;
    assists: number;
    headshots: number;
    adr: number;
    kast: number;
    rating: number;
  }): void {
    this.predictionLoading.set(true);
    this.predictionError.set(null);

    this.analyticsService.predict(metrics).subscribe({
      next: (response) => {
        this.prediction.set(response);
        this.predictionLoading.set(false);
      },
      error: () => {
        this.predictionError.set('No se pudo ejecutar la inferencia. Verifica que la API esté activa.');
        this.predictionLoading.set(false);
      },
    });
  }

  selectedPlayerLabel(): string {
    const player = this.selectedPlayer();
    if (!player) {
      return '';
    }

    return player.nickname || player.steam_id;
  }

  latestStats(): MatchStats | null {
    const stats = this.matchStats();
    return stats.length > 0 ? stats[0] : null;
  }
}
