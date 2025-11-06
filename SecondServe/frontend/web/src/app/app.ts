import { Component, signal } from '@angular/core';
import { RouterOutlet, Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { CommonModule } from '@angular/common';

/**
 * Root Application Component
 * 
 * The main application component that serves as the root of the Angular application.
 * Handles routing, layout management, and global application state.
 * 
 * Features:
 * - Manages router outlet for navigation
 * - Tracks current route for conditional layout rendering
 * - Provides navigation methods
 * - Controls layout visibility based on route
 * 
 * @selector app-root
 * @standalone true
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  /** Current active route path for conditional layout logic */
  currentRoute = '';

  /** Application title using Angular signals for reactive updates */
  protected readonly title = signal('web');

  /**
   * Component constructor
   * @param router Router service for navigation and route tracking
   */
  constructor(private router: Router) {
    /**
     * Subscribe to router events to track navigation changes
     * Filters for NavigationEnd events to update currentRoute
     */
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.currentRoute = event.url;
    });
  }

  /**
   * Navigates to the login page
   * Used for navigation controls in the layout template
   */
  onLogin() {
    this.router.navigate(['/login']);
  }

  /**
   * Determines whether to show the main application layout
   * Hides layout on login page for a clean authentication experience
   * @returns boolean indicating if layout should be displayed
   */
  showLayout(): boolean {
    return this.currentRoute !== '/login';
  }
}