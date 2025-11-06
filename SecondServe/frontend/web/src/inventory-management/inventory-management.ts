import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule, DatePipe } from '@angular/common';

interface InventoryItem {
  name: string;
  type: string;          // display label
  quantity: number;
  expiration?: string | null;
  expiryDate?: Date | null;
  donated?: boolean;     // frontend-only flag
}

interface EditInventoryResponse {
  details: string;
}

@Component({
  standalone: true,
  selector: 'app-inventory-management',
  templateUrl: './inventory-management.html',
  styleUrls: ['./inventory-management.css'],
  imports: [CommonModule, DatePipe],
})
export class InventoryManagement implements OnInit {
  inventory: InventoryItem[] = [];
  loading = true;

  // Map display label → backend choice key
  readonly TYPE_MAP: { [key: string]: string } = {
    'Prepared': 'prepared',
    'Produce': 'produce',
    'Refrigerated': 'refrigerated',
    'Shelf Stable': 'stable'
  };

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.fetchInventory();
  }

  // ---------------- CSRF ----------------
  getCsrfToken(): string {
    const name = 'csrftoken=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (let c of ca) {
      c = c.trim();
      if (c.indexOf(name) === 0) return c.substring(name.length, c.length);
    }
    return '';
  }

  getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'X-CSRFToken': this.getCsrfToken(),
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    });
  }

  // ---------------- Fetch Inventory ----------------
  fetchInventory(): void {
    this.loading = true;
    this.http
      .get<{ inventory: InventoryItem[] }>('http://localhost:8000/inventory/', { withCredentials: true })
      .subscribe({
        next: (response) => {
          this.inventory = (response.inventory || []).map(item => ({
            ...item,
            quantity: +item.quantity || 0,
            expiryDate: item.expiration ? new Date(item.expiration) : null,
            donated: false
          }));
          this.loading = false;
        },
        error: (err: HttpErrorResponse) => {
          console.error('Error fetching inventory:', err.message);
          this.loading = false;
        }
      });
  }

  // ---------------- Navigation ----------------
  goToHome(): void { this.router.navigate(['/home']); }
  goToAccount(): void { this.router.navigate(['/account']); }
  goToInventory(): void { this.router.navigate(['/inventory-management']); }
  goToOrders(): void { this.router.navigate(['/order-history']); }

  // ---------------- Donate Item ----------------
  donateItem(item: InventoryItem): void {
    if (item.quantity <= 0) return;

    const newQuantity = item.quantity - 1;

    const payload = {
      item_name: item.name,
      attributes: ['quantity'],            // update quantity in backend
      values: [newQuantity.toString()]     // backend expects integer as string
    };

    this.http.put<EditInventoryResponse>('http://localhost:8000/inventory/edit/', payload, {
      headers: this.getHeaders(),
      withCredentials: true
    }).subscribe({
      next: (res) => {
        console.log('Donation marked:', res.details);
        // Update frontend immediately
        item.quantity = newQuantity;
        if (item.quantity <= 0) item.donated = true;
      },
      error: (err: HttpErrorResponse) => {
        console.error('Backend PUT error:', err.message);
      }
    });
  }

  // ---------------- Logout ----------------
  logout(): void {
    this.http.post('http://localhost:8000/logout/', {}, {
      headers: this.getHeaders(),
      withCredentials: true
    }).subscribe({
      next: () => {
        console.log('Logged out successfully');
        this.router.navigate(['/login']);
      },
      error: (err: HttpErrorResponse) => {
        console.error('Error logging out:', err.message);
      }
    });
  }
}
