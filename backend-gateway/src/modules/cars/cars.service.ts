import { Injectable, NotFoundException } from '@nestjs/common';
import { Car, CarCategory, CarStatus } from '../../common/types/schema.types';

@Injectable()
export class CarsService {
  private cars: Car[] = [
    {
      id: 'car_jaguar_xe',
      name: 'Jaguar XE L Prestige',
      brand: 'Jaguar',
      model: 'XE L Prestige 250PS',
      year: 2024,
      category: 'Luxury',
      transmission: 'Automatic',
      fuelType: 'Petrol',
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      mileageLimit: 'Unlimited',
      dailyRate: 85,
      securityDeposit: 250,
      licensePlate: 'DHK-MET-GA-11-2049',
      images: [
        'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80',
        'https://images.unsplash.com/photo-1541348263662-e0c8de4259ba?auto=format&fit=crop&w=800&q=80'
      ],
      features: ['Leather Seats', 'Sunroof', 'Adaptive Cruise', '360 Camera', 'Apple CarPlay', 'Meridian Audio'],
      currentHub: 'Hazrat Shahjalal Intl Airport (DAC)',
      status: 'AVAILABLE',
      ratingAverage: 4.9,
      reviewCount: 48,
      createdAt: '2026-01-10T00:00:00Z',
      updatedAt: '2026-01-10T00:00:00Z'
    },
    {
      id: 'car_audi_a6',
      name: 'Audi A6 Business Executive',
      brand: 'Audi',
      model: 'A6 45 TFSI Quattro',
      year: 2024,
      category: 'Sedan',
      transmission: 'Automatic',
      fuelType: 'Petrol',
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      mileageLimit: 'Unlimited',
      dailyRate: 95,
      securityDeposit: 300,
      licensePlate: 'DHK-MET-GHA-14-8832',
      images: [
        'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=800&q=80'
      ],
      features: ['Virtual Cockpit', 'Matrix LED', 'Quattro AWD', 'Heated Seats', 'Lane Assist'],
      currentHub: 'Hazrat Shahjalal Intl Airport (DAC)',
      status: 'AVAILABLE',
      ratingAverage: 4.8,
      reviewCount: 36,
      createdAt: '2026-01-15T00:00:00Z',
      updatedAt: '2026-01-15T00:00:00Z'
    },
    {
      id: 'car_prado_suv',
      name: 'Toyota Land Cruiser Prado TX',
      brand: 'Toyota',
      model: 'Land Cruiser Prado TX-L',
      year: 2024,
      category: 'SUV',
      transmission: 'Automatic',
      fuelType: 'Diesel',
      seats: 7,
      doors: 5,
      luggageCapacity: 5,
      mileageLimit: 'Unlimited',
      dailyRate: 145,
      securityDeposit: 350,
      licensePlate: 'DHK-MET-GHA-19-9021',
      images: [
        'https://images.unsplash.com/photo-1594502184342-2e12f877aa73?auto=format&fit=crop&w=800&q=80'
      ],
      features: ['4x4 Terrain Mode', 'Diff Lock', '7 Seats', 'Rear AC', 'Roof Rails', 'Heavy Duty Suspension'],
      currentHub: 'Hazrat Shahjalal Intl Airport (DAC)',
      status: 'AVAILABLE',
      ratingAverage: 4.9,
      reviewCount: 64,
      createdAt: '2026-01-18T00:00:00Z',
      updatedAt: '2026-01-18T00:00:00Z'
    },
    {
      id: 'car_hyundai_tucson',
      name: 'Hyundai Tucson Limited Edition',
      brand: 'Hyundai',
      model: 'Tucson 1.6T HTRAC',
      year: 2024,
      category: 'SUV',
      transmission: 'Automatic',
      fuelType: 'Hybrid',
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      mileageLimit: 'Unlimited',
      dailyRate: 75,
      securityDeposit: 200,
      licensePlate: 'DHK-MET-KHA-21-4920',
      images: [
        'https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=800&q=80'
      ],
      features: ['Panoramic Sunroof', 'Smart Cruise', 'Blind Spot Monitor', 'Wireless Charging'],
      currentHub: 'Gulshan Diplomatic Zone, Dhaka',
      status: 'AVAILABLE',
      ratingAverage: 4.7,
      reviewCount: 29,
      createdAt: '2026-02-01T00:00:00Z',
      updatedAt: '2026-02-01T00:00:00Z'
    },
    {
      id: 'car_tesla_modely',
      name: 'Tesla Model Y Long Range',
      brand: 'Tesla',
      model: 'Model Y Dual Motor AWD',
      year: 2024,
      category: 'Electric',
      transmission: 'Automatic',
      fuelType: 'Electric',
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      mileageLimit: 'Unlimited',
      dailyRate: 110,
      securityDeposit: 300,
      licensePlate: 'DHK-MET-EV-01-3042',
      images: [
        'https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=800&q=80'
      ],
      features: ['520km Range', 'Autopilot Hardware', 'Supercharging Enabled', 'Glass Roof', 'Premium Audio'],
      currentHub: 'Banani Central Hub',
      status: 'AVAILABLE',
      ratingAverage: 4.9,
      reviewCount: 52,
      createdAt: '2026-02-05T00:00:00Z',
      updatedAt: '2026-02-05T00:00:00Z'
    },
    {
      id: 'car_mercedes_eclass',
      name: 'Mercedes-Benz E-Class AMG Line',
      brand: 'Mercedes-Benz',
      model: 'E 300 AMG Line',
      year: 2024,
      category: 'Luxury',
      transmission: 'Automatic',
      fuelType: 'Petrol',
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      mileageLimit: 'Unlimited',
      dailyRate: 160,
      securityDeposit: 400,
      licensePlate: 'DHK-MET-GHA-18-7741',
      images: [
        'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=800&q=80'
      ],
      features: ['Burmester 3D Sound', 'Air Balance', 'MBUX Navigation', 'Nappa Leather', 'Executive Rear Package'],
      currentHub: 'Hazrat Shahjalal Intl Airport (DAC)',
      status: 'AVAILABLE',
      ratingAverage: 5.0,
      reviewCount: 41,
      createdAt: '2026-02-12T00:00:00Z',
      updatedAt: '2026-02-12T00:00:00Z'
    },
    {
      id: 'car_mustang_gt',
      name: 'Ford Mustang GT V8 Convertible',
      brand: 'Ford',
      model: 'Mustang GT 5.0 V8',
      year: 2024,
      category: 'Sports',
      transmission: 'Automatic',
      fuelType: 'Petrol',
      seats: 4,
      doors: 2,
      luggageCapacity: 2,
      mileageLimit: '250 km/day',
      dailyRate: 175,
      securityDeposit: 500,
      licensePlate: 'DHK-MET-KHA-09-5501',
      images: [
        'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?auto=format&fit=crop&w=800&q=80'
      ],
      features: ['V8 Quad Exhaust', 'Brembo Brakes', 'Convertible Soft Top', 'Track Apps', 'Launch Control'],
      currentHub: 'Gulshan Diplomatic Zone, Dhaka',
      status: 'AVAILABLE',
      ratingAverage: 4.9,
      reviewCount: 22,
      createdAt: '2026-02-20T00:00:00Z',
      updatedAt: '2026-02-20T00:00:00Z'
    },
    {
      id: 'car_hiace_vip',
      name: 'Toyota HiAce VIP Super Grandia',
      brand: 'Toyota',
      model: 'HiAce Super Grandia VIP',
      year: 2024,
      category: 'Passenger Van',
      transmission: 'Automatic',
      fuelType: 'Diesel',
      seats: 10,
      doors: 4,
      luggageCapacity: 8,
      mileageLimit: 'Unlimited',
      dailyRate: 130,
      securityDeposit: 300,
      licensePlate: 'DHK-MET-CHA-15-4490',
      images: [
        'https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80'
      ],
      features: ['Captain Reclining Seats', 'Dual Power Sliding Doors', 'High Roof', 'Rear TV Monitor', '10 Passengers'],
      currentHub: 'Hazrat Shahjalal Intl Airport (DAC)',
      status: 'AVAILABLE',
      ratingAverage: 4.8,
      reviewCount: 38,
      createdAt: '2026-02-22T00:00:00Z',
      updatedAt: '2026-02-22T00:00:00Z'
    }
  ];

