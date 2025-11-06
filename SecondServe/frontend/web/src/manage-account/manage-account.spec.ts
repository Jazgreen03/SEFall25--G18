import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountManagement } from './manage-account';

describe('AccountManagement', () => {
  let component: AccountManagement;
  let fixture: ComponentFixture<AccountManagement>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccountManagement]
    })
      .compileComponents();

    fixture = TestBed.createComponent(AccountManagement);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
