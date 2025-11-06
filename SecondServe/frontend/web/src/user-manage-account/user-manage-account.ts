import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';


interface User {
  email: string;
  first_name: string;
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
    first_name: '',
    address: '',
  };

  showPassword = false;
  successMessage: string | null = null;
  errorMessage: string | null = null;
  updating = false;

  private apiUrl = 'http://localhost:8000/user'; // Django backend URL

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadUser();
  }

  /** Load currently logged-in user info */
  loadUser(): void {
    this.http.get<User>(`${this.apiUrl}/info/`, { withCredentials: true }).subscribe({
      next: (data) => {
        this.user = { ...data, password: '' };
        console.log('Logged in user:', data);
      },
      error: (err) => {
        console.error('Not logged in', err);
        this.errorMessage = 'You must be logged in to manage your account.';
      },
    });
  }

  /** Fetch CSRF token from cookie */
  getCsrfToken(): string {
    const match = document.cookie.match(/csrftoken=([\w-]+)/);
    return match ? match[1] : '';
  }

  /** Update account attributes (first_name, address, password) */
  async updateAccount(): Promise<void> {
    this.updating = true;
    this.successMessage = null;
    this.errorMessage = null;

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-CSRFToken': this.getCsrfToken(),
    });

    try {
      // Update first_name
      await this.http
        .put(
          `${this.apiUrl}/update/`,
          { attribute: 'first_name', new_value: this.user.first_name },
          { headers, withCredentials: true }
        )
        .toPromise();
      this.successMessage = 'Name updated successfully!';

      // Update password if provided
      if (this.user.password) {
        await this.http
          .put(
            `${this.apiUrl}/update/`,
            { attribute: 'password', new_value: this.user.password },
            { headers, withCredentials: true }
          )
          .toPromise();
        this.successMessage += ' Password updated successfully!';
        this.user.password = '';
      }

      // Update address (if you handle it on backend)
      if (this.user.address) {
        await this.http
          .put(
            `${this.apiUrl}/update/`,
            { attribute: 'address', new_value: this.user.address },
            { headers, withCredentials: true }
          )
          .toPromise();
        this.successMessage += ' Address updated successfully!';
      }
    } catch (err) {
      console.error('Update failed:', err);
      this.errorMessage = 'Failed to update account. Make sure you are logged in.';
    } finally {
      this.updating = false;
    }
  }

  togglePassword(): void {
    this.showPassword = !this.showPassword;
  }

  // Navigation / Header buttons
  goToAccount(): void {
    this.loadUser(); // reload user info
  }

  goToHome(): void {
    window.location.href = '/home';
  }

  goToOrders(): void {
    window.location.href = '/history';
  }

  logout(): void {
    window.location.href = '/login';
  }
}
