import { Injectable, Logger } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';
import axios from 'axios';
import { CarsService } from '../cars/cars.service';
import { RagQueryDto } from './dto/rag-query.dto';
import { RecommendCarDto } from './dto/recommend-car.dto';

interface ChatTurn {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

@Injectable()
export class AiProxyService {
  private readonly logger = new Logger(AiProxyService.name);
  private readonly aiServiceUrl: string;
  private readonly geminiApiKey: string;
  private readonly geminiModels: string[];
  private sessionStore = new Map<string, ChatTurn[]>();

  constructor(
    private readonly httpService: HttpService,
    private readonly carsService: CarsService
  ) {
    this.aiServiceUrl = process.env.AI_SERVICE_URL || 'http://localhost:8000';
    this.geminiApiKey = process.env.GEMINI_API_KEY || '';
    this.geminiModels = [
      process.env.GEMINI_MODEL || 'gemini-3.6-flash',
      'gemini-3.5-flash-lite',
      'gemini-3.5-flash',
      'gemini-3.7-flash'
    ];
  }

  async agenticChat(
    dto: { query: string; sessionId?: string; userId?: string; category?: string },
    currentUser?: any,
    authHeader?: string
  ) {
    const sessionId = dto.sessionId || `session_${Date.now()}`;
    const userRole = currentUser?.role || 'CUSTOMER';
    const userName = currentUser?.name || currentUser?.customerName || 'Shahriar Khan';

    // 1. Try forwarding to standalone Python RAG AI microservice if available
    try {
      const headers: Record<string, string> = {};
      if (authHeader) {
        headers['Authorization'] = authHeader;
      }

      const payload = {
        query: dto.query,
        session_id: sessionId,
        user_id: currentUser?.id || dto.userId || 'usr_cust_1',
        user_name: userName,
        user_email: currentUser?.email || 'customer@example.com',
        user_phone: currentUser?.phone || '+8801819234567',
        user_role: userRole,
        category: dto.category
      };

      const response = await firstValueFrom(
        this.httpService.post(`${this.aiServiceUrl}/rag/chat`, payload, {
          headers,
          timeout: 25000
        })
      );
      const d = response.data;
      this.recordTurn(sessionId, 'user', dto.query);
      this.recordTurn(sessionId, 'assistant', d.answer || d.message || '');

      return {
        session_id: d.session_id || sessionId,
        query: dto.query,
        answer: d.answer || d.message || '',
        message: d.message || d.answer || '',
        language: d.language || 'english',
        intent: d.intent || 'general_faq',
        query_type: d.query_type || 'hybrid',
        confidence_score: d.confidence_score || 0.96,
        sources: d.sources || [],
        matched_vehicles: d.matched_vehicles || [],
        booking_action: d.booking_action,
        data: d.data || []
      };
    } catch (microserviceErr: any) {
      this.logger.log(
        `Standalone AI Microservice notice (${microserviceErr.message}). Engaging Gateway Direct Gemini & Fleet RAG Engine.`
      );
    }

    // 2. Fallback: Direct Gemini LLM + Live Database Fleet RAG inside Gateway
    return await this.executeGatewayDirectRAG(dto.query, sessionId, userName, dto.category);
  }

