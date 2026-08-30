export type UserRole = 'ADMIN' | 'CUSTOMER' | 'CAR_DRIVER' | 'admin' | 'customer' | 'car_driver';
export type UserStatus = 'ACTIVE' | 'SUSPENDED' | 'PENDING_VERIFICATION';
export type KycStatus = 'NOT_SUBMITTED' | 'PENDING' | 'VERIFIED' | 'REJECTED';

export interface User {
  id: string;
  email: string;
  passwordHash?: string;
  name: string;
  phone?: string;
  role: UserRole;
  status: UserStatus;
  kycStatus?: KycStatus;
  avatar?: string;
  avatarUrl?: string;
  drivingLicenseNumber?: string;
  drivingLicenseNo?: string;
  licenseExpiryDate?: string;
  licenseImageFront?: string;
  licenseImageBack?: string;
  experienceYears?: number;
  isAvailableForTrip?: boolean;
  driverRating?: number;
  totalTripsCompleted?: number;
  address?: string;
  city?: string;
  createdAt: string;
  updatedAt?: string;
}

export type CarCategory =
  | 'Sedan' | 'SUV' | 'Electric' | 'Luxury' | 'Passenger Van' | 'Sports' | 'Hatchback'
  | 'SEDAN' | 'SUV' | 'ELECTRIC' | 'LUXURY' | 'PASSENGER_VAN' | 'SPORTS' | 'HATCHBACK';

export type Transmission = 'Automatic' | 'Manual' | 'AUTOMATIC' | 'MANUAL';
export type FuelType = 'Petrol' | 'Diesel' | 'Electric' | 'Hybrid' | 'Octane' | 'CNG' | 'PETROL' | 'DIESEL' | 'ELECTRIC' | 'HYBRID' | 'OCTANE' | 'CNG';
export type CarStatus = 'AVAILABLE' | 'RENTED' | 'MAINTENANCE' | 'DECOMMISSIONED';

export interface LocationHub {
  id: string;
  name: string;
  code: string;
  address: string;
  city: string;
  phone?: string;
  email?: string;
  latitude?: number;
  longitude?: number;
  isActive: boolean;
  createdAt: string;
  updatedAt?: string;
}

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
  vin?: string;
  currentHubId?: string;
  currentHub?: string | LocationHub;
  status: CarStatus;
  ratingAverage: number;
  reviewCount: number;
  isFeatured?: boolean;
  images: string[];
  features: string[];
  createdAt: string;
  updatedAt?: string;
}

export type AvailabilityBlockType = 'Maintenance' | 'Booking' | 'Reserved' | 'MAINTENANCE' | 'BOOKING' | 'ADMIN_HOLD';

export interface AvailabilityBlock {
  id: string;
  carId: string;
  carName?: string;
  startDate: string;
  endDate: string;
  type: AvailabilityBlockType;
  reason?: string;
  notes?: string;
  status?: string;
  createdAt?: string;
}

export type ProtectionPlan =
  | 'Basic CDW' | 'Comprehensive Plus' | 'VIP Full Shield'
  | 'BASIC_CDW' | 'COMPREHENSIVE_PLUS' | 'VIP_FULL_SHIELD';

export type BookingStatus =
  | 'Pending' | 'Confirmed' | 'Active' | 'Completed' | 'Cancelled'
  | 'PENDING' | 'CONFIRMED' | 'ACTIVE_RENTAL' | 'COMPLETED' | 'CANCELLED';

export type PaymentStatus =
  | 'Pending' | 'Paid' | 'Failed' | 'Refunded'
  | 'PENDING' | 'PAID' | 'FAILED' | 'REFUNDED' | 'COMPLETED';

export type PaymentMethod =
  | 'Credit Card' | 'Debit Card' | 'bKash' | 'Nagad' | 'Cash on Delivery' | 'Cash'
  | 'CREDIT_CARD' | 'DEBIT_CARD' | 'BKASH' | 'NAGAD' | 'CASH' | 'BANK_TRANSFER';

export type RentalServiceType =
  | 'SELF_DRIVE'
  | 'CHAUFFEUR_DRIVEN'
  | 'AIRPORT_TRANSFER'
  | 'INTERCITY_TOUR'
  | 'HOURLY_CHARTER'
  | 'WEDDING_VIP_EVENT';

export type RentalAddon =
  | 'CHILD_BABY_SEAT'
  | 'PORTABLE_WIFI_HOTSPOT'
  | 'DASHCAM_RECORDER'
  | 'ROOF_LUGGAGE_BOX'
  | 'ADDITIONAL_DRIVER_PERMIT'
  | 'PET_PROTECTION_COVER';

export type MaintenanceType =
  | 'ROUTINE_OIL_FILTER_SERVICE'
  | 'BRAKE_PAD_REPLACEMENT'
  | 'TIRE_ALIGNMENT_ROTATION'
  | 'BATTERY_HEALTH_CHECK'
  | 'CERAMIC_DETAILING'
  | 'BODY_PAINT_REPAIR'
  | 'AC_DEEP_CLEAN';

