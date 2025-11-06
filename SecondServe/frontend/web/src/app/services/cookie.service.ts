// cookie.service.ts
import { Injectable } from '@angular/core';
import { getCookie } from '../../../utils';

@Injectable({ providedIn: 'root' })
export class CookieService {
  getCookie(name: string): string {
    return getCookie(name) || '';
  }
}
