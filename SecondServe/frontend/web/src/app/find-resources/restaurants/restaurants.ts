import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-restaurants',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './restaurants.html',
  styleUrl: './restaurants.css',
})
export class Restaurants {
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}
