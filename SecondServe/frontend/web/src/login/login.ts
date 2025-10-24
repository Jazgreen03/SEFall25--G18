
// login.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  loginForm: FormGroup;
  userType: 'individual' | 'business' = 'individual';
  showPassword = false;
  isLoading = false;
  errorMessage = '';
  obj: any
  data: any

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private http: HttpClient
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  setUserType(type: 'individual' | 'business') {
    this.userType = type;
    this.errorMessage = '';
  }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.isLoading = true;
      this.errorMessage = '';

      // Simulate API call
      setTimeout(() => {
        const { email, password } = this.loginForm.value;


        // Mock authentication logic
        if (email && password.length >= 6) {
          // // Navigate based on user type
          // if (this.userType === 'individual') {
          //   this.router.navigate(['/dashboard/individual']);
          // } else {
          //   this.router.navigate(['/dashboard/business']);
          // }
          this.data = {
            "username": email,
            "password": password,
          }
          this.http.post("http://localhost:8000/api/login", this.data).subscribe((response: any) => {
            this.obj = response;
          });
          // if(this.obj == 'success'){
          //   //add route to the next page
          // }
        } else {
          this.errorMessage = 'Invalid credentials. Please try again.';
          this.isLoading = false;
        }
      }, 1500);
    } else {
      this.markFormGroupTouched(this.loginForm);
    }
  }

  private markFormGroupTouched(formGroup: FormGroup) {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();
    });
  }

  get email() {
    return this.loginForm.get('email');
  }

  get password() {
    return this.loginForm.get('password');
  }
}