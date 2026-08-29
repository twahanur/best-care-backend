import { Module } from '@nestjs/common';
import { AnalyticsService } from './analytics.service';
import { AnalyticsController } from './analytics.controller';
import { BookingsModule } from '../bookings/bookings.module';
import { VehiclesModule } from '../vehicles/vehicles.module';

@Module({
  imports: [BookingsModule, VehiclesModule],
  controllers: [AnalyticsController],
  providers: [AnalyticsService],
  exports: [AnalyticsService]
})
export class AnalyticsModule {}
