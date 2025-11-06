import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

/**
 * Restaurant data structure
 * Represents a restaurant with available food items for pickup/delivery
 */
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

/**
 * Pickup request data structure
 * Defines the payload for scheduling a food pickup or delivery
 */
interface PickupRequest {
  restaurantId: number;
  userId: number;
  pickupTime: string;
  deliveryType: 'pickup' | 'delivery';
  items: number[];
}

/**
 * User Home Component
 * 
 * Main dashboard for authenticated users to browse restaurants and schedule food pickups/deliveries.
 * Displays available restaurants with food items and handles order scheduling.
 * 
 * @selector app-home
 * @standalone true
 */
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './user-home.html',
  styleUrls: ['./user-home.css']
})
export class UserHome implements OnInit {
  restaurants: Restaurant[] = [];
  loading = false;
  error: string | null = null;

  private apiUrl = 'http://localhost:8080/api/user';

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
    this.loadRestaurants();
  }

  // --- Navigation Methods --- //

  /** Navigates to user account management page */
  goToAccount(): void {
    this.router.navigate(['/account']);
  }

  /** Navigates to home page (current implementation refreshes page) */
  goToHome(): void {
    window.location.href = '/user-home';
  }

  /** Navigates to order history page */
  goToOrders(): void {
    this.router.navigate(['/history']);
  }

  /** Logs out user by clearing token and redirecting to login */
  logout(): void {
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }

  // --- Restaurant Methods --- //

  /** Loads available restaurants from API (currently commented out) */
  loadRestaurants(): void {
    // Implementation pending API integration
  }

  /** Schedules a food pickup with the specified restaurant (commented out) */
  schedulePickup(request: PickupRequest): void {
    // Implementation pending API integration
  }

  /** Handles pickup button click for a restaurant */
  onPickupClick(restaurant: Restaurant): void {
    // Implementation pending API integration
  }

  /** Handles delivery button click - prompts for address then schedules delivery */
  onDeliveryClick(restaurant: Restaurant): void {
    // Implementation pending API integration
  }

  /** Refreshes the restaurant list */
  refreshRestaurants(): void {
    // Implementation pending
  }
}