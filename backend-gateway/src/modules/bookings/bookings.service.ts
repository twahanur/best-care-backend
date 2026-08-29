import { Injectable, NotFoundException } from '@nestjs/common';
import { Booking, BookingStatus, ProtectionPlan } from './booking.interface';
import { CreateBookingDto } from './dto/create-booking.dto';
import { UpdateBookingStatusDto } from './dto/update-booking-status.dto';

@Injectable()
export class BookingsService {
  private bookings: Booking[] = [
    {
      id: 'bkg_1001',
      bookingCode: 'DP-BK-78901',
      vehicleId: 'car_prado_suv',
      vehicleName: 'Toyota Land Cruiser Prado TX',
      customerName: 'Shahriar Khan',
      customerEmail: 'shahriar.khan@apexholdings.com',
      customerPhone: '+8801819234567',
      pickupDate: '2026-08-28T09:00:00Z',
      dropoffDate: '2026-09-02T18:00:00Z',
      pickupLocation: 'Dhaka Hazrat Shahjalal International Airport (DAC)',
      dropoffLocation: 'Sylhet City Center Hub',
      totalDays: 5,
      dailyRate: 145,
      protectionPlan: 'Comprehensive Plus',
      protectionFee: 90, // $18 * 5
      totalAmount: 815,
      status: 'Active',
      paymentStatus: 'Paid',
      notes: 'Corporate client delegation trip to tea estates. VIP driver required.',
      aiLeadScore: {
        score: 92,
        classification: 'Hot',
        priority: 'High (Immediate 15-min SLA)',
        suggestedAction: 'Assign dedicated account manager, send priority quote with VIP Full Shield upgrade.'
      },
      createdAt: '2026-08-27T14:30:00Z'
    },
    {
      id: 'bkg_1002',
      bookingCode: 'DP-BK-78902',
      vehicleId: 'car_mercedes_eclass',
      vehicleName: 'Mercedes-Benz E-Class AMG Line',
      customerName: 'Nusrat Jahan',
      customerEmail: 'nusrat.jahan@unilever.bd',
      customerPhone: '+8801711987654',
      pickupDate: '2026-08-30T10:00:00Z',
      dropoffDate: '2026-09-01T20:00:00Z',
      pickupLocation: 'Gulshan Diplomatic Zone, Dhaka',
      dropoffLocation: 'Dhaka Hazrat Shahjalal International Airport (DAC)',
      totalDays: 2,
      dailyRate: 160,
      protectionPlan: 'VIP Full Shield',
      protectionFee: 60, // $30 * 2
      totalAmount: 380,
      status: 'Confirmed',
      paymentStatus: 'Paid',
      notes: 'VIP Airport transfer for regional managing director.',
      aiLeadScore: {
        score: 88,
        classification: 'Hot',
        priority: 'High (Immediate 15-min SLA)',
        suggestedAction: 'Executive chauffeur pre-assigned with vehicle detailing inspection.'
      },
      createdAt: '2026-08-28T09:15:00Z'
    },
    {
      id: 'bkg_1003',
      bookingCode: 'DP-BK-78903',
      vehicleId: 'car_tesla_modely',
      vehicleName: 'Tesla Model Y Long Range',
      customerName: 'Farhan Chowdhury',
      customerEmail: 'farhan.tech@gmail.com',
      customerPhone: '+8801912345678',
      pickupDate: '2026-09-03T08:00:00Z',
      dropoffDate: '2026-09-07T18:00:00Z',
      pickupLocation: 'Banani Central Hub',
      dropoffLocation: 'Banani Central Hub',
      totalDays: 4,
      dailyRate: 110,
      protectionPlan: 'Basic CDW',
      protectionFee: 0,
      totalAmount: 440,
      status: 'Pending',
      paymentStatus: 'Pending',
      notes: 'Family weekend eco tour along Padma Expressway.',
      aiLeadScore: {
        score: 68,
        classification: 'Warm',
        priority: 'Medium (Within 2 hours)',
        suggestedAction: 'Send automated booking confirmation email with vehicle spec sheet.'
      },
      createdAt: '2026-08-28T16:45:00Z'
    },
    {
      id: 'bkg_1004',
      bookingCode: 'DP-BK-78904',
      vehicleId: 'car_camry_hybrid',
      vehicleName: 'Toyota Camry Premium Hybrid',
      customerName: 'Anisur Rahman',
      customerEmail: 'anisur.r@standardbank.com',
      customerPhone: '+8801612345678',
      pickupDate: '2026-08-20T08:00:00Z',
      dropoffDate: '2026-08-24T18:00:00Z',
      pickupLocation: 'Motijheel Commercial Area',
      dropoffLocation: 'Chittagong Port City Hub',
      totalDays: 4,
      dailyRate: 70,
      protectionPlan: 'Comprehensive Plus',
      protectionFee: 72,
      totalAmount: 352,
      status: 'Completed',
      paymentStatus: 'Paid',
      notes: 'Inter-city branch audit commute.',
      aiLeadScore: {
        score: 74,
        classification: 'Warm',
        priority: 'Medium',
        suggestedAction: 'Send customer feedback survey and loyalty discount.'
      },
      createdAt: '2026-08-19T11:20:00Z'
    },
    {
      id: 'bkg_1005',
      bookingCode: 'DP-BK-78905',
      vehicleId: 'car_mustang_gt',
      vehicleName: 'Ford Mustang GT V8 Convertible',
      customerName: 'Arman Latif',
      customerEmail: 'arman.l@creativepulse.io',
      customerPhone: '+8801512345678',
      pickupDate: '2026-08-29T10:00:00Z',
      dropoffDate: '2026-08-31T18:00:00Z',
      pickupLocation: 'Dhanmondi Hub',
      dropoffLocation: 'Coxs Bazar Beach Hub',
      totalDays: 2,
      dailyRate: 175,
      protectionPlan: 'VIP Full Shield',
      protectionFee: 60,
      totalAmount: 410,
      status: 'Active',
      paymentStatus: 'Paid',
      notes: 'Scenic photoshoot & weekend tour.',
      aiLeadScore: {
        score: 85,
        classification: 'Hot',
        priority: 'High',
        suggestedAction: 'Pre-authorize deposit and verify sport driving agreement.'
      },
      createdAt: '2026-08-28T18:00:00Z'
    }
  ];

