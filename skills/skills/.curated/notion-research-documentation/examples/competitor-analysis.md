# Example: Competitor Analysis

## User Request

> "Research competitor pricing models and create a comparison document"

## Workflow Execution

### Step 1: Search for Competitor Information

```
Notion:notion-search
query: "competitor pricing"
query_type: "internal"
filters: {
  created_date_range: {
    start_date: "2024-01-01"
  }
}
```

**Results Found:**
- "Competitor Analysis - Stripe" (Product)
- "Market Research Q3 2024" (Strategy)
- "Pricing Strategy Discussion" (Product)
- "Competitor Feature Matrix" (Product)

### Step 2: Fetch and Analyze

```
Notion:notion-fetch for each page
```

**Extracted Information:**

**Stripe**:
- Pay-as-you-go: 2.9% + $0.30 per transaction
- No monthly fees
- Volume discounts available

**Square**:
- Pay-as-you-go: 2.6% + $0.10 per transaction
- Monthly plan: $29/month with lower rates
- Hardware costs separate

**PayPal**:
- Standard: 3.49% + $0.49 per transaction
- Advanced: $30/month + 2.59% + $0.49
- Multi-currency fees

**Adyen**:
- Interchange++ pricing model
- Custom enterprise pricing
- Setup and monthly fees apply

### Step 3: Create Comparison Document

```
Notion:notion-create-pages

pages: [{
  properties: {
    "title": "Competitor Pricing Analysis - Payment Processors"
  },
  content: "[Comparison document using template]"
}]
```

## Output Document

```markdown
# Competitor Pricing Analysis - Payment Processors

**Date**: October 14, 2025  
**Research Team**: Product Strategy

## Executive Summary

We analyzed four major payment processor competitors: Stripe, Square, PayPal, and Adyen. Pricing models vary from simple pay-as-you-go (Stripe) to complex interchange-plus (Adyen). Key insight: All competitors offer volume discounts for high-transaction merchants, with breakpoints typically at $100K/month processing volume.

## Comparison Matrix

| Feature | Stripe | Square | PayPal | Adyen |
|---------|--------|--------|--------|-------|
| **Base Rate** | 2.9% + $0.30 | 2.6% + $0.10 | 3.49% + $0.49 | Interchange++ |
| **Monthly Fee** | $0 | $0-29 | $0-30 | Custom |
| **Volume Discounts** | Yes, >$80K | Yes, >$250K | Yes, >$100K | Yes, custom |
| **Setup Fee** | $0 | $0 | $0 | $1,000-5,000 |
| **Multi-currency** | 1% extra | 3% extra | 3-4% extra | Included |
| **Chargeback Fee** | $15 | $15-25 | $20 | Custom |
| **Target Market** | Startups-Enterprise | Small-Medium | Small-Medium | Enterprise |

## Detailed Analysis

### Stripe

**Pricing Structure**:
- **Standard**: 2.9% + $0.30 per successful card charge
- **Volume discounts**: Available for businesses processing >$80,000/month
- **International cards**: +1% fee
- **Currency conversion**: 1% above market rate

**Strengths**:
- Simple, transparent pricing
- No setup fees or monthly minimums
- Excellent developer experience
- Quick onboarding

**Weaknesses**:
- Higher per-transaction fee for high volume
- Volume discounts less aggressive than Adyen

**Best for**: Startups and growth-stage companies needing quick integration

**Source**: <mention-page url="...">Competitor Analysis - Stripe</mention-page>

### Square

**Pricing Structure**:
- **Pay-as-you-go**: 2.6% + $0.10 per tap, dip, or swipe
- **Keyed-in**: 3.5% + $0.15
- **Plus plan**: $29/month for lower rates (2.5% + $0.10)
- **Premium plan**: Custom pricing

**Strengths**:
- Lowest per-transaction fee for in-person
- All-in-one hardware + software
- No long-term contracts

**Weaknesses**:
- Higher rates for online/keyed transactions
- Hardware costs ($49-$299)
- Less suitable for online-only businesses

**Best for**: Brick-and-mortar retail and restaurants

**Source**: <mention-page url="...">Market Research Q3 2024</mention-page>

### PayPal

**Pricing Structure**:
- **Standard**: 3.49% + $0.49 per transaction
- **Advanced**: $30/month + 2.59% + $0.49
- **Payments Pro**: Additional $30/month for direct credit card processing

**Strengths**:
- Huge customer base (PayPal checkout)
- Buyer protection increases trust
- International reach (200+ countries)

**Weaknesses**:
- Highest per-transaction fees
- Complex fee structure
- Account holds and reserves common

**Best for**: Businesses where PayPal brand trust matters (e-commerce, marketplaces)

**Source**: <mention-page url="...">Pricing Strategy Discussion</mention-page>

### Adyen

**Pricing Structure**:
- **Interchange++**: Actual interchange + scheme fees + fixed markup
- **Setup fee**: $1,000-5,000 (negotiable)
- **Monthly minimum**: Typically $10,000+ processing volume
- **Per-transaction**: Interchange + 0.6% + $0.12 (example)

**Strengths**:
- Most transparent cost structure at scale
- Lowest effective rate for high volume
- True multi-currency (100+ currencies)
- Direct connections to schemes

**Weaknesses**:
- Complex pricing requires analysis
- High minimums ($10K+/month)
- Longer integration time
- Not suitable for small businesses

**Best for**: Enterprise with $1M+/month processing volume

**Source**: <mention-page url="...">Competitor Feature Matrix</mention-page>

## Pricing Trends & Insights

### Volume-Based Discounting
All competitors offer discounts at scale:
- **Entry point**: $80K-$250K/month processing
- **Typical discount**: 10-30 basis points reduction
- **Negotiation leverage**: Begins at $500K/month+

### Hidden Costs to Consider

| Cost Type | Stripe | Square | PayPal | Adyen |
|-----------|--------|--------|--------|-------|
| Chargeback | $15 | $15-25 | $20 | $15-25 |
| Account verification | $0 | $0 | $0 | Varies |
| PCI compliance | $0 | $0 | $0 | $0 |
| Currency conversion | 1% | 3% | 3-4% | 0% |
| Refund fees | Returned | Returned | Not returned | Varies |

### Market Positioning

```
High Volume / Enterprise
    ↑
    |                    Adyen
    |                      
    |         Stripe             
    |    
    |  Square    PayPal
    |
    └──────────────────→
      Small / Simple        Complex / International