export type DriverTripStatus =
  | 'NOT_ASSIGNED'
  | 'ASSIGNED_PENDING'
  | 'ACCEPTED'
  | 'REJECTED'
  | 'EN_ROUTE_TO_PICKUP'
  | 'ARRIVED_AT_HUB'
  | 'TRIP_IN_PROGRESS'
  | 'DROPOFF_COMPLETED';

export interface BookingAddonItem {
  id?: string;
  addon: RentalAddon;
  dailyPrice: number;
  totalPrice: number;
}

export interface Booking {
  id: string;
  bookingCode: string;
  userId: string;
  driverId?: string;
  serviceType?: RentalServiceType;
  driverTripStatus?: DriverTripStatus;
  customerName?: string;
  customerEmail?: string;
  customerPhone?: string;
  carId: string;
  vehicleName?: string;
  vehicleImage?: string;
  pickupDate?: string;
  dropoffDate?: string;
  pickupDateTime?: string;
  dropoffDateTime?: string;
  pickupLocation?: string;
  dropoffLocation?: string;
  totalDays: number;
  dailyRate: number;
  driverFee?: number;
  baseAmount: number;
  protectionPlan: ProtectionPlan;
  protectionFee: number;
  securityDeposit: number;
  discountAmount: number;
  taxAmount?: number;
  totalAmount: number;
  withDriver?: boolean;
  addons?: BookingAddonItem[];
  status: BookingStatus;
  paymentStatus: PaymentStatus;
  cancellationReason?: string;
  cancelledAt?: string;
  refundAmount?: number;
  notes?: string;
  customerNotes?: string;
  adminNotes?: string;
  aiLeadScore?: {
    score: number;
    classification: 'Hot' | 'Warm' | 'Cold';
    priority: string;
    suggestedAction: string;
  };
  createdAt: string;
  updatedAt?: string;
}

export interface RentalInspection {
  id: string;
  bookingId: string;
  pickupOdometer: number;
  returnOdometer?: number;
  pickupFuelLevel: number;
  returnFuelLevel?: number;
  pickupDamageNotes?: string;
  returnDamageNotes?: string;
  extraMileageFee: number;
  extraFuelFee: number;
  damageFee: number;
  totalExtraFee: number;
  inspectedByPickup?: string;
  inspectedByReturn?: string;
  createdAt: string;
  updatedAt?: string;
}

export interface Payment {
  id: string;
  transactionId?: string;
  transactionCode?: string;
  bookingId: string;
  bookingCode?: string;
  userId: string;
  customerName?: string;
  customerEmail?: string;
  amount: number;
  currency: string;
  paymentMethod: PaymentMethod;
  paymentStatus?: PaymentStatus;
  status?: PaymentStatus;
  gatewayName?: string;
  gatewayResponseJson?: Record<string, any>;
  invoiceNumber?: string;
  receiptUrl?: string;
  paidAt?: string;
  refundedAt?: string;
  refundReason?: string;
  createdAt: string;
  updatedAt?: string;
}

export interface Invoice {
  id: string;
  invoiceNumber: string;
  bookingId: string;
  userId: string;
  paymentId?: string;
  subtotal: number;
  tax: number;
  discount: number;
  total: number;
  pdfUrl?: string;
  issuedAt: string;
  paidAt?: string;
  createdAt: string;
}

export type ReviewStatus = 'PENDING_MODERATION' | 'APPROVED' | 'REJECTED';

export interface Review {
  id: string;
  carId: string;
  carName?: string;
  userId: string;
  userName?: string;
  userAvatar?: string;
  bookingId: string;
  rating: number;
  driverRating?: number;
  title?: string;
  comment: string;
  isApproved?: boolean;
  adminReply?: string;
  status?: ReviewStatus;
  adminModeratedBy?: string;
  moderatedAt?: string;
  createdAt: string;
  updatedAt?: string;
}

export interface PricingRule {
  id: string;
  name: string;
  code?: string;
  category?: CarCategory | string;
  startDate?: string;
  endDate?: string;
  multiplier: number;
  fixedAdjustment?: number;
  driverDailyRate?: number;
  isActive: boolean;
  createdAt: string;
  updatedAt?: string;
}

export interface DiscountCoupon {
  id: string;
  code: string;
  discountType: 'PERCENTAGE' | 'FIXED_AMOUNT';
  discountValue: number;
  minBookingAmount: number;
  maxDiscountAmount?: number;
  startDate: string;
  endDate: string;
  usageLimit: number;
  usedCount: number;
  isActive: boolean;
  createdAt: string;
  updatedAt?: string;
}

export type ReportType = 'REVENUE' | 'FLEET_UTILIZATION' | 'BOOKING_SUMMARY' | 'USER_ANALYTICS';

export interface ReportRecord {
  id: string;
  reportType: ReportType;
  title: string;
  parametersJson?: Record<string, any>;
  summaryJson: Record<string, any>;
  generatedById?: string;
  createdAt: string;
}
