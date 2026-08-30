import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { Payment, PaymentMethod, PaymentStatus } from '../../common/types/schema.types';
import { sanitizeText } from '../../common/security/sanitize.util';

@Injectable()
export class PaymentsService {
  private payments: Payment[] = [
    {
      id: 'txn_9001',
      transactionCode: 'TXN-892301',
      bookingId: 'bkg_1001',
      bookingCode: 'RC-BK-78901',
      userId: 'usr_cust_1',
      customerName: 'Shahriar Khan',
      amount: 815,
      currency: 'USD',
      paymentMethod: 'Credit Card',
      status: 'COMPLETED',
      paidAt: '2026-08-27T14:35:00Z',
      receiptUrl: 'https://rentcars.com/receipts/TXN-892301.pdf',
      createdAt: '2026-08-27T14:35:00Z'
    },
    {
      id: 'txn_9002',
      transactionCode: 'TXN-892302',
      bookingId: 'bkg_1002',
      bookingCode: 'RC-BK-78902',
      userId: 'usr_cust_2',
      customerName: 'Nusrat Jahan',
      amount: 380,
      currency: 'USD',
      paymentMethod: 'bKash',
      status: 'COMPLETED',
      paidAt: '2026-08-28T09:20:00Z',
      receiptUrl: 'https://rentcars.com/receipts/TXN-892302.pdf',
      createdAt: '2026-08-28T09:20:00Z'
    },
    {
      id: 'txn_9003',
      transactionCode: 'TXN-892303',
      bookingId: 'bkg_1004',
      bookingCode: 'RC-BK-78904',
      userId: 'usr_cust_1',
      customerName: 'Anisur Rahman',
      amount: 352,
      currency: 'USD',
      paymentMethod: 'Credit Card',
      status: 'COMPLETED',
      paidAt: '2026-08-19T11:25:00Z',
      receiptUrl: 'https://rentcars.com/receipts/TXN-892303.pdf',
      createdAt: '2026-08-19T11:25:00Z'
    }
  ];

  findAll(query?: { status?: string; search?: string; userId?: string }): Payment[] {
    let result = [...this.payments];

    if (query?.status && query.status !== 'All') {
      result = result.filter(p => p.status.toLowerCase() === query.status!.toLowerCase());
    }

    if (query?.userId) {
      result = result.filter(p => p.userId === query.userId);
    }

    if (query?.search) {
      const q = query.search.toLowerCase();
      result = result.filter(p =>
        p.transactionCode.toLowerCase().includes(q) ||
        p.bookingCode.toLowerCase().includes(q) ||
        p.customerName.toLowerCase().includes(q) ||
        p.paymentMethod.toLowerCase().includes(q)
      );
    }

    return result;
  }

  create(dto: { bookingId: string; bookingCode?: string; userId: string; customerName: string; amount: number; paymentMethod?: PaymentMethod }): Payment {
    const rawAmount = Number(dto.amount);
    // BUSINESS LOGIC & SECURITY FIX: Reject negative or non-positive payment amounts
    if (isNaN(rawAmount) || rawAmount <= 0) {
      throw new BadRequestException('Payment amount must be a positive number.');
    }

    const randomCode = `TXN-${Math.floor(100000 + Math.random() * 900000)}`;
    const newPayment: Payment = {
      id: `txn_${Date.now()}`,
      transactionCode: randomCode,
      bookingId: dto.bookingId,
      bookingCode: dto.bookingCode || `RC-BK-${Math.floor(10000 + Math.random() * 90000)}`,
      userId: dto.userId,
      customerName: sanitizeText(dto.customerName) || 'Customer',
      amount: rawAmount,
      currency: 'USD',
      paymentMethod: dto.paymentMethod || 'Credit Card',
      status: 'COMPLETED',
      paidAt: new Date().toISOString(),
      receiptUrl: `https://rentcars.com/receipts/${randomCode}.pdf`,
      createdAt: new Date().toISOString()
    };

    this.payments.unshift(newPayment);
    return newPayment;
  }

  refund(paymentId: string, reason?: string): Payment {
    const payment = this.payments.find(p => p.id === paymentId || p.transactionCode === paymentId || p.bookingId === paymentId);
    if (!payment) {
      throw new NotFoundException(`Payment record not found.`);
    }

    payment.status = 'REFUNDED';
    payment.refundedAt = new Date().toISOString();
    return payment;
  }

  getPaymentStats() {
    const completed = this.payments.filter(p => p.status === 'COMPLETED');
    const totalCollected = completed.reduce((sum, p) => sum + p.amount, 0);
    const refunded = this.payments.filter(p => p.status === 'REFUNDED').reduce((sum, p) => sum + p.amount, 0);

    return {
      totalCollected,
      refundedTotal: refunded,
      transactionCount: this.payments.length,
      methodBreakdown: {
        creditCard: this.payments.filter(p => p.paymentMethod === 'Credit Card').length,
        bKash: this.payments.filter(p => p.paymentMethod === 'bKash').length,
        cash: this.payments.filter(p => p.paymentMethod === 'Cash on Delivery').length,
      }
    };
  }
}
