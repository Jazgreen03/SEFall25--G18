import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgAccountManagement } from './org-manage-account';

describe('ManageAccount', () => {
  let component: OrgAccountManagement;
  let fixture: ComponentFixture<OrgAccountManagement>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrgAccountManagement],
    }).compileComponents();

    fixture = TestBed.createComponent(OrgAccountManagement);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
