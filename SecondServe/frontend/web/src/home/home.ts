import { Component, ViewChild, ViewContainerRef, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../app/services/auth.service';
import { Router } from '@angular/router';

// Import your role-specific components
import { UserHome } from '../user-home/user-home';
import { OrgHome } from '../org-home/org-home';
import { DriverHome } from '../driver-home/driver-home';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class Home implements OnInit {
  @ViewChild('dynamicContent', { read: ViewContainerRef }) dynamicContent!: ViewContainerRef;

  constructor(private authService: AuthService, private router: Router,) { }

  ngOnInit() {
    const role = this.authService.getRole();
    this.loadRoleContent(role);
  }

  private loadRoleContent(role: string | null) {
    this.dynamicContent.clear();

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
  }
}
