import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { getCookie } from '../../utils';
import { AuthService } from '../app/services/auth.service';

/**
 * Login Component
 * 
 * Handles user authentication with email/password login.
 * Supports multiple user types (user, organization, driver) and role-based redirection.
 * Includes CSRF protection and session management.
 * 
 * @selector app-login
 * @standalone true
 */
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  /** Form group for login credentials */
  loginForm: FormGroup;

  /** Toggle state for password visibility */
  showPassword = false;

  /** Loading state during authentication */
  isLoading = false;

  /** Error message display */
  errorMessage = '';

  /** Success message display */
  successMessage = '';

  /** Selected user type for login */
  userType: 'user' | 'organization' | 'driver' = 'user';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private http: HttpClient,
    private authService: AuthService
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  /** Toggles password field visibility */
  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  /** Sets the user type for login */
  setUserType(type: 'user' | 'organization' | 'driver') {
    this.userType = type;
  }

  /** Fetches CSRF token from backend for secure form submission */
  private getCsrfToken(): Promise<void> {
    return this.http
      .get('http://localhost:8000/api/csrf/', { withCredentials: true })
      .toPromise()
      .then(() => console.log('CSRF cookie set'));
  }

  /** Handles login form submission and authentication */
  async onSubmit() {
    if (!this.loginForm.valid) {
      this.markFormGroupTouched(this.loginForm);
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    // Ensure CSRF cookie exists first
    await this.getCsrfToken();

    const csrfToken = getCookie('csrftoken') || '';
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    });

    const { email, password } = this.loginForm.value;

    this.http.post('http://localhost:8000/user/login/', { email, password }, { headers, withCredentials: true })
      .subscribe({
        next: (res: any) => {
          this.isLoading = false;
          this.successMessage = 'Login successful! Redirecting...';
          console.log('Login response:', res);

          const userRole = res['role'];

          // Set role in auth service for application-wide access
          this.authService.setRole(userRole);

          // Validate role matches selected user type
          const knownRoles = ['user', 'organization', 'driver'];
          if (knownRoles.includes(userRole) && userRole !== this.userType) {
            this.errorMessage = "This account type doesn't match your selection.";
            return;
          }

          // Redirect based on user role
          switch (userRole) {
            case 'user':
              this.router.navigate(['/home']);
              break;
            case 'organization':
              this.router.navigate(['/home']);
              break;
            case 'driver':
              this.router.navigate(['/home']);
              break;
            default:
              this.router.navigate(['/']);
          }
        },
        error: (err) => {
          this.isLoading = false;
          console.error('Login error:', err);
          this.errorMessage = err.error?.message || 'Invalid email or password.';
        }
      });
  }

  /** Marks all form controls as touched to trigger validation display */
  private markFormGroupTouched(formGroup: FormGroup) {
    Object.keys(formGroup.controls).forEach(key => {
      formGroup.get(key)?.markAsTouched();
    });
  }

  // Form control getters for template validation
  get email() { return this.loginForm.get('email'); }
  get password() { return this.loginForm.get('password'); }
}