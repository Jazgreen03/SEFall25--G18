import { Component, ViewChild, ViewContainerRef, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../app/services/auth.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import { UserAccountManagement } from '../user-manage-account/user-manage-account';
import { OrgAccountManagement } from '../org-manage-account/org-manage-account';
import { DriverAccountManagement } from '../driver-manage-account/driver-manage-account';

@Component({
  selector: 'app-account-management',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './manage-account.html',
  styleUrls: ['./manage-account.css']
})
export class AccountManagement implements OnInit, AfterViewInit {
  @ViewChild('dynamicContent', { read: ViewContainerRef }) dynamicContent!: ViewContainerRef;
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

  private loadRoleContent(role: string) {
    this.http.get("http://localhost:8000/user/info", { withCredentials: true }).subscribe({
      next: () => {
        console.log("Role content loading:", role);
        switch (role) {
          case 'user':
            this.dynamicContent.createComponent(UserAccountManagement);
            break;
          case 'organization':
            this.dynamicContent.createComponent(OrgAccountManagement);
            break;
          case 'driver':
            this.dynamicContent.createComponent(DriverAccountManagement);
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
