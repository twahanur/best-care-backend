import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { APP_GUARD, APP_FILTER } from '@nestjs/core';
import { AuthModule } from './modules/auth/auth.module';
import { CarsModule } from './modules/cars/cars.module';
import { VehiclesModule } from './modules/vehicles/vehicles.module';
import { BookingsModule } from './modules/bookings/bookings.module';
import { PaymentsModule } from './modules/payments/payments.module';
import { ReviewsModule } from './modules/reviews/reviews.module';
import { AvailabilityModule } from './modules/availability/availability.module';
import { PricingModule } from './modules/pricing/pricing.module';
import { ReportsModule } from './modules/reports/reports.module';
import { AnalyticsModule } from './modules/analytics/analytics.module';
import { AiProxyModule } from './modules/ai-proxy/ai-proxy.module';
import { AutomationModule } from './modules/automation/automation.module';
import { GlobalHttpExceptionFilter } from './common/filters/http-exception.filter';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    // Rate Limiting: 120 requests per 60 seconds window per IP
    ThrottlerModule.forRoot([{
      ttl: 60000,
      limit: 120,
    }]),
    AuthModule,
    CarsModule,
    VehiclesModule,
    BookingsModule,
    PaymentsModule,
    ReviewsModule,
    AvailabilityModule,
    PricingModule,
    ReportsModule,
    AnalyticsModule,
    AiProxyModule,
    AutomationModule,
  ],
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard,
    },
    {
      provide: APP_FILTER,
      useClass: GlobalHttpExceptionFilter,
    },
  ],
})
export class AppModule {}
