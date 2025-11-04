import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-donate',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './donate.html',
  styleUrl: './donate.css',
})
export class Donate {
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}
