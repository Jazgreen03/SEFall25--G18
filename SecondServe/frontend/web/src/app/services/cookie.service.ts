// cookie.service.ts
import { Injectable } from '@angular/core';
import { getCookie } from '../../../utils';

/**
 * Cookie Service
 * 
 * Provides cookie management functionality across the application.
 * Wraps utility cookie functions in an injectable service for dependency injection.
 * 
 * @injectable providedIn: 'root'
 */
@Injectable({ providedIn: 'root' })
export class CookieService {
  /**
   * Retrieves a cookie value by name
   * @param name The name of the cookie to retrieve
   * @returns The cookie value or empty string if not found
   */
  getCookie(name: string): string {
    return getCookie(name) || '';
  }
}