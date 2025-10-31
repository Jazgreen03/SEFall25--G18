import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

interface Delivery {
  id: number;
  restaurantName: string;
  pickupAddress: string;
  deliveryAddress: string;
  items: string[];
  requestedTime: string;
  status: 'Pending' | 'Accepted' | 'Completed';
}

@Component({
  selector: 'app-driver-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './driver-home.html',
  styleUrls: ['./driver-home.css'],
})
export class DriverHome implements OnInit {
  currentTab: 'account' | 'orders' | 'deliveries' = 'deliveries';
  deliveries: Delivery[] = [];
  loading = false;
  error: string | null = null;

  private apiUrl = 'http://localhost:8080/api';

  constructor(
    private http: HttpClient,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.loadDeliveries();
  }

  // --- Navigation Methods --- //
  goToAccount(): void {
    this.currentTab = 'account';
    this.router.navigate(['/account']);
  }

  goToOrders(): void {
    this.currentTab = 'orders';
    this.router.navigate(['/driver-history']);
  }

  goToHome(): void {
    window.location.href = '/driver-home';
  }

  goToDeliveries(): void {
    window.location.href = '/driver-home';
  }

  logout(): void {
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }

  // --- API Methods --- //
  loadDeliveries(): void {
    this.loading = true;
    this.error = null;

    this.http.get<Delivery[]>(`${this.apiUrl}/driver/deliveries/available`).subscribe({
      next: (data) => {
        this.deliveries = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load deliveries.';
        this.loading = false;
        console.error('Error loading deliveries:', err);
      },
    });
  }

  refreshDeliveries(): void {
    this.loadDeliveries();
  }

  acceptDelivery(delivery: Delivery): void {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

    this.http
      .post(`${this.apiUrl}/driver/deliveries/accept`, { deliveryId: delivery.id }, { headers })
      .subscribe({
        next: () => {
          alert(`Delivery ${delivery.id} accepted!`);
          this.loadDeliveries(); // reload list after accepting
        },
        error: (err) => {
          this.error = 'Failed to accept delivery.';
          console.error(err);
        },
      });
  }
}
