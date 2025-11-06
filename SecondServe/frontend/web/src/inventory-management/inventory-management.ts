import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule, DatePipe } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-inventory-management',
  templateUrl: './inventory-management.html',
  styleUrls: ['./inventory-management.css'],
  imports: [CommonModule, DatePipe],
})
export class InventoryManagement implements OnInit {
  inventory: any[] = [];
  loading = true;

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.fetchInventory();
  }

  fetchInventory(): void {
    this.http
      .get<any>('http://localhost:8000/inventory/', { withCredentials: true })
      .subscribe({
        next: (response) => {
          this.inventory = response.inventory || [];
          this.loading = false;
        },
        error: (err) => {
          console.error('Error fetching inventory:', err);
          this.loading = false;
        },
      });
  }

  goToHome(): void {
  this.router.navigate(['/home']);
}

  goToAccount(): void {
    this.router.navigate(['/account']);
  }

  goToInventory(): void {
    this.router.navigate(['/inventory-management']);
  }


  donateItem(item: any): void {
    const payload = {
      item_name: item.name,
      attributes: ['type'],
      values: ['donated'],
    };

    this.http
      .put('http://localhost:8000/inventory/edit/', payload, { withCredentials: true })
      .subscribe({
        next: (response) => {
          console.log('Donation marked successfully:', response);
          this.fetchInventory();
        },
        error: (error) => {
          console.error('Error marking donation:', error);
        },
      });
  }

  // ✅ NEW FUNCTIONS

  goToOrders(): void {
    this.router.navigate(['/order-history']); // or your actual route name
  }

  logout(): void {
    this.http
      .post('http://localhost:8000/logout/', {}, { withCredentials: true })
      .subscribe({
        next: () => {
          console.log('Logged out successfully');
          this.router.navigate(['/login']);
        },
        error: (err) => {
          console.error('Error logging out:', err);
        },
      });
  }
}
