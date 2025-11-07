import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

interface Order {
  id: number;
  date: string;
  items: string[];
  status: 'Pending' | 'In Transit' | 'Completed' | 'Cancelled';
}

@Component({
  selector: 'app-driver-order-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './driver-order-history.html',
  styleUrls: ['./driver-order-history.css'],
})
export class DriverOrderHistory implements OnInit {
  currentTab: 'account' | 'history' | 'deliveries' = 'deliveries';
  history: Order[] = [];
  loading = false;
  error: string | null = null;
  activeTab = 'history';

  private apiUrl = 'http://localhost:8080/api';

  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.loadOrders();
  }

  // --- Navigation Methods --- //
  goToHome(): void {
    this.router.navigate(['/home']);
  }

  goToAccount(): void {
    this.router.navigate(['/account']);
  }

  goToHistory(): void {
    this.activeTab = 'orders';
    this.loadOrders();
  }

  goToDeliveries(): void {
    window.location.href = '/deliveries';
  }

  logout(): void {
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }

  // --- API Methods --- //
  loadOrders(): void {
    this.loading = true;
    this.error = null;

    this.http.get<Order[]>(`${this.apiUrl}/driver/orders`).subscribe({
      next: (data) => {
        this.history = data;
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
    this.router.navigate([`/driver/order/${orderId}`]);
  }
}
