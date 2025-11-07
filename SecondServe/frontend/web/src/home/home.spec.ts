import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { Home } from './home';
import { AuthService } from '../app/services/auth.service';
import { Router } from '@angular/router';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ViewContainerRef } from '@angular/core';

describe('Home Component', () => {
  let component: Home;
  let fixture: ComponentFixture<Home>;
  let authService: jasmine.SpyObj<AuthService>;
  let router: jasmine.SpyObj<Router>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    const authSpy = jasmine.createSpyObj('AuthService', ['getRole']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      imports: [Home, HttpClientTestingModule],
      providers: [
        { provide: AuthService, useValue: authSpy },
        { provide: Router, useValue: routerSpy },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(Home);
    component = fixture.componentInstance;
    authService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    router = TestBed.inject(Router) as jasmine.SpyObj<Router>;
    httpMock = TestBed.inject(HttpTestingController);

    // Spy dynamicContent to avoid TypeScript issues with actual components
    component.dynamicContent = {
      createComponent: jasmine.createSpy('createComponent'),
      clear: jasmine.createSpy('clear'),
    } as unknown as ViewContainerRef;
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should get role from AuthService on init', () => {
    authService.getRole.and.returnValue('user');
    component.ngOnInit();
    expect(component['role']).toBe('user');
  });

  it('should navigate to / if no role on AfterViewInit', () => {
    component['role'] = null;
    component.ngAfterViewInit();
    expect(router.navigate).toHaveBeenCalledWith(['/']);
  });

  it('should load UserHome if role is user', fakeAsync(() => {
    component['role'] = 'user';
    component.ngAfterViewInit();

    const req = httpMock.expectOne('http://localhost:8000/user/info');
    req.flush({});

    tick();
    expect(component.dynamicContent.createComponent).toHaveBeenCalledWith(jasmine.any(Function));
  }));

  it('should load OrgHome if role is organization', fakeAsync(() => {
    component['role'] = 'organization';
    component.ngAfterViewInit();

    const req = httpMock.expectOne('http://localhost:8000/user/info');
    req.flush({});

    tick();
    expect(component.dynamicContent.createComponent).toHaveBeenCalledWith(jasmine.any(Function));
  }));

  it('should load DriverHome if role is driver', fakeAsync(() => {
    component['role'] = 'driver';
    component.ngAfterViewInit();

    const req = httpMock.expectOne('http://localhost:8000/user/info');
    req.flush({});

    tick();
    expect(component.dynamicContent.createComponent).toHaveBeenCalledWith(jasmine.any(Function));
  }));

  it('should navigate to / if role is unknown', fakeAsync(() => {
    component['role'] = 'unknown' as any; // cast to bypass TS type
    component.ngAfterViewInit();

    const req = httpMock.expectOne('http://localhost:8000/user/info');
    req.flush({});

    tick();
    expect(router.navigate).toHaveBeenCalledWith(['/']);
  }));

  it('should navigate to / if HTTP request fails', fakeAsync(() => {
    component['role'] = 'user';
    component.ngAfterViewInit();

    const req = httpMock.expectOne('http://localhost:8000/user/info');
    req.error(new ErrorEvent('Network error'));

    tick();
    expect(router.navigate).toHaveBeenCalledWith(['/']);
  }));
});
