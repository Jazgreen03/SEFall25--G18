import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-blog',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './blog.html',
  styleUrl: './blog.css',
})
export class Blog {
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}
