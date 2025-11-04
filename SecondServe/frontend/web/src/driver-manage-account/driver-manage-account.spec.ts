import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DriverAccountManagement } from './driver-manage-account';

describe('ManageAccount', () => {
  let component: DriverAccountManagement;
  let fixture: ComponentFixture<DriverAccountManagement>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DriverAccountManagement],
    }).compileComponents();

    fixture = TestBed.createComponent(DriverAccountManagement);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
