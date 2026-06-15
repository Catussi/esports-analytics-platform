import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';

import { AnalyticsService } from './analytics.service';

describe('AnalyticsService', () => {
  let service: AnalyticsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AnalyticsService, provideHttpClient(), provideHttpClientTesting()],
    });

    service = TestBed.inject(AnalyticsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should post metrics to predict endpoint', () => {
    const payload = {
      kills: 20,
      deaths: 15,
      assists: 5,
      headshots: 10,
      adr: 80,
      kast: 70,
      rating: 1.1,
    };

    service.predict(payload).subscribe((response) => {
      expect(response.cluster_id).toBe(1);
      expect(response.cluster_label).toBe('Entry Fragger');
    });

    const request = httpMock.expectOne('http://localhost:8000/api/v1/analytics/predict');
    expect(request.request.method).toBe('POST');
    request.flush({
      cluster_id: 1,
      cluster_label: 'Entry Fragger',
      analytical_feedback: 'Test feedback',
      confidence_score: 0.9,
      pca_components: [1, 0, -1],
      feature_vector: ['kills'],
    });
  });
});
