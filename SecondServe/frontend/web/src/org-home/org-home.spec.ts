import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgHome } from './org-home';

describe('OrgHome', () => {
  let component: OrgHome;
  let fixture: ComponentFixture<OrgHome>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrgHome]
    })
      .compileComponents();

    fixture = TestBed.createComponent(OrgHome);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
