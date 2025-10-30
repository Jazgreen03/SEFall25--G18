import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

interface Restaurant {
  id: number;
  name: string;
  address: string;
  distance: number;
  availableItems: number;
  expiryDate: string;
  imageUrl: string;
  foodTypes: string[];
  openUntil: string;
}

interface PickupRequest {
  restaurantId: number;
  userId: number;
  pickupTime: string;
  deliveryType: 'pickup' | 'delivery';
  items: number[];
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class UserHome implements OnInit {
  restaurants: Restaurant[] = [];
  loading = false;
  error: string | null = null;

  private apiUrl = 'http://localhost:8080/api';

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
    this.loadRestaurants();
  }

  // --- Navigation Methods --- //
  goToAccount(): void {
    this.router.navigate(['/account']);
  }

  goToHome(): void {
    // Navigate to orders page
    window.location.href = '/home';
  }

  goToOrders(): void {
    this.router.navigate(['/orders']);
  }

  logout(): void {
    // clear token and navigate to login
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }

  // --- API Methods --- //

  loadRestaurants(): void {
    this.loading = true;
    this.error = null;

    this.http.get<Restaurant[]>(`${this.apiUrl}/restaurants/available`)
      .subscribe({
        next: (data) => {
          this.restaurants = data;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to load restaurants.';
          this.loading = false;
          console.error('Error loading restaurants:', err);
        }
      });
  }

  schedulePickup(request: PickupRequest): void {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    this.loading = true;

    this.http.post(`${this.apiUrl}/pickups/schedule`, request, { headers })
      .subscribe({
        next: () => {
          alert('Pickup scheduled successfully!');
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to schedule pickup.';
          this.loading = false;
          console.error(err);
        }
      });
  }

  onPickupClick(restaurant: Restaurant): void {
    const pickupRequest: PickupRequest = {
      restaurantId: restaurant.id,
      userId: 1,
      pickupTime: new Date(Date.now() + 3600000).toISOString(),
      deliveryType: 'pickup',
      items: []
    };
    this.schedulePickup(pickupRequest);
  }

  onDeliveryClick(restaurant: Restaurant): void {
    const address = prompt('Enter delivery address:');
    if (!address) return;

    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const deliveryRequest = {
      restaurantId: restaurant.id,
      deliveryAddress: address,
      requestedTime: new Date().toISOString()
    };

    this.loading = true;
    this.http.post(`${this.apiUrl}/deliveries/request`, deliveryRequest, { headers })
      .subscribe({
        next: () => {
          alert('Delivery requested!');
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Delivery request failed.';
          this.loading = false;
          console.error(err);
        }
      });
  }

  refreshRestaurants(): void {
    this.loadRestaurants();
  }
}
