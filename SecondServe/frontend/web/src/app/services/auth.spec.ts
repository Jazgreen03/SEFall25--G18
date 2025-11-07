// src/app/services/auth.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { AuthService } from './auth.service';

describe('AuthService (edge cases)', () => {
  let service: AuthService;

  // Mock sessionStorage
  const store: Record<string, string> = {};
  const mockSessionStorage = {
    getItem: (key: string): string | null => store[key] !== undefined ? store[key] : null, // Fixed: don't use || null
    setItem: (key: string, value: string) => {
      store[key] = value;
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      Object.keys(store).forEach(key => delete store[key]);
    }
  };

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [AuthService] });
    service = TestBed.inject(AuthService);

    spyOn(sessionStorage, 'getItem').and.callFake(mockSessionStorage.getItem);
    spyOn(sessionStorage, 'setItem').and.callFake(mockSessionStorage.setItem);
    spyOn(sessionStorage, 'removeItem').and.callFake(mockSessionStorage.removeItem);

    service.clearRole();
    mockSessionStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#setRole', () => {
    it('should set and overwrite roles correctly', () => {
      service.setRole('user');
      expect(service.getRole()).toBe('user');

      service.setRole('driver');
      expect(service.getRole()).toBe('driver');
      expect(sessionStorage.setItem).toHaveBeenCalledWith('userRole', 'driver');
    });

    it('should accept empty string as a role', () => {
      service.setRole('');
      expect(service.getRole()).toBe(''); // This should work now with the fixed mock
    });

    // Remove this test - your AuthService doesn't convert types
    // it('should convert non-string input to string', () => {
    //   // @ts-expect-error role should be non-empty string
    //   service.setRole(123);
    //   expect(service.getRole()).toBe('123');
    // });
  });

  describe('#getRole', () => {
    it('should return null if sessionStorage is empty and role not in memory', () => {
      const role = service.getRole();
      expect(role).toBeNull();
    });

    it('should handle repeated clearRole calls gracefully', () => {
      service.setRole('user');
      service.clearRole();
      service.clearRole();
      expect(service.getRole()).toBeNull();
    });

    it('should handle sessionStorage throwing error', () => {
      // Simulate sessionStorage.getItem throwing
      (sessionStorage.getItem as jasmine.Spy).and.callFake(() => { throw new Error('Storage error'); });
      expect(() => service.getRole()).toThrowError('Storage error');
    });
  });

  describe('#clearRole', () => {
    it('should clear role from memory and sessionStorage', () => {
      service.setRole('user');
      service.clearRole();
      expect(service.getRole()).toBeNull();
      expect(sessionStorage.removeItem).toHaveBeenCalledWith('userRole');
    });

    it('should not throw when clearing an already cleared role', () => {
      service.clearRole();
      expect(() => service.clearRole()).not.toThrow();
    });
  });

  // Add test for memory caching behavior
  describe('Memory caching', () => {
    it('should return role from memory without hitting sessionStorage', () => {
      service.setRole('user');

      // Clear the sessionStorage mock calls
      (sessionStorage.getItem as jasmine.Spy).calls.reset();

      const role = service.getRole();
      expect(role).toBe('user');
      expect(sessionStorage.getItem).not.toHaveBeenCalled();
    });

    it('should fall back to sessionStorage when memory is cleared', () => {
      service.setRole('user');
      service.clearRole();

      // Manually set sessionStorage to simulate persisted data
      mockSessionStorage.setItem('userRole', 'organization');

      const role = service.getRole();
      expect(role).toBe('organization');
      expect(sessionStorage.getItem).toHaveBeenCalledWith('userRole');
    });
  });
});