  findAll(query?: { category?: string; search?: string; transmission?: string; fuelType?: string; maxPrice?: number; hub?: string; status?: string }): Car[] {
    let result = [...this.cars];

    if (query?.category && query.category !== 'All' && query.category !== 'All Deals') {
      result = result.filter(c => c.category.toLowerCase() === query.category!.toLowerCase());
    }

    if (query?.transmission && query.transmission !== 'All') {
      result = result.filter(c => c.transmission.toLowerCase() === query.transmission!.toLowerCase());
    }

    if (query?.fuelType && query.fuelType !== 'All') {
      result = result.filter(c => c.fuelType.toLowerCase() === query.fuelType!.toLowerCase());
    }

    if (query?.maxPrice) {
      result = result.filter(c => c.dailyRate <= Number(query.maxPrice));
    }

    if (query?.hub && query.hub !== 'All') {
      result = result.filter(c => c.currentHub.toLowerCase().includes(query.hub!.toLowerCase()));
    }

    if (query?.status && query.status !== 'All') {
      result = result.filter(c => c.status.toLowerCase() === query.status!.toLowerCase());
    }

    if (query?.search) {
      const q = query.search.toLowerCase();
      result = result.filter(c =>
        c.name.toLowerCase().includes(q) ||
        c.brand.toLowerCase().includes(q) ||
        c.model.toLowerCase().includes(q) ||
        c.licensePlate.toLowerCase().includes(q) ||
        c.category.toLowerCase().includes(q)
      );
    }

    return result;
  }

