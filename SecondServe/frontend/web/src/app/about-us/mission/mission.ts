import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-mission',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './mission.html',
  styleUrl: './mission.css',
})
export class Mission {
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}
