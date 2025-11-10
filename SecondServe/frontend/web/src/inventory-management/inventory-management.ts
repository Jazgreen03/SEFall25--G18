import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

interface Delivery {
  id: number;
  foodName: string;
  quantity: number;
  recipient: string;
  pickupTime: string;
  driver?: string;
  status: string;
}

interface InventoryItem {
  id: number;
  name: string;
  quantity: number;
  expiryDate: string;
}

@Component({
  selector: 'app-org-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inventory-management.html',
  styleUrls: ['./inventory-management.css'],
})
export class InventoryManagement implements OnInit {
  activeDeliveries: Delivery[] = [];
  inventory: InventoryItem[] = [];
  loading = false;
  error: string | null = null;

  private apiUrl = 'http://localhost:8080/api';

  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.loadData();
  }

  /** Load both active deliveries and inventory items */
  loadData(): void {
    this.loading = true;
    this.error = null;

    // Simulated parallel API calls
    setTimeout(() => {
      try {
        this.activeDeliveries = [
          {
            id: 1,
            foodName: 'Fresh Sandwiches',
            quantity: 25,
            recipient: 'Downtown Shelter',
            pickupTime: new Date('2025-10-31T13:00:00').toISOString(),
            driver: 'John Doe',
            status: 'Out for Delivery',
          },
          {
            id: 2,
            foodName: 'Canned Soup',
            quantity: 50,
            recipient: 'Food Aid Center',
            pickupTime: new Date('2025-10-31T15:30:00').toISOString(),
            status: 'Pending Pickup',
          },
        ];

        this.inventory = [
          { id: 1, name: 'Bread Loaves', quantity: 40, expiryDate: '2025-11-05' },
          { id: 2, name: 'Apples', quantity: 100, expiryDate: '2025-11-10' },
          { id: 3, name: 'Cereal Boxes', quantity: 25, expiryDate: '2025-12-01' },
        ];
      } catch (e) {
        console.error(e);
        this.error = 'Failed to load data. Please try again.';
      } finally {
        this.loading = false;
      }
    }, 800);
  }

  /** Reload data manually */
  reloadData(): void {
    this.loadData();
  }

  /** Mark inventory item for donation */
  donateItem(item: InventoryItem): void {
  const confirmed = confirm(`Mark "${item.name}" as donated?`);
  if (!confirmed) return;

  // Get the logged-in restaurant's username
  const restaurantUsername = localStorage.getItem('username');

  // Prepare the delivery data to send to backend
  const payload = {
    restaurantName: restaurantUsername,
    items: [item.name],
    quantity: item.quantity,
    pickupAddress: 'Restaurant Address',  // replace with real data if available
    deliveryAddress: 'Food Bank / Organization' // or dynamically assigned later
  };

  // Send to backend API
  this.http.post(`${this.apiUrl}/deliveries`, payload).subscribe({
    next: () => {
      alert(`${item.name} marked for donation and sent for delivery!`);
      // Remove the donated item from inventory (frontend)
      this.inventory = this.inventory.filter((i) => i.id !== item.id);
    },
    error: (err) => {
      console.error('Donation failed:', err);
      alert('Failed to mark donation — please try again.');
    }
  });
}


  /** View more details about a delivery */
  viewDeliveryDetails(delivery: Delivery): void {
    alert(`Viewing details for: ${delivery.foodName}`);
    // Optionally navigate to delivery details page:
    // this.router.navigate(['/delivery', delivery.id]);
  }

  // --- Navigation Methods --- //

  goToAccount(): void {
    this.router.navigate(['/account']);
  }

  goToHome(): void {
    this.router.navigate(['/home']);
  }

  goToOrders(): void {
    this.router.navigate(['/history']);
  }

  goToInventory(): void {
    this.router.navigate(['/inventory']);
  }

  logout(): void {
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }
}
