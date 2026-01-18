# Structural Issues Analysis for num2words2
## Generated: 2026-01-18

## Critical Naming Convention and Structural Issues Found

### 1. ✅ RESOLVED: lang_EU.py Dual Purpose Problem

**Issue was successfully migrated**: `lang_EU.py` → `lang_EUR.py`
- **Old problem**: Confused Basque language code (eu) with European base class
- **Solution implemented**: Renamed to `lang_EUR.py` to clearly indicate Euro/European functionality
- **Files updated**: 25+ language files that inherit from this base class

#### Migration Details:
```
✅ Successfully updated 25+ languages that inherit from Num2Word_EUR:
- AF (Afrikaans), AM (Amharic), CA (Catalan), CE (Chechen)
- CY (Welsh), DA (Danish), DE (German), EL (Greek)
- EN (English), ES (Spanish), FI (Finnish), FR (French)
- HU (Hungarian), IS (Icelandic), IT (Italian), KN (Kannada)
- NL (Dutch), NO (Norwegian), PT (Portuguese), RO (Romanian)
- SL (Slovenian), SV (Swedish), TE (Telugu), TET (Tetum), TG (Tajik)
```

#### ✅ Problems Resolved:
1. **Naming Clarity**: `lang_EUR.py` clearly indicates Euro/European functionality
2. **No Language Code Conflict**: Basque (eu) can now be properly implemented
3. **Inheritance Clear**: All dependent files updated with new naming
4. **Verified Working**: All currency and number conversion functions tested successfully

#### Migration Completed:
- ✅ Created `lang_EUR.py` with `Num2Word_EUR` class
- ✅ Updated 25+ import statements: `from .lang_EU` → `from .lang_EUR`
- ✅ Updated 25+ class inheritance: `Num2Word_EU` → `Num2Word_EUR`
- ✅ Updated method calls: `Num2Word_EU.setup()` → `Num2Word_EUR.setup()`
- ✅ Updated documentation in README.md
- ✅ Removed old `lang_EU.py` file
- ✅ Verified all languages and currency conversion still work

### 2. Deprecated Currency Codes Still Present

Found obsolete currency codes that should be removed:

#### In lang_EU.py:
```python
# replaced by EUR
'EEK': (('kroon', 'kroons'), ('sent', 'senti')),  # Estonian Kroon - replaced by EUR in 2011
# replaced by EUR
'LTL': (('litas', 'litas'), GENERIC_CENTS),       # Lithuanian Litas - replaced by EUR in 2015
# replaced by EUR
'LVL': (('lat', 'lats'), ('santim', 'santims')), # Latvian Lat - replaced by EUR in 2014
```

#### Recommendation:
Remove these deprecated currencies or move them to a "historical currencies" section with clear deprecation warnings.

### 3. Inconsistent Currency Support Architecture

#### Pattern Analysis:
- **Some languages** inherit from `Num2Word_EU` (gets extensive currency support)
- **Other languages** inherit from `Num2Word_Base` (minimal/no currency support)
- **No clear pattern** for which languages get which base class

#### Languages Inheriting from Num2Word_EU (25 languages):
These get extensive currency support automatically:
- All major European languages (DE, FR, IT, ES, etc.)
- Some non-European languages (AM-Amharic, KN-Kannada, TE-Telugu)

#### Languages Inheriting from Num2Word_Base (50 languages):
These have limited/no currency support:
- Major languages: Hindi, Chinese variants, Arabic, Russian, Japanese
- Most Asian, African, and American languages

#### Problem:
This creates an **arbitrary division** where some languages get rich currency support while others get none, not based on linguistic or regional logic.

### 4. Missing Basque Language Implementation

The "EU" naming conflict masks that **Basque language (eu) is completely unimplemented**:
- Basque is spoken by 750K people in Spain/France
- Currently shows as "implemented" in LANGUAGES.md but actually isn't
- The lang_EU.py file prevents creating a proper lang_EU.py for Basque

### 5. Inconsistent Regional Variant Naming

#### Current Pattern:
```
lang_EN.py     -> English
lang_EN_IN.py  -> English (India)
lang_EN_NG.py  -> English (Nigeria)

lang_ES.py     -> Spanish
lang_ES_CO.py  -> Spanish (Colombia)
lang_ES_CR.py  -> Spanish (Costa Rica)
etc.
```

#### Issues Found:
- **Chinese variants** use CN/HK/TW suffixes correctly
- **English variants** use IN/NG suffixes correctly
- **Spanish variants** use country codes correctly
- **No issues found with regional naming patterns**

### 6. Currency vs Language Module Separation

#### Current Structure Issues:
```
num2words2/
├── lang_EU.py        # BOTH base class AND currency module (PROBLEM)
├── currency.py       # Generic currency utilities
├── base.py          # Main base class
└── lang_XX.py       # Individual languages
```

#### Recommended Structure:
```
num2words2/
├── lang_EUROPEAN_BASE.py  # Base class for European languages
├── lang_EU.py            # Basque language (currently missing)
├── currency.py           # Generic currency utilities
├── base.py              # Main base class
└── lang_XX.py           # Individual languages
```

## Severity Assessment

### Critical (Must Fix):
1. **Rename lang_EU.py** to avoid Basque language code conflict
2. **Implement actual Basque language** support

### High Priority:
3. **Remove deprecated currency codes** (EEK, LTL, LVL)
4. **Standardize currency support architecture** across languages

### Medium Priority:
5. **Document base class hierarchy** clearly
6. **Review which languages should inherit from European base**

## Implementation Recommendations

### Phase 1: Critical Fixes
1. Rename `lang_EU.py` → `lang_EUROPEAN_BASE.py`
2. Update all 25+ import statements in dependent files
3. Implement proper Basque language as `lang_EU.py`
4. Update LANGUAGES.md to reflect actual Basque status

### Phase 2: Architecture Cleanup
1. Remove deprecated currency codes
2. Create clear documentation of base class hierarchy
3. Review which non-European languages should inherit from European base
4. Standardize currency support patterns

### Phase 3: Enhancement
1. Consider creating regional base classes (Asian, African, etc.)
2. Implement missing high-priority languages
3. Add comprehensive currency support to major languages

## Files Requiring Updates (Rename Impact)

If lang_EU.py is renamed, these 25+ files need import updates:
```
lang_AF.py, lang_AM.py, lang_CA.py, lang_CE.py, lang_CY.py,
lang_DA.py, lang_DE.py, lang_EL.py, lang_EN.py, lang_ES.py,
lang_FI.py, lang_FR.py, lang_HU.py, lang_IS.py, lang_IT.py,
lang_KN.py, lang_NL.py, lang_NO.py, lang_PT.py, lang_RO.py,
lang_SL.py, lang_SV.py, lang_TE.py, lang_TET.py, lang_TG.py
```

## Conclusion

The lang_EU.py issue is more complex than initially thought - it's not just a naming problem but a fundamental architectural issue affecting 25+ languages. The rename needs careful coordination to avoid breaking the inheritance hierarchy that many European languages depend on.

The good news is that most other structural patterns in the codebase are consistent and well-organized. The main issues center around this single problematic file and the currency support architecture it enables.
