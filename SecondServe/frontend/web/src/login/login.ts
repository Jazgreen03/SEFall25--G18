import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { getCookie } from '../../utils';
import { AuthService } from '../app/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  loginForm: FormGroup;
  showPassword = false;
  isLoading = false;
  errorMessage = '';
  successMessage = '';

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

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  userType: 'user' | 'organization' | 'driver' = 'user';

  setUserType(type: 'user' | 'organization' | 'driver') {
    this.userType = type;
  }

  /** Fetch CSRF cookie from backend */
  private getCsrfToken(): Promise<void> {
    return this.http
      .get('http://localhost:8000/api/csrf/', { withCredentials: true })
      .toPromise()
      .then(() => console.log('CSRF cookie set'));
  }

  /** Handle form submission */
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

          // First, set the role regardless of what it is
          this.authService.setRole(userRole);

          // Then check if it matches the selected user type for known roles
          const knownRoles = ['user', 'organization', 'driver'];
          if (knownRoles.includes(userRole) && userRole !== this.userType) {
            this.errorMessage = "This account type doesn't match your selection.";
            return;
          }

          // ✅ Redirect based on role
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

  /** Helper to mark all fields as touched */
  private markFormGroupTouched(formGroup: FormGroup) {
    Object.keys(formGroup.controls).forEach(key => {
      formGroup.get(key)?.markAsTouched();
    });
  }

  // Getters for cleaner template usage
  get email() { return this.loginForm.get('email'); }
  get password() { return this.loginForm.get('password'); }
}