import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';
/**
 * Contact Component
 * 
 * Provides contact information and communication channels for users to reach the organization.
 * Handles user inquiries, support requests, feedback, and general communication.
 * 
 * @selector app-contact
 * @standalone true
 */
@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './contact.html',
  styleUrl: './contact.css',
})
export class Contact {
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}
