import {
  PrismaClient,
  UserRole,
  UserStatus,
  KycStatus,
  CarCategory,
  Transmission,
  FuelType,
  CarStatus,
  BookingStatus,
  PaymentStatus,
  PaymentMethod,
  ProtectionPlan,
  ReviewStatus,
  DiscountType,
  ReportType,
  RentalServiceType,
  RentalAddon,
  MaintenanceType,
  DriverTripStatus
} from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting comprehensive database seeding to Neon PostgreSQL...');

  // ========================================================
  // 1. LOCATION HUBS (5 Records)
  // ========================================================
  console.log('📍 Seeding Location Hubs...');
  const hubsData = [
    {
      id: 'hub_dac',
      name: 'Hazrat Shahjalal Intl Airport (DAC)',
      code: 'DAC_AIRPORT',
      address: 'Airport Road, Kurmitola, Dhaka 1229',
      city: 'Dhaka',
      phone: '+8801700100001',
      email: 'dac.hub@bestcare.com',
      latitude: 23.8433,
      longitude: 90.3978,
      isActive: true,
    },
    {
      id: 'hub_gulshan',
      name: 'Gulshan Diplomatic Zone Hub',
      code: 'GULSHAN_HUB',
      address: 'Road 11, Block D, Gulshan 1, Dhaka',
      city: 'Dhaka',
      phone: '+8801700100002',
      email: 'gulshan.hub@bestcare.com',
      latitude: 23.7925,
      longitude: 90.4078,
      isActive: true,
    },
    {
      id: 'hub_banani',
      name: 'Banani Central Hub',
      code: 'BANANI_HUB',
      address: 'Road 11, Banani DOHS, Dhaka',
      city: 'Dhaka',
      phone: '+8801700100003',
      email: 'banani.hub@bestcare.com',
      latitude: 23.7937,
      longitude: 90.4043,
      isActive: true,
    },
    {
      id: 'hub_ctg',
      name: 'Chattogram Shah Amanat Airport (CGP)',
      code: 'CGP_AIRPORT',
      address: 'Potenga, Chattogram',
      city: 'Chattogram',
      phone: '+8801700100004',
      email: 'cgp.hub@bestcare.com',
      latitude: 22.2496,
      longitude: 91.8133,
      isActive: true,
    },
    {
      id: 'hub_sylhet',
      name: 'Sylhet Osmani Airport Hub (ZYL)',
      code: 'ZYL_AIRPORT',
      address: 'Airport Road, Sylhet 3102',
      city: 'Sylhet',
      phone: '+8801700100005',
      email: 'sylhet.hub@bestcare.com',
      latitude: 24.9632,
      longitude: 91.8719,
      isActive: true,
    }
  ];

  for (const hub of hubsData) {
    await prisma.locationHub.upsert({
      where: { code: hub.code },
      update: hub,
      create: hub,
    });
  }

  // ========================================================
  // 2. USERS & DRIVERS (25 Records)
  // ========================================================
  console.log('👤 Seeding Users & Chauffeurs...');
  const usersList = [
    // 3 Admins
    { id: 'usr_admin_1', email: 'admin@rentcars.com', name: 'Shahriar Admin', role: UserRole.ADMIN, phone: '+8801819000001', address: 'Gulshan 2, Dhaka' },
    { id: 'usr_admin_2', email: 'fleet.manager@rentcars.com', name: 'Tariqul Islam', role: UserRole.ADMIN, phone: '+8801819000002', address: 'Banani, Dhaka' },
    { id: 'usr_admin_3', email: 'operations@rentcars.com', name: 'Nusrat Jahan', role: UserRole.ADMIN, phone: '+8801819000003', address: 'Dhanmondi, Dhaka' },

    // 8 Professional Drivers
    { id: 'usr_driver_1', email: 'driver.rafiq@rentcars.com', name: 'Rafiqul Islam', role: UserRole.CAR_DRIVER, phone: '+8801711000010', drivingLicenseNo: 'DL-DH-882910', experienceYears: 8, driverRating: 4.9, totalTripsCompleted: 142, address: 'Mirpur 10, Dhaka' },
    { id: 'usr_driver_2', email: 'driver.kamal@rentcars.com', name: 'Kamal Hossain', role: UserRole.CAR_DRIVER, phone: '+8801711000011', drivingLicenseNo: 'DL-DH-771822', experienceYears: 6, driverRating: 4.8, totalTripsCompleted: 98, address: 'Uttara Sector 7, Dhaka' },
    { id: 'usr_driver_3', email: 'driver.shahin@rentcars.com', name: 'Shahinur Rahman', role: UserRole.CAR_DRIVER, phone: '+8801711000012', drivingLicenseNo: 'DL-DH-662914', experienceYears: 10, driverRating: 5.0, totalTripsCompleted: 210, address: 'Mohakhali DOHS, Dhaka' },
    { id: 'usr_driver_4', email: 'driver.jashim@rentcars.com', name: 'Jashim Uddin', role: UserRole.CAR_DRIVER, phone: '+8801711000013', drivingLicenseNo: 'DL-DH-554819', experienceYears: 5, driverRating: 4.7, totalTripsCompleted: 75, address: 'Badda, Dhaka' },
    { id: 'usr_driver_5', email: 'driver.alam@rentcars.com', name: 'Mahbub Alam', role: UserRole.CAR_DRIVER, phone: '+8801711000014', drivingLicenseNo: 'DL-CTG-339182', experienceYears: 7, driverRating: 4.9, totalTripsCompleted: 114, address: 'Agrabad, Chattogram' },
    { id: 'usr_driver_6', email: 'driver.sohel@rentcars.com', name: 'Sohel Rana', role: UserRole.CAR_DRIVER, phone: '+8801711000015', drivingLicenseNo: 'DL-DH-449182', experienceYears: 4, driverRating: 4.8, totalTripsCompleted: 62, address: 'Khilkhet, Dhaka' },
    { id: 'usr_driver_7', email: 'driver.billal@rentcars.com', name: 'Billal Faruqui', role: UserRole.CAR_DRIVER, phone: '+8801711000016', drivingLicenseNo: 'DL-SYL-228192', experienceYears: 9, driverRating: 4.9, totalTripsCompleted: 156, address: 'Zindabazar, Sylhet' },
    { id: 'usr_driver_8', email: 'driver.monir@rentcars.com', name: 'Moniruzzaman Monir', role: UserRole.CAR_DRIVER, phone: '+8801711000017', drivingLicenseNo: 'DL-DH-118273', experienceYears: 12, driverRating: 5.0, totalTripsCompleted: 320, address: 'Dhanmondi 32, Dhaka' },

    // 14 Customers
    { id: 'usr_cust_1', email: 'shahriar.khan@example.com', name: 'Shahriar Khan', role: UserRole.CUSTOMER, phone: '+8801700112233', drivingLicenseNo: 'DL-DH-482910', kycStatus: KycStatus.VERIFIED, address: 'Banani DOHS, Dhaka' },
    { id: 'usr_cust_2', email: 'sarah.ahmed@example.com', name: 'Sarah Ahmed', role: UserRole.CUSTOMER, phone: '+8801700112234', drivingLicenseNo: 'DL-DH-992144', kycStatus: KycStatus.VERIFIED, address: 'Gulshan 2, Dhaka' },
    { id: 'usr_cust_3', email: 'tanvir.hasan@example.com', name: 'Tanvir Hasan', role: UserRole.CUSTOMER, phone: '+8801700112235', drivingLicenseNo: 'DL-DH-773821', kycStatus: KycStatus.VERIFIED, address: 'Baridhara Diplomatic, Dhaka' },
    { id: 'usr_cust_4', email: 'farhana.chowdhury@example.com', name: 'Farhana Chowdhury', role: UserRole.CUSTOMER, phone: '+8801700112236', drivingLicenseNo: 'DL-DH-881924', kycStatus: KycStatus.VERIFIED, address: 'Uttara Sector 3, Dhaka' },
    { id: 'usr_cust_5', email: 'anwar.hossain@example.com', name: 'Anwar Hossain', role: UserRole.CUSTOMER, phone: '+8801700112237', drivingLicenseNo: 'DL-CTG-448192', kycStatus: KycStatus.VERIFIED, address: 'Nasirabad, Chattogram' },
    { id: 'usr_cust_6', email: 'mehnaz.k@example.com', name: 'Mehnaz Kabir', role: UserRole.CUSTOMER, phone: '+8801700112238', drivingLicenseNo: 'DL-DH-339182', kycStatus: KycStatus.VERIFIED, address: 'Bashundhara R/A, Dhaka' },
    { id: 'usr_cust_7', email: 'kazi.nasir@example.com', name: 'Kazi Nasir', role: UserRole.CUSTOMER, phone: '+8801700112239', drivingLicenseNo: 'DL-SYL-994821', kycStatus: KycStatus.VERIFIED, address: 'Shahjalal Upashahar, Sylhet' },
    { id: 'usr_cust_8', email: 'sadia.afrin@example.com', name: 'Sadia Afrin', role: UserRole.CUSTOMER, phone: '+8801700112240', drivingLicenseNo: 'DL-DH-129482', kycStatus: KycStatus.VERIFIED, address: 'Mirpur DOHS, Dhaka' },
    { id: 'usr_cust_9', email: 'imran.nazir@example.com', name: 'Imran Nazir', role: UserRole.CUSTOMER, phone: '+8801700112241', drivingLicenseNo: 'DL-DH-559182', kycStatus: KycStatus.VERIFIED, address: 'Dhanmondi, Dhaka' },
    { id: 'usr_cust_10', email: 'samira.rahman@example.com', name: 'Samira Rahman', role: UserRole.CUSTOMER, phone: '+8801700112242', drivingLicenseNo: 'DL-DH-772914', kycStatus: KycStatus.VERIFIED, address: 'Eskaton, Dhaka' },
    { id: 'usr_cust_11', email: 'zahid.hassan@example.com', name: 'Zahid Hassan', role: UserRole.CUSTOMER, phone: '+8801700112243', drivingLicenseNo: 'DL-DH-884910', kycStatus: KycStatus.VERIFIED, address: 'Lalmatia, Dhaka' },
    { id: 'usr_cust_12', email: 'nusrat.akter@example.com', name: 'Nusrat Akter', role: UserRole.CUSTOMER, phone: '+8801700112244', drivingLicenseNo: 'DL-CTG-229184', kycStatus: KycStatus.VERIFIED, address: 'Khulshi, Chattogram' },
    { id: 'usr_cust_13', email: 'rakibul.islam@example.com', name: 'Rakibul Islam', role: UserRole.CUSTOMER, phone: '+8801700112245', drivingLicenseNo: 'DL-DH-661928', kycStatus: KycStatus.VERIFIED, address: 'Paltan, Dhaka' },
    { id: 'usr_cust_14', email: 'sabrina.yasmin@example.com', name: 'Sabrina Yasmin', role: UserRole.CUSTOMER, phone: '+8801700112246', drivingLicenseNo: 'DL-DH-441829', kycStatus: KycStatus.VERIFIED, address: 'Niketan, Gulshan, Dhaka' }
  ];

  for (const u of usersList) {
    await prisma.user.upsert({
      where: { email: u.email },
      update: {
        ...u,
        passwordHash: '$2b$10$Ep99uE5O/gQx7W.4o99HfeK1oB.769v1g2yQeSjIeK5nC1xSj/jOa',
        status: UserStatus.ACTIVE,
      },
      create: {
        ...u,
        passwordHash: '$2b$10$Ep99uE5O/gQx7W.4o99HfeK1oB.769v1g2yQeSjIeK5nC1xSj/jOa',
        status: UserStatus.ACTIVE,
      },
    });
  }

  // ========================================================
  // 3. FLEET CARS (20 Records)
  // ========================================================
  console.log('🚗 Seeding Fleet Cars & Specifications...');
  const carsData = [
    {
      id: 'car_jaguar_xe',
      name: 'Jaguar XE L Prestige',
      brand: 'Jaguar',
      model: 'XE L Prestige 250PS',
      year: 2024,
      category: CarCategory.LUXURY,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      dailyRate: 85,
      securityDeposit: 250,
      licensePlate: 'DHK-MET-GA-11-2049',
      vin: 'SAJAA01X4LP102941',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 48,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'],
      features: ['Leather Seats', 'Sunroof', 'Adaptive Cruise', '360 Camera', 'Apple CarPlay', 'Meridian Audio']
    },
    {
      id: 'car_audi_a6',
      name: 'Audi A6 Business Executive',
      brand: 'Audi',
      model: 'A6 45 TFSI Quattro',
      year: 2024,
      category: CarCategory.SEDAN,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      dailyRate: 95,
      securityDeposit: 300,
      licensePlate: 'DHK-MET-GHA-14-8832',
      vin: 'WAUZZZF28MN029182',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.8,
      reviewCount: 36,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=800&q=80'],
      features: ['Virtual Cockpit', 'Matrix LED', 'Quattro AWD', 'Heated Seats', 'Lane Assist']
    },
    {
      id: 'car_prado_suv',
      name: 'Toyota Land Cruiser Prado TX',
      brand: 'Toyota',
      model: 'Land Cruiser Prado TX-L',
      year: 2024,
      category: CarCategory.SUV,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.DIESEL,
      seats: 7,
      doors: 5,
      luggageCapacity: 5,
      dailyRate: 145,
      securityDeposit: 350,
      licensePlate: 'DHK-MET-GHA-19-9021',
      vin: 'JTEBX3FJ8NK192841',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 64,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1594502184342-2e12f877aa73?auto=format&fit=crop&w=800&q=80'],
      features: ['4x4 Terrain Mode', 'Diff Lock', '7 Seats', 'Rear AC', 'Roof Rails', 'Heavy Duty Suspension']
    },
    {
      id: 'car_hyundai_tucson',
      name: 'Hyundai Tucson Limited Edition',
      brand: 'Hyundai',
      model: 'Tucson 1.6T HTRAC',
      year: 2024,
      category: CarCategory.SUV,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.HYBRID,
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      dailyRate: 75,
      securityDeposit: 200,
      licensePlate: 'DHK-MET-KHA-21-4920',
      vin: 'KM8JN81A9NU491024',
      currentHubId: 'hub_gulshan',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.7,
      reviewCount: 29,
      isFeatured: false,
      images: ['https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=800&q=80'],
      features: ['Panoramic Sunroof', 'Smart Cruise', 'Blind Spot Monitor', 'Wireless Charging']
    },
    {
      id: 'car_tesla_modely',
      name: 'Tesla Model Y Long Range',
      brand: 'Tesla',
      model: 'Model Y Dual Motor AWD',
      year: 2024,
      category: CarCategory.ELECTRIC,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.ELECTRIC,
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      dailyRate: 110,
      securityDeposit: 300,
      licensePlate: 'DHK-MET-EV-01-3042',
      vin: '5YJYGDEE8PF910283',
      currentHubId: 'hub_banani',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 52,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=800&q=80'],
      features: ['520km Range', 'Autopilot Hardware', 'Supercharging Enabled', 'Glass Roof', 'Premium Audio']
    },
    {
      id: 'car_mercedes_eclass',
      name: 'Mercedes-Benz E-Class AMG Line',
      brand: 'Mercedes-Benz',
      model: 'E 300 AMG Line',
      year: 2024,
      category: CarCategory.LUXURY,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      dailyRate: 160,
      securityDeposit: 400,
      licensePlate: 'DHK-MET-GHA-18-7741',
      vin: 'WDD2130831A910284',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 5.0,
      reviewCount: 41,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=800&q=80'],
      features: ['Burmester 3D Sound', 'Air Balance', 'MBUX Navigation', 'Nappa Leather', 'Executive Rear Package']
    },
    {
      id: 'car_mustang_gt',
      name: 'Ford Mustang GT V8 Convertible',
      brand: 'Ford',
      model: 'Mustang GT 5.0 V8',
      year: 2024,
      category: CarCategory.SPORTS,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 4,
      doors: 2,
      luggageCapacity: 2,
      dailyRate: 175,
      securityDeposit: 450,
      licensePlate: 'DHK-MET-GA-22-1082',
      vin: '1FA6P8CF4N5192841',
      currentHubId: 'hub_gulshan',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 33,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?auto=format&fit=crop&w=800&q=80'],
      features: ['V8 450HP Engine', 'Convertible Soft Top', 'Brembo Brakes', 'Sport Exhaust Valve', 'Track Apps']
    },
    {
      id: 'car_hiace_vip',
      name: 'Toyota HiAce VIP Super Grandia',
      brand: 'Toyota',
      model: 'HiAce Super Grandia VIP',
      year: 2024,
      category: CarCategory.PASSENGER_VAN,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.DIESEL,
      seats: 10,
      doors: 5,
      luggageCapacity: 8,
      dailyRate: 130,
      securityDeposit: 250,
      licensePlate: 'DHK-MET-CHA-55-9011',
      vin: 'JT3HN12A9K1928371',
      currentHubId: 'hub_dac',
      status: CarStatus.MAINTENANCE,
      ratingAverage: 4.8,
      reviewCount: 57,
      isFeatured: false,
      images: ['https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'],
      features: ['Captain Recliner Seats', 'Dual Zone Climate AC', 'Overhead Screen', 'Huge Luggage Trunk', 'USB Ports All Rows']
    },
    {
      id: 'car_bmw_5series',
      name: 'BMW 530i M Sport',
      brand: 'BMW',
      model: '530i M Sport LCI',
      year: 2024,
      category: CarCategory.LUXURY,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      dailyRate: 140,
      securityDeposit: 350,
      licensePlate: 'DHK-MET-GHA-17-4821',
      vin: 'WBA53BJ04NW891024',
      currentHubId: 'hub_banani',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 38,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80'],
      features: ['Harman Kardon Audio', 'Head-Up Display', 'Wireless Apple CarPlay', 'M Sport Brakes']
    },
    {
      id: 'car_honda_crv',
      name: 'Honda CR-V Turbo Prestige',
      brand: 'Honda',
      model: 'CR-V 1.5 VTEC Turbo',
      year: 2024,
      category: CarCategory.SUV,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 7,
      doors: 5,
      luggageCapacity: 4,
      dailyRate: 80,
      securityDeposit: 200,
      licensePlate: 'DHK-MET-KHA-19-3382',
      vin: '7FARW2H81PE910283',
      currentHubId: 'hub_ctg',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.8,
      reviewCount: 44,
      isFeatured: false,
      images: ['https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=800&q=80'],
      features: ['Honda Sensing ADAS', 'Hands-free Power Tailgate', 'Panoramic Roof', '7 Seat Config']
    },
    {
      id: 'car_nissan_x_trail',
      name: 'Nissan X-Trail e-POWER AWD',
      brand: 'Nissan',
      model: 'X-Trail e-POWER Ti-L',
      year: 2024,
      category: CarCategory.SUV,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.HYBRID,
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      dailyRate: 85,
      securityDeposit: 220,
      licensePlate: 'DHK-MET-GHA-16-1920',
      vin: 'JN1TCNT33U0192841',
      currentHubId: 'hub_sylhet',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.7,
      reviewCount: 26,
      isFeatured: false,
      images: ['https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80'],
      features: ['e-4ORCE AWD', 'ProPILOT with Navi-link', 'Bose 10-Speaker Audio', 'Zero Gravity Seats']
    },
    {
      id: 'car_toyota_harrier',
      name: 'Toyota Harrier Elegance Plus',
      brand: 'Toyota',
      model: 'Harrier 2.0 Dynamic Force',
      year: 2024,
      category: CarCategory.SUV,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      dailyRate: 95,
      securityDeposit: 250,
      licensePlate: 'DHK-MET-GHA-20-4491',
      vin: 'JTMBA3EV2P0192847',
      currentHubId: 'hub_gulshan',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 50,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'],
      features: ['Dimmable Panoramic Roof', 'Digital Rearview Mirror', 'Toyota Safety Sense 3.0', 'JBL Sound']
    },
    {
      id: 'car_toyota_corolla_cross',
      name: 'Toyota Corolla Cross Hybrid',
      brand: 'Toyota',
      model: 'Corolla Cross 1.8 HEV',
      year: 2024,
      category: CarCategory.SUV,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.HYBRID,
      seats: 5,
      doors: 5,
      luggageCapacity: 3,
      dailyRate: 65,
      securityDeposit: 150,
      licensePlate: 'DHK-MET-KHA-22-9910',
      vin: 'MR0BA3EV1P0192842',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.8,
      reviewCount: 68,
      isFeatured: false,
      images: ['https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=800&q=80'],
      features: ['24 km/L Fuel Economy', 'Apple CarPlay', 'Blind Spot Monitor', 'Electric Parking Brake']
    },
    {
      id: 'car_hyundai_ioniq5',
      name: 'Hyundai Ioniq 5 EV Lounge',
      brand: 'Hyundai',
      model: 'Ioniq 5 Long Range AWD',
      year: 2024,
      category: CarCategory.ELECTRIC,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.ELECTRIC,
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      dailyRate: 115,
      securityDeposit: 300,
      licensePlate: 'DHK-MET-EV-02-1092',
      vin: 'KM8KR4DE1PU192841',
      currentHubId: 'hub_banani',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 31,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=800&q=80'],
      features: ['Ultra-fast 800V Charging', 'V2L Power Outlet', 'Relaxation Comfort Seats', 'Vision Roof']
    },
    {
      id: 'car_toyota_camry',
      name: 'Toyota Camry Hybrid Executive',
      brand: 'Toyota',
      model: 'Camry 2.5 HEV Luxury',
      year: 2024,
      category: CarCategory.SEDAN,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.HYBRID,
      seats: 5,
      doors: 4,
      luggageCapacity: 3,
      dailyRate: 85,
      securityDeposit: 200,
      licensePlate: 'DHK-MET-GA-15-7721',
      vin: '4T1B21HK1PU192842',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 58,
      isFeatured: false,
      images: ['https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=800&q=80'],
      features: ['Executive Reclining Rear Seats', 'Rear Console Touchscreen', 'Ventilated Front Seats', 'JBL Sound']
    },
    {
      id: 'car_porsche_macan',
      name: 'Porsche Macan GTS Sport',
      brand: 'Porsche',
      model: 'Macan GTS 2.9 TT V6',
      year: 2024,
      category: CarCategory.SPORTS,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 5,
      doors: 5,
      luggageCapacity: 3,
      dailyRate: 220,
      securityDeposit: 600,
      licensePlate: 'DHK-MET-GA-25-9901',
      vin: 'WP1AA2A51PL192841',
      currentHubId: 'hub_gulshan',
      status: CarStatus.AVAILABLE,
      ratingAverage: 5.0,
      reviewCount: 22,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80'],
      features: ['440HP Twin-Turbo V6', 'Sport Chrono Package', 'Air Suspension with PASM', 'Sport Exhaust']
    },
    {
      id: 'car_range_rover_sport',
      name: 'Range Rover Sport Dynamic SE',
      brand: 'Land Rover',
      model: 'Range Rover Sport P400',
      year: 2024,
      category: CarCategory.LUXURY,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      dailyRate: 210,
      securityDeposit: 550,
      licensePlate: 'DHK-MET-GHA-23-1102',
      vin: 'SALWR2V41PA192841',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 5.0,
      reviewCount: 39,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'],
      features: ['Dynamic Air Suspension', 'Meridian 3D Sound', 'All-Wheel Steering', 'Pixel LED']
    },
    {
      id: 'car_lexus_rx350',
      name: 'Lexus RX 350 F-Sport',
      brand: 'Lexus',
      model: 'RX 350 F SPORT AWD',
      year: 2024,
      category: CarCategory.LUXURY,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 5,
      doors: 5,
      luggageCapacity: 4,
      dailyRate: 150,
      securityDeposit: 350,
      licensePlate: 'DHK-MET-GHA-21-8840',
      vin: '2T2HAMA81PC192841',
      currentHubId: 'hub_gulshan',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 34,
      isFeatured: false,
      images: ['https://images.unsplash.com/photo-1594502184342-2e12f877aa73?auto=format&fit=crop&w=800&q=80'],
      features: ['Mark Levinson 21-Speaker Audio', 'F SPORT Adaptive Variable Suspension', 'Panoramic Sunroof']
    },
    {
      id: 'car_toyota_noah_hybrid',
      name: 'Toyota Noah S-Z VIP Luxury Van',
      brand: 'Toyota',
      model: 'Noah Hybrid S-Z 7-Seater',
      year: 2024,
      category: CarCategory.PASSENGER_VAN,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.HYBRID,
      seats: 7,
      doors: 5,
      luggageCapacity: 5,
      dailyRate: 90,
      securityDeposit: 200,
      licensePlate: 'DHK-MET-CHA-54-1029',
      vin: 'MR0BA3EV8P0192849',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.8,
      reviewCount: 47,
      isFeatured: false,
      images: ['https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'],
      features: ['Captain Seats with Ottoman', 'Dual Power Sliding Doors', 'Rear TV Monitor', '23.4 km/L Hybrid']
    },
    {
      id: 'car_audi_q7',
      name: 'Audi Q7 55 TFSI Quattro',
      brand: 'Audi',
      model: 'Q7 S-Line 7-Seater',
      year: 2024,
      category: CarCategory.SUV,
      transmission: Transmission.AUTOMATIC,
      fuelType: FuelType.PETROL,
      seats: 7,
      doors: 5,
      luggageCapacity: 5,
      dailyRate: 180,
      securityDeposit: 450,
      licensePlate: 'DHK-MET-GHA-24-3391',
      vin: 'WAUZZZ4M8ND192841',
      currentHubId: 'hub_dac',
      status: CarStatus.AVAILABLE,
      ratingAverage: 4.9,
      reviewCount: 43,
      isFeatured: true,
      images: ['https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=800&q=80'],
      features: ['Adaptive Air Suspension', 'Bang & Olufsen 3D Sound', 'Virtual Cockpit Plus', 'HD Matrix LED']
    }
  ];

  for (const car of carsData) {
    const { images, features, ...carFields } = car;
    await prisma.car.upsert({
      where: { id: car.id },
      update: carFields,
      create: {
        ...carFields,
        images: {
          create: images.map((url, i) => ({ url, isPrimary: i === 0, displayOrder: i }))
        },
        features: {
          create: features.map(name => ({ name }))
        }
      }
    });
  }

  // ========================================================
  // 4. DYNAMIC PRICING RULES (10 Records)
  // ========================================================
  console.log('📈 Seeding Pricing Rules...');
  const rulesData = [
    { id: 'rule_1', name: 'Weekend Surge Special', code: 'WEEKEND_SURGE', category: CarCategory.LUXURY, multiplier: 1.15, driverDailyRate: 35, isActive: true },
    { id: 'rule_2', name: 'Long-term 7+ Days Discount', code: 'LONG_TERM_7', multiplier: 0.90, driverDailyRate: 30, isActive: true },
    { id: 'rule_3', name: 'Airport Hub Priority Rate', code: 'AIRPORT_HUB', multiplier: 1.05, driverDailyRate: 40, isActive: true },
    { id: 'rule_4', name: 'Eid Festival Surge', code: 'EID_SURGE', multiplier: 1.25, driverDailyRate: 50, isActive: true },
    { id: 'rule_5', name: 'Electric Green Mobility Discount', code: 'EV_DISCOUNT', category: CarCategory.ELECTRIC, multiplier: 0.92, driverDailyRate: 30, isActive: true },
    { id: 'rule_6', name: 'Corporate Business Tier', code: 'CORP_PRESTIGE', multiplier: 0.88, driverDailyRate: 35, isActive: true },
    { id: 'rule_7', name: 'Off-Peak Midweek Saver', code: 'MIDWEEK_SAVER', multiplier: 0.95, driverDailyRate: 25, isActive: true },
    { id: 'rule_8', name: 'Monsoon Offroad Special', code: 'MONSOON_4X4', category: CarCategory.SUV, multiplier: 1.10, driverDailyRate: 40, isActive: true },
    { id: 'rule_9', name: 'VIP Chauffeur Bundle', code: 'VIP_CHAUFFEUR', multiplier: 1.12, driverDailyRate: 45, isActive: true },
    { id: 'rule_10', name: 'Winter Tour Package', code: 'WINTER_TOUR', multiplier: 1.08, driverDailyRate: 35, isActive: true }
  ];

  for (const r of rulesData) {
    await prisma.pricingRule.upsert({
      where: { code: r.code },
      update: r,
      create: r
    });
  }

  // ========================================================
  // 5. DISCOUNT PROMO COUPONS (10 Records)
  // ========================================================
  console.log('🏷️ Seeding Promo Discount Coupons...');
  const couponsData = [
    { id: 'cpn_1', code: 'WEEKEND20', discountType: DiscountType.PERCENTAGE, discountValue: 20, minBookingAmount: 150, maxDiscountAmount: 100, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 500, usedCount: 240, isActive: true },
    { id: 'cpn_2', code: 'AIRPORTVIP', discountType: DiscountType.FIXED_AMOUNT, discountValue: 25, minBookingAmount: 100, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 300, usedCount: 185, isActive: true },
    { id: 'cpn_3', code: 'TESLAFUTURE', discountType: DiscountType.PERCENTAGE, discountValue: 15, minBookingAmount: 200, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 200, usedCount: 92, isActive: true },
    { id: 'cpn_4', code: 'FIRSTDRIVE', discountType: DiscountType.PERCENTAGE, discountValue: 10, minBookingAmount: 50, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 1000, usedCount: 640, isActive: true },
    { id: 'cpn_5', code: 'LUXURY50', discountType: DiscountType.FIXED_AMOUNT, discountValue: 50, minBookingAmount: 300, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 150, usedCount: 78, isActive: true },
    { id: 'cpn_6', code: 'CHATTOGRAM30', discountType: DiscountType.FIXED_AMOUNT, discountValue: 30, minBookingAmount: 150, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 250, usedCount: 110, isActive: true },
    { id: 'cpn_7', code: 'SYLHETTOUR', discountType: DiscountType.PERCENTAGE, discountValue: 12, minBookingAmount: 180, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 200, usedCount: 88, isActive: true },
    { id: 'cpn_8', code: 'SUMMERFEST', discountType: DiscountType.PERCENTAGE, discountValue: 18, minBookingAmount: 220, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 400, usedCount: 215, isActive: true },
    { id: 'cpn_9', code: 'CORPORATE100', discountType: DiscountType.FIXED_AMOUNT, discountValue: 100, minBookingAmount: 600, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 100, usedCount: 45, isActive: true },
    { id: 'cpn_10', code: 'BESTCARE10', discountType: DiscountType.PERCENTAGE, discountValue: 10, minBookingAmount: 0, startDate: new Date('2026-01-01'), endDate: new Date('2026-12-31'), usageLimit: 2000, usedCount: 1420, isActive: true }
  ];

  for (const c of couponsData) {
    await prisma.discountCoupon.upsert({
      where: { code: c.code },
      update: c,
      create: c
    });
  }

  // ========================================================
  // 6. BOOKINGS (20 Records)
  // ========================================================
  console.log('📑 Seeding Bookings & Chauffeur Assignments...');
  const bookingsData = [
    {
      id: 'bkg_1',
      bookingCode: 'BC-2026-8910',
      userId: 'usr_cust_1',
      carId: 'car_jaguar_xe',
      driverId: 'usr_driver_1',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_dac',
      pickupDateTime: new Date('2026-03-01T10:00:00Z'),
      dropoffDateTime: new Date('2026-03-04T10:00:00Z'),
      totalDays: 3,
      dailyRate: 85,
      baseAmount: 255,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 54,
      securityDeposit: 250,
      totalAmount: 399,
      status: BookingStatus.ACTIVE_RENTAL,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_2',
      bookingCode: 'BC-2026-8911',
      userId: 'usr_cust_2',
      carId: 'car_audi_a6',
      driverId: 'usr_driver_2',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_gulshan',
      pickupDateTime: new Date('2026-02-20T09:00:00Z'),
      dropoffDateTime: new Date('2026-02-23T09:00:00Z'),
      totalDays: 3,
      dailyRate: 95,
      baseAmount: 285,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.VIP_FULL_SHIELD,
      protectionFee: 90,
      securityDeposit: 300,
      totalAmount: 465,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_3',
      bookingCode: 'BC-2026-8912',
      userId: 'usr_cust_3',
      carId: 'car_prado_suv',
      driverId: 'usr_driver_3',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_dac',
      pickupDateTime: new Date('2026-03-05T08:00:00Z'),
      dropoffDateTime: new Date('2026-03-09T08:00:00Z'),
      totalDays: 4,
      dailyRate: 145,
      baseAmount: 580,
      driverFee: 120,
      withDriver: true,
      protectionPlan: ProtectionPlan.VIP_FULL_SHIELD,
      protectionFee: 120,
      securityDeposit: 350,
      totalAmount: 820,
      status: BookingStatus.CONFIRMED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_4',
      bookingCode: 'BC-2026-8913',
      userId: 'usr_cust_4',
      carId: 'car_tesla_modely',
      driverId: null,
      pickupHubId: 'hub_banani',
      dropoffHubId: 'hub_banani',
      pickupDateTime: new Date('2026-02-15T12:00:00Z'),
      dropoffDateTime: new Date('2026-02-18T12:00:00Z'),
      totalDays: 3,
      dailyRate: 110,
      baseAmount: 330,
      driverFee: 0,
      withDriver: false,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 54,
      securityDeposit: 300,
      totalAmount: 384,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_5',
      bookingCode: 'BC-2026-8914',
      userId: 'usr_cust_5',
      carId: 'car_mercedes_eclass',
      driverId: 'usr_driver_8',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_gulshan',
      pickupDateTime: new Date('2026-03-02T14:00:00Z'),
      dropoffDateTime: new Date('2026-03-05T14:00:00Z'),
      totalDays: 3,
      dailyRate: 160,
      baseAmount: 480,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.VIP_FULL_SHIELD,
      protectionFee: 90,
      securityDeposit: 400,
      totalAmount: 660,
      status: BookingStatus.ACTIVE_RENTAL,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_6',
      bookingCode: 'BC-2026-8915',
      userId: 'usr_cust_6',
      carId: 'car_mustang_gt',
      driverId: null,
      pickupHubId: 'hub_gulshan',
      dropoffHubId: 'hub_gulshan',
      pickupDateTime: new Date('2026-02-25T11:00:00Z'),
      dropoffDateTime: new Date('2026-02-27T11:00:00Z'),
      totalDays: 2,
      dailyRate: 175,
      baseAmount: 350,
      driverFee: 0,
      withDriver: false,
      protectionPlan: ProtectionPlan.VIP_FULL_SHIELD,
      protectionFee: 60,
      securityDeposit: 450,
      totalAmount: 410,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_7',
      bookingCode: 'BC-2026-8916',
      userId: 'usr_cust_7',
      carId: 'car_nissan_x_trail',
      driverId: 'usr_driver_7',
      pickupHubId: 'hub_sylhet',
      dropoffHubId: 'hub_sylhet',
      pickupDateTime: new Date('2026-03-08T09:00:00Z'),
      dropoffDateTime: new Date('2026-03-12T09:00:00Z'),
      totalDays: 4,
      dailyRate: 85,
      baseAmount: 340,
      driverFee: 120,
      withDriver: true,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 72,
      securityDeposit: 220,
      totalAmount: 532,
      status: BookingStatus.CONFIRMED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_8',
      bookingCode: 'BC-2026-8917',
      userId: 'usr_cust_8',
      carId: 'car_honda_crv',
      driverId: 'usr_driver_5',
      pickupHubId: 'hub_ctg',
      dropoffHubId: 'hub_ctg',
      pickupDateTime: new Date('2026-02-18T10:00:00Z'),
      dropoffDateTime: new Date('2026-02-22T10:00:00Z'),
      totalDays: 4,
      dailyRate: 80,
      baseAmount: 320,
      driverFee: 120,
      withDriver: true,
      protectionPlan: ProtectionPlan.BASIC_CDW,
      protectionFee: 0,
      securityDeposit: 200,
      totalAmount: 440,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_9',
      bookingCode: 'BC-2026-8918',
      userId: 'usr_cust_9',
      carId: 'car_porsche_macan',
      driverId: null,
      pickupHubId: 'hub_gulshan',
      dropoffHubId: 'hub_gulshan',
      pickupDateTime: new Date('2026-03-10T15:00:00Z'),
      dropoffDateTime: new Date('2026-03-13T15:00:00Z'),
      totalDays: 3,
      dailyRate: 220,
      baseAmount: 660,
      driverFee: 0,
      withDriver: false,
      protectionPlan: ProtectionPlan.VIP_FULL_SHIELD,
      protectionFee: 90,
      securityDeposit: 600,
      totalAmount: 750,
      status: BookingStatus.CONFIRMED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_10',
      bookingCode: 'BC-2026-8919',
      userId: 'usr_cust_10',
      carId: 'car_bmw_5series',
      driverId: 'usr_driver_4',
      pickupHubId: 'hub_banani',
      dropoffHubId: 'hub_dac',
      pickupDateTime: new Date('2026-02-12T10:00:00Z'),
      dropoffDateTime: new Date('2026-02-15T10:00:00Z'),
      totalDays: 3,
      dailyRate: 140,
      baseAmount: 420,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 54,
      securityDeposit: 350,
      totalAmount: 564,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_11',
      bookingCode: 'BC-2026-8920',
      userId: 'usr_cust_11',
      carId: 'car_toyota_harrier',
      driverId: 'usr_driver_6',
      pickupHubId: 'hub_gulshan',
      dropoffHubId: 'hub_dac',
      pickupDateTime: new Date('2026-03-04T09:00:00Z'),
      dropoffDateTime: new Date('2026-03-07T09:00:00Z'),
      totalDays: 3,
      dailyRate: 95,
      baseAmount: 285,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 54,
      securityDeposit: 250,
      totalAmount: 429,
      status: BookingStatus.ACTIVE_RENTAL,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_12',
      bookingCode: 'BC-2026-8921',
      userId: 'usr_cust_12',
      carId: 'car_toyota_corolla_cross',
      driverId: null,
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_dac',
      pickupDateTime: new Date('2026-02-22T08:00:00Z'),
      dropoffDateTime: new Date('2026-02-25T08:00:00Z'),
      totalDays: 3,
      dailyRate: 65,
      baseAmount: 195,
      driverFee: 0,
      withDriver: false,
      protectionPlan: ProtectionPlan.BASIC_CDW,
      protectionFee: 0,
      securityDeposit: 150,
      totalAmount: 195,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_13',
      bookingCode: 'BC-2026-8922',
      userId: 'usr_cust_13',
      carId: 'car_hyundai_ioniq5',
      driverId: null,
      pickupHubId: 'hub_banani',
      dropoffHubId: 'hub_banani',
      pickupDateTime: new Date('2026-03-12T10:00:00Z'),
      dropoffDateTime: new Date('2026-03-15T10:00:00Z'),
      totalDays: 3,
      dailyRate: 115,
      baseAmount: 345,
      driverFee: 0,
      withDriver: false,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 54,
      securityDeposit: 300,
      totalAmount: 399,
      status: BookingStatus.PENDING,
      paymentStatus: PaymentStatus.PENDING
    },
    {
      id: 'bkg_14',
      bookingCode: 'BC-2026-8923',
      userId: 'usr_cust_14',
      carId: 'car_toyota_camry',
      driverId: 'usr_driver_1',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_dac',
      pickupDateTime: new Date('2026-02-14T09:00:00Z'),
      dropoffDateTime: new Date('2026-02-17T09:00:00Z'),
      totalDays: 3,
      dailyRate: 85,
      baseAmount: 255,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 54,
      securityDeposit: 200,
      totalAmount: 399,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_15',
      bookingCode: 'BC-2026-8924',
      userId: 'usr_cust_1',
      carId: 'car_range_rover_sport',
      driverId: 'usr_driver_3',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_gulshan',
      pickupDateTime: new Date('2026-03-15T12:00:00Z'),
      dropoffDateTime: new Date('2026-03-18T12:00:00Z'),
      totalDays: 3,
      dailyRate: 210,
      baseAmount: 630,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.VIP_FULL_SHIELD,
      protectionFee: 90,
      securityDeposit: 550,
      totalAmount: 810,
      status: BookingStatus.CONFIRMED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_16',
      bookingCode: 'BC-2026-8925',
      userId: 'usr_cust_2',
      carId: 'car_lexus_rx350',
      driverId: 'usr_driver_2',
      pickupHubId: 'hub_gulshan',
      dropoffHubId: 'hub_gulshan',
      pickupDateTime: new Date('2026-02-05T08:00:00Z'),
      dropoffDateTime: new Date('2026-02-08T08:00:00Z'),
      totalDays: 3,
      dailyRate: 150,
      baseAmount: 450,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.VIP_FULL_SHIELD,
      protectionFee: 90,
      securityDeposit: 350,
      totalAmount: 630,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_17',
      bookingCode: 'BC-2026-8926',
      userId: 'usr_cust_3',
      carId: 'car_toyota_noah_hybrid',
      driverId: 'usr_driver_8',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_dac',
      pickupDateTime: new Date('2026-03-01T10:00:00Z'),
      dropoffDateTime: new Date('2026-03-05T10:00:00Z'),
      totalDays: 4,
      dailyRate: 90,
      baseAmount: 360,
      driverFee: 120,
      withDriver: true,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 72,
      securityDeposit: 200,
      totalAmount: 552,
      status: BookingStatus.ACTIVE_RENTAL,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_18',
      bookingCode: 'BC-2026-8927',
      userId: 'usr_cust_4',
      carId: 'car_audi_q7',
      driverId: 'usr_driver_4',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_dac',
      pickupDateTime: new Date('2026-03-06T09:00:00Z'),
      dropoffDateTime: new Date('2026-03-10T09:00:00Z'),
      totalDays: 4,
      dailyRate: 180,
      baseAmount: 720,
      driverFee: 120,
      withDriver: true,
      protectionPlan: ProtectionPlan.VIP_FULL_SHIELD,
      protectionFee: 120,
      securityDeposit: 450,
      totalAmount: 960,
      status: BookingStatus.CONFIRMED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_19',
      bookingCode: 'BC-2026-8928',
      userId: 'usr_cust_5',
      carId: 'car_hyundai_tucson',
      driverId: null,
      pickupHubId: 'hub_gulshan',
      dropoffHubId: 'hub_gulshan',
      pickupDateTime: new Date('2026-01-20T10:00:00Z'),
      dropoffDateTime: new Date('2026-01-23T10:00:00Z'),
      totalDays: 3,
      dailyRate: 75,
      baseAmount: 225,
      driverFee: 0,
      withDriver: false,
      protectionPlan: ProtectionPlan.BASIC_CDW,
      protectionFee: 0,
      securityDeposit: 200,
      totalAmount: 225,
      status: BookingStatus.COMPLETED,
      paymentStatus: PaymentStatus.PAID
    },
    {
      id: 'bkg_20',
      bookingCode: 'BC-2026-8929',
      userId: 'usr_cust_6',
      carId: 'car_audi_a6',
      driverId: 'usr_driver_6',
      pickupHubId: 'hub_dac',
      dropoffHubId: 'hub_banani',
      pickupDateTime: new Date('2026-03-20T08:00:00Z'),
      dropoffDateTime: new Date('2026-03-23T08:00:00Z'),
      totalDays: 3,
      dailyRate: 95,
      baseAmount: 285,
      driverFee: 90,
      withDriver: true,
      protectionPlan: ProtectionPlan.COMPREHENSIVE_PLUS,
      protectionFee: 54,
      securityDeposit: 300,
      totalAmount: 429,
      status: BookingStatus.PENDING,
      paymentStatus: PaymentStatus.PENDING
    }
  ];

  for (const b of bookingsData) {
    await prisma.booking.upsert({
      where: { id: b.id },
      update: b,
      create: b
    });
  }

  // ========================================================
  // 7. PAYMENTS & INVOICES (20 Records)
  // ========================================================
  console.log('💳 Seeding Payments & Invoices...');
  const methods = [
    PaymentMethod.CREDIT_CARD,
    PaymentMethod.BKASH,
    PaymentMethod.NAGAD,
    PaymentMethod.CREDIT_CARD,
    PaymentMethod.DEBIT_CARD,
    PaymentMethod.CASH
  ];

  for (let i = 0; i < bookingsData.length; i++) {
    const b = bookingsData[i];
    const isPaid = b.paymentStatus === PaymentStatus.PAID;
    const payment = await prisma.payment.upsert({
      where: { id: `pay_${b.id}` },
      update: {
        amount: b.totalAmount,
        paymentStatus: isPaid ? PaymentStatus.PAID : PaymentStatus.PENDING,
        paidAt: isPaid ? new Date() : null
      },
      create: {
        id: `pay_${b.id}`,
        transactionId: `TXN-${Math.floor(10000000 + Math.random() * 90000000)}`,
        bookingId: b.id,
        userId: b.userId,
        amount: b.totalAmount,
        currency: 'USD',
        paymentMethod: methods[i % methods.length],
        paymentStatus: isPaid ? PaymentStatus.PAID : PaymentStatus.PENDING,
        paidAt: isPaid ? new Date() : null
      }
    });

    await prisma.invoice.upsert({
      where: { id: `inv_${b.id}` },
      update: {
        total: b.totalAmount,
        paidAt: isPaid ? new Date() : null
      },
      create: {
        id: `inv_${b.id}`,
        invoiceNumber: `INV-2026-${1000 + i}`,
        bookingId: b.id,
        userId: b.userId,
        paymentId: payment.id,
        subtotal: b.baseAmount + b.driverFee,
        tax: Number((b.totalAmount * 0.05).toFixed(2)),
        discount: 0,
        total: b.totalAmount,
        paidAt: isPaid ? new Date() : null,
        pdfUrl: `https://bestcare.com/invoices/INV-2026-${1000 + i}.pdf`
      }
    });
  }

  // ========================================================
  // 8. CUSTOMER REVIEWS & RATINGS (20 Records)
  // ========================================================
  console.log('⭐ Seeding Customer Reviews & Star Ratings...');
  const reviewsData = [
    { id: 'rev_1', bookingId: 'bkg_2', userId: 'usr_cust_2', carId: 'car_audi_a6', rating: 5, driverRating: 5, comment: 'Outstanding Audi A6! Extremely smooth highway ride and driver Kamal was very punctual.', status: ReviewStatus.APPROVED },
    { id: 'rev_2', bookingId: 'bkg_4', userId: 'usr_cust_4', carId: 'car_tesla_modely', rating: 5, driverRating: null, comment: 'Loved driving the Tesla Model Y. Autopilot worked flawlessly and battery lasted the entire trip!', status: ReviewStatus.APPROVED },
    { id: 'rev_3', bookingId: 'bkg_6', userId: 'usr_cust_6', carId: 'car_mustang_gt', rating: 5, driverRating: null, comment: 'The V8 rumble is intoxicating! Best sports car rental experience in Dhaka.', status: ReviewStatus.APPROVED },
    { id: 'rev_4', bookingId: 'bkg_8', userId: 'usr_cust_8', carId: 'car_honda_crv', rating: 4, driverRating: 5, comment: 'Comfortable family trip in Chattogram. Driver Mahbub knew all scenic routes.', status: ReviewStatus.APPROVED },
    { id: 'rev_5', bookingId: 'bkg_10', userId: 'usr_cust_10', carId: 'car_bmw_5series', rating: 5, driverRating: 5, comment: 'Executive luxury at its best. Harman Kardon sound was phenomenal.', status: ReviewStatus.APPROVED },
    { id: 'rev_6', bookingId: 'bkg_12', userId: 'usr_cust_12', carId: 'car_toyota_corolla_cross', rating: 4, driverRating: null, comment: 'Incredible fuel economy! Very practical city crossover.', status: ReviewStatus.APPROVED },
    { id: 'rev_7', bookingId: 'bkg_14', userId: 'usr_cust_14', carId: 'car_toyota_camry', rating: 5, driverRating: 5, comment: 'Rear executive recliner seats are top-notch. Highly recommended for corporate travel.', status: ReviewStatus.APPROVED },
    { id: 'rev_8', bookingId: 'bkg_16', userId: 'usr_cust_2', carId: 'car_lexus_rx350', rating: 5, driverRating: 5, comment: 'Mark Levinson sound system blew me away. Immaculate luxury.', status: ReviewStatus.APPROVED },
    { id: 'rev_9', bookingId: 'bkg_19', userId: 'usr_cust_5', carId: 'car_hyundai_tucson', rating: 4, driverRating: null, comment: 'Clean car, smooth pickup at Gulshan hub. Great service.', status: ReviewStatus.APPROVED },
    { id: 'rev_10', bookingId: 'bkg_1', userId: 'usr_cust_1', carId: 'car_jaguar_xe', rating: 5, driverRating: 5, comment: 'Prestigious Jaguar XE. Superb styling and very responsive.', status: ReviewStatus.APPROVED },
    { id: 'rev_11', bookingId: 'bkg_3', userId: 'usr_cust_3', carId: 'car_prado_suv', rating: 5, driverRating: 5, comment: 'Prado 4x4 handled rainy roads effortlessly. Spacious for 7 people.', status: ReviewStatus.APPROVED },
    { id: 'rev_12', bookingId: 'bkg_5', userId: 'usr_cust_5', carId: 'car_mercedes_eclass', rating: 5, driverRating: 5, comment: 'Mercedes-Benz AMG Line was pristine. Chauffeur Monir was extremely courteous.', status: ReviewStatus.APPROVED },
    { id: 'rev_13', bookingId: 'bkg_7', userId: 'usr_cust_7', carId: 'car_nissan_x_trail', rating: 4, driverRating: 5, comment: 'e-POWER hybrid was whisper quiet during our Sylhet tea garden tour.', status: ReviewStatus.APPROVED },
    { id: 'rev_14', bookingId: 'bkg_9', userId: 'usr_cust_9', carId: 'car_porsche_macan', rating: 5, driverRating: null, comment: 'Pure adrenaline and precision. Unbelievable acceleration!', status: ReviewStatus.APPROVED },
    { id: 'rev_15', bookingId: 'bkg_11', userId: 'usr_cust_11', carId: 'car_toyota_harrier', rating: 5, driverRating: 5, comment: 'Harrier elegance is unmatched. Dimmable glass roof was super cool.', status: ReviewStatus.APPROVED },
    { id: 'rev_16', bookingId: 'bkg_15', userId: 'usr_cust_1', carId: 'car_range_rover_sport', rating: 5, driverRating: 5, comment: 'King of SUVs. Dynamic air suspension feels like floating on clouds.', status: ReviewStatus.APPROVED },
    { id: 'rev_17', bookingId: 'bkg_17', userId: 'usr_cust_3', carId: 'car_toyota_noah_hybrid', rating: 5, driverRating: 5, comment: 'Family loved the captain seats and rear entertainment screen.', status: ReviewStatus.APPROVED },
    { id: 'rev_18', bookingId: 'bkg_18', userId: 'usr_cust_4', carId: 'car_audi_q7', rating: 5, driverRating: 5, comment: 'Spacious 7-seater with sport performance. Audi Matrix LED lights are great at night.', status: ReviewStatus.APPROVED },
    { id: 'rev_19', bookingId: 'bkg_13', userId: 'usr_cust_13', carId: 'car_hyundai_ioniq5', rating: 5, driverRating: null, comment: 'Futuristic design and incredibly quiet ride. Loved every minute!', status: ReviewStatus.APPROVED },
    { id: 'rev_20', bookingId: 'bkg_20', userId: 'usr_cust_6', carId: 'car_audi_a6', rating: 5, driverRating: 5, comment: 'Best luxury rental service in Bangladesh. Seamless experience!', status: ReviewStatus.APPROVED }
  ];

  for (const r of reviewsData) {
    await prisma.review.upsert({
      where: { id: r.id },
      update: r,
      create: r
    });
  }

  // ========================================================
  // 9. AVAILABILITY BLOCKS (15 Records)
  // ========================================================
  console.log('🔧 Seeding Availability Blocks & Maintenance Schedules...');
  const blocksData = [
    { id: 'blk_1', carId: 'car_hiace_vip', startDate: new Date('2026-08-25'), endDate: new Date('2026-09-02'), status: CarStatus.MAINTENANCE, note: 'Periodic Brake & Engine Overhaul' },
    { id: 'blk_2', carId: 'car_jaguar_xe', startDate: new Date('2026-09-10'), endDate: new Date('2026-09-12'), status: CarStatus.AVAILABLE, note: 'VIP Showroom Display Hold' },
    { id: 'blk_3', carId: 'car_audi_a6', startDate: new Date('2026-09-15'), endDate: new Date('2026-09-18'), status: CarStatus.RENTED, note: 'Corporate Exhibition Reservation' },
    { id: 'blk_4', carId: 'car_prado_suv', startDate: new Date('2026-09-20'), endDate: new Date('2026-09-22'), status: CarStatus.MAINTENANCE, note: '4x4 Suspension Routine Check' },
    { id: 'blk_5', carId: 'car_tesla_modely', startDate: new Date('2026-09-05'), endDate: new Date('2026-09-07'), status: CarStatus.MAINTENANCE, note: 'Software Update & Battery Diagnostic' },
    { id: 'blk_6', carId: 'car_mercedes_eclass', startDate: new Date('2026-09-25'), endDate: new Date('2026-09-28'), status: CarStatus.AVAILABLE, note: 'Diplomatic State Summit Hold' },
    { id: 'blk_7', carId: 'car_mustang_gt', startDate: new Date('2026-09-18'), endDate: new Date('2026-09-20'), status: CarStatus.AVAILABLE, note: 'Track Day Showcase' },
    { id: 'blk_8', carId: 'car_bmw_5series', startDate: new Date('2026-10-01'), endDate: new Date('2026-10-03'), status: CarStatus.MAINTENANCE, note: 'Detailing & Ceramic Coating' },
    { id: 'blk_9', carId: 'car_honda_crv', startDate: new Date('2026-10-05'), endDate: new Date('2026-10-08'), status: CarStatus.AVAILABLE, note: 'Chattogram Hub Rotation' },
    { id: 'blk_10', carId: 'car_porsche_macan', startDate: new Date('2026-10-10'), endDate: new Date('2026-10-12'), status: CarStatus.MAINTENANCE, note: 'Brembo Brake Pad Replacement' },
    { id: 'blk_11', carId: 'car_range_rover_sport', startDate: new Date('2026-10-15'), endDate: new Date('2026-10-17'), status: CarStatus.AVAILABLE, note: 'Airport VIP Delegation Hold' },
    { id: 'blk_12', carId: 'car_toyota_harrier', startDate: new Date('2026-10-20'), endDate: new Date('2026-10-22'), status: CarStatus.MAINTENANCE, note: 'Scheduled 15,000km Service' },
    { id: 'blk_13', carId: 'car_hyundai_ioniq5', startDate: new Date('2026-10-25'), endDate: new Date('2026-10-27'), status: CarStatus.MAINTENANCE, note: 'Tire Rotation & Balance' },
    { id: 'blk_14', carId: 'car_toyota_noah_hybrid', startDate: new Date('2026-11-01'), endDate: new Date('2026-11-04'), status: CarStatus.MAINTENANCE, note: 'Air Conditioner Deep Clean' },
    { id: 'blk_15', carId: 'car_audi_q7', startDate: new Date('2026-11-10'), endDate: new Date('2026-11-12'), status: CarStatus.MAINTENANCE, note: 'Winter Service Inspection' }
  ];

  for (const b of blocksData) {
    await prisma.carAvailability.upsert({
      where: { id: b.id },
      update: b,
      create: b
    });
  }

  console.log('🛠️ Seeding Workshop Maintenance Schedules...');
  const maintenanceSchedulesData = [
    { id: 'maint_1', carId: 'car_hiace_vip', maintenanceType: MaintenanceType.ROUTINE_OIL_FILTER_SERVICE, title: 'Engine Oil & Filter Service', description: 'Synthetic 5W-30 flush and filter swap', cost: 120, startDate: new Date('2026-08-25'), endDate: new Date('2026-09-02'), isCompleted: false, servicedBy: 'Navana Workshop Dhaka' },
    { id: 'maint_2', carId: 'car_porsche_macan', maintenanceType: MaintenanceType.BRAKE_PAD_REPLACEMENT, title: 'Brembo Brake Overhaul', description: 'Front ceramic carbon compound brake pads', cost: 450, startDate: new Date('2026-10-10'), endDate: new Date('2026-10-12'), isCompleted: false, servicedBy: 'Porsche Certified Center' },
    { id: 'maint_3', carId: 'car_tesla_modely', maintenanceType: MaintenanceType.BATTERY_HEALTH_CHECK, title: 'High Voltage Battery Diagnostics', description: 'Firmware 2026 update and cell balancing', cost: 180, startDate: new Date('2026-09-05'), endDate: new Date('2026-09-07'), isCompleted: false, servicedBy: 'Tesla EV Hub Dhaka' },
    { id: 'maint_4', carId: 'car_bmw_5series', maintenanceType: MaintenanceType.CERAMIC_DETAILING, title: '9H Ceramic Shield Detailing', description: 'Full body clay bar, polish, and nano coating', cost: 350, startDate: new Date('2026-10-01'), endDate: new Date('2026-10-03'), isCompleted: false, servicedBy: 'Auto Spa Gulshan' },
    { id: 'maint_5', carId: 'car_toyota_harrier', maintenanceType: MaintenanceType.ROUTINE_OIL_FILTER_SERVICE, title: '15,000 KM Periodic Maintenance', description: 'Coolant check, engine oil, spark plugs', cost: 150, startDate: new Date('2026-10-20'), endDate: new Date('2026-10-22'), isCompleted: false, servicedBy: 'Rangs Workshop' },
    { id: 'maint_6', carId: 'car_hyundai_ioniq5', maintenanceType: MaintenanceType.TIRE_ALIGNMENT_ROTATION, title: 'Michelin EV Tire Rotation & Alignment', description: '3D laser wheel alignment and balancing', cost: 90, startDate: new Date('2026-10-25'), endDate: new Date('2026-10-27'), isCompleted: false, servicedBy: 'Bridgestone Care CTG' },
    { id: 'maint_7', carId: 'car_toyota_noah_hybrid', maintenanceType: MaintenanceType.AC_DEEP_CLEAN, title: 'Air Conditioner Deep Clean & Gas Refill', description: 'Evaporator antibacterial wash and R134a refill', cost: 110, startDate: new Date('2026-11-01'), endDate: new Date('2026-11-04'), isCompleted: false, servicedBy: 'Cooling Hub Dhaka' },
    { id: 'maint_8', carId: 'car_prado_suv', maintenanceType: MaintenanceType.BODY_PAINT_REPAIR, title: 'Bumper Scuff Paint Recovery', description: 'OEM pearl white blending and clear coat', cost: 220, startDate: new Date('2026-09-20'), endDate: new Date('2026-09-22'), isCompleted: false, servicedBy: 'Navana Body Shop' }
  ];

  for (const m of maintenanceSchedulesData) {
    await prisma.maintenanceSchedule.upsert({
      where: { id: m.id },
      update: m,
      create: m
    });
  }

  console.log('🎒 Seeding Booking Addon Items...');
  const bookingAddonsData = [
    { id: 'addon_1', bookingId: 'bkg_1', addon: RentalAddon.PORTABLE_WIFI_HOTSPOT, dailyPrice: 8, totalPrice: 24 },
    { id: 'addon_2', bookingId: 'bkg_1', addon: RentalAddon.DASHCAM_RECORDER, dailyPrice: 5, totalPrice: 15 },
    { id: 'addon_3', bookingId: 'bkg_3', addon: RentalAddon.CHILD_BABY_SEAT, dailyPrice: 10, totalPrice: 40 },
    { id: 'addon_4', bookingId: 'bkg_3', addon: RentalAddon.ROOF_LUGGAGE_BOX, dailyPrice: 15, totalPrice: 60 },
    { id: 'addon_5', bookingId: 'bkg_5', addon: RentalAddon.PORTABLE_WIFI_HOTSPOT, dailyPrice: 8, totalPrice: 24 },
    { id: 'addon_6', bookingId: 'bkg_7', addon: RentalAddon.DASHCAM_RECORDER, dailyPrice: 5, totalPrice: 20 },
    { id: 'addon_7', bookingId: 'bkg_8', addon: RentalAddon.CHILD_BABY_SEAT, dailyPrice: 10, totalPrice: 40 },
    { id: 'addon_8', bookingId: 'bkg_10', addon: RentalAddon.PORTABLE_WIFI_HOTSPOT, dailyPrice: 8, totalPrice: 16 },
    { id: 'addon_9', bookingId: 'bkg_14', addon: RentalAddon.ADDITIONAL_DRIVER_PERMIT, dailyPrice: 12, totalPrice: 36 },
    { id: 'addon_10', bookingId: 'bkg_17', addon: RentalAddon.PET_PROTECTION_COVER, dailyPrice: 7, totalPrice: 35 }
  ];

  for (const a of bookingAddonsData) {
    await prisma.bookingAddon.upsert({
      where: { id: a.id },
      update: a,
      create: a
    });
  }

  // ========================================================
  // 10. EXECUTIVE REPORT RECORDS (5 Records)
  // ========================================================
  console.log('📊 Seeding Executive Analytics Report Records...');
  const reportsData = [
    { id: 'rpt_1', reportType: ReportType.REVENUE, title: 'January 2026 Fleet Revenue & Expense Audit', generatedById: 'usr_admin_1', summaryJson: { revenue: 18500, expenses: 7200, bookingsCount: 85, topHub: 'DAC Airport' } },
    { id: 'rpt_2', reportType: ReportType.REVENUE, title: 'February 2026 Executive Financial Performance', generatedById: 'usr_admin_1', summaryJson: { revenue: 24200, expenses: 8400, bookingsCount: 112, topHub: 'DAC Airport' } },
    { id: 'rpt_3', reportType: ReportType.FLEET_UTILIZATION, title: 'Q1 2026 Fleet Utilization & Downtime Log', generatedById: 'usr_admin_2', summaryJson: { utilizationRate: 88, maintenanceHours: 42, activeCars: 19 } },
    { id: 'rpt_4', reportType: ReportType.USER_ANALYTICS, title: 'Chauffeur Satisfaction & Safety Ratings 2026', generatedById: 'usr_admin_3', summaryJson: { averageDriverRating: 4.9, totalTrips: 1240, onTimeRate: 98.4 } },
    { id: 'rpt_5', reportType: ReportType.BOOKING_SUMMARY, title: 'Q1 Customer Acquisition & KYC Verification Report', generatedById: 'usr_admin_1', summaryJson: { newCustomers: 340, kycApprovalRate: 96.2, retentionRate: 84.5 } }
  ];

  for (const r of reportsData) {
    await prisma.reportRecord.upsert({
      where: { id: r.id },
      update: r,
      create: r
    });
  }

  console.log('✅ DATABASE SEEDING COMPLETED SUCCESSFULLY!');
  console.log('📊 Total Records Seeded: 150+');
  console.log('   - 5 Location Hubs');
  console.log('   - 25 Users & Drivers (Admin, Customer, Car Driver)');
  console.log('   - 20 Fleet Cars & Specifications (Linked to Drivers/Owners)');
  console.log('   - 10 Pricing Rules');
  console.log('   - 10 Discount Coupons');
  console.log('   - 20 Booking Reservations & Driver Assignments (Service Types & Statuses)');
  console.log('   - 10 Booking Addons & Accessories');
  console.log('   - 20 Payments & Invoices');
  console.log('   - 20 Customer Reviews & Star Ratings');
  console.log('   - 15 Availability & Calendar Blocks');
  console.log('   - 8 Maintenance Workshop Schedules');
  console.log('   - 5 Executive Report Records');
}

main()
  .catch((e) => {
    console.error('❌ Seeding failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
