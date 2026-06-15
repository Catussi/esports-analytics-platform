import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaginationComponent } from './pagination.component';

describe('PaginationComponent', () => {
  let component: PaginationComponent;
  let fixture: ComponentFixture<PaginationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PaginationComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(PaginationComponent);
    component = fixture.componentInstance;
    component.page = 0;
    component.pageSize = 25;
    component.total = 100;
    fixture.detectChanges();
  });

  it('should calculate total pages', () => {
    expect(component.totalPages).toBe(4);
  });

  it('should emit next page', () => {
    const spy = spyOn(component.pageChange, 'emit');
    component.changePage(1);
    expect(spy).toHaveBeenCalledWith(1);
  });

  it('should not emit invalid page', () => {
    const spy = spyOn(component.pageChange, 'emit');
    component.changePage(-1);
    component.changePage(99);
    expect(spy).not.toHaveBeenCalled();
  });
});
