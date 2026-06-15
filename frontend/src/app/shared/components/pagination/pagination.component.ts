import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-pagination',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="flex items-center justify-between border-t border-border px-3 py-2 font-mono text-2xs">
      <button
        type="button"
        class="btn-ghost"
        [disabled]="page <= 0 || disabled"
        (click)="changePage(page - 1)"
      >
        Anterior
      </button>

      <span class="text-text-muted">
        Pág {{ page + 1 }} / {{ totalPages || 1 }}
        <span class="text-text-dim">· {{ total }} total</span>
      </span>

      <button
        type="button"
        class="btn-ghost"
        [disabled]="page >= totalPages - 1 || disabled"
        (click)="changePage(page + 1)"
      >
        Siguiente
      </button>
    </div>
  `,
})
export class PaginationComponent {
  @Input({ required: true }) page = 0;
  @Input({ required: true }) pageSize = 25;
  @Input({ required: true }) total = 0;
  @Input() disabled = false;

  @Output() pageChange = new EventEmitter<number>();

  get totalPages(): number {
    return Math.ceil(this.total / this.pageSize);
  }

  changePage(nextPage: number): void {
    if (nextPage < 0 || nextPage >= this.totalPages) {
      return;
    }

    this.pageChange.emit(nextPage);
  }
}
