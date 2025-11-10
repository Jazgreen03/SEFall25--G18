import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

interface User {
  email: string;
  first_name: string;
  password?: string;
}

@Component({
  selector: 'app-manage-account',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './driver-manage-account.html',
  styleUrls: ['./driver-manage-account.css'],
})
export class DriverAccountManagement implements OnInit {
  user: User = { email: '', first_name: '' };
  showPassword = false;
  successMessage: string | null = null;
  errorMessage: string | null = null;
  updating = false;

  private apiUrl = 'http://localhost:8000/user'; // Django backend URL

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadUser(); // load current user if session exists
  }

  /** Load currently logged-in user info */
  loadUser(): void {
    this.http.get<User>(`${this.apiUrl}/info/`, { withCredentials: true }).subscribe({
      next: (data) => {
        console.log('Logged in user:', data);
        this.user = { ...data, password: '' };
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

  /** Update account */
  async updateAccount(): Promise<void> {
    this.updating = true;
    this.successMessage = null;
    this.errorMessage = null;

    const csrfToken = this.getCsrfToken();
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    });

    try {
      // First: update first_name
      await this.http
        .put(
          `${this.apiUrl}/update/`,
          { attribute: 'first_name', new_value: this.user.first_name },
          { headers, withCredentials: true }
        )
        .toPromise();

      this.successMessage = 'Name updated successfully!';

      // Second: update password if provided
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
    } catch (err: any) {
      console.error('Update failed:', err);
      this.errorMessage =
        err.error?.details || 'Failed to update account. Make sure you are logged in.';
    } finally {
      this.updating = false;
    }
  }


  togglePassword(): void {
    this.showPassword = !this.showPassword;
  }

  goToAccount(): void {
    this.loadUser();
  }

  goToHome(): void {
    window.location.href = '/home';
  }

  goToOrders(): void {
    window.location.href = '/driver-history';
  }

  goToDeliveries(): void {
    window.location.href = '/deliveries';
  }

  logout(): void {
    window.location.href = '/login';
  }
}
