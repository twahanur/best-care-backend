import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { Booking, BookingStatus, ProtectionPlan } from '../../common/types/schema.types';
import { CarsService } from '../cars/cars.service';
import { PaymentsService } from '../payments/payments.service';
import { sanitizeText } from '../../common/security/sanitize.util';

@Injectable()
export class BookingsService {
  constructor(
    private readonly carsService: CarsService,
    private readonly paymentsService: PaymentsService,
  ) {}

  private bookings: Booking[] = [
    {
      id: 'bkg_1001',
      bookingCode: 'RC-BK-78901',
      userId: 'usr_cust_1',
      customerName: 'Shahriar Khan',
      customerEmail: 'shahriar@example.com',
      customerPhone: '+8801819234567',
      carId: 'car_jaguar_xe',
      vehicleName: 'Jaguar XE L Prestige',
      vehicleImage: 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80',
      pickupDate: '2026-08-28T09:00:00Z',
      dropoffDate: '2026-09-02T18:00:00Z',
      pickupLocation: 'Hazrat Shahjalal Intl Airport (DAC)',
      dropoffLocation: 'Hazrat Shahjalal Intl Airport (DAC)',
      totalDays: 5,
      dailyRate: 85,
      baseAmount: 425,
      protectionPlan: 'Comprehensive Plus',
      protectionFee: 90,
      securityDeposit: 250,
      discountAmount: 0,
      totalAmount: 515,
      status: 'Active',
      paymentStatus: 'Paid',
      notes: 'Corporate client VIP airport pick-up.',
      createdAt: '2026-08-27T14:30:00Z',
      updatedAt: '2026-08-27T14:30:00Z'
    },
    {
      id: 'bkg_1002',
      bookingCode: 'RC-BK-78902',
      userId: 'usr_cust_2',
      customerName: 'Nusrat Jahan',
      customerEmail: 'nusrat@example.com',
      customerPhone: '+8801711987654',
      carId: 'car_audi_a6',
      vehicleName: 'Audi A6 Business Executive',
      vehicleImage: 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=800&q=80',
      pickupDate: '2026-08-30T10:00:00Z',
      dropoffDate: '2026-09-01T20:00:00Z',
      pickupLocation: 'Gulshan Diplomatic Zone, Dhaka',
      dropoffLocation: 'Hazrat Shahjalal Intl Airport (DAC)',
      totalDays: 2,
      dailyRate: 95,
      baseAmount: 190,
      protectionPlan: 'VIP Full Shield',
      protectionFee: 60,
      securityDeposit: 300,
      discountAmount: 0,
      totalAmount: 250,
      status: 'Confirmed',
      paymentStatus: 'Paid',
      notes: 'VIP Airport transfer for regional managing director.',
      createdAt: '2026-08-28T09:15:00Z',
      updatedAt: '2026-08-28T09:15:00Z'
    },
    {
      id: 'bkg_1003',
      bookingCode: 'RC-BK-78903',
      userId: 'usr_cust_1',
      customerName: 'Shahriar Khan',
      customerEmail: 'shahriar@example.com',
      customerPhone: '+8801912345678',
      carId: 'car_tesla_modely',
      vehicleName: 'Tesla Model Y Long Range',
      vehicleImage: 'https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=800&q=80',
      pickupDate: '2026-09-03T08:00:00Z',
      dropoffDate: '2026-09-07T18:00:00Z',
      pickupLocation: 'Banani Central Hub',
      dropoffLocation: 'Banani Central Hub',
      totalDays: 4,
      dailyRate: 110,
      baseAmount: 440,
      protectionPlan: 'Basic CDW',
      protectionFee: 0,
      securityDeposit: 300,
      discountAmount: 0,
      totalAmount: 440,
      status: 'Pending',
      paymentStatus: 'Pending',
      notes: 'Family weekend eco tour along Padma Expressway.',
      createdAt: '2026-08-28T16:45:00Z',
      updatedAt: '2026-08-28T16:45:00Z'
    },
    {
      id: 'bkg_1004',
      bookingCode: 'RC-BK-78904',
      userId: 'usr_cust_1',
      customerName: 'Shahriar Khan',
      customerEmail: 'shahriar@example.com',
      customerPhone: '+8801819234567',
      carId: 'car_hyundai_tucson',
      vehicleName: 'Hyundai Tucson Limited Edition',
      vehicleImage: 'https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=800&q=80',
      pickupDate: '2026-08-15T08:00:00Z',
      dropoffDate: '2026-08-18T18:00:00Z',
      pickupLocation: 'Gulshan Diplomatic Zone, Dhaka',
      dropoffLocation: 'Gulshan Diplomatic Zone, Dhaka',
      totalDays: 3,
      dailyRate: 75,
      baseAmount: 225,
      protectionPlan: 'Comprehensive Plus',
      protectionFee: 54,
      securityDeposit: 200,
      discountAmount: 0,
      totalAmount: 279,
      status: 'Completed',
      paymentStatus: 'Paid',
      notes: 'Weekend client meeting commute.',
      createdAt: '2026-08-14T11:20:00Z',
      updatedAt: '2026-08-14T11:20:00Z'
    }
  ];

