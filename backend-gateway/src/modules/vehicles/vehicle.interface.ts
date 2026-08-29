export type VehicleCategory = 'SUV' | 'Sedan' | 'Luxury' | 'Electric' | 'Van' | 'Sports';
export type TransmissionType = 'Automatic' | 'Manual';
export type FuelType = 'Petrol' | 'Diesel' | 'Hybrid' | 'Electric';

export interface Vehicle {
  id: string;
  name: string;
  brand: string;
  category: VehicleCategory;
  dailyRate: number;
  seats: number;
  doors: number;
  luggageCapacity: number; // In standard suitcases
  transmission: TransmissionType;
  fuelType: FuelType;
  fuelEfficiency: string; // e.g. "15 km/L"
  terrainCapability: string; // e.g. "Hilly / Mountain / 4x4"
  image: string;
  rating: number;
  reviewsCount: number;
  featured: boolean;
  available: boolean;
  features: string[];
  specs: {
    engine: string;
    horsepower: number;
    acceleration0to100: string;
    topSpeed: string;
  };
}
