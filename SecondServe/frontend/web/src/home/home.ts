import { Component, ViewChild, ViewContainerRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../app/services/auth.service';
import { Router } from '@angular/router';

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
export class Home implements AfterViewInit {
  @ViewChild('dynamicContent', { read: ViewContainerRef }) dynamicContent!: ViewContainerRef;

  constructor(private authService: AuthService, private router: Router) { }

  ngAfterViewInit() {
    const role = this.authService.getRole();
    this.loadRoleContent(role);
  }

  private loadRoleContent(role: string | null) {
    if (!this.dynamicContent) return; // safety check

    this.dynamicContent.clear();

    console.log(role);

    switch (role) {
      case 'user':
        console.log("Loading user home");
        this.dynamicContent.createComponent(UserHome);
        break;
      case 'organization':
        console.log("Loading Organization home");
        this.dynamicContent.createComponent(OrgHome);
        break;
      case 'driver':
        console.log("Loading Driver home");
        this.dynamicContent.createComponent(DriverHome);
        break;
      default:
        this.router.navigate(['/']);
    }
  }
}
