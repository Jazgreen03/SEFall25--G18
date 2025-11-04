import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-events',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './events.html',
  styleUrl: './events.css',
})
export class Events {
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}
