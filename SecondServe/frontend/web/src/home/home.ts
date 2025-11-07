import { Component, ViewChild, ViewContainerRef, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../app/services/auth.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import { UserHome } from '../user-home/user-home';
import { OrgHome } from '../org-home/org-home';
import { DriverHome } from '../driver-home/driver-home';

/**
 * Home Component
 * 
 * Dynamic home page container that loads role-specific dashboard components.
 * Routes users to appropriate interfaces based on their authentication role.
 * 
 * @selector app-home
 * @standalone true
 */
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class Home implements OnInit, AfterViewInit {
  /** Reference to dynamic content container for role-specific components */
  @ViewChild('dynamicContent', { read: ViewContainerRef }) dynamicContent!: ViewContainerRef;

  /** Current user role from auth service */
  private role: string | null = null;

  constructor(
    private authService: AuthService,
    private router: Router,
    private http: HttpClient
  ) { }

  ngOnInit() {
    this.role = this.authService.getRole();
  }

  ngAfterViewInit() {
    if (this.role) {
      this.loadRoleContent(this.role);
    } else {
      this.router.navigate(['/']);
    }
  }

  /**
   * Loads the appropriate home/dashboard component based on user role
   * Verifies user authentication before loading component
   * @param role The user role determining which dashboard to display
   */
  private loadRoleContent(role: string) {
    this.http.get("http://localhost:8000/user/info", { withCredentials: true }).subscribe({
      next: () => {
        console.log("Role content loading:", role);
        switch (role) {
          case 'user':
            this.dynamicContent.createComponent(UserHome);
            break;
          case 'organization':
            this.dynamicContent.createComponent(OrgHome);
            break;
          case 'driver':
            this.dynamicContent.createComponent(DriverHome);
            break;
          default:
            this.router.navigate(['/']);
        }
      },
      error: () => {
        this.router.navigate(['/']);
      }
    });
  }
}