  private async executeGatewayDirectRAG(
    query: string,
    sessionId: string,
    userName: string,
    categoryFilter?: string
  ) {
    const allCars = this.carsService.findAll();
    const hubs = this.carsService.getHubs();

    // Detect language
    const lang = this.detectLanguage(query);

    // Filter relevant fleet candidates
    const matchedCars = this.findMatchingCars(query, allCars, categoryFilter);

    // Save user turn
    this.recordTurn(sessionId, 'user', query);

    // Try Gemini API directly
    let generatedText = '';
    if (this.geminiApiKey) {
      generatedText = await this.callGeminiDirect(query, sessionId, userName, lang, allCars, hubs);
    }

    // If Gemini was unreachable or failed, synthesize dynamic grounded response
    if (!generatedText) {
      generatedText = this.synthesizeDynamicGroundedResponse(query, lang, matchedCars, userName);
    }

    // Save assistant turn
    this.recordTurn(sessionId, 'assistant', generatedText);

    // Build rich source citations
    const sources = matchedCars.slice(0, 3).map((c) => ({
      title: `${c.name} (${c.category.toUpperCase()})`,
      category: 'Fleet Specs',
      score: 0.92
    }));

    if (sources.length === 0) {
      sources.push(
        { title: 'Best Care Rental Terms & Policies', category: 'Rental Policy', score: 0.95 },
        { title: 'Hub Locations & Pickup Guidelines', category: 'Hub Guide', score: 0.91 }
      );
    }

    // Detect booking action in fallback
    let bookingAction: any = null;
    const qLower = query.toLowerCase();
    if (qLower.includes('book') || qLower.includes('reserve') || qLower.includes('rent')) {
      const topCar = matchedCars[0];
      if (topCar) {
        bookingAction = {
          status: 'collecting',
          collected: {
            car_id: topCar.id,
            car_name: topCar.name,
            daily_rate: topCar.dailyRate,
            category: topCar.category
          },
          missing: ['pickup_date', 'pickup_location']
        };
      }
    }

    return {
      session_id: sessionId,
      query,
      answer: generatedText,
      message: generatedText,
      language: lang,
      intent: this.detectIntent(query),
      query_type: 'semantic_rag',
      confidence_score: 0.96,
      sources,
      matched_vehicles: matchedCars.slice(0, 4).map((c) => ({
        id: c.id,
        name: c.name,
        brand: c.brand,
        model: c.model,
        dailyRate: c.dailyRate,
        seats: c.seats,
        category: c.category,
        image: c.images[0] || '',
        currentHub: typeof c.currentHub === 'object' && c.currentHub !== null ? (c.currentHub as any).name : c.currentHub,
        status: c.status
      })),
      booking_action: bookingAction,
      data: matchedCars.slice(0, 3).map((c) => ({
        id: `doc_${c.id}`,
        title: `${c.brand} ${c.name} (${c.category.toUpperCase()})`,
        category: 'Fleet Specs',
        content: `Model: ${c.name}. Category: ${c.category}. Daily Rate: $${c.dailyRate}/day. Security Deposit: $${c.securityDeposit}. Seats: ${c.seats}. Fuel: ${c.fuelType}. Hub: ${typeof c.currentHub === 'object' && c.currentHub !== null ? (c.currentHub as any).name : c.currentHub}. Status: ${c.status}. Rating: ${c.ratingAverage}/5.0.`
      }))
    };
  }

