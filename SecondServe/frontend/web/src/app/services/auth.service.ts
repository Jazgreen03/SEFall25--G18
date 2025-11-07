import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

/**
 * Authentication Service
 * 
 * Manages user role information in memory and session storage.
 * Provides role-based authentication state across the application.
 * 
 * @injectable providedIn: 'root'
 */
@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private role: string | null = null;
  private apiUrl = 'http://localhost:8000/user'; // Django backend URL

  constructor(private http: HttpClient) {}

  /**
   * Sets the user role in memory and session storage
   * @param role The user role to store
   */
  setRole(role: string) {
    console.log('AuthService: setRole ->', role);
    this.role = role;
    localStorage.setItem('userRole', role);
  }

  /**
   * Gets the current user role
   * @returns The user role or null if not set
   */
  getRole(): string | null {
    if (!this.role) {
      this.role = localStorage.getItem('userRole');
    }
    console.log('AuthService: getRole ->', this.role);
    return this.role;
  }

  /** Clear role from memory and storage */
  clearRole() {
    this.role = null;
    localStorage.removeItem('userRole');
  }

  /** Login user, store session cookie automatically */
  login(email: string, password: string): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post(
      `${this.apiUrl}/login/`,
      { email, password },
      { headers, withCredentials: true } // important: keeps session cookie
    ).pipe(
      tap((res: any) => {
        if (res?.role) {
          this.setRole(res.role); // store role after login
        }
      })
    );
  }

  /** Logout user and clear stored role */
  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout/`, {}, { withCredentials: true }).pipe(
      tap(() => this.clearRole())
    );
  }

  /** Get current user info from backend (requires session cookie) */
  getCurrentUser(): Observable<any> {
    return this.http.get(`${this.apiUrl}/info/`, { withCredentials: true });
  }
}