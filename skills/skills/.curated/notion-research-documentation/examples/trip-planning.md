# Example: Group Trip Research & Planning

**User Request**: "Research and plan our friends' trip to Japan in March - we're 6 people looking for 10 days"

## Workflow

### 1. Search Existing Notes
```
Notion:notion-search
query: "Japan travel"
```
Found: Japan Travel Guide (from friend), Tokyo Restaurants, Kyoto Temple Guide

### 2. Fetch & Extract Tips
```
Notion:notion-fetch (3x)
```
**Key info from previous travelers:**
- Best time: March-April (cherry blossoms)
- Must-see: Tokyo, Kyoto, Osaka
- Budget: $200-300/day (mid-range)
- Book accommodations 3 months ahead
- Get JR Pass before arrival
- Top restaurants: Sushi Dai, Ichiran Ramen, Tsunahachi Tempura

### 3. Research & Synthesize
Combined previous traveler insights with:
- Flight options and prices
- Accommodation types (hotels/ryokans/Airbnb)
- Transportation (JR Pass essential)
- 10-day itinerary structure
- Budget breakdown

### 4. Create Comprehensive Plan
```
Notion:notion-create-pages
parent: { page_id: "travel-plans-parent-id" }
pages: [{
  properties: {
    title: "Japan Trip 2026 - March 15-25 (10 Days)"
  },
  content: "[Full trip plan with itinerary, budget, tips...]"
}]
```

## Output Sample

```markdown
# Japan Trip 2026 - March 15-25 (10 Days)

## Trip Overview
**Dates**: March 15-25, 2026 (Cherry Blossom Season 🌸)
**Group**: 6 people | **Budget**: $3,000-4,000/person

## Itinerary Summary

**Days 1-3: Tokyo**
- Arrive, explore Shibuya, Harajuku, Shinjuku
- Visit Tsukiji Market, Imperial Palace, Sensoji Temple
- Experience Tokyo nightlife, teamLab Borderless

**Days 4-5: Hakone**  
- Day trip from Tokyo
- Hot springs, Mt. Fuji views, Lake Ashi cruise

**Days 6-8: Kyoto**
- Bullet train from Tokyo
- Fushimi Inari, Kinkaku-ji, Arashiyama Bamboo Grove
- Geisha district (Gion), traditional tea ceremony

**Days 9-10: Osaka + Depart**
- Osaka Castle, Dotonbori food district
- Nara day trip (deer park, Todai-ji Temple)
- Return flight from Osaka (KIX)

## Budget Breakdown (per person)
- **Flights**: $900-1,200 (round-trip)
- **Accommodations**: $700-1,000 (9 nights)
- **JR Pass**: $280 (7-day pass)
- **Food**: $500-700 ($50-70/day)
- **Activities**: $300-400
- **Local transport**: $100
**Total**: $2,780-3,680

## Key Bookings
- **Flights**: Book 3-4 months ahead
- **Hotels**: Book now (cherry blossom season)
  - Tokyo: Shinjuku area (2 nights) + Asakusa (1 night)
  - Kyoto: Gion area (3 nights)
  - Osaka: Namba area (2 nights)
- **JR Pass**: Order 2-3 weeks before travel
- **Restaurants**: Reserve 1 week ahead (Sushi Dai, high-end spots)

## Essential Tips
Source: <mention-page url="...">Japan Travel Guide</mention-page>
- Get pocket WiFi or eSIM on arrival
- Download: Google Translate, Hyperdia (train routes), Tabelog (restaurants)
- Cash-heavy country - withdraw at 7-Eleven ATMs
- Shoes off in temples, ryokans, some restaurants
- Trains extremely punctual - don't be late
- Learn basic phrases: arigatou, sumimasen, itadakimasu

## Packing List
- Comfortable walking shoes (10k+ steps/day)
- Light jacket (March 55-65°F)
- Backpack for day trips
- Cash pouch
- Portable charger

## Next Steps
- [ ] Book flights (target: <$1,100/person)
- [ ] Order JR Passes
- [ ] Book hotels (Tokyo → Kyoto → Osaka)
- [ ] Create shared expense tracker
- [ ] Schedule group planning call

## Sources
- <mention-page url="...">Japan Travel Guide</mention-page> (Sarah's 2024 trip)
- <mention-page url="...">Tokyo Restaurant Recommendations</mention-page>
- <mention-page url="...">Kyoto Temple Guide</mention-page>
```

## Key Takeaways
- Leveraged previous traveler notes from Notion
- Combined personal insights with research
- Created actionable itinerary with budget breakdown
- Included practical tips from experienced travelers
- Set clear next steps for group coordination
