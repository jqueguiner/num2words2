# Aviation and ICAO English

`num2words2` includes aviation English converters for digit-by-digit phraseology.

## Recommended Codes

| Code | Profile |
|---|---|
| `en_Aero_ICAO` | ICAO |
| `en_Aero_FAA` | FAA |
| `en_Aero_NATO` | NATO STANAG 1059 |
| `en_Aero_USN` | US Navy |
| `en_Aero_US_Navy` | US Navy alias |
| `en_Aero_US_Army` | US Army |

Compatibility aliases include `en_AERO`, `en_aero_icao`, and `en_x_aero_icao`.

## Basic Conversion

```python
from num2words2 import num2words

num2words(5739, lang="en_Aero_ICAO")
# 'fife seven tree niner'
```

In aviation profiles, cardinal values are typically read digit by digit. Ordinals, fractions, currency, and cheque modes fall back to compatible English behavior where available.

## Specialized Phraseology

Specialized methods live on the converter object:

```python
from num2words2 import CONVERTER_CLASSES

aero = CONVERTER_CLASSES["en_Aero_ICAO"]

aero.to_altitude(5500)
# 'fife thousand fife hundred feet'

aero.to_flight_level(230)
# 'flight level too tree zero'

aero.to_heading(30)
# 'heading zero tree zero'

aero.to_squawk(7700)
# 'squawk seven seven zero zero'

aero.to_runway("27R")
# 'runway too seven right'

aero.to_frequency(121.5)
# 'wun too wun decimal fife'
```

## Direct Class Usage

```python
from num2words2.lang_EN_AERO import Num2Word_EN_AERO

Num2Word_EN_AERO(profile="FAA").to_cardinal(5739)
# 'fife seven tree niner'
```

Invalid profile names raise `ValueError`.

