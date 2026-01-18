# Currency Support Analysis for num2words2
## Generated: 2026-01-18

## Executive Summary
The num2words2 library supports **181 unique currency codes** across **51 languages** (68% of all implemented languages). However, there are significant gaps in currency support, particularly for major languages and their local currencies.

## Currency Support Statistics

### Global Overview
- **Total unique currencies**: 181
- **Languages with currency support**: 51 out of 75 (68%)
- **Languages without any currency support**: 24 (32%)
- **Most comprehensive**: Spanish (171 currencies), Catalan (167), Ukrainian (150)

### Top Supported Currencies by Language Count
| Currency | Code | Languages Supporting | Coverage % |
|----------|------|---------------------|------------|
| US Dollar | USD | 31 | 41% |
| Euro | EUR | 31 | 41% |
| British Pound | GBP | 23 | 31% |
| Russian Ruble | RUB | 12 | 16% |
| Chinese Yuan | CNY | 11 | 15% |
| Japanese Yen | JPY | 10 | 13% |
| Polish Złoty | PLN | 8 | 11% |
| Norwegian Krone | NOK | 8 | 11% |
| Canadian Dollar | CAD | 8 | 11% |
| Australian Dollar | AUD | 8 | 11% |

## Critical Gaps in Currency Support

### Major Languages WITHOUT Currency Support
These languages have no currency conversion capability at all:

| Language | Code | Speakers | Missing Local Currency |
|----------|------|----------|------------------------|
| English | en | Global | USD, GBP |
| English (India) | en_in | 125M | INR |
| Portuguese (Brazil) | pt_br | 260M | BRL |
| Turkish | tr | 80M | TRY |
| Hindi | hi | 600M | INR |
| Indonesian | id | 200M | IDR |
| Vietnamese | vi | 85M | VND |
| Korean | ko | 80M | KRW |
| Thai | th | 60M | THB |
| Malay | ms | 280M | MYR |

### Major Languages Missing Their LOCAL Currency
| Language | Has Currency Support | Missing Local Currency |
|----------|---------------------|------------------------|
| Chinese (all variants) | ❌ | CNY |
| Arabic | ✅ (only KWD, EGP, TND) | SAR, AED, QAR, OMR |
| Japanese | ✅ (only JPY) | ✓ Has local |
| Bengali | ❌ | BDT |
| Tamil | ❌ | INR, LKR |

## Missing Major World Currencies

### Top 20 Global Currencies by Trade Volume - Coverage Analysis
| Currency | Code | Global Trade Rank | Language Coverage |
|----------|------|------------------|-------------------|
| US Dollar | USD | #1 | ✅ Excellent (31 languages) |
| Euro | EUR | #2 | ✅ Excellent (31 languages) |
| Japanese Yen | JPY | #3 | ⚠️ Moderate (10 languages) |
| British Pound | GBP | #4 | ✅ Good (23 languages) |
| Chinese Yuan | CNY | #5 | ⚠️ Moderate (11 languages) |
| Australian Dollar | AUD | #6 | ⚠️ Limited (8 languages) |
| Canadian Dollar | CAD | #7 | ⚠️ Limited (8 languages) |
| Swiss Franc | CHF | #8 | ⚠️ Limited (7 languages) |
| Hong Kong Dollar | HKD | #9 | ❌ Poor (4 languages) |
| Singapore Dollar | SGD | #10 | ❌ Poor (5 languages) |
| Swedish Krona | SEK | #11 | ⚠️ Limited (7 languages) |
| South Korean Won | KRW | #12 | ❌ Poor (5 languages) |
| Norwegian Krone | NOK | #13 | ⚠️ Limited (8 languages) |
| New Zealand Dollar | NZD | #14 | ❌ Poor (4 languages) |
| Indian Rupee | INR | #15 | ⚠️ Limited (6 languages) |
| Mexican Peso | MXN | #16 | ⚠️ Limited (7 languages) |
| South African Rand | ZAR | #17 | ❌ Poor (3 languages) |
| Brazilian Real | BRL | #18 | ❌ Poor (4 languages) |
| Danish Krone | DKK | #19 | ❌ Poor (4 languages) |
| Thai Baht | THB | #20 | ❌ Poor (3 languages) |

### Cryptocurrency Support
**None found** - No support for any cryptocurrencies (BTC, ETH, etc.)

