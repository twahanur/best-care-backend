import { Module } from '@nestjs/common';
import { ReportsService } from './reports.service';
import { ReportsController } from './reports.controller';
import { BookingsModule } from '../bookings/bookings.module';
import { CarsModule } from '../cars/cars.module';
import { PaymentsModule } from '../payments/payments.module';

@Module({
  imports: [BookingsModule, CarsModule, PaymentsModule],
  controllers: [ReportsController],
  providers: [ReportsService],
  exports: [ReportsService],
})
export class ReportsModule {}
