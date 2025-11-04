import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private role: string | null = null;

  setRole(role: string) {
    console.log('AuthService: setRole ->', role);
    this.role = role;
    // optional: persist in localStorage/sessionStorage to survive reload
    localStorage.setItem('userRole', role);
  }

  getRole(): string | null {
    // fallback to localStorage if role is undefined
    if (!this.role) {
      this.role = localStorage.getItem('userRole');
    }
    console.log('AuthService: getRole ->', this.role);
    return this.role;
  }

  clearRole() {
    this.role = null;
    localStorage.removeItem('userRole');
  }
}
