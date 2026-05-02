# Currency, Cheques, and Fractions

## Currency

Use `to="currency"` for monetary values.

```python
from num2words2 import num2words

num2words(42.50, to="currency", currency="USD")
# 'forty-two dollars, fifty cents'

num2words(2.14, lang="es", to="currency")
# 'dos euros con catorce céntimos'
```

If `currency` is omitted, most converters default to `EUR`.

## Currency Options

```python
num2words(
    1234.56,
    lang="en",
    to="currency",
    currency="USD",
    cents=True,
    separator=",",
)
```

Common options:

| Option | Purpose |
|---|---|
| `currency` | Currency code such as `EUR`, `USD`, `GBP`, `INR`, `JPY` |
| `cents` | Controls subunit output. Boolean legacy values and string modes are supported by current converters |
| `separator` | Text between major and minor currency units |
| `adjective` | Enables adjective currency names where implemented |

Supported currency codes vary by language. The shared base includes major 2-decimal currencies and 3-decimal currencies such as `BHD`, `KWD`, `OMR`, `JOD`, `TND`, `LYD`, and `IQD`.

## Fractional Cents

`num2words2` preserves fractional subunits when the input has more precision than the currency normally uses.

```python
num2words(1234.653, lang="en", to="currency", currency="USD")
# 'one thousand, two hundred and thirty-four dollars, sixty-five point three cents'
```

For standard financial display, pass values rounded to the precision you want before conversion.

## Cheque Format

Use `to="cheque"` for bank-style output.

```python
num2words(1234.56, to="cheque", currency="USD")
# 'ONE THOUSAND, TWO HUNDRED AND THIRTY-FOUR AND 56/100 DOLLARS'

num2words(1.00, to="cheque", currency="USD")
# 'ONE AND 00/100 DOLLARS'
```

Cheque mode composes with 3-decimal currencies:

```python
num2words(1.234, to="cheque", currency="BHD")
# 'ONE AND 234/1000 DINARS'
```

## Fractions

Pass strict fraction strings in `n/d` form.

```python
num2words("1/2")
# 'one half'

num2words("1/3")
# 'one third'

num2words("3/4")
# 'three quarters'
```

Language-specific idioms are implemented for common denominators in several languages:

```python
num2words("1/2", lang="fr")
num2words("2/3", lang="it")
num2words("3/4", lang="de")
```

Invalid fractions behave like normal Python numeric errors:

- `1/0` raises `ZeroDivisionError`.
- Malformed strings are parsed as normal numeric strings if possible, otherwise they fail.
- Negative numerator or denominator produces a negative fraction phrase.

