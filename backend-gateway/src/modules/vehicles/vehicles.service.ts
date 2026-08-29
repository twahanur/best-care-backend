import { Injectable, NotFoundException } from '@nestjs/common';
import { Vehicle } from './vehicle.interface';
import { CreateVehicleDto } from './dto/create-vehicle.dto';
import { FilterVehicleDto } from './dto/filter-vehicle.dto';

@Injectable()
export class VehiclesService {
  private vehicles: Vehicle[] = [
    {
      id: 'car_prado_suv',
      name: 'Toyota Land Cruiser Prado TX',
      brand: 'Toyota',
      category: 'SUV',
      dailyRate: 145,
      seats: 7,
      doors: 5,
      luggageCapacity: 4,
      transmission: 'Automatic',
      fuelType: 'Diesel',
      fuelEfficiency: '12 km/L',
      terrainCapability: 'Mountainous / 4WD Off-road (Sylhet, Bandarban, Sajek)',
      image: 'https://images.unsplash.com/photo-1594502184342-2e12f877aa73?auto=format&fit=crop&w=800&q=80',
      rating: 4.9,
      reviewsCount: 128,
      featured: true,
      available: true,
      features: ['4x4 Low-Range', 'Dual Zone AC', 'GPS Navigation', 'Hill Descent Control', 'ISOFIX Child Seat Ready', 'Roof Rack'],
      specs: {
        engine: '2.8L Turbo Diesel',
        horsepower: 204,
        acceleration0to100: '9.8s',
        topSpeed: '175 km/h'
      }
    },
    {
      id: 'car_tucson_suv',
      name: 'Hyundai Tucson AWD',
      brand: 'Hyundai',
      category: 'SUV',
      dailyRate: 85,
      seats: 5,
      doors: 5,
      luggageCapacity: 3,
      transmission: 'Automatic',
      fuelType: 'Hybrid',
      fuelEfficiency: '15 km/L',
      terrainCapability: 'All-Weather Highway & Light Gravel',
      image: 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80',
      rating: 4.8,
      reviewsCount: 94,
      featured: true,
      available: true,
      features: ['Panoramic Sunroof', 'Apple CarPlay & Android Auto', 'Smart Cruise Control', 'Lane Keep Assist', 'Spacious Cargo'],
      specs: {
        engine: '1.6L Turbo Hybrid',
        horsepower: 180,
        acceleration0to100: '8.4s',
        topSpeed: '190 km/h'
      }
    },
    {
      id: 'car_tesla_modely',
      name: 'Tesla Model Y Long Range',
      brand: 'Tesla',
      category: 'Electric',
      dailyRate: 110,
      seats: 5,
      doors: 5,
      luggageCapacity: 3,
      transmission: 'Automatic',
      fuelType: 'Electric',
      fuelEfficiency: '510 km / Full Charge',
      terrainCapability: 'Paved Highways & Urban Expressways',
      image: 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=800&q=80',
      rating: 4.95,
      reviewsCount: 156,
      featured: true,
      available: true,
      features: ['Autopilot Capability', '15-inch Touchscreen Hub', 'Zero Emissions', 'Supercharging Enabled', 'Glass Roof', 'Heated Seats'],
      specs: {
        engine: 'Dual Motor All-Wheel Drive',
        horsepower: 384,
        acceleration0to100: '4.8s',
        topSpeed: '217 km/h'
      }
    },
    {
      id: 'car_mercedes_eclass',
      name: 'Mercedes-Benz E-Class AMG Line',
      brand: 'Mercedes-Benz',
      category: 'Luxury',
      dailyRate: 160,
      seats: 5,
      doors: 4,
      luggageCapacity: 2,
      transmission: 'Automatic',
      fuelType: 'Hybrid',
      fuelEfficiency: '14 km/L',
      terrainCapability: 'Executive Urban & Smooth Highway',
      image: 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=800&q=80',
      rating: 4.9,
      reviewsCount: 82,
      featured: true,
      available: true,
      features: ['Burmester 3D Surround Sound', 'Nappa Leather Upholstery', '64-Color Ambient Lighting', 'Executive Tint', 'Chauffeur Option'],
      specs: {
        engine: '2.0L Turbo Mild-Hybrid',
        horsepower: 255,
        acceleration0to100: '6.2s',
        topSpeed: '250 km/h'
      }
    },
    {
      id: 'car_camry_hybrid',
      name: 'Toyota Camry Premium Hybrid',
      brand: 'Toyota',
      category: 'Sedan',
      dailyRate: 70,
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      transmission: 'Automatic',
      fuelType: 'Hybrid',
      fuelEfficiency: '22 km/L Eco',
      terrainCapability: 'Inter-District & City Roads',
      image: 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=800&q=80',
      rating: 4.75,
      reviewsCount: 110,
      featured: false,
      available: true,
      features: ['Whisper Quiet Cabin', 'Wireless Smartphone Charger', 'Blind Spot Detection', 'Ventilated Cooling Seats', 'Huge Trunk Space'],
      specs: {
        engine: '2.5L Dynamic Force Hybrid',
        horsepower: 208,
        acceleration0to100: '7.8s',
        topSpeed: '195 km/h'
      }
    },
    {
      id: 'car_hiace_luxury',
      name: 'Toyota HiAce Grandia Luxury',
      brand: 'Toyota',
      category: 'Van',
      dailyRate: 130,
      seats: 11,
      doors: 4,
      luggageCapacity: 8,
      transmission: 'Automatic',
      fuelType: 'Diesel',
      fuelEfficiency: '11 km/L',
      terrainCapability: 'Tour Highway & Long-Distance Interstate',
      image: 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80',
      rating: 4.85,
      reviewsCount: 76,
      featured: false,
      available: true,
      features: ['11 Individual Captain Seats', 'Individual Overhead AC Vents', 'Dual Sliding Doors', 'High Roof Ceiling', 'USB Fast Chargers'],
      specs: {
        engine: '2.8L Turbo Diesel',
        horsepower: 176,
        acceleration0to100: '12.0s',
        topSpeed: '160 km/h'
      }
    },
    {
      id: 'car_civic_sport',
      name: 'Honda Civic Sport',
      brand: 'Honda',
      category: 'Sedan',
      dailyRate: 55,
      seats: 5,
      doors: 4,
      luggageCapacity: 2,
      transmission: 'Automatic',
      fuelType: 'Petrol',
      fuelEfficiency: '16 km/L',
      terrainCapability: 'Urban City & Suburban Commute',
      image: 'https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&w=800&q=80',
      rating: 4.7,
      reviewsCount: 142,
      featured: false,
      available: true,
      features: ['Honda Sensing Suite', 'Digital Cockpit Display', 'Paddle Shifters', 'Sport Wheels', 'Eco Assist Drive Mode'],
      specs: {
        engine: '1.5L VTEC Turbo',
        horsepower: 180,
        acceleration0to100: '7.5s',
        topSpeed: '210 km/h'
      }
    },
    {
      id: 'car_mustang_gt',
      name: 'Ford Mustang GT V8 Convertible',
      brand: 'Ford',
      category: 'Sports',
      dailyRate: 175,
      seats: 4,
      doors: 2,
      luggageCapacity: 2,
      transmission: 'Automatic',
      fuelType: 'Petrol',
      fuelEfficiency: '10 km/L',
      terrainCapability: 'Scenic Coastal Roads & Highways',
      image: 'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?auto=format&fit=crop&w=800&q=80',
      rating: 4.95,
      reviewsCount: 65,
      featured: true,
      available: false, // Currently rented out for realistic status display
      features: ['Power Soft-Top Convertible', 'Active Valve Exhaust', 'Brembo High Performance Brakes', 'Track Apps', 'Heated & Cooled Seats'],
      specs: {
        engine: '5.0L Ti-VCT V8',
        horsepower: 450,
        acceleration0to100: '4.3s',
        topSpeed: '250 km/h'
      }
    }
  ];