## Regional Currency Support Patterns

### European Union
All EU member languages properly support EUR:
- ✅ German (DE), French (FR), Italian (IT), Spanish (ES)
- ✅ Dutch (NL), Greek (EL), Portuguese (PT)
- ✅ Czech (CS), Slovak (SK), Polish (PL)

### Asia-Pacific
Limited regional currency support:
- ❌ No comprehensive Asian currency basket in any language
- ❌ Missing: SGD, MYR, THB, PHP, IDR in most languages
- ⚠️ Japanese (JA) only supports JPY
- ❌ Chinese languages lack any currency support

### Americas
Mixed support:
- ✅ Spanish variants have extensive coverage
- ❌ English lacks currency support entirely
- ❌ Portuguese (Brazil) lacks currency support

### Middle East & Africa
Very limited support:
- ⚠️ Arabic only supports 3 currencies (KWD, EGP, TND)
- ❌ Missing major currencies: SAR, AED, QAR, BHD, OMR
- ❌ African currencies poorly represented (only XOF, XAF, ZAR in few languages)

## Implementation Priorities

### Critical Priority (Major Languages)
1. **Add currency support to English (en)**
   - Currencies: USD, GBP, EUR, CAD, AUD at minimum

2. **Add currency support to Hindi (hi)**
   - Currencies: INR, USD, EUR, GBP

3. **Add currency support to Chinese variants**
   - Currencies: CNY, USD, EUR, HKD, TWD

4. **Add currency support to Portuguese Brazil (pt_br)**
   - Currencies: BRL, USD, EUR

### High Priority (Trade Currencies)
Add these major trade currencies to more languages:
- **Singapore Dollar (SGD)** - Currently only 5 languages
- **Hong Kong Dollar (HKD)** - Currently only 4 languages
- **South Korean Won (KRW)** - Currently only 5 languages
- **Swiss Franc (CHF)** - Currently only 7 languages

### Medium Priority (Regional Currencies)
Expand support for regional currencies in their respective language families:
- **Southeast Asian**: THB, MYR, SGD, PHP, IDR, VND
- **Middle Eastern**: SAR, AED, QAR, BHD, OMR, JOD
- **African**: ZAR, NGN, KES, GHS, EGP, MAD
- **Latin American**: BRL, MXN, ARS, CLP, COP, PEN

## Recommendations

### Immediate Actions
1. ✅ Implement basic currency support for English (en) - This is critical
2. ✅ Add INR support to Hindi and all Indian language variants
3. ✅ Add CNY support to all Chinese language variants
4. ✅ Create a standard "currency package" with top 20 currencies for easy language integration

### Standardization
1. Create currency groups:
   - **BASIC**: USD, EUR, GBP (minimum for any language)
   - **EXTENDED**: Top 20 global currencies
   - **REGIONAL**: Local + neighboring country currencies
   - **COMPREHENSIVE**: All 180+ currencies (like Spanish/Catalan)

2. Ensure every language supports at least:
   - Its local/national currency
   - USD and EUR (global reserve currencies)
   - Regional trade partners' currencies

### Quality Improvements
1. Remove deprecated currency codes (EEK, LTL, LVL, etc.)
2. Add support for decimal subdivisions (cents, pence, etc.) consistently
3. Consider adding cryptocurrency support (BTC, ETH)
4. Implement currency symbol support alongside codes

## File Structure Issues

### Critical Naming Convention Problem
The file `lang_EU.py` contains generic EURO/currency definitions but is confusingly named as if it were the Basque (eu) language file.

**Recommended naming convention for currency files:**
- Rename `lang_EU.py` → `lang_CURRENCY_EU.py` or `lang_CURRENCY_EUR.py`
- Use prefix `lang_CURRENCY_` for all currency-specific modules
- This clearly distinguishes currency modules from language modules

**Benefits of this convention:**
- Prevents confusion with language codes (EU could be mistaken for Basque)
- Makes it clear which files are for languages vs currencies
- Allows for multiple currency-focused modules if needed
- Follows a consistent, predictable naming pattern

## Conclusion
While num2words2 has a solid foundation for currency support with 181 currencies defined across various languages, there are critical gaps:
- Major languages like English, Hindi, and Chinese lack currency support entirely
- Many languages don't support their own local currencies
- Global trade currencies have limited language coverage

Addressing these gaps would significantly improve the library's utility for international applications.
