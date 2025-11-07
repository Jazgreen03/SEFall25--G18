import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

/**
 * User data structure for account management
 * Represents user profile information for display and updates
 */
interface User {
  email: string;
  name: string;
  address: string;
  password?: string;
}

/**
 * User Account Management Component
 * 
 * Handles user profile management including viewing and updating account information.
 * Provides functionality to update email, name, address, and password.
 * 
 * @selector app-manage-account
 * @standalone true
 */
@Component({
  selector: 'app-manage-account',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-manage-account.html',
  styleUrls: ['./user-manage-account.css'],
})
export class UserAccountManagement implements OnInit {
  /** Current user profile data */
  user: User = {
    email: '',
    name: '',
    address: '',
  };

  /** Toggle state for password visibility */
  showPassword = false;

  /** Success message for user feedback */
  successMessage: string | null = null;

  /** Error message for user feedback */
  errorMessage: string | null = null;

  private apiUrl = 'http://localhost:8080/api/users';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadUser();
  }

  /** Loads current user data from API */
  loadUser(): void {
    this.http.get<User>(`${this.apiUrl}/me`).subscribe({
      next: (data) => (this.user = data),
      error: (err) => console.error('Failed to load user', err),
    });
  }

  /** Updates user account information via API */
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

  /** Toggles password field visibility */
  togglePassword(): void {
    this.showPassword = !this.showPassword;
  }

  // --- Navigation Methods --- //

  /** Reloads current account page */
  goToAccount(): void {
    this.loadUser();
  }

  /** Navigates to home page */
  goToHome(): void {
    window.location.href = '/home';
  }

  /** Navigates to order history page */
  goToOrders(): void {
    window.location.href = '/history';
  }

  /** Logs out user and redirects to login page */
  logout(): void {
    window.location.href = '/login';
  }
}