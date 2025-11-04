import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-community',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './community.html',
  styleUrl: './community.css',
})
export class Community {
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}
