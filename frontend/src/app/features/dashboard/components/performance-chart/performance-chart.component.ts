import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnChanges,
  OnDestroy,
  SimpleChanges,
  ViewChild,
} from '@angular/core';
import {
  Chart,
  ChartConfiguration,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Legend,
  Tooltip,
  Filler,
} from 'chart.js';

import { MatchStats } from '../../../../core/models/match-stats.model';

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Legend,
  Tooltip,
  Filler,
);

@Component({
  selector: 'app-performance-chart',
  standalone: true,
  template: `
    <section class="panel">
      <header class="border-b border-border px-3 py-2">
        <h2 class="text-xs font-semibold uppercase tracking-[0.2em] text-text">Performance Trend</h2>
        <p class="font-mono text-2xs text-text-dim">{{ playerLabel || 'Selecciona un jugador' }}</p>
      </header>

      @if (!stats.length) {
        <p class="px-3 py-4 font-mono text-2xs text-text-dim">Sin datos suficientes para graficar.</p>
      } @else {
        <div class="p-3">
          <canvas #chartCanvas height="120"></canvas>
        </div>
      }
    </section>
  `,
})
export class PerformanceChartComponent implements AfterViewInit, OnChanges, OnDestroy {
  @ViewChild('chartCanvas') chartCanvas?: ElementRef<HTMLCanvasElement>;

  @Input({ required: true }) stats: MatchStats[] = [];
  @Input() playerLabel = '';

  private chart?: Chart;

  ngAfterViewInit(): void {
    this.renderChart();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['stats'] && this.chartCanvas) {
      this.renderChart();
    }
  }

  ngOnDestroy(): void {
    this.chart?.destroy();
  }

  private renderChart(): void {
    if (!this.chartCanvas || !this.stats.length) {
      return;
    }

    const ordered = [...this.stats].reverse();
    const labels = ordered.map(
      (row) => row.match_external_id?.toString() ?? row.id.toString(),
    );

    const config: ChartConfiguration<'line'> = {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Kills',
            data: ordered.map((row) => row.kills),
            borderColor: '#6abf8a',
            backgroundColor: 'rgba(106, 191, 138, 0.08)',
            tension: 0.25,
            pointRadius: 2,
            borderWidth: 1.5,
          },
          {
            label: 'ADR',
            data: ordered.map((row) => row.adr),
            borderColor: '#7eb8da',
            backgroundColor: 'rgba(126, 184, 218, 0.06)',
            tension: 0.25,
            pointRadius: 2,
            borderWidth: 1.5,
            yAxisID: 'y1',
          },
          {
            label: 'Rating',
            data: ordered.map((row) => row.rating),
            borderColor: '#c4872e',
            backgroundColor: 'rgba(196, 135, 46, 0.06)',
            tension: 0.25,
            pointRadius: 2,
            borderWidth: 1.5,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            labels: {
              color: '#8b939e',
              font: { family: 'Chakra Petch', size: 10 },
              boxWidth: 10,
            },
          },
          tooltip: {
            backgroundColor: '#1a1f26',
            borderColor: '#2a313c',
            borderWidth: 1,
            titleColor: '#e8eaed',
            bodyColor: '#8b939e',
            titleFont: { family: 'IBM Plex Mono', size: 11 },
            bodyFont: { family: 'IBM Plex Mono', size: 11 },
          },
        },
        scales: {
          x: {
            ticks: { color: '#5c6370', font: { family: 'IBM Plex Mono', size: 9 } },
            grid: { color: '#222831' },
          },
          y: {
            position: 'left',
            ticks: { color: '#5c6370', font: { family: 'IBM Plex Mono', size: 9 } },
            grid: { color: '#2a313c' },
          },
          y1: {
            position: 'right',
            ticks: { color: '#5c6370', font: { family: 'IBM Plex Mono', size: 9 } },
            grid: { drawOnChartArea: false },
          },
        },
      },
    };

    this.chart?.destroy();
    this.chart = new Chart(this.chartCanvas.nativeElement, config);
  }
}
