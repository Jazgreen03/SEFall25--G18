import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _role: string | null = null;

  setRole(role: string) {
    this._role = role;
  }

  getRole(): string | null {
    return this._role;
  }

  clearRole() {
    this._role = null;
  }

  isLoggedIn(): boolean {
    return !!this._role;
  }
}
