import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { MatchStats } from '../../../../core/models/match-stats.model';
import { PredictionResponse } from '../../../../core/models/prediction.model';

@Component({
  selector: 'app-prediction-panel',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './prediction-panel.component.html',
})
export class PredictionPanelComponent implements OnChanges {
  @Input() latestStats: MatchStats | null = null;
  @Input() prediction: PredictionResponse | null = null;
  @Input() loading = false;
  @Input() error: string | null = null;

  @Output() predict = new EventEmitter<{
    kills: number;
    deaths: number;
    assists: number;
    headshots: number;
    adr: number;
    kast: number;
    rating: number;
  }>();

  private readonly formBuilder = new FormBuilder();

  readonly metricsForm = this.formBuilder.nonNullable.group({
    kills: [0, [Validators.required, Validators.min(0)]],
    deaths: [0, [Validators.required, Validators.min(0)]],
    assists: [0, [Validators.required, Validators.min(0)]],
    headshots: [0, [Validators.required, Validators.min(0)]],
    adr: [0, [Validators.required, Validators.min(0)]],
    kast: [0, [Validators.required, Validators.min(0), Validators.max(100)]],
    rating: [1, [Validators.required, Validators.min(0)]],
  });

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['latestStats']?.currentValue) {
      this.patchFromStats(changes['latestStats'].currentValue as MatchStats);
    }
  }

  patchFromStats(stats: MatchStats): void {
    this.metricsForm.patchValue({
      kills: stats.kills,
      deaths: stats.deaths,
      assists: stats.assists,
      headshots: stats.headshots,
      adr: stats.adr,
      kast: stats.kast,
      rating: stats.rating,
    });
  }

  submit(): void {
    if (this.metricsForm.invalid) {
      this.metricsForm.markAllAsTouched();
      return;
    }

    this.predict.emit(this.metricsForm.getRawValue());
  }
}