  findAll(status?: string, search?: string, userId?: string): Booking[] {
    let result = [...this.bookings];

    if (userId) {
      result = result.filter(b => b.userId === userId);
    }

    if (status && status !== 'All') {
      result = result.filter(b => b.status.toLowerCase() === status.toLowerCase());
    }

    if (search) {
      const q = search.toLowerCase();
      result = result.filter(b =>
        b.bookingCode.toLowerCase().includes(q) ||
        b.customerName.toLowerCase().includes(q) ||
        b.customerEmail.toLowerCase().includes(q) ||
        b.vehicleName.toLowerCase().includes(q)
      );
    }

    return result;
  }

  findOne(id: string): Booking {
    const booking = this.bookings.find(b => b.id === id || b.bookingCode === id);
    if (!booking) {
      throw new NotFoundException(`Booking with ID/Code "${id}" not found.`);
    }
    return booking;
  }

  create(dto: any, aiLeadScore?: any): Booking {
    const carId = dto.carId || dto.vehicleId;
    if (!carId) {
      throw new BadRequestException('Car ID is required to create a booking.');
    }

    const car = this.carsService.findOne(carId);
    if (!car) {
      throw new NotFoundException('Selected vehicle was not found.');
    }

    // BUSINESS LOGIC VALIDATION: Validate Dates
    let pickupDate = dto.pickupDate;
    let dropoffDate = dto.dropoffDate;
    let totalDays = Number(dto.totalDays) || 1;

    if (pickupDate && dropoffDate) {
      const pTime = new Date(pickupDate).getTime();
      const dTime = new Date(dropoffDate).getTime();
      if (isNaN(pTime) || isNaN(dTime) || dTime <= pTime) {
        throw new BadRequestException('Invalid booking date range: dropoff date must be after pickup date.');
      }
      totalDays = Math.max(1, Math.ceil((dTime - pTime) / (1000 * 60 * 60 * 24)));
    } else {
      pickupDate = new Date().toISOString();
      const nextDate = new Date();
      nextDate.setDate(nextDate.getDate() + totalDays);
      dropoffDate = nextDate.toISOString();
    }

    // Server-side calculated rates
    const dailyRate = car.dailyRate;
    const plan: ProtectionPlan = dto.protectionPlan || 'Comprehensive Plus';
    let dailyProtectionFee = 0;
    if (plan === 'Comprehensive Plus') dailyProtectionFee = 18;
    else if (plan === 'VIP Full Shield') dailyProtectionFee = 30;

    const protectionFee = dailyProtectionFee * totalDays;
    const baseAmount = dailyRate * totalDays;
    const discountAmount = Math.max(0, Number(dto.discountAmount) || 0);
    const totalAmount = Math.max(0, baseAmount + protectionFee - discountAmount);

    const id = `bkg_${Date.now()}`;
    const randomCode = `RC-BK-${Math.floor(10000 + Math.random() * 90000)}`;

    const newBooking: Booking = {
      id,
      bookingCode: randomCode,
      userId: dto.userId || 'usr_cust_1',
      customerName: sanitizeText(dto.customerName) || 'Customer',
      customerEmail: (dto.customerEmail || 'customer@example.com').toLowerCase().trim(),
      customerPhone: sanitizeText(dto.customerPhone) || '+8801700000000',
      carId: car.id,
      vehicleName: car.name,
      vehicleImage: car.images && car.images[0] ? car.images[0] : 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80',
      pickupDate,
      dropoffDate,
      pickupLocation: sanitizeText(dto.pickupLocation) || 'Hazrat Shahjalal Intl Airport (DAC)',
      dropoffLocation: sanitizeText(dto.dropoffLocation) || 'Hazrat Shahjalal Intl Airport (DAC)',
      totalDays,
      dailyRate,
      baseAmount,
      protectionPlan: plan,
      protectionFee,
      securityDeposit: car.securityDeposit || 200,
      discountAmount,
      totalAmount,
      status: 'Confirmed',
      paymentStatus: 'Paid',
      notes: sanitizeText(dto.notes) || '',
      aiLeadScore: aiLeadScore || {
        score: 82,
        classification: 'Hot',
        priority: 'High (Immediate 15-min SLA)',
        suggestedAction: 'Send automated confirmation pass and assign vehicle inspection.'
      },
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.bookings.unshift(newBooking);

    // Auto-record completed payment using verified server totalAmount
    this.paymentsService.create({
      bookingId: newBooking.id,
      bookingCode: newBooking.bookingCode,
      userId: newBooking.userId,
      customerName: newBooking.customerName,
      amount: newBooking.totalAmount,
      paymentMethod: dto.paymentMethod || 'Credit Card'
    });

    return newBooking;
  }

  updateStatus(id: string, newStatus: BookingStatus): Booking {
    const booking = this.findOne(id);
    booking.status = newStatus;
    booking.updatedAt = new Date().toISOString();

    if (newStatus === 'Active') {
      this.carsService.updateCarStatus(booking.carId, 'RENTED');
    } else if (newStatus === 'Completed' || newStatus === 'Cancelled') {
      this.carsService.updateCarStatus(booking.carId, 'AVAILABLE');
    }

    return booking;
  }

  cancelBooking(id: string, reason: string): Booking {
    const booking = this.findOne(id);
    if (booking.status === 'Completed' || booking.status === 'Cancelled') {
      throw new BadRequestException(`Cannot cancel a booking that is already ${booking.status}.`);
    }

    booking.status = 'Cancelled';
    booking.cancellationReason = sanitizeText(reason) || 'Customer requested free cancellation.';
    booking.cancelledAt = new Date().toISOString();
    booking.refundAmount = booking.totalAmount;
    booking.paymentStatus = 'Refunded';
    booking.updatedAt = new Date().toISOString();

    // Release vehicle & process payment refund
    this.carsService.updateCarStatus(booking.carId, 'AVAILABLE');
    this.paymentsService.refund(booking.id, reason);

    return booking;
  }

  processRentalReturn(id: string, inspection: { returnOdometer: number; returnFuelLevel: number; returnDamageNotes?: string; extraCharges?: number }): Booking {
    const booking = this.findOne(id);
    booking.status = 'Completed';
    booking.updatedAt = new Date().toISOString();
    
    // Release vehicle
    this.carsService.updateCarStatus(booking.carId, 'AVAILABLE');

    return booking;
  }

  createPosBooking(dto: any): Booking {
    return this.create({
      ...dto,
      notes: `POS Walk-in Counter Order: ${dto.notes || 'Instant Desk Checkout'}`
    });
  }

  getDriverBookings(driverId: string): Booking[] {
    return this.bookings.filter(b => b.driverId === driverId || (!b.driverId && b.withDriver));
  }

  driverRespondToTrip(id: string, driverId: string, action: 'ACCEPT' | 'REJECT'): Booking {
    const booking = this.findOne(id);
    if (action === 'ACCEPT') {
      booking.driverId = driverId;
      booking.driverTripStatus = 'ACCEPTED';
      booking.status = 'Confirmed';
    } else {
      booking.driverTripStatus = 'REJECTED';
      booking.driverId = undefined;
    }
    booking.updatedAt = new Date().toISOString();
    return booking;
  }

  updateDriverTripStatus(id: string, tripStatus: any): Booking {
    const booking = this.findOne(id);
    booking.driverTripStatus = tripStatus;
    booking.updatedAt = new Date().toISOString();

    if (tripStatus === 'TRIP_IN_PROGRESS') {
      booking.status = 'Active';
      this.carsService.updateCarStatus(booking.carId, 'RENTED');
    } else if (tripStatus === 'DROPOFF_COMPLETED') {
      booking.status = 'Completed';
      this.carsService.updateCarStatus(booking.carId, 'AVAILABLE');
    }

    return booking;
  }

  getCustomerBookings(userId: string): Booking[] {
    return this.bookings.filter(b => b.userId === userId);
  }

  getRecentBookings(limit: number = 5): Booking[] {
    return this.bookings.slice(0, limit);
  }

  getMetrics() {
    const totalBookings = this.bookings.length;
    const activeRentals = this.bookings.filter(b => b.status === 'Active').length;
    const totalRevenue = this.bookings
      .filter(b => b.status !== 'Cancelled')
      .reduce((sum, b) => sum + b.totalAmount, 0);

    return {
      totalBookings,
      activeRentals,
      totalRevenue,
      revenueGrowthPct: 15.8,
      fleetUtilizationRate: 88,
    };
  }

  getAllBookingsRaw(): Booking[] {
    return this.bookings;
  }
}
