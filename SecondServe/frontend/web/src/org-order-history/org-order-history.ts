import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

interface OrgOrder {
  id: number;
  date: string;
  items: string[];
  restaurantName: string;
  status: 'Pending' | 'In Transit' | 'Completed' | 'Cancelled';
}

@Component({
  selector: 'app-org-order-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './org-order-history.html',
  styleUrls: ['./org-order-history.css'],
})
export class OrgOrderHistory implements OnInit {
  orders: OrgOrder[] = [];
  loading = false;
  error: string | null = null;
  activeTab = 'orders';

  private apiUrl = 'http://localhost:8080/api';

  constructor(
    private http: HttpClient,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  // --- Navigation ---
  goToHome(): void {
    this.router.navigate(['/org-home']);
  }

  goToAccount(): void {
    this.router.navigate(['/org-account']);
  }

  goToOrders(): void {
    this.activeTab = 'orders';
    this.loadOrders();
  }

  goToInventory(): void {
    this.router.navigate(['/inventory']);
  }

  logout(): void {
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }

  // --- API Methods ---
  loadOrders(): void {
    this.loading = true;
    this.error = null;

    this.http.get<OrgOrder[]>(`${this.apiUrl}/organization/orders`).subscribe({
      next: (data) => {
        this.orders = data;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.error = 'Failed to load orders.';
        this.loading = false;
      },
    });
  }

  refreshOrders(): void {
    this.loadOrders();
  }

  viewOrder(orderId: number): void {
    this.router.navigate([`/org/order/${orderId}`]);
  }
}