  findAll(status?: string, search?: string): Booking[] {
    let result = [...this.bookings];

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

  create(dto: CreateBookingDto, aiLeadScore?: any): Booking {
    const id = `bkg_${Date.now()}`;
    const randomCodeSuffix = Math.floor(10000 + Math.random() * 90000);
    const bookingCode = `DP-BK-${randomCodeSuffix}`;

    const plan = dto.protectionPlan || 'Basic CDW';
    let dailyProtectionFee = 0;
    if (plan === 'Comprehensive Plus') dailyProtectionFee = 18;
    else if (plan === 'VIP Full Shield') dailyProtectionFee = 30;

    const protectionFee = dailyProtectionFee * dto.totalDays;
    const totalAmount = (dto.dailyRate * dto.totalDays) + protectionFee;

    const newBooking: Booking = {
      id,
      bookingCode,
      vehicleId: dto.vehicleId,
      vehicleName: dto.vehicleName,
      customerName: dto.customerName,
      customerEmail: dto.customerEmail,
      customerPhone: dto.customerPhone,
      pickupDate: dto.pickupDate,
      dropoffDate: dto.dropoffDate,
      pickupLocation: dto.pickupLocation,
      dropoffLocation: dto.dropoffLocation,
      totalDays: dto.totalDays,
      dailyRate: dto.dailyRate,
      protectionPlan: plan,
      protectionFee,
      totalAmount,
      status: 'Confirmed',
      paymentStatus: 'Paid',
      notes: dto.notes || '',
      aiLeadScore: aiLeadScore || {
        score: 75,
        classification: 'Warm',
        priority: 'Medium (Within 2 hours)',
        suggestedAction: 'Send automated confirmation and vehicle check-in guide.'
      },
      createdAt: new Date().toISOString()
    };

    this.bookings.unshift(newBooking);
    return newBooking;
  }

  updateStatus(id: string, dto: UpdateBookingStatusDto): Booking {
    const booking = this.findOne(id);
    booking.status = dto.status;
    return booking;
  }

  getRecentBookings(limit: number = 5): Booking[] {
    return this.bookings.slice(0, limit);
  }

  getAllBookingsRaw(): Booking[] {
    return this.bookings;
  }
}
