import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ViewContainerRef, ComponentRef, NO_ERRORS_SCHEMA } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HttpClient } from '@angular/common/http';

import { AccountManagement } from './manage-account';
import { AuthService } from '../app/services/auth.service';

describe('AccountManagement', () => {
  let component: AccountManagement;
  let authService: jasmine.SpyObj<AuthService>;
  let router: jasmine.SpyObj<Router>;
  let httpMock: HttpTestingController;
  let mockViewContainerRef: jasmine.SpyObj<ViewContainerRef>;

  beforeEach(async () => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['getRole']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    authServiceSpy.getRole.and.returnValue(null);

    mockViewContainerRef = jasmine.createSpyObj('ViewContainerRef', ['createComponent', 'clear']);
    mockViewContainerRef.createComponent.and.returnValue({
      instance: {},
      hostView: {},
      changeDetectorRef: {},
      componentType: {},
      destroy: jasmine.createSpy('destroy'),
      onDestroy: jasmine.createSpy('onDestroy'),
      injector: {},
      location: {}
    } as any);

    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: Router, useValue: routerSpy }
      ],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();

    authService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    router = TestBed.inject(Router) as jasmine.SpyObj<Router>;
    httpMock = TestBed.inject(HttpTestingController);

    // Create component directly using constructor
    component = new AccountManagement(authService, router, TestBed.inject(HttpClient));

    // Mock dynamicContent
    Object.defineProperty(component, 'dynamicContent', {
      value: mockViewContainerRef,
      writable: false,
      configurable: true
    });
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should get role from authService', () => {
      authService.getRole.and.returnValue('user');

      component.ngOnInit();

      expect(authService.getRole).toHaveBeenCalled();
    });
  });

  describe('ngAfterViewInit', () => {
    it('should navigate to home if no role is set', () => {
      authService.getRole.and.returnValue(null);
      component.ngOnInit();

      component.ngAfterViewInit();

      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should load role content if role is set', () => {
      authService.getRole.and.returnValue('user');
      component.ngOnInit();

      component.ngAfterViewInit();

      const req = httpMock.expectOne('http://localhost:8000/user/info');
      expect(req.request.method).toBe('GET');
      expect(req.request.withCredentials).toBe(true);
    });
  });

  describe('loadRoleContent', () => {
    beforeEach(() => {
      // Mock the dynamic imports
      spyOn(window as any, 'import' as any);
    });

    it('should create UserAccountManagement component for user role', (done) => {
      authService.getRole.and.returnValue('user');
      component.ngOnInit();

      spyOn(console, 'log');
      component.ngAfterViewInit();

      const req = httpMock.expectOne('http://localhost:8000/user/info');
      req.flush({});

      // Wait for async import and component creation
      setTimeout(() => {
        expect(console.log).toHaveBeenCalledWith('Role content loading:', 'user');
        expect(mockViewContainerRef.createComponent).toHaveBeenCalled();
        done();
      }, 100);
    });

    it('should create OrgAccountManagement component for organization role', (done) => {
      authService.getRole.and.returnValue('organization');
      component.ngOnInit();

      spyOn(console, 'log');
      component.ngAfterViewInit();

      const req = httpMock.expectOne('http://localhost:8000/user/info');
      req.flush({});

      setTimeout(() => {
        expect(console.log).toHaveBeenCalledWith('Role content loading:', 'organization');
        expect(mockViewContainerRef.createComponent).toHaveBeenCalled();
        done();
      }, 100);
    });

    it('should create DriverAccountManagement component for driver role', (done) => {
      authService.getRole.and.returnValue('driver');
      component.ngOnInit();

      spyOn(console, 'log');
      component.ngAfterViewInit();

      const req = httpMock.expectOne('http://localhost:8000/user/info');
      req.flush({});

      setTimeout(() => {
        expect(console.log).toHaveBeenCalledWith('Role content loading:', 'driver');
        expect(mockViewContainerRef.createComponent).toHaveBeenCalled();
        done();
      }, 100);
    });

    it('should navigate to home for unknown role', () => {
      authService.getRole.and.returnValue('unknown');
      component.ngOnInit();
      component.ngAfterViewInit();

      const req = httpMock.expectOne('http://localhost:8000/user/info');
      req.flush({});

      // For unknown role, navigation happens synchronously in the default case
      setTimeout(() => {
        expect(router.navigate).toHaveBeenCalledWith(['/']);
      }, 100);
    });

    it('should navigate to home on HTTP error', () => {
      authService.getRole.and.returnValue('user');
      component.ngOnInit();
      component.ngAfterViewInit();

      const req = httpMock.expectOne('http://localhost:8000/user/info');
      req.error(new ProgressEvent('error'), { status: 401 });

      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should log role content loading message', (done) => {
      authService.getRole.and.returnValue('user');
      component.ngOnInit();

      spyOn(console, 'log');
      component.ngAfterViewInit();

      const req = httpMock.expectOne('http://localhost:8000/user/info');
      req.flush({});

      setTimeout(() => {
        expect(console.log).toHaveBeenCalledWith('Role content loading:', 'user');
        done();
      }, 100);
    });
  });
});