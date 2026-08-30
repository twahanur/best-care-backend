import { Test, TestingModule } from '@nestjs/testing';
import { BookingsService } from './bookings.service';
import { CarsService } from '../cars/cars.service';
import { PaymentsService } from '../payments/payments.service';

describe('BookingsService', () => {
  let service: BookingsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [BookingsService, CarsService, PaymentsService],
    }).compile();

    service = module.get<BookingsService>(BookingsService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should return seed bookings', () => {
    const bookings = service.findAll();
    expect(bookings.length).toBeGreaterThanOrEqual(4);
  });

  it('should create a new booking with calculated total and protection fee', () => {
    const newBooking = service.create({
      vehicleId: 'car_prado_suv',
      vehicleName: 'Toyota Land Cruiser Prado TX',
      customerName: 'Tareq Rahman',
      customerEmail: 'tareq@test.com',
      customerPhone: '+8801700112233',
      pickupDate: '2026-09-10T10:00:00Z',
      dropoffDate: '2026-09-13T10:00:00Z',
      pickupLocation: 'Dhaka Airport',
      dropoffLocation: 'Dhaka Airport',
      totalDays: 3,
      dailyRate: 145,
      protectionPlan: 'Comprehensive Plus',
      notes: 'Test booking'
    });

    expect(newBooking).toBeDefined();
    expect(newBooking.bookingCode).toContain('RC-BK-');
    expect(newBooking.protectionFee).toBe(18 * 3); // 54
    expect(newBooking.totalAmount).toBe(145 * 3 + 54); // 489
  });

  it('should update booking status', () => {
    const updated = service.updateStatus('bkg_1003', 'Confirmed');
    expect(updated.status).toBe('Confirmed');
  });
});
