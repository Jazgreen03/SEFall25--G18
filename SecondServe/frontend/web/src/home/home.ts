import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
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
export class Home implements OnInit {
  restaurants: Restaurant[] = [];
  loading = false;
  error: string | null = null;
  
  // Backend API base URL - update with your actual backend URL
  private apiUrl = 'http://localhost:8080/api';
  
  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadRestaurants();
  }

  // GET: Fetch all available restaurants
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
          this.error = 'Failed to load restaurants. Please try again.';
          this.loading = false;
          console.error('Error loading restaurants:', err);
        }
      });
  }

  // GET: Fetch restaurants by location
  loadRestaurantsByLocation(latitude: number, longitude: number, radius: number = 10): void {
    this.loading = true;
    this.error = null;

    const params = {
      lat: latitude.toString(),
      lng: longitude.toString(),
      radius: radius.toString()
    };

    this.http.get<Restaurant[]>(`${this.apiUrl}/restaurants/nearby`, { params })
      .subscribe({
        next: (data) => {
          this.restaurants = data;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to load nearby restaurants.';
          this.loading = false;
          console.error('Error loading nearby restaurants:', err);
        }
      });
  }

  // GET: Fetch restaurant details
  getRestaurantDetails(restaurantId: number): Observable<Restaurant> {
    return this.http.get<Restaurant>(`${this.apiUrl}/restaurants/${restaurantId}`);
  }

  // POST: Schedule a pickup
  schedulePickup(request: PickupRequest): void {
    this.loading = true;
    this.error = null;

    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    this.http.post(`${this.apiUrl}/pickups/schedule`, request, { headers })
      .subscribe({
        next: (response) => {
          alert('Pickup scheduled successfully!');
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to schedule pickup. Please try again.';
          this.loading = false;
          console.error('Error scheduling pickup:', err);
        }
      });
  }

  // POST: Request delivery
  requestDelivery(restaurantId: number, deliveryAddress: string): void {
    this.loading = true;
    this.error = null;

    const deliveryRequest = {
      restaurantId,
      deliveryAddress,
      requestedTime: new Date().toISOString()
    };

    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    this.http.post(`${this.apiUrl}/deliveries/request`, deliveryRequest, { headers })
      .subscribe({
        next: (response) => {
          alert('Delivery request submitted successfully!');
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to request delivery. Please try again.';
          this.loading = false;
          console.error('Error requesting delivery:', err);
        }
      });
  }

  // POST: Register user interest
  registerInterest(email: string): void {
    const interest = { email, timestamp: new Date().toISOString() };
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    this.http.post(`${this.apiUrl}/users/register-interest`, interest, { headers })
      .subscribe({
        next: () => {
          alert('Thank you for your interest!');
        },
        error: (err) => {
          console.error('Error registering interest:', err);
        }
      });
  }

  // Helper method to handle pickup button click
  onPickupClick(restaurant: Restaurant): void {
    const pickupRequest: PickupRequest = {
      restaurantId: restaurant.id,
      userId: 1, // Replace with actual logged-in user ID
      pickupTime: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now
      deliveryType: 'pickup',
      items: []
    };
    
    this.schedulePickup(pickupRequest);
  }

  // Helper method to handle delivery button click
  onDeliveryClick(restaurant: Restaurant): void {
    const address = prompt('Please enter your delivery address:');
    if (address) {
      this.requestDelivery(restaurant.id, address);
    }
  }

  // Refresh restaurant list
  refreshRestaurants(): void {
    this.loadRestaurants();
  }
}