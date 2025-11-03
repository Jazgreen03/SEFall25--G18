import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

interface User {
  email: string;
  name: string;
  address: string;
  password?: string;
}

@Component({
  selector: 'app-manage-account',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-manage-account.html',
  styleUrls: ['./user-manage-account.css'],
})
export class UserAccountManagement implements OnInit {
  user: User = {
    email: '',
    name: '',
    address: '',
  };

  showPassword = false;
  successMessage: string | null = null;
  errorMessage: string | null = null;

  private apiUrl = 'http://localhost:8080/api/users';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadUser();
  }

  loadUser(): void {
    // Fetch current user info
    this.http.get<User>(`${this.apiUrl}/me`).subscribe({
      next: (data) => (this.user = data),
      error: (err) => console.error('Failed to load user', err),
    });
  }

  updateAccount(): void {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    this.http.put(`${this.apiUrl}/update`, this.user, { headers }).subscribe({
      next: () => {
        this.successMessage = 'Account updated successfully!';
        this.errorMessage = null;
        this.user.password = ''; // clear password field
      },
      error: (err) => {
        this.errorMessage = 'Failed to update account.';
        this.successMessage = null;
        console.error(err);
      },
    });
  }

  togglePassword(): void {
    this.showPassword = !this.showPassword;
  }

  // Navigation / Header buttons
  goToAccount(): void {
    // Already on account page; can optionally reload
    this.loadUser();
  }

  goToHome(): void {
    // Navigate to home page
    window.location.href = '/home';
  }

  goToOrders(): void {
    // Navigate to orders page
    window.location.href = '/history';
  }

  logout(): void {
    // Clear session / redirect
    // Example:
    window.location.href = '/login';
  }
}
