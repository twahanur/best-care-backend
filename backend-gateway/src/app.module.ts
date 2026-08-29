import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { VehiclesModule } from './modules/vehicles/vehicles.module';
import { BookingsModule } from './modules/bookings/bookings.module';
import { AnalyticsModule } from './modules/analytics/analytics.module';
import { AiProxyModule } from './modules/ai-proxy/ai-proxy.module';
import { AutomationModule } from './modules/automation/automation.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    VehiclesModule,
    BookingsModule,
    AnalyticsModule,
    AiProxyModule,
    AutomationModule
  ]
})
export class AppModule {}