  findAll(filters?: FilterVehicleDto): Vehicle[] {
    let result = [...this.vehicles];

    if (!filters) {
      return result;
    }

    if (filters.category) {
      result = result.filter(v => v.category.toLowerCase() === filters.category.toLowerCase());
    }

    if (filters.search) {
      const q = filters.search.toLowerCase();
      result = result.filter(v =>
        v.name.toLowerCase().includes(q) ||
        v.brand.toLowerCase().includes(q) ||
        v.category.toLowerCase().includes(q) ||
        v.terrainCapability.toLowerCase().includes(q)
      );
    }

    if (filters.minPrice !== undefined) {
      result = result.filter(v => v.dailyRate >= filters.minPrice);
    }

    if (filters.maxPrice !== undefined) {
      result = result.filter(v => v.dailyRate <= filters.maxPrice);
    }

    if (filters.seats !== undefined) {
      result = result.filter(v => v.seats >= filters.seats);
    }

    if (filters.transmission) {
      result = result.filter(v => v.transmission.toLowerCase() === filters.transmission.toLowerCase());
    }

    if (filters.fuelType) {
      result = result.filter(v => v.fuelType.toLowerCase() === filters.fuelType.toLowerCase());
    }

    if (filters.available !== undefined) {
      result = result.filter(v => v.available === filters.available);
    }

    if (filters.featured !== undefined) {
      result = result.filter(v => v.featured === filters.featured);
    }

    return result;
  }

  findOne(id: string): Vehicle {
    const vehicle = this.vehicles.find(v => v.id === id);
    if (!vehicle) {
      throw new NotFoundException(`Vehicle with ID "${id}" not found.`);
    }
    return vehicle;
  }

  create(dto: CreateVehicleDto): Vehicle {
    const id = `car_${Date.now()}`;
    const newVehicle: Vehicle = {
      id,
      ...dto,
      rating: 5.0,
      reviewsCount: 0,
      specs: {
        engine: 'Standard 2.0L Engine',
        horsepower: 180,
        acceleration0to100: '8.5s',
        topSpeed: '200 km/h'
      }
    };
    this.vehicles.unshift(newVehicle);
    return newVehicle;
  }

  updateStatus(id: string, available: boolean): Vehicle {
    const vehicle = this.findOne(id);
    vehicle.available = available;
    return vehicle;
  }
}
