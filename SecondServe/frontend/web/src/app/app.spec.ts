import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { App } from './app';
import { Router, NavigationEnd } from '@angular/router';
import { Subject } from 'rxjs';

describe('App', () => {
  let routerEvents$: Subject<any>;
  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    routerEvents$ = new Subject<any>();
    routerSpy = jasmine.createSpyObj('Router', ['navigate'], { events: routerEvents$ });

    await TestBed.configureTestingModule({
      imports: [App],
      providers: [
        { provide: Router, useValue: routerSpy }
      ]
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  // Remove or update this test based on your actual template content
  // it('should render title', () => {
  //   const fixture = TestBed.createComponent(App);
  //   fixture.detectChanges();
  //   const compiled = fixture.nativeElement as HTMLElement;
  //   expect(compiled.querySelector('h1')?.textContent).toContain('Hello, web');
  // });

  // Add a test that checks for actual content in your template
  it('should contain router outlet', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('router-outlet')).toBeTruthy();
  });

  it('should navigate to /login on onLogin()', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    app.onLogin();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/login']);
  });

  it('should return true from showLayout() for non-login routes', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    app.currentRoute = '/home';
    expect(app.showLayout()).toBeTrue();
  });

  it('should return false from showLayout() for /login route', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    app.currentRoute = '/login';
    expect(app.showLayout()).toBeFalse();
  });

  it('should update currentRoute on NavigationEnd', fakeAsync(() => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    routerEvents$.next(new NavigationEnd(1, '/home', '/home'));
    tick();
    expect(app.currentRoute).toBe('/home');
  }));

  it('should handle multiple NavigationEnd events', fakeAsync(() => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    routerEvents$.next(new NavigationEnd(1, '/home', '/home'));
    tick();
    expect(app.currentRoute).toBe('/home');

    routerEvents$.next(new NavigationEnd(2, '/about', '/about'));
    tick();
    expect(app.currentRoute).toBe('/about');
  }));

  it('should not change currentRoute for non-NavigationEnd events', fakeAsync(() => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    routerEvents$.next({ type: 'otherEvent', url: '/ignored' });
    tick();
    expect(app.currentRoute).toBe('');
  }));

  it('should have default title signal value', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app['title']()).toBe('web');
  });
});