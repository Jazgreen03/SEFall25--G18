import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule, DatePipe, NgClass } from '@angular/common';
import { NgFor, NgIf } from '@angular/common';

interface Order {
  id: number;
  date: Date;
  restaurant: string;
  status: string;
  items: string[];
}

@Component({
  selector: 'app-order-history',
  standalone: true,
  imports: [CommonModule, NgIf, NgFor, NgClass, DatePipe],
  templateUrl: './user-order-history.html',
  styleUrls: ['./user-order-history.css'],
})
export class UserOrderHistory implements OnInit {
  orders: Order[] = [];
  loading = true;
  error: string | null = null;

  // Add activeTab for navbar highlighting
  activeTab = 'orders';

  constructor(private router: Router) {}

  ngOnInit() {
    this.loadOrders();
  }

  // Simulate fetching orders from API
  loadOrders() {
    this.loading = true;
    this.error = null;

    setTimeout(() => {
      try {
        this.orders = [
          {
            id: 101,
            date: new Date('2025-10-25T14:00:00'),
            restaurant: 'Fresh Bites Café',
            status: 'Delivered',
            items: ['Pasta', 'Salad'],
          },
          {
            id: 102,
            date: new Date('2025-10-27T18:30:00'),
            restaurant: 'Community Kitchen',
            status: 'In Progress',
            items: ['Soup', 'Bread'],
          },
        ];
      } catch (e) {
        this.error = 'Failed to load orders. Please try again.';
      } finally {
        this.loading = false;
      }
    }, 800);
  }

  refreshOrders() {
    this.loadOrders();
  }

  viewOrder(orderId: number) {
    const order = this.orders.find((o) => o.id === orderId);
    if (order) {
      this.viewDetails(order);
    }
  }

  viewDetails(order: Order) {
    this.router.navigate(['/order', order.id]);
  }

  goToAccount() {
    this.activeTab = 'account';
    this.router.navigate(['/account']);
  }

  goToHome() {
    this.activeTab = '';
    this.router.navigate(['/home']);
  }

  // New: goToOrders for the template
  goToOrders() {
    this.activeTab = 'orders';
    this.router.navigate(['/orders']);
  }

  logout() {
    localStorage.removeItem('user');
    this.router.navigate(['/login']);
  }
}
