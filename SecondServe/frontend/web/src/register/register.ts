import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { getCookie } from '../../utils';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class Register {
  currentStep = 1;
  userType: 'individual' | 'business' | 'driver' = 'individual';

  registerForm: FormGroup;
  detailsForm: FormGroup;

  showPassword = false;
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private http: HttpClient
  ) {
    // Step 1 form: email/password
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validator: this.passwordsMatchValidator });

    // Step 2 form: additional details
    this.detailsForm = this.fb.group({
      name: [''],
      address: [''],
      businessType: ['']
    });
  }

  private passwordsMatchValidator(form: FormGroup) {
    const pass = form.get('password')?.value;
    const confirm = form.get('confirmPassword')?.value;
    return pass === confirm ? null : { mismatch: true };
  }

  setUserType(type: 'individual' | 'business' | 'driver') {
    this.userType = type;
  }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  /** Step 1 submit: go to details step if valid */
  goToNextStep() {
    if (this.registerForm.valid) {
      this.currentStep = 2;
      this.errorMessage = '';
    } else {
      this.markFormGroupTouched(this.registerForm);
    }
  }

  /** Fetch CSRF cookie from backend */
  private getCsrfToken(): Promise<void> {
    return this.http.get('http://localhost:8000/api/csrf/', { withCredentials: true })
      .toPromise()
      .then(() => console.log('CSRF cookie set'));
  }

  /** Step 2 submit: send registration payload to API */
  async onSubmitFinal() {
    if (!this.detailsForm.valid) {
      this.markFormGroupTouched(this.detailsForm);
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // Ensure CSRF cookie exists
    await this.getCsrfToken();

    const baseData = this.registerForm.value;
    const extraData = this.detailsForm.value;

    const payload = {
      username: baseData.email,
      password: baseData.password,
      user_type: this.userType,
      ...extraData
    };

    const csrfToken = getCookie('csrftoken') || '';
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',      // <--- Explicitly tell Django it's JSON
      'Accept': 'application/json'
    });

    this.http.post('http://localhost:8000/user/create/', payload, { headers, withCredentials: true })
      .subscribe({
        next: (res: any) => {
          this.isLoading = false;
          this.successMessage = 'Registration successful! Redirecting...';
          setTimeout(() => this.router.navigate(['/login']), 1500);
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = err.error?.message || 'Registration failed.';
        }
      });
  }

  /** Go back to previous step */
  goBack() {
    this.currentStep = 1;
  }

  /** Mark all controls as touched to show validation errors */
  private markFormGroupTouched(formGroup: FormGroup) {
    Object.keys(formGroup.controls).forEach(key => {
      formGroup.get(key)?.markAsTouched();
    });
  }

  // Step 1 getters
  get email() { return this.registerForm.get('email'); }
  get password() { return this.registerForm.get('password'); }
  get confirmPassword() { return this.registerForm.get('confirmPassword'); }

  // Step 2 getters
  get name() { return this.detailsForm.get('name'); }
  get address() { return this.detailsForm.get('address'); }
  get businessType() { return this.detailsForm.get('businessType'); }
}
