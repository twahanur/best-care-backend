import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AuthModule } from './modules/auth/auth.module';
import { CarsModule } from './modules/cars/cars.module';
import { BookingsModule } from './modules/bookings/bookings.module';
import { PaymentsModule } from './modules/payments/payments.module';
import { ReviewsModule } from './modules/reviews/reviews.module';
import { AvailabilityModule } from './modules/availability/availability.module';
import { PricingModule } from './modules/pricing/pricing.module';
import { ReportsModule } from './modules/reports/reports.module';
import { AiProxyModule } from './modules/ai-proxy/ai-proxy.module';
import { AutomationModule } from './modules/automation/automation.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    AuthModule,
    CarsModule,
    BookingsModule,
    PaymentsModule,
    ReviewsModule,
    AvailabilityModule,
    PricingModule,
    ReportsModule,
    AiProxyModule,
    AutomationModule
  ]
})
export class AppModule {}
