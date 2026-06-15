import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

import { Player } from '../../../../core/models/player.model';
import { PaginationComponent } from '../../../../shared/components/pagination/pagination.component';

@Component({
  selector: 'app-player-table',
  standalone: true,
  imports: [CommonModule, PaginationComponent],
  templateUrl: './player-table.component.html',
})
export class PlayerTableComponent {
  @Input({ required: true }) players: Player[] = [];
  @Input() total = 0;
  @Input() page = 0;
  @Input() pageSize = 25;
  @Input() selectedPlayerId: number | null = null;
  @Input() loading = false;

  @Output() playerSelected = new EventEmitter<Player>();
  @Output() pageChange = new EventEmitter<number>();

  selectPlayer(player: Player): void {
    this.playerSelected.emit(player);
  }
}
