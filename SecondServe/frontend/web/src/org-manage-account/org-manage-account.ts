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
  templateUrl: './org-manage-account.html',
  styleUrls: ['./org-manage-account.css'],
})
export class OrgAccountManagement implements OnInit {
  user: User = { email: '', name: '', address: '' };
  showPassword = false;
  successMessage: string | null = null;
  errorMessage: string | null = null;
  updating = false;

  private apiUrl = 'http://localhost:8000/user'; // backend URL for org routes

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadUser();
  }

  /** Load currently logged-in org user info */
  loadUser(): void {
    this.http.get<User>(`${this.apiUrl}/info/`, { withCredentials: true }).subscribe({
      next: (data) => {
        console.log('Logged in organization:', data);
        this.user = { ...data, password: '' };
      },
      error: (err) => {
        console.error('Not logged in', err);
        this.errorMessage = 'You must be logged in to manage your organization account.';
      },
    });
  }

  /** Fetch CSRF token from cookie */
  getCsrfToken(): string {
    const match = document.cookie.match(/csrftoken=([\w-]+)/);
    return match ? match[1] : '';
  }

  /** Update account info */
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
      // Update name
      await this.http
        .put(
          `${this.apiUrl}/update/`,
          { attribute: 'first_name', new_value: this.user.name },
          { headers, withCredentials: true }
        )
        .toPromise();

      // Update address
      await this.http
        .put(
          `${this.apiUrl}/update/`,
          { attribute: 'address', new_value: this.user.address },
          { headers, withCredentials: true }
        )
        .toPromise();

      this.successMessage = 'Organization details updated successfully!';

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
    } catch (err: any) {
      console.error('Update failed:', err);
      this.errorMessage =
        err.error?.details || 'Failed to update organization account. Make sure you are logged in.';
    } finally {
      this.updating = false;
    }
  }

  togglePassword(): void {
    this.showPassword = !this.showPassword;
  }

  // ---------------- Navigation ----------------
  goToAccount(): void {
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

  goToInventory(): void {
    window.location.href = '/inventory';
  }

  logout(): void {
    window.location.href = '/login';
  }
}
