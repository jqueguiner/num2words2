# Sentence Conversion

`num2words_sentence` converts numbers embedded in natural-language text while keeping the surrounding sentence intact.

```python
from num2words2 import num2words_sentence

num2words_sentence("I bought 6 apples.")
# 'I bought six apples.'
```

Aliases:

```python
from num2words2 import convert_sentence, sentence_to_words
```

Both aliases call the same implementation.

## What It Handles

The sentence converter recognizes common number contexts:

- regular numbers
- decimals
- negative values
- ordinals such as `1st`, `2nd`, `3rd`, `4th`
- dates such as `April 5, 2024`
- year-like values in date contexts
- temperatures such as `25C`, `25 C`, `25°C`, and language-specific degree words
- currency symbols such as `$`, `€`, `£`, and `¥`

## Examples

```python
num2words_sentence("The temperature is -5 degrees.")
# 'The temperature is minus five degrees.'

num2words_sentence("On April 5, 2024, I paid $12.50.")
# 'On April fifth, twenty twenty-four, I paid twelve dollars, fifty cents.'

num2words_sentence("The 1st place winner got $100.")
# 'The first place winner got one hundred dollars.'
```

Pass `lang=` when you know the sentence language:

```python
num2words_sentence("J'ai acheté 5 livres pour 20 euros.", lang="fr")

num2words_sentence("Tengo 100 dólares.", lang="es")
```

## Language Detection

If `lang` is omitted, the converter tries language detection when optional detection libraries are installed. It falls back to simple keyword heuristics and then English.

For deterministic production systems, pass `lang=` explicitly.

## Output Mode

The `to=` argument is passed through to individual conversions where appropriate.

```python
num2words_sentence("Items 1, 2, and 3", to="ordinal")
```

Context-specific detections such as dates, temperatures, and currencies may override the generic mode when that gives a more natural result.

## Limitations

Sentence conversion is heuristic. It is designed for common text-normalization cases, not full natural-language parsing. For high-stakes or domain-specific text, run representative tests for each language and content type you plan to process.

