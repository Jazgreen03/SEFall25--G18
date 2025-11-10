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

interface ClaimedOrder {
  id: number;
  status: 'Pending' | 'In Transit' | 'Delivered';
  deliveryAddress: string;
  items: { name: string; quantity: number }[];
  organization: string;
}

@Component({
  selector: 'app-driver-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './driver-home.html',
  styleUrls: ['./driver-home.css'],
})
export class DriverHome implements OnInit {
  currentTab: 'account' | 'orders' | 'deliveries' | 'history' = 'deliveries';
  deliveries: Delivery[] = [];        // Open deliveries from restaurants
  claimedOrders: ClaimedOrder[] = []; // Orders already claimed by driver
  loading = false;
  error: string | null = null;

  private apiUrl = 'http://localhost:8000/api/driver';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.loadDeliveries();
    this.loadClaimedOrders();
  }

  // --- Navigation Methods --- //
  goToAccount(): void {
    this.currentTab = 'account';
    this.router.navigate(['/account']);
  }

  goToOrders(): void {
    this.currentTab = 'orders';
    this.router.navigate(['/history']);
  }

  goToHome(): void {
    window.location.href = '/home';
  }

  goToDeliveries(): void {
    window.location.href = '/deliveries';
  }

  logout(): void {
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }

  // --- API Methods --- //

  /** Load all available deliveries from restaurants */
 loadDeliveries(): void {
  this.loading = true;
  this.error = null;

  this.http.get<Delivery[]>(`${this.apiUrl}/deliveries/available/`).subscribe({
    next: (data) => {
      this.deliveries = data;
      this.loading = false;

      // Show message if list is empty
      if (this.deliveries.length === 0) {
        this.error = 'No deliveries are available at this time.';
      } else {
        this.error = null;
      }
    },
    error: (err) => {
      console.error(err);
      // Only show real error if HTTP request fails
      this.error = 'Failed to load deliveries. Please try again later.';
      this.loading = false;
    },
  });
}


  /** Refresh both open and claimed deliveries */
  refreshDeliveries(): void {
    this.loadDeliveries();
    this.loadClaimedOrders();
  }

 acceptDelivery(delivery: Delivery): void {
  const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
  this.http.post(`${this.apiUrl}/deliveries/accept/`, { deliveryId: delivery.id }, { headers })
    .subscribe({
      next: () => {
        alert(`Delivery ${delivery.id} accepted!`);
        
        // Remove from available deliveries
        this.deliveries = this.deliveries.filter(d => d.id !== delivery.id);

        // Add to claimed orders
        const claimed: ClaimedOrder = {
          id: delivery.id,
          status: 'Pending',
          deliveryAddress: delivery.deliveryAddress,
          items: delivery.items.map(item => ({ name: item, quantity: 1 })),
          organization: delivery.restaurantName,
        };
        this.claimedOrders.push(claimed);

      },
      error: (err) => {
        this.error = 'Failed to accept delivery.';
        console.error(err);
      },
  });
}
 /** Load claimed orders assigned to this driver */
loadClaimedOrders(): void {
  const driverUsername = localStorage.getItem('username');
  if (!driverUsername) return;

  this.http
    .get<ClaimedOrder[]>(`${this.apiUrl}/deliveries/claimed/${driverUsername}`)
    .subscribe({
      next: (data) => {
        this.claimedOrders = data;
      },
      error: (err) => {
        console.error('Failed to load claimed deliveries:', err);
        this.error = 'Failed to load claimed deliveries.';
      },
    });
}

  /** Update the status of a claimed order */
  updateOrderStatus(orderId: number, newStatus: 'In Transit' | 'Delivered') {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    this.http.put(`${this.apiUrl}/order/${orderId}/update/`, { new_status: newStatus }, { headers })
      .subscribe({
        next: () => {
          alert(`Order ${orderId} updated to ${newStatus}`);
          this.loadClaimedOrders(); // reload claimed orders
        },
        error: (err) => console.error('Failed to update order:', err)
      });
  }
}
