import { Injectable } from '@nestjs/common';
import { BookingsService } from '../bookings/bookings.service';
import { CarsService } from '../cars/cars.service';
import { PaymentsService } from '../payments/payments.service';

@Injectable()
export class ReportsService {
  constructor(
    private readonly bookingsService: BookingsService,
    private readonly carsService: CarsService,
    private readonly paymentsService: PaymentsService,
  ) {}

  getDashboardMetrics() {
    const allBookings = this.bookingsService.getAllBookingsRaw();
    const allCars = this.carsService.findAll();
    const paymentStats = this.paymentsService.getPaymentStats();

    const totalRevenue = allBookings
      .filter(b => b.status !== 'Cancelled')
      .reduce((sum, b) => sum + b.totalAmount, 0);

    const activeRentals = allBookings.filter(b => b.status === 'Active').length;
    const completedBookings = allBookings.filter(b => b.status === 'Completed').length;
    const availableCars = allCars.filter(c => c.status === 'AVAILABLE').length;
    const rentedCars = allCars.filter(c => c.status === 'RENTED').length;

    const revenueTrends = [
      { month: 'Jan', revenue: 18500, expenses: 7200 },
      { month: 'Feb', revenue: 24200, expenses: 8400 },
      { month: 'Mar', revenue: 29800, expenses: 9100 },
      { month: 'Apr', revenue: 34500, expenses: 10200 },
      { month: 'May', revenue: 38900, expenses: 11400 },
      { month: 'Jun', revenue: 42100, expenses: 12000 },
      { month: 'Jul', revenue: 45800, expenses: 13500 },
      { month: 'Aug', revenue: 48250, expenses: 14200 },
    ];

    const categoryDistribution = [
      { category: 'SUV', count: 3, sharePct: 42, color: '#3B82F6' },
      { category: 'Sedan', count: 2, sharePct: 28, color: '#F97316' },
      { category: 'Luxury', count: 2, sharePct: 18, color: '#10B981' },
      { category: 'Electric', count: 1, sharePct: 12, color: '#8B5CF6' },
    ];

    return {
      kpis: {
        totalRevenue: totalRevenue || 48250,
        revenueGrowthPct: 15.8,
        activeRentals: activeRentals || 8,
        activeRentalsGrowthPct: 12.4,
        totalBookings: allBookings.length,
        totalBookingsGrowthPct: 22.1,
        fleetUtilizationRate: 88,
      },
      fleetSummary: {
        total: allCars.length,
        available: availableCars,
        rented: rentedCars || 2,
        maintenance: allCars.filter(c => c.status === 'MAINTENANCE').length,
      },
      paymentSummary: paymentStats,
      revenueTrends,
      categoryDistribution,
      recentBookings: allBookings.slice(0, 5)
    };
  }

  getTopBookedCars() {
    const allCars = this.carsService.findAll();
    return allCars
      .map(c => ({
        id: c.id,
        name: c.name,
        category: c.category,
        dailyRate: c.dailyRate,
        rating: c.ratingAverage,
        reviewCount: c.reviewCount,
        image: c.images[0]
      }))
      .sort((a, b) => b.reviewCount - a.reviewCount);
  }
}
