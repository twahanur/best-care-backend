import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, UnauthorizedException, ForbiddenException, BadRequestException } from '@nestjs/common';
import { AuthService } from '../src/modules/auth/auth.service';
import { BookingsService } from '../src/modules/bookings/bookings.service';
import { PaymentsService } from '../src/modules/payments/payments.service';
import { CarsService } from '../src/modules/cars/cars.service';
import { JwtUtil } from '../src/common/security/jwt.util';
import { sanitizeText } from '../src/common/security/sanitize.util';

describe('Security & Vulnerability Audit Verification', () => {
  let authService: AuthService;
  let bookingsService: BookingsService;
  let paymentsService: PaymentsService;
  let carsService: CarsService;

  beforeEach(async () => {
    authService = new AuthService();
    carsService = new CarsService();
    paymentsService = new PaymentsService();
    bookingsService = new BookingsService(carsService, paymentsService);
  });

  describe('1. Login Bypass & Password Verification', () => {
    it('should REJECT login when password is omitted', () => {
      expect(() => {
        authService.login({ email: 'admin@rentcars.com' });
      }).toThrow(UnauthorizedException);
    });

    it('should REJECT login with incorrect password', () => {
      expect(() => {
        authService.login({ email: 'admin@rentcars.com', password: 'wrongpassword' });
      }).toThrow(UnauthorizedException);
    });

    it('should SUCCEED login with correct password and return signed JWT token', () => {
      const res = authService.login({ email: 'admin@rentcars.com', password: 'admin123' });
      expect(res.accessToken).toBeDefined();
      const payload = JwtUtil.verify(res.accessToken);
      expect(payload.email).toBe('admin@rentcars.com');
      expect(payload.role).toBe('ADMIN');
    });

    it('should REJECT forged or tampered JWT tokens', () => {
      expect(() => {
        JwtUtil.verify('forged_fake_token_123');
      }).toThrow();
    });
  });

  describe('2. Privilege Escalation Protection', () => {
    it('should NOT allow registering users to escalate role to ADMIN', () => {
      const res = authService.register({
        name: 'Attacker',
        email: `attacker_${Date.now()}@evil.com`,
        password: 'password123',
        ...({ role: 'ADMIN' } as any)
      });
      expect(res.user.role).toBe('CUSTOMER');
    });
  });

  describe('3. Content Injection & XSS Sanitization', () => {
    it('should strip script tags and dangerous HTML from user inputs', () => {
      const raw = '<script>alert("XSS")</script><b>Test User</b>';
      const clean = sanitizeText(raw);
      expect(clean).toBe('Test User');
      expect(clean).not.toContain('<script>');
    });
  });

  describe('4. Business Logic & Payment Manipulation', () => {
    it('should REJECT negative payment amounts', () => {
      expect(() => {
        paymentsService.create({
          bookingId: 'bkg_1001',
          userId: 'usr_cust_1',
          customerName: 'Test',
          amount: -500
        });
      }).toThrow(BadRequestException);
    });

    it('should REJECT zero payment amounts', () => {
      expect(() => {
        paymentsService.create({
          bookingId: 'bkg_1001',
          userId: 'usr_cust_1',
          customerName: 'Test',
          amount: 0
        });
      }).toThrow(BadRequestException);
    });

    it('should REJECT invalid booking date ranges where dropoff is before pickup', () => {
      expect(() => {
        bookingsService.create({
          carId: 'car_jaguar_xe',
          pickupDate: '2026-09-10T10:00:00Z',
          dropoffDate: '2026-09-05T10:00:00Z', // Before pickup!
          userId: 'usr_cust_1'
        });
      }).toThrow(BadRequestException);
    });
  });
});
