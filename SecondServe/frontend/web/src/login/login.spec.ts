import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';

import { Login } from './login';
import { AuthService } from '../app/services/auth.service';

// Mock the getCookie function
const mockGetCookie = jasmine.createSpy('getCookie').and.returnValue('mock-csrf-token');

describe('LoginComponent', () => {
  let component: Login;
  let fixture: ComponentFixture<Login>;
  let authService: AuthService;
  let router: Router;
  let httpClient: HttpClient;

  const mockRouter = {
    navigate: jasmine.createSpy('navigate')
  };

  const mockAuthService = {
    setRole: jasmine.createSpy('setRole')
  };

  const mockHttpClient = {
    get: jasmine.createSpy('get').and.returnValue(of({})),
    post: jasmine.createSpy('post')
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        ReactiveFormsModule,
        Login
      ],
      providers: [
        { provide: Router, useValue: mockRouter },
        { provide: AuthService, useValue: mockAuthService },
        { provide: HttpClient, useValue: mockHttpClient }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(Login);
    component = fixture.componentInstance;
    authService = TestBed.inject(AuthService);
    router = TestBed.inject(Router);
    httpClient = TestBed.inject(HttpClient);

    // Reset all spies
    mockRouter.navigate.calls.reset();
    mockAuthService.setRole.calls.reset();
    mockHttpClient.get.calls.reset();
    mockHttpClient.post.calls.reset();
    mockGetCookie.calls.reset();

    // Mock the getCookie function in the component's scope
    (component as any).getCookie = mockGetCookie;
  });

  describe('Component Initialization', () => {
    it('should create', () => {
      expect(component).toBeTruthy();
    });

    it('should initialize form with empty values', () => {
      expect(component.loginForm.value).toEqual({ email: '', password: '' });
    });
  });

  describe('Form Validation', () => {
    it('should mark form as invalid when empty', () => {
      expect(component.loginForm.valid).toBeFalse();
    });

    it('should validate email format', () => {
      const email = component.loginForm.controls['email'];
      email.setValue('invalid');
      expect(email.valid).toBeFalse();

      email.setValue('test@example.com');
      expect(email.valid).toBeTrue();
    });
  });

  describe('User Interactions', () => {
    it('should toggle password visibility', () => {
      component.togglePasswordVisibility();
      expect(component.showPassword).toBeTrue();
    });

    it('should set user type correctly', () => {
      component.setUserType('organization');
      expect(component.userType).toBe('organization');
    });
  });

  describe('Form Submission', () => {
    beforeEach(() => {
      component.loginForm.setValue({
        email: 'test@example.com',
        password: 'password123'
      });
    });

    it('should not submit when form is invalid', () => {
      component.loginForm.controls['email'].setValue('');
      component.onSubmit();
      expect(component.isLoading).toBeFalse();
    });

    it('should handle successful login for user role', fakeAsync(() => {
      component.userType = 'user';
      mockHttpClient.post.and.returnValue(of({ role: 'user' }));

      component.onSubmit();
      tick();

      expect(mockHttpClient.get).toHaveBeenCalledWith('http://localhost:8000/api/csrf/', { withCredentials: true });
      expect(mockHttpClient.post).toHaveBeenCalledWith(
        'http://localhost:8000/user/login/',
        { email: 'test@example.com', password: 'password123' },
        jasmine.any(Object) // headers object
      );
      expect(component.isLoading).toBeFalse();
      expect(component.successMessage).toBe('Login successful! Redirecting...');
      expect(authService.setRole).toHaveBeenCalledWith('user');
      expect(router.navigate).toHaveBeenCalledWith(['/home']);
    }));

    it('should handle successful login for organization role', fakeAsync(() => {
      component.userType = 'organization';
      mockHttpClient.post.and.returnValue(of({ role: 'organization' }));

      component.onSubmit();
      tick();

      expect(authService.setRole).toHaveBeenCalledWith('organization');
      expect(router.navigate).toHaveBeenCalledWith(['/home']);
    }));

    it('should handle successful login for driver role', fakeAsync(() => {
      component.userType = 'driver';
      mockHttpClient.post.and.returnValue(of({ role: 'driver' }));

      component.onSubmit();
      tick();

      expect(authService.setRole).toHaveBeenCalledWith('driver');
      expect(router.navigate).toHaveBeenCalledWith(['/home']);
    }));

    it('should show error when role does not match selected user type', fakeAsync(() => {
      component.userType = 'user';
      mockHttpClient.post.and.returnValue(of({ role: 'organization' }));

      component.onSubmit();
      tick();

      expect(component.errorMessage).toBe("This account type doesn't match your selection.");
      // Now expect setRole to BE called (since it happens before the check)
      expect(authService.setRole).toHaveBeenCalledWith('organization');
      expect(router.navigate).not.toHaveBeenCalled();
    }));

    it('should handle login error with server message', fakeAsync(() => {
      const errorResponse = { error: { message: 'Invalid credentials' } };
      mockHttpClient.post.and.returnValue(throwError(() => errorResponse));

      component.onSubmit();
      tick();

      expect(component.errorMessage).toBe('Invalid credentials');
    }));

    it('should handle login error with default message', fakeAsync(() => {
      mockHttpClient.post.and.returnValue(throwError(() => ({})));

      component.onSubmit();
      tick();

      expect(component.errorMessage).toBe('Invalid email or password.');
    }));

    it('should handle unknown role by navigating to root', fakeAsync(() => {
      component.userType = 'user';
      mockHttpClient.post.and.returnValue(of({ role: 'unknown_role' }));

      component.onSubmit();
      tick();

      expect(authService.setRole).toHaveBeenCalledWith('unknown_role');
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    }));
  });

  describe('Form Control Getters', () => {
    it('should provide email control getter', () => {
      expect(component.email).toBe(component.loginForm.get('email'));
    });
  });
});