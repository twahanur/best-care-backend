export type UserRole = 'CUSTOMER' | 'ADMIN' | 'FLEET_MANAGER';
export type UserStatus = 'ACTIVE' | 'SUSPENDED' | 'PENDING_VERIFICATION';

export interface User {
  id: string;
  name: string;
  email: string;
  passwordHash: string;
  role: UserRole;
  phone: string;
  avatar?: string;
  drivingLicenseNumber?: string;
  drivingLicenseImage?: string;
  address?: string;
  status: UserStatus;
  createdAt: string;
  updatedAt: string;
}

export type CarCategory = 'Sedan' | 'SUV' | 'Electric' | 'Luxury' | 'Passenger Van' | 'Sports';
export type Transmission = 'Automatic' | 'Manual';
export type FuelType = 'Petrol' | 'Diesel' | 'Electric' | 'Hybrid';
export type CarStatus = 'AVAILABLE' | 'RENTED' | 'MAINTENANCE' | 'DECOMMISSIONED';

export interface Car {
  id: string;
  name: string;
  brand: string;
  model: string;
  year: number;
  category: CarCategory;
  transmission: Transmission;
  fuelType: FuelType;
  seats: number;
  doors: number;
  luggageCapacity: number;
  mileageLimit: string;
  dailyRate: number;
  securityDeposit: number;
  licensePlate: string;
  images: string[];
  features: string[];
  currentHub: string;
  status: CarStatus;
  ratingAverage: number;
  reviewCount: number;
  createdAt: string;
  updatedAt: string;
}

export type ProtectionPlan = 'Basic CDW' | 'Comprehensive Plus' | 'VIP Full Shield';
export type BookingStatus = 'Pending' | 'Confirmed' | 'Active' | 'Completed' | 'Cancelled';

export interface Booking {
  id: string;
  bookingCode: string;
  userId: string;
  customerName: string;
  customerEmail: string;
  customerPhone: string;
  carId: string;
  vehicleName: string;
  vehicleImage?: string;
  pickupDate: string;
  dropoffDate: string;
  pickupLocation: string;
  dropoffLocation: string;
  totalDays: number;
  dailyRate: number;
  baseAmount: number;
  protectionPlan: ProtectionPlan;
  protectionFee: number;
  securityDeposit: number;
  discountAmount: number;
  totalAmount: number;
  status: BookingStatus;
  paymentStatus: 'Pending' | 'Paid' | 'Refunded' | 'Failed';
  cancellationReason?: string;
  cancelledAt?: string;
  refundAmount?: number;
  notes?: string;
  aiLeadScore?: {
    score: number;
    classification: 'Hot' | 'Warm' | 'Cold';
    priority: string;
    suggestedAction: string;
  };
  createdAt: string;
  updatedAt: string;
}

export type PaymentMethod = 'Credit Card' | 'Debit Card' | 'bKash' | 'Nagad' | 'Cash on Delivery';
export type PaymentStatus = 'PENDING' | 'COMPLETED' | 'FAILED' | 'REFUNDED';

export interface Payment {
  id: string;
  transactionCode: string;
  bookingId: string;
  bookingCode: string;
  userId: string;
  customerName: string;
  amount: number;
  currency: string;
  paymentMethod: PaymentMethod;
  status: PaymentStatus;
  paidAt?: string;
  refundedAt?: string;
  receiptUrl?: string;
  createdAt: string;
}

export interface Review {
  id: string;
  bookingId: string;
  userId: string;
  userName: string;
  userAvatar?: string;
  carId: string;
  carName: string;
  rating: number; // 1 to 5
  comment: string;
  isApproved: boolean;
  adminReply?: string;
  createdAt: string;
}

export type AvailabilityBlockType = 'BOOKING' | 'MAINTENANCE' | 'ADMIN_HOLD' | 'INSPECTION';

export interface AvailabilityBlock {
  id: string;
  carId: string;
  carName: string;
  bookingId?: string;
  startDate: string;
  endDate: string;
  type: AvailabilityBlockType;
  notes?: string;
  createdAt: string;
}

export interface PricingRule {
  id: string;
  name: string;
  category?: string;
  multiplier: number;
  startDate?: string;
  endDate?: string;
  isActive: boolean;
  createdAt: string;
}
