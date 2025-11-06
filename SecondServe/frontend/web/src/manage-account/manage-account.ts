import { Component, ViewChild, ViewContainerRef, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../app/services/auth.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

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

  private async loadRoleContent(role: string) {
    this.http.get("http://localhost:8000/user/info", { withCredentials: true }).subscribe({
      next: async () => {
        console.log("Role content loading:", role);
        switch (role) {
          case 'user': {
            const { UserAccountManagement } = await import('../user-manage-account/user-manage-account');
            this.dynamicContent.createComponent(UserAccountManagement);
            break;
          }
          case 'organization': {
            const { OrgAccountManagement } = await import('../org-manage-account/org-manage-account');
            this.dynamicContent.createComponent(OrgAccountManagement);
            break;
          }
          case 'driver': {
            const { DriverAccountManagement } = await import('../driver-manage-account/driver-manage-account');
            this.dynamicContent.createComponent(DriverAccountManagement);
            break;
          }
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