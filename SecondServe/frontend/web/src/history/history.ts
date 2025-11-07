import { Component, ViewChild, ViewContainerRef, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../app/services/auth.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import { UserOrderHistory } from '../user-order-history/user-order-history';
import { OrgOrderHistory } from '../org-order-history/org-order-history';
import { DriverOrderHistory } from '../driver-order-history/driver-order-history';

/**
 * Order History Component
 * 
 * Dynamic order history container that loads role-specific order tracking components.
 * Displays order history and tracking interfaces tailored to each user type.
 * 
 * @selector app-history
 * @standalone true
 */
@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history.html',
  styleUrls: ['./history.css']
})
export class OrderHistory implements OnInit, AfterViewInit {
  /** Reference to dynamic content container for role-specific order history components */
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
   * Loads the appropriate order history component based on user role
   * Verifies user authentication before loading component
   * @param role The user role determining which order history interface to display
   */
  private loadRoleContent(role: string) {
    this.http.get("http://localhost:8000/user/info", { withCredentials: true }).subscribe({
      next: () => {
        console.log("Role content loading:", role);
        switch (role) {
          case 'user':
            this.dynamicContent.createComponent(UserOrderHistory);
            break;
          case 'organization':
            this.dynamicContent.createComponent(OrgOrderHistory);
            break;
          case 'driver':
            this.dynamicContent.createComponent(DriverOrderHistory);
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