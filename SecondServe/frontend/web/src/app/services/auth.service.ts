import { Injectable } from '@angular/core';

/**
 * Authentication Service
 * 
 * Manages user role information in memory and session storage.
 * Provides role-based authentication state across the application.
 * 
 * @injectable providedIn: 'root'
 */
@Injectable({ providedIn: 'root' })
export class AuthService {
  private roleKey = 'userRole';
  private role: string | null = null;

  /**
   * Sets the user role in memory and session storage
   * @param role The user role to store
   */
  setRole(role: string) {
    this.role = role;
    sessionStorage.setItem(this.roleKey, role);
  }

  /**
   * Gets the current user role
   * @returns The user role or null if not set
   */
  getRole(): string | null {
    // If already stored in memory, return it
    if (this.role) return this.role;

    // Otherwise retrieve from sessionStorage
    const stored = sessionStorage.getItem(this.roleKey);
    this.role = stored;
    return stored;
  }

  /**
   * Clears the user role from memory and session storage
   */
  clearRole() {
    this.role = null;
    sessionStorage.removeItem(this.roleKey);
  }
}