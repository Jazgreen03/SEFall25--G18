import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private roleKey = 'userRole';
  private role: string | null = null;

  setRole(role: string) {
    this.role = role;
    sessionStorage.setItem(this.roleKey, role);
  }

  getRole(): string | null {
    // If already stored in memory, return it
    if (this.role) return this.role;

    // Otherwise retrieve from sessionStorage
    const stored = sessionStorage.getItem(this.roleKey);
    this.role = stored;
    return stored;
  }

  clearRole() {
    this.role = null;
    sessionStorage.removeItem(this.roleKey);
  }
}
