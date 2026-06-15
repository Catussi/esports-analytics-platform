import { Component, Input } from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';

import { MatchStats } from '../../../../core/models/match-stats.model';

@Component({
  selector: 'app-match-history',
  standalone: true,
  imports: [CommonModule, DecimalPipe],
  templateUrl: './match-history.component.html',
})
export class MatchHistoryComponent {
  @Input({ required: true }) stats: MatchStats[] = [];
  @Input() total = 0;
  @Input() playerLabel = '';
  @Input() loading = false;
}
