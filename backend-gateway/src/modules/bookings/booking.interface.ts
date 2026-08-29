export type BookingStatus = 'Pending' | 'Confirmed' | 'Active' | 'Completed' | 'Cancelled';
export type PaymentStatus = 'Paid' | 'Pending' | 'Refunded';
export type ProtectionPlan = 'Basic CDW' | 'Comprehensive Plus' | 'VIP Full Shield';

export interface Booking {
  id: string;
  bookingCode: string;
  vehicleId: string;
  vehicleName: string;
  customerName: string;
  customerEmail: string;
  customerPhone: string;
  pickupDate: string;
  dropoffDate: string;
  pickupLocation: string;
  dropoffLocation: string;
  totalDays: number;
  dailyRate: number;
  protectionPlan: ProtectionPlan;
  protectionFee: number;
  totalAmount: number;
  status: BookingStatus;
  paymentStatus: PaymentStatus;
  notes?: string;
  aiLeadScore?: {
    score: number;
    classification: 'Hot' | 'Warm' | 'Cold';
    priority: string;
    suggestedAction: string;
  };
  createdAt: string;
}