```

## Strategic Implications

### For Startups (<$100K/month)
**Recommended**: Stripe
- Lowest friction to start
- No upfront costs
- Great documentation
- Acceptable rates at this scale

### For Growing Companies ($100K-$1M/month)
**Recommended**: Stripe or Square
- Negotiate volume discounts
- Evaluate interchange++ if international
- Consider Square if in-person dominant

### For Enterprises (>$1M/month)
**Recommended**: Adyen or Negotiated Stripe
- Interchange++ models save significantly
- Direct scheme connections
- Multi-region capabilities matter
- ROI on integration complexity

## Recommendations

1. **Immediate**: Benchmark our current 2.8% + $0.25 against Stripe's standard
2. **Short-term**: Request volume discount quote from Stripe at our current $150K/month
3. **Long-term**: Evaluate Adyen when we cross $1M/month threshold

## Next Steps

- [ ] Request detailed pricing proposal from Stripe for volume discounts
- [ ] Create pricing calculator comparing all 4 at different volume levels
- [ ] Interview customers about payment method preferences
- [ ] Analyze our transaction mix (domestic vs international, card types)

## Sources

### Primary Research
- <mention-page url="...">Competitor Analysis - Stripe</mention-page>
- <mention-page url="...">Market Research Q3 2024</mention-page>
- <mention-page url="...">Pricing Strategy Discussion</mention-page>
- <mention-page url="...">Competitor Feature Matrix</mention-page>

### External References
- Stripe.com pricing page (Oct 2025)
- Square pricing documentation
- PayPal merchant fees
- Adyen pricing transparency report
```

## Key Success Factors

1. **Structured comparison**: Matrix format for quick scanning
2. **Multiple dimensions**: Price, features, target market
3. **Strategic recommendations**: Not just data, but implications
4. **Visual elements**: Table and positioning diagram
5. **Actionable next steps**: Clear recommendations
6. **Comprehensive sources**: Internal research + external validation

## Workflow Pattern Demonstrated

- **Date-filtered search** (recent information only)
- **Multiple competitor synthesis** (4 different companies)
- **Comparison template** (matrix + detailed analysis)
- **Strategic layer** (implications and recommendations)
- **Action-oriented** (next steps included)

