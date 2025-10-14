import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Component } from '@angular/core';
import 'zone.js';

@Component({
  selector: 'app-test',
  template: '<p>Test works!</p>',
  standalone: true, // mark as standalone
})
class TestComponent {}

describe('TestComponent', () => {
  let component: TestComponent;
  let fixture: ComponentFixture<TestComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      // Standalone components go in imports, not declarations
      imports: [TestComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(TestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
