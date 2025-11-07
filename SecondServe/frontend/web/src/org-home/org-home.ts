import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

interface InventoryItem {
  id: number;
  name: string;
  quantity: number;
  expiryDate: string;
  type: string;
}

@Component({
  selector: 'app-org-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './org-home.html',
  styleUrls: ['./org-home.css'],
})
export class OrgHome implements OnInit {
  inventory: InventoryItem[] = [];
  loading = false;
  error: string | null = null;
  editItemId: number | null = null;
  newItem = { name: '', quantity: 0, expiryDate: '', type: 'prepared' };
  private apiUrl = 'http://localhost:8000/inventory';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.loadData();
  }

  /** ==================== CSRF TOKEN HELPERS ==================== */
  private getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
  }

  private async getCsrfToken(): Promise<void> {
    await this.http
      .get('http://localhost:8000/api/csrf/', { withCredentials: true })
      .toPromise()
      .catch(() => {});
  }

  private async makeHeaders(): Promise<HttpHeaders> {
    await this.getCsrfToken();
    const csrfToken = this.getCookie('csrftoken') || '';
    return new HttpHeaders({
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
      Accept: 'application/json',
    });
  }

  /** ==================== UTILITIES ==================== */
  private mapTypeToKey(type: string): string {
    switch (type.toLowerCase()) {
      case 'prepared':
        return 'prepared';
      case 'produce':
        return 'produce';
      case 'refrigerated':
        return 'refrigerated';
      case 'shelf stable':
        return 'stable';
      default:
        return 'prepared';
    }
  }

  /** Format date as "November 14, 2025" (for Django backend) */
  private formatDateForBackend(dateStr: string): string {
    const dateObj = new Date(dateStr);
    if (isNaN(dateObj.getTime())) return dateStr; // fallback
    return dateObj.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  }

  /** ==================== LOAD INVENTORY ==================== */
  loadData(): void {
    this.loading = true;
    this.error = null;

    this.http
      .get<{ inventory: any[] }>(`${this.apiUrl}/`, { withCredentials: true })
      .subscribe({
        next: (data) => {
          this.inventory = data.inventory.map((item, idx) => ({
            id: idx + 1,
            name: item.name,
            quantity: item.quantity,
            expiryDate: item.expiration,
            type: item.type || 'prepared',
          }));
          this.loading = false;
        },
        error: (err) => {
          console.error(err);
          this.error = 'Failed to load inventory.';
          this.loading = false;
        },
      });
  }

  /** ==================== ADD ITEM ==================== */
  async addItem(): Promise<void> {
    if (!this.newItem.name || !this.newItem.expiryDate || this.newItem.quantity <= 0) {
      alert('Please fill all fields correctly.');
      return;
    }

    const headers = await this.makeHeaders();

    const formattedDate = this.formatDateForBackend(this.newItem.expiryDate);

    const payload = {
      name: this.newItem.name.trim(),
      quantity: this.newItem.quantity,
      expiration: formattedDate,
      type: this.mapTypeToKey(this.newItem.type),
    };

    this.http
      .post(`${this.apiUrl}/add/`, payload, { headers, withCredentials: true })
      .subscribe({
        next: () => {
          alert('✅ Item added successfully!');
          this.newItem = { name: '', quantity: 0, expiryDate: '', type: 'prepared' };
          this.loadData();
        },
        error: (err) => {
          console.error(err);
          alert('❌ Failed to add item: ' + (err.error?.details || err.message));
        },
      });
  }

  /** ==================== EDIT ITEM ==================== */
  async saveEdit(item: InventoryItem): Promise<void> {
    const headers = await this.makeHeaders();

    const quantity = parseInt(item.quantity as any, 10);
    if (isNaN(quantity) || quantity < 0) {
      alert('Invalid quantity value');
      return;
    }

    const formattedDate = this.formatDateForBackend(item.expiryDate);

    const payload = {
      item_name: String(item.name).trim(),
      attributes: ['name', 'quantity', 'expiration', 'type'],
      values: [
        String(item.name).trim(),
        String(item.quantity),
        formattedDate,
        this.mapTypeToKey(item.type),
      ],
    };

    console.log('Sending payload:', payload);

    this.http
      .put(`${this.apiUrl}/edit/`, payload, { headers, withCredentials: true })
      .subscribe({
        next: () => {
          alert('✅ Item updated successfully!');
          this.editItemId = null;
          this.loadData();
        },
        error: (err) => {
          console.error('Backend error:', err);
          alert('❌ Failed to update item: ' + (err.error?.details || err.message));
        },
      });
  }

  /** ==================== DONATE ITEM ==================== */
  async donateItem(item: InventoryItem): Promise<void> {
    if (!confirm(`Mark "${item.name}" as donated?`)) return;
    const headers = await this.makeHeaders();

    this.http
      .put(
        `${this.apiUrl}/edit/`,
        {
          item_name: item.name,
          attributes: ['quantity'],
          values: [0],
        },
        { headers, withCredentials: true }
      )
      .subscribe({
        next: () => {
          alert('🎉 Item marked as donated!');
          this.loadData();
        },
        error: (err) => {
          console.error(err);
          alert('❌ Failed to update donation: ' + (err.error?.details || err.message));
        },
      });
  }

  /** ==================== NAVIGATION ==================== */
  goToAccount(): void {
    this.router.navigate(['/org-account']);
  }
  goToHome(): void {
    this.router.navigate(['/org-home']);
  }
  goToOrders(): void {
    this.router.navigate(['/org-history']);
  }
  goToInventory(): void {
    this.router.navigate(['/inventory']);
  }
  logout(): void {
    localStorage.removeItem('authToken');
    this.router.navigate(['/login']);
  }
}
