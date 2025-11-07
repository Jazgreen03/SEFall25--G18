import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

/**
 * Landing Component
 * 
 * The main landing page component that serves as the entry point to the application.
 * Typically includes hero section, feature overview, and call-to-action elements.
 * 
 * @selector app-landing
 * @standalone true
 */
@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './landing.html',
  styleUrls: ['./landing.css']
})
export class Landing {
  /**
   * Landing page component - serves as the application's homepage
   * Provides introduction to the platform and navigation to key sections
   */
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}