  findOne(id: string): Car {
    const car = this.cars.find(c => c.id === id);
    if (!car) {
      throw new NotFoundException(`Car with ID "${id}" not found.`);
    }
    return car;
  }

  create(dto: Partial<Car>): Car {
    const newCar: Car = {
      id: `car_${Date.now()}`,
      name: dto.name || 'New Rental Vehicle',
      brand: dto.brand || 'Toyota',
      model: dto.model || 'Standard',
      year: dto.year || 2024,
      category: dto.category || 'Sedan',
      transmission: dto.transmission || 'Automatic',
      fuelType: dto.fuelType || 'Petrol',
      seats: dto.seats || 5,
      doors: dto.doors || 4,
      luggageCapacity: dto.luggageCapacity || 3,
      mileageLimit: dto.mileageLimit || 'Unlimited',
      dailyRate: Number(dto.dailyRate) || 80,
      securityDeposit: Number(dto.securityDeposit) || 200,
      licensePlate: dto.licensePlate || `DHK-MET-GA-${Math.floor(10 + Math.random() * 89)}-${Math.floor(1000 + Math.random() * 8999)}`,
      images: dto.images && dto.images.length > 0 ? dto.images : ['https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'],
      features: dto.features || ['Air Conditioning', 'GPS', 'Bluetooth'],
      currentHub: dto.currentHub || 'Hazrat Shahjalal Intl Airport (DAC)',
      status: dto.status || 'AVAILABLE',
      ratingAverage: 5.0,
      reviewCount: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.cars.unshift(newCar);
    return newCar;
  }

  update(id: string, dto: Partial<Car>): Car {
    const car = this.findOne(id);
    Object.assign(car, {
      ...dto,
      dailyRate: dto.dailyRate !== undefined ? Number(dto.dailyRate) : car.dailyRate,
      securityDeposit: dto.securityDeposit !== undefined ? Number(dto.securityDeposit) : car.securityDeposit,
      seats: dto.seats !== undefined ? Number(dto.seats) : car.seats,
      updatedAt: new Date().toISOString()
    });
    return car;
  }

  delete(id: string): { success: boolean; message: string } {
    const idx = this.cars.findIndex(c => c.id === id);
    if (idx === -1) {
      throw new NotFoundException(`Car with ID "${id}" not found.`);
    }
    this.cars.splice(idx, 1);
    return { success: true, message: `Vehicle ${id} deleted successfully.` };
  }

  updateCarRating(carId: string, rating: number) {
    const car = this.cars.find(c => c.id === carId);
    if (car) {
      const currentTotal = car.ratingAverage * car.reviewCount;
      car.reviewCount += 1;
      car.ratingAverage = Number(((currentTotal + rating) / car.reviewCount).toFixed(1));
    }
  }

  updateCarStatus(carId: string, status: CarStatus) {
    const car = this.cars.find(c => c.id === carId);
    if (car) {
      car.status = status;
      car.updatedAt = new Date().toISOString();
    }
  }
}
