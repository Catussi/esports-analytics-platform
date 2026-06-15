import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';

import { PlayerService } from './player.service';

describe('PlayerService', () => {
  let service: PlayerService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [PlayerService, provideHttpClient(), provideHttpClientTesting()],
    });

    service = TestBed.inject(PlayerService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should fetch players list', () => {
    service.listPlayers().subscribe((response) => {
      expect(response.total).toBe(1);
      expect(response.items[0].steam_id).toBe('76561198036987787');
    });

    const request = httpMock.expectOne(
      (req) => req.url === 'http://localhost:8000/api/v1/players' && req.params.get('limit') === '50',
    );
    expect(request.request.method).toBe('GET');
    request.flush({
      total: 1,
      items: [
        {
          id: 1,
          steam_id: '76561198036987787',
          nickname: 'Player_7787',
          team: null,
          is_active: true,
          created_at: '2026-01-01T00:00:00Z',
          updated_at: '2026-01-01T00:00:00Z',
        },
      ],
    });
  });
});
