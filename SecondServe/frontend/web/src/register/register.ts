import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { getCookie } from '../../utils';

/**
 * Registration Component
 * 
 * A multi-step registration form that handles user registration for different account types:
 * - Individual users
 * - Business/organization accounts  
 * - Driver accounts
 * 
 * Features:
 * - Two-step form process (credentials → details)
 * - Real-time form validation
 * - CSRF protection for API calls
 * - Automatic redirect on success
 * - User type-specific form fields
 * 
 * @selector app-register
 * @standalone true
 */
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class Register {
  /** Current step in the multi-step form (1 = credentials, 2 = details) */
  currentStep = 1;

  /** Selected user type for registration */
  userType: 'individual' | 'business' | 'driver' = 'individual';

  /** Form group for step 1 - email and password credentials */
  registerForm: FormGroup;

  /** Form group for step 2 - additional user details */
  detailsForm: FormGroup;

  /** Toggle state for password visibility */
  showPassword = false;

  /** Loading state during form submission */
  isLoading = false;

  /** Error message display for registration failures */
  errorMessage = '';

  /** Success message display for successful registration */
  successMessage = '';

  /**
   * Component constructor
   * @param fb FormBuilder service for creating reactive forms
   * @param router Router service for navigation
   * @param http HttpClient service for API calls
   */
  constructor(
    private fb: FormBuilder,
    private router: Router,
    private http: HttpClient
  ) {
    // Step 1 form: email and password with validation
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validator: this.passwordsMatchValidator });

    // Step 2 form: additional details with validation
    this.detailsForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      address: ['', [Validators.required, Validators.minLength(5)]],
      businessType: ['', [Validators.required]]
    });
  }

  /**
   * Custom validator to ensure password and confirm password fields match
   * @param form FormGroup containing password and confirmPassword controls
   * @returns Validation error object or null if valid
   */
  private passwordsMatchValidator(form: FormGroup) {
    const pass = form.get('password')?.value;
    const confirm = form.get('confirmPassword')?.value;
    return pass === confirm ? null : { mismatch: true };
  }

  /**
   * Sets the user type for registration
   * @param type The type of user account being created
   */
  setUserType(type: 'individual' | 'business' | 'driver') {
    this.userType = type;
  }

  /**
   * Toggles password field visibility between text and password types
   */
  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  /**
   * Validates step 1 form and advances to step 2 if valid
   * Shows validation errors if form is invalid
   */
  goToNextStep() {
    if (this.registerForm.valid) {
      this.currentStep = 2;
      this.errorMessage = '';
    } else {
      this.markFormGroupTouched(this.registerForm);
    }
  }

  /**
   * Fetches CSRF token from backend for form submission security
   * @returns Promise that resolves when CSRF token is set
   */
  private getCsrfToken(): Promise<void> {
    return this.http.get('http://localhost:8000/api/csrf/', { withCredentials: true })
      .toPromise()
      .then(() => console.log('CSRF cookie set'));
  }

  /**
   * Handles final form submission
   * - Validates step 2 form
   * - Fetches CSRF token
   * - Maps user types to backend roles
   * - Sends registration payload to API
   * - Handles success/error responses
   */
  async onSubmitFinal() {
    // Validate step 2 form before submission
    if (!this.detailsForm.valid) {
      this.markFormGroupTouched(this.detailsForm);
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // Ensure CSRF cookie exists for secure form submission
    await this.getCsrfToken();

    const baseData = this.registerForm.value;
    const extraData = this.detailsForm.value;

    // Map frontend user types to backend role values
    let mappedUserType = '';
    switch (this.userType) {
      case 'individual':
        mappedUserType = 'user';
        break;
      case 'business':
        mappedUserType = 'organization';
        break;
      case 'driver':
        mappedUserType = 'driver';
        break;
      default:
        mappedUserType = 'user';  // fallback to individual user
    }

    // Construct registration payload
    const payload = {
      email: baseData.email,
      password: baseData.password,
      role: mappedUserType,
      ...extraData
    };

    // Get CSRF token for secure request
    const csrfToken = getCookie('csrftoken') || '';
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    });

    // Submit registration to backend API
    this.http.post('http://localhost:8000/user/create/', payload, { headers, withCredentials: true })
      .subscribe({
        next: (res: any) => {
          this.isLoading = false;
          this.successMessage = 'Registration successful! Redirecting...';
          // Redirect to login after successful registration
          setTimeout(() => this.router.navigate(['/login']), 1500);
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = err.error?.message || 'Registration failed.';
        }
      });
  }

  /**
   * Returns to the previous step in the multi-step form
   */
  goBack() {
    this.currentStep = 1;
  }

  /**
   * Marks all controls in a form group as touched to trigger validation display
   * @param formGroup The form group to mark as touched
   */
  private markFormGroupTouched(formGroup: FormGroup) {
    Object.keys(formGroup.controls).forEach(key => {
      formGroup.get(key)?.markAsTouched();
    });
  }

  // STEP 1 FORM GETTERS - Provides easy access to form controls for validation

  /** Gets email form control for validation messages */
  get email() { return this.registerForm.get('email'); }

  /** Gets password form control for validation messages */
  get password() { return this.registerForm.get('password'); }

  /** Gets confirmPassword form control for validation messages */
  get confirmPassword() { return this.registerForm.get('confirmPassword'); }

  // STEP 2 FORM GETTERS - Provides easy access to form controls for validation

  /** Gets name form control for validation messages */
  get name() { return this.detailsForm.get('name'); }

  /** Gets address form control for validation messages */
  get address() { return this.detailsForm.get('address'); }

  /** Gets businessType form control for validation messages */
  get businessType() { return this.detailsForm.get('businessType'); }
}