  private async callGeminiDirect(
    query: string,
    sessionId: string,
    userName: string,
    lang: string,
    cars: any[],
    hubs: any[]
  ): Promise<string> {
    const history = this.sessionStore.get(sessionId) || [];
    const historyStr = history
      .slice(-8)
      .map((h) => `${h.role === 'user' ? 'Customer' : 'Assistant'}: ${h.content}`)
      .join('\n');

    const fleetCatalog = cars
      .map(
        (c) =>
          `• [${c.id}] ${c.name} | Brand: ${c.brand} | Cat: ${c.category} | Rate: $${c.dailyRate}/day | Deposit: $${c.securityDeposit} | Seats: ${c.seats} | Fuel: ${c.fuelType} | Hub: ${typeof c.currentHub === 'object' && c.currentHub !== null ? (c.currentHub as any).name : c.currentHub} | Status: ${c.status} | Rating: ⭐${c.ratingAverage} | Features: ${c.features.join(', ')}`
      )
      .join('\n');

    const hubsList = hubs.map((h) => `${h.name} (${h.city})`).join(', ');

    const systemPrompt = `You are the AI Concierge and Fleet Specialist for "Best Care Car Rental" (Bangladesh's premier luxury & corporate car rental service).
Customer Name: ${userName}
Detected Preferred Language: ${lang}

LIVE VERIFIED COMPANY FLEET & POLICIES (DATABASE TRUTH):
${fleetCatalog}

HUBS / LOCATIONS:
${hubsList}

OFFICIAL RENTAL POLICIES:
- Security Deposit: $200 to $450 depending on vehicle tier (100% refundable within 24-48 hours after vehicle return).
- Cancellation Policy: 100% full refund for cancellations made >24 hours prior to booking pickup.
- Mileage: Unlimited mileage included on all rentals 3+ days.
- Chauffeur / Driver: Available for $25/day with professional verified drivers.
- Self-Drive Requirements: Valid driving license and national ID/passport.

CRITICAL INSTRUCTIONS:
1. Pay attention to the full conversation history. If the customer already specified a route (e.g. Khulna to Dhaka), retain that context!
2. If customer asks for recommendation for a specific number of passengers (e.g. "7 joner", "7 people", "family of 7"): ONLY recommend vehicles with AT LEAST that seating capacity (e.g., Toyota Land Cruiser Prado TX with 7 seats, or Toyota HiAce with 11 seats). Clearly state the seat capacity and why it fits!
3. If customer says "Audi book koro" or asks to book a specific car: Confirm their choice of that exact vehicle (e.g. Audi A6) and politely ask for their preferred pickup date, duration, and pickup hub location to finalize the booking!
4. Respond in the customer's language (${lang === 'banglish' ? 'Banglish (Bengali written in English letters, e.g. "Apnar 7 joner jattrar jonno amader 7-seater Toyota Land Cruiser Prado TX ($145/day) shobcheye best hobe...")' : lang === 'bangla' ? 'Standard Bengali script' : 'Polite, professional English'}).
5. Keep responses concise, organized with clean bullet points and emojis. Always encourage booking progress.`;

    const fullPrompt = `${systemPrompt}

RECENT CONVERSATION HISTORY:
${historyStr || '(No prior turns in this session)'}

CURRENT CUSTOMER MESSAGE:
"${query}"

CONCISE ASSISTANT RESPONSE:`;

    for (const model of this.geminiModels) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${this.geminiApiKey}`;
        const res = await axios.post(
          url,
          {
            contents: [{ parts: [{ text: fullPrompt }] }],
            generationConfig: {
              temperature: 0.2,
              maxOutputTokens: 800
            }
          },
          { timeout: 15000 }
        );

        const candidate = res.data?.candidates?.[0]?.content?.parts?.[0]?.text;
        if (candidate && candidate.trim()) {
          return candidate.trim();
        }
      } catch (err: any) {
        this.logger.debug(`Gemini model ${model} attempt failed: ${err.message}`);
      }
    }

    return '';
  }

  private synthesizeDynamicGroundedResponse(
    query: string,
    lang: string,
    matchedCars: any[],
    userName: string
  ): string {
    const q = query.toLowerCase();

    // 1. Specific Booking Intent
    if (q.includes('book') || q.includes('reserve') || q.includes('rent')) {
      const targetCar = matchedCars[0] || { name: 'Vehicle', dailyRate: 95, category: 'Luxury' };
      if (lang === 'banglish') {
        return `✨ **${targetCar.name}** select kora hoyeche!\n\n• **Daily Rate:** $${targetCar.dailyRate}/day\n• **Category:** ${targetCar.category}\n\nApni kon tarikh theke kon tarikh porjonto ebong kon location theke gari ti pickup korte chan janaben ki? Amra apnar booking confirm kore dicchi!`;
      } else if (lang === 'bangla') {
        return `✨ **${targetCar.name}** নির্বাচন করা হয়েছে!\n\n• **ভাড়া:** $${targetCar.dailyRate}/দিন\n• **ক্যাটাগরি:** ${targetCar.category}\n\nআপনি কোন তারিখ থেকে গাড়িটি পিকআপ করতে চান জানালে বুকিং নিশ্চিত করে দেওয়া হবে।`;
      }
      return `✨ **${targetCar.name}** selected for booking!\n\n• **Daily Rate:** $${targetCar.dailyRate}/day\n• **Category:** ${targetCar.category}\n\nPlease let us know your preferred pickup date, return date, and pickup location to finalize your reservation.`;
    }

    // 2. Passenger / Group Capacity (e.g. 7 joner, 7 seat, family)
    const seatMatch = q.match(/(\d+)\s*(?:jon|joner|seat|seater|passenger|person)/);
    if (seatMatch || q.includes('7 jon') || q.includes('7 joner') || q.includes('family') || q.includes('group')) {
      const passengerCount = seatMatch ? parseInt(seatMatch[1], 10) : 7;
      const largeCars = matchedCars.filter((c) => c.seats >= passengerCount);
      const chosenList = largeCars.length > 0 ? largeCars : matchedCars;

      if (lang === 'banglish') {
        const listStr = chosenList.slice(0, 2).map((c, i) =>
          `🚗 **${i + 1}. ${c.name} (${c.category})**\n• **Rate:** $${c.dailyRate}/day | **Seats:** ${c.seats} Persons\n• **Specs:** ${c.transmission} (${c.fuelType}) | ⭐ ${c.ratingAverage}/5.0`
        ).join('\n\n');
        return `Assalamu Alaikum ${userName}! Apnar **${passengerCount} joner** jattrar jonno amader best recommendations:\n\n${listStr}\n\n${chosenList[0]?.name || 'Toyota Prado'} apnader 7 joner shonge luggage soho aramdayok travel-er jonno perfect hobe! Apni ki eiti book korte chan?`;
      }

      const listStr = chosenList.slice(0, 2).map((c, i) =>
        `🚗 **${i + 1}. ${c.name} (${c.category})**\n• **Rate:** $${c.dailyRate}/day | **Seats:** ${c.seats} Passengers\n• **Specs:** ${c.transmission} (${c.fuelType}) | ⭐ ${c.ratingAverage}/5.0`
      ).join('\n\n');
      return `Hello ${userName}! For a group of **${passengerCount} passengers**, here are our top recommended spacious vehicles:\n\n${listStr}\n\nWould you like to reserve one of these for your journey?`;
    }

    // 3. Mountain / Off-road
    if (q.includes('sajek') || q.includes('sylhet') || q.includes('pahad') || q.includes('mountain') || q.includes('hill')) {
      if (lang === 'banglish') {
        return `Assalamu Alaikum ${userName}! Sajek ba Sylhet pahari rastar jonno amader 4x4 AWD SUVs perfect:\n\n🚗 **1. Toyota Land Cruiser Prado TX (4WD SUV)**\n• **Rate:** $145/day | **Deposit:** $350\n• **Specs:** 7 Seats, 5 Suitcases, Diff Lock & Terrain Control | ⭐ 4.9\n\n🚗 **2. Hyundai Tucson Limited (AWD SUV)**\n• **Rate:** $75/day | **Deposit:** $200\n• **Specs:** 5 Seats, 4 Suitcases, HTRAC All-Wheel Drive | ⭐ 4.7\n\nUnlimited mileage included for 3+ days. Driver service available for $25/day!`;
      }
      return `For mountain terrains like Sajek or Sylhet, we strongly recommend our 4WD SUVs:\n\n🚗 **1. Toyota Land Cruiser Prado TX (4WD SUV)** — $145/day (7 Seats, Diff Lock, 4x4)\n🚗 **2. Hyundai Tucson Limited (AWD SUV)** — $75/day (5 Seats, HTRAC All-Wheel Drive)\n\nBoth vehicles feature dual AC and comprehensive all-terrain safety.`;
    }

    // 4. Deposit & Refund Policies
    if (q.includes('deposit') || q.includes('refund') || q.includes('taka') || q.includes('policy') || q.includes('cancel')) {
      if (lang === 'banglish') {
        return `Best Care Car Rental-er policy summary:\n\n💳 **Security Deposit:**\n• Standard/Sedan: $200 - $300\n• Luxury/SUV: $350 - $450\n• Gari return korar 24-48 ghontar moddhe deposit 100% refund hoye jay.\n\n🔄 **Cancellation:**\n• Pickup shomoyer 24 ghonta age cancel korle 100% full refund paben.\n\n🛣️ **Mileage:** 3 diner beshi rent korle Unlimited mileage free!`;
      }
      return `Best Care Rental & Deposit Policy:\n\n💳 **Security Deposit:** $200 - $450 depending on vehicle category. 100% refunded within 24-48 hours after vehicle inspection.\n🔄 **Cancellation:** 100% full refund for cancellations made >24 hours prior to scheduled pickup.\n🛣️ **Mileage:** Unlimited mileage on bookings of 3 or more days.`;
    }

    // 5. Specific or general cars list
    const topCars = matchedCars.slice(0, 3);
    if (topCars.length > 0) {
      if (lang === 'banglish') {
        const carList = topCars
          .map(
            (c, i) =>
              `🚗 **${i + 1}. ${c.name} (${c.category})**\n• **Rate:** $${c.dailyRate}/day | **Deposit:** $${c.securityDeposit}\n• **Specs:** ${c.seats} Passengers, ${c.transmission} (${c.fuelType})\n• **Hub:** ${typeof c.currentHub === 'object' && c.currentHub !== null ? (c.currentHub as any).name : c.currentHub} | ⭐ ${c.ratingAverage}/5.0`
          )
          .join('\n\n');

        return `Assalamu Alaikum ${userName}! Apnar query onujayi amader best available options:\n\n${carList}\n\nApni kon tarikh theke kon tarikh porjonto gari ti book korte chan janaben ki?`;
      }

      if (lang === 'bangla') {
        const carList = topCars
          .map(
            (c, i) =>
              `🚗 **${i + 1}. ${c.name} (${c.category})**\n• **ভাড়া:** $${c.dailyRate}/দিন | **সিকিউরিটি ডিপোজিট:** $${c.securityDeposit}\n• **আসন:** ${c.seats} জন, ${c.transmission} (${c.fuelType})\n• **হাব লোকেশন:** ${typeof c.currentHub === 'object' && c.currentHub !== null ? (c.currentHub as any).name : c.currentHub} | ⭐ ${c.ratingAverage}/5.0`
          )
          .join('\n\n');

        return `আসসালামু আলাইকুম ${userName}! আপনার জন্য সেরা অপশনসমূহ:\n\n${carList}\n\nকোন গাড়িটি বুক করতে চান জানালে রিজার্ভেশন করে দিতে পারি।`;
      }

      const carList = topCars
        .map(
          (c, i) =>
            `🚗 **${i + 1}. ${c.name} (${c.category})**\n• **Rate:** $${c.dailyRate}/day | **Deposit:** $${c.securityDeposit}\n• **Specs:** ${c.seats} Passengers, ${c.transmission} (${c.fuelType})\n• **Hub:** ${typeof c.currentHub === 'object' && c.currentHub !== null ? (c.currentHub as any).name : c.currentHub} | ⭐ ${c.ratingAverage}/5.0`
        )
        .join('\n\n');

      return `Hello ${userName}! Here are our top available vehicles matching your request:\n\n${carList}\n\nWould you like to reserve one of these for your journey?`;
    }

    return `Best Care Car Rental এ আপনাকে স্বাগতম। আপনি গাড়ি ভাড়া, রেট, বা বুকিং সম্পর্কিত যেকোনো প্রশ্ন করতে পারেন।`;
  }

  private findMatchingCars(query: string, allCars: any[], categoryFilter?: string): any[] {
    const q = query.toLowerCase();

    if (categoryFilter && categoryFilter !== 'All') {
      const filtered = allCars.filter((c) => c.category.toLowerCase() === categoryFilter.toLowerCase());
      if (filtered.length > 0) return filtered;
    }

    // 1. Check passenger seat requirement (e.g. 7 joner, 7 seat, 10 seat, 6 person)
    const seatMatch = q.match(/(\d+)\s*(?:jon|joner|seat|seater|passenger|person)/);
    if (seatMatch) {
      const requiredSeats = parseInt(seatMatch[1], 10);
      const largeCars = allCars.filter((c) => c.seats >= requiredSeats);
      if (largeCars.length > 0) return largeCars;
    }

    // 2. Specific brand / model keywords
    if (q.includes('audi')) {
      const audiCars = allCars.filter((c) => c.brand.toLowerCase().includes('audi') || c.name.toLowerCase().includes('audi'));
      if (audiCars.length > 0) return audiCars;
    }
    if (q.includes('prado')) {
      const pradoCars = allCars.filter((c) => c.name.toLowerCase().includes('prado'));
      if (pradoCars.length > 0) return pradoCars;
    }
    if (q.includes('tucson')) {
      const tucsonCars = allCars.filter((c) => c.name.toLowerCase().includes('tucson'));
      if (tucsonCars.length > 0) return tucsonCars;
    }
    if (q.includes('mercedes') || q.includes('benz')) {
      const benzCars = allCars.filter((c) => c.brand.toLowerCase().includes('mercedes') || c.name.toLowerCase().includes('mercedes'));
      if (benzCars.length > 0) return benzCars;
    }
    if (q.includes('bmw')) {
      const bmwCars = allCars.filter((c) => c.brand.toLowerCase().includes('bmw') || c.name.toLowerCase().includes('bmw'));
      if (bmwCars.length > 0) return bmwCars;
    }
    if (q.includes('jaguar')) {
      const jagCars = allCars.filter((c) => c.brand.toLowerCase().includes('jaguar') || c.name.toLowerCase().includes('jaguar'));
      if (jagCars.length > 0) return jagCars;
    }
    if (q.includes('hiace') || q.includes('micro') || q.includes('van')) {
      const vanCars = allCars.filter((c) => c.category.toLowerCase() === 'passenger van' || c.seats >= 7);
      if (vanCars.length > 0) return vanCars;
    }
    if (q.includes('tesla') || q.includes('ev') || q.includes('electric')) {
      const evCars = allCars.filter((c) => c.category.toLowerCase() === 'electric');
      if (evCars.length > 0) return evCars;
    }

    // 3. Category keywords
    if (q.includes('suv') || q.includes('sajek') || q.includes('sylhet')) {
      return allCars.filter((c) => c.category.toLowerCase() === 'suv');
    }
    if (q.includes('luxury') || q.includes('vip')) {
      return allCars.filter((c) => c.category.toLowerCase() === 'luxury' || c.category.toLowerCase() === 'sedan');
    }
    if (q.includes('sports') || q.includes('mustang') || q.includes('convertible') || q.includes('v8')) {
      return allCars.filter((c) => c.category.toLowerCase() === 'sports');
    }
    if (q.includes('cheap') || q.includes('budget') || q.includes('sosta') || q.includes('kam rate')) {
      return [...allCars].sort((a, b) => a.dailyRate - b.dailyRate);
    }

    return allCars;
  }

  private detectLanguage(query: string): string {
    const banglaPattern = /[\u0980-\u09FF]/;
    if (banglaPattern.test(query)) {
      return 'bangla';
    }

    const banglishWords = [
      'ami', 'korte', 'chai', 'gari', 'bhara', 'koto', 'lagbe', 'ache', 'ki', 'apnader',
      'bhalo', 'shagotom', 'dorkar', 'kobe', 'pabo', 'kothay', 'sajek', 'chole', 'jabo',
      'konta', 'joner', 'jonno', 'koro', 'korbo', 'thik', 'hobe', 'kalke', 'tarikh', 'dekhao', 'chao'
    ];
    const qLower = query.toLowerCase();
    const isBanglish = banglishWords.some((w) => qLower.includes(w));
    if (isBanglish) {
      return 'banglish';
    }

    return 'english';
  }

  private detectIntent(query: string): string {
    const q = query.toLowerCase();
    if (q.includes('book') || q.includes('reserve') || q.includes('rent')) return 'booking_inquiry';
    if (q.includes('price') || q.includes('rate') || q.includes('koto') || q.includes('cost')) return 'price_inquiry';
    if (q.includes('sajek') || q.includes('sylhet') || q.includes('mountain') || q.includes('trip')) return 'trip_recommendation';
    if (q.includes('deposit') || q.includes('refund') || q.includes('policy')) return 'policy_inquiry';
    if (q.includes('jon') || q.includes('joner') || q.includes('seat') || q.includes('passenger') || q.includes('family')) return 'car_recommendation';
    return 'general_faq';
  }

  private recordTurn(sessionId: string, role: 'user' | 'assistant', content: string) {
    if (!this.sessionStore.has(sessionId)) {
      this.sessionStore.set(sessionId, []);
    }
    const turns = this.sessionStore.get(sessionId)!;
    turns.push({ role, content, timestamp: new Date().toISOString() });
    if (turns.length > 20) {
      turns.splice(0, turns.length - 20);
    }
  }

  async getSessionHistory(sessionId: string) {
    try {
      const response = await firstValueFrom(
        this.httpService.get(`${this.aiServiceUrl}/rag/sessions/${sessionId}/history`, { timeout: 3000 })
      );
      return response.data;
    } catch {
      const history = this.sessionStore.get(sessionId) || [];
      return {
        session_id: sessionId,
        total_turns: history.length,
        history: history.map((h) => ({
          role: h.role,
          message: h.content,
          timestamp: h.timestamp
        }))
      };
    }
  }

  async clearSessionHistory(sessionId: string) {
    try {
      await firstValueFrom(
        this.httpService.delete(`${this.aiServiceUrl}/rag/sessions/${sessionId}`, { timeout: 3000 })
      );
    } catch {
      this.sessionStore.delete(sessionId);
    }
    return { status: 'cleared', session_id: sessionId };
  }

  async executeRagQuery(dto: RagQueryDto) {
    return this.agenticChat({ query: dto.query, category: dto.category });
  }

  async recommendCar(dto: RecommendCarDto) {
    const prompt = `Recommend a car for ${dto.passengers || 4} passengers going to ${dto.terrain || 'highway'} with description: ${dto.tripDescription}`;
    return this.agenticChat({ query: prompt, category: 'Fleet Specs' });
  }

  async qualifyLead(dto: any) {
    try {
      const response = await firstValueFrom(
        this.httpService.post(`${this.aiServiceUrl}/rag/qualify-lead`, dto, {
          timeout: 4000
        })
      );
      return response.data;
    } catch {
      let score = 50;
      const reasons: string[] = [];

      if (dto.isCorporate) {
        score += 25;
        reasons.push('Corporate account client (+25)');
      }
      if (dto.totalDays && dto.totalDays >= 5) {
        score += 15;
        reasons.push('Long-term rental duration (+15)');
      }
      if (dto.estimatedBudget && dto.estimatedBudget >= 500) {
        score += 15;
        reasons.push('High estimated budget threshold (+15)');
      }
      if (
        dto.vehicleCategory &&
        (dto.vehicleCategory.toLowerCase().includes('luxury') ||
          dto.vehicleCategory.toLowerCase().includes('suv') ||
          dto.vehicleCategory.toLowerCase().includes('prado'))
      ) {
        score += 10;
        reasons.push('Premium/Luxury fleet tier selected (+10)');
      }
      if (
        dto.notes &&
        (dto.notes.toLowerCase().includes('vip') ||
          dto.notes.toLowerCase().includes('urgent') ||
          dto.notes.toLowerCase().includes('executive'))
      ) {
        score += 10;
        reasons.push('VIP/Executive special requirements (+10)');
      }

      score = Math.min(score, 98);
      let classification: 'Hot' | 'Warm' | 'Cold' = 'Cold';
      if (score >= 80) {
        classification = 'Hot';
      } else if (score >= 60) {
        classification = 'Warm';
      }

      return {
        lead_score: score,
        classification,
        confidence: 0.92,
        estimated_deal_value: dto.estimatedBudget
          ? `$${dto.estimatedBudget}`
          : `$${(dto.totalDays || 1) * 85}`,
        reasons,
        suggested_action:
          classification === 'Hot'
            ? 'Immediate Executive SLA Call & SMS'
            : classification === 'Warm'
            ? 'Automated Quotation & Vehicle Spec Dispatch'
            : 'Drip Marketing Campaign',
        summary: `Qualified as ${classification} lead (Score: ${score}/100) based on rental inquiry parameters.`
      };
    }
  }

  async getKnowledgeDocs() {
    try {
      const response = await firstValueFrom(
        this.httpService.get(`${this.aiServiceUrl}/rag/documents`, { timeout: 3000 })
      );
      return response.data;
    } catch {
      const cars = this.carsService.findAll();
      return {
        total: cars.length + 4,
        documents: [
          ...cars.map((c) => ({
            id: `doc_${c.id}`,
            category: 'Fleet Specs',
            title: `${c.brand} ${c.name} (${c.category})`
          })),
          { id: 'policy_deposit_refund', category: 'Rental Policy', title: 'Security Deposit & Refund Timelines' },
          { id: 'policy_cancellation', category: 'Rental Policy', title: 'Cancellation & 100% Refund Rules' },
          { id: 'guide_mountain_sajek', category: 'Trip Guide', title: 'Mountainous Road & 4x4 SUV Selection' },
          { id: 'guide_airport_transfer', category: 'Hub Guide', title: 'Hazrat Shahjalal Airport (DAC) Hub Pickup' }
        ]
      };
    }
  }
}
