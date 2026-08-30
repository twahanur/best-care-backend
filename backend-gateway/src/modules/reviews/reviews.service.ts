import { Injectable, NotFoundException } from '@nestjs/common';
import { Review } from '../../common/types/schema.types';
import { CarsService } from '../cars/cars.service';
import { sanitizeText } from '../../common/security/sanitize.util';

@Injectable()
export class ReviewsService {
  constructor(private readonly carsService: CarsService) {}

  private reviews: Review[] = [
    {
      id: 'rev_1',
      bookingId: 'bkg_1001',
      userId: 'usr_cust_1',
      userName: 'Shahriar Khan',
      userAvatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80',
      carId: 'car_jaguar_xe',
      carName: 'Jaguar XE L Prestige',
      rating: 5,
      comment: 'Rented the Jaguar XE for a 4-day corporate summit. Vehicle was delivered sparkling clean directly to DAC Terminal 2 within 15 minutes. Outstanding service!',
      isApproved: true,
      adminReply: 'Thank you Mr. Shahriar! We look forward to hosting your next corporate expedition.',
      createdAt: '2026-08-28T10:00:00Z'
    },
    {
      id: 'rev_2',
      bookingId: 'bkg_1002',
      userId: 'usr_cust_2',
      userName: 'Nusrat Jahan',
      userAvatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80',
      carId: 'car_audi_a6',
      carName: 'Audi A6 Business Executive',
      rating: 5,
      comment: 'The booking process took under 2 minutes. The Audi A6 was in pristine condition, and the zero-excess protection allowed our team to travel with absolute peace of mind.',
      isApproved: true,
      adminReply: 'Glad you enjoyed the Audi A6! Travel safe.',
      createdAt: '2026-08-25T14:30:00Z'
    },
    {
      id: 'rev_3',
      bookingId: 'bkg_1003',
      userId: 'usr_cust_1',
      userName: 'Farhan Chowdhury',
      userAvatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80',
      carId: 'car_tesla_modely',
      carName: 'Tesla Model Y Long Range',
      rating: 5,
      comment: 'Took the Tesla Model Y for a weekend trip across Padma Expressway. Smooth performance, supercharging was effortless, and the 24/7 concierge support was extremely responsive.',
      isApproved: true,
      createdAt: '2026-08-22T09:15:00Z'
    }
  ];

  findAll(query?: { carId?: string; userId?: string; isApproved?: boolean }): Review[] {
    let result = [...this.reviews];

    if (query?.carId) {
      result = result.filter(r => r.carId === query.carId);
    }

    if (query?.userId) {
      result = result.filter(r => r.userId === query.userId);
    }

    if (query?.isApproved !== undefined) {
      result = result.filter(r => r.isApproved === query.isApproved);
    }

    return result;
  }

  create(dto: { bookingId: string; userId: string; userName: string; userAvatar?: string; carId: string; carName: string; rating: number; comment: string }): Review {
    const cleanUserName = sanitizeText(dto.userName) || 'Verified Renter';
    const cleanComment = sanitizeText(dto.comment);
    const cleanCarName = sanitizeText(dto.carName) || 'Fleet Vehicle';

    const newReview: Review = {
      id: `rev_${Date.now()}`,
      bookingId: dto.bookingId,
      userId: dto.userId,
      userName: cleanUserName,
      userAvatar: dto.userAvatar || `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(cleanUserName)}`,
      carId: dto.carId,
      carName: cleanCarName,
      rating: Math.min(5, Math.max(1, Number(dto.rating) || 5)),
      comment: cleanComment,
      isApproved: true,
      createdAt: new Date().toISOString()
    };

    this.reviews.unshift(newReview);
    // Update car score
    this.carsService.updateCarRating(dto.carId, newReview.rating);

    return newReview;
  }

  moderate(reviewId: string, isApproved: boolean, adminReply?: string): Review {
    const review = this.reviews.find(r => r.id === reviewId);
    if (!review) {
      throw new NotFoundException(`Review with ID "${reviewId}" not found.`);
    }

    review.isApproved = isApproved;
    if (adminReply !== undefined) {
      review.adminReply = sanitizeText(adminReply);
    }
    return review;
  }
}
