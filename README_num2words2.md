# num2words2

[![PyPI version](https://badge.fury.io/py/num2words2.svg)](https://badge.fury.io/py/num2words2)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL%20v2.1-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1)
[![Python Versions](https://img.shields.io/pypi/pyversions/num2words2.svg)](https://pypi.org/project/num2words2/)

`num2words2` is a modern, actively maintained fork of the original `num2words` library, optimized for LLM/AI/speech applications. It converts numbers like `42` to words like `forty-two` across 50+ languages. This fork was created because the original Savoir-faire Linux repository was no longer being maintained at the pace required for the rapidly evolving AI, machine learning, and speech synthesis ecosystem.

## Why num2words2?

The original `num2words` library by Savoir-faire Linux became unmaintained and couldn't keep up with the rapid pace of innovation in the AI/LLM/speech technology space. Modern applications like:

- **Large Language Models (LLMs)** requiring robust text preprocessing
- **Speech synthesis systems** needing accurate number-to-word conversion
- **Voice assistants and chatbots** processing numerical data
- **AI training pipelines** requiring consistent text normalization
- **Multilingual AI applications** spanning 50+ languages

...needed a more actively maintained solution with faster bug fixes, enhanced language support, and compatibility with modern Python ecosystems.

## Features

- Convert numbers to words in 50+ languages
- Support for cardinal, ordinal, currency, and year conversion
- Enhanced language support including recent additions (Armenian, Mongolian, Shona)
- Critical bug fixes for decimal handling, negative numbers, and float conversions
- Optimized for modern AI/ML/speech applications
- Actively maintained with regular updates and community contributions
- Drop-in replacement for the original num2words
- Modern CI/CD pipeline with comprehensive testing

## Installation

```bash
pip install num2words2
```

## Usage

### Basic Usage

```python
from num2words2 import num2words

# Cardinal numbers
print(num2words(42))  # forty-two
print(num2words(42, lang='es'))  # cuarenta y dos
print(num2words(42, lang='fr'))  # quarante-deux

# Ordinal numbers
print(num2words(42, to='ordinal'))  # forty-second
print(num2words(42, to='ordinal', lang='es'))  # cuadragésimo segundo

# Currency
print(num2words(42.50, to='currency'))  # forty-two euro, fifty cents
print(num2words(42.50, to='currency', lang='es'))  # cuarenta y dos euros con cincuenta céntimos

# Year
print(num2words(2024, to='year'))  # two thousand and twenty-four
```

### Command Line Interface

```bash
$ num2words2 10001
ten thousand and one

$ num2words2 24120.10
twenty-four thousand, one hundred and twenty point one

$ num2words2 24120.10 -l es
veinticuatro mil ciento veinte punto uno

$ num2words2 2.14 -l es --to currency
dos euros con catorce céntimos

# List all supported languages
$ num2words2 --list-languages

# List all converters
$ num2words2 --list-converters
```

## Supported Languages

`num2words2` supports over 50 languages:

- ar (Arabic)
- az (Azerbaijani)
- be (Belarusian)
- bn (Bengali)
- ca (Catalan)
- ce (Chechen)
- cs (Czech)
- cy (Welsh)
- da (Danish)
- de (German)
- el (Greek)
- en (English)
- eo (Esperanto)
- es (Spanish)
- fa (Persian)
- fi (Finnish)
- fr (French)
- he (Hebrew)
- hi (Hindi)
- hu (Hungarian)
- hy (Armenian)
- id (Indonesian)
- is (Icelandic)
- it (Italian)
- ja (Japanese)
- kn (Kannada)
- ko (Korean)
- kz (Kazakh)
- lt (Lithuanian)
- lv (Latvian)
- mn (Mongolian)
- nl (Dutch)
- no (Norwegian)
- pl (Polish)
- pt (Portuguese)
- ro (Romanian)
- ru (Russian)
- sk (Slovak)
- sl (Slovenian)
- sn (Shona)
- sr (Serbian)
- sv (Swedish)
- te (Telugu)
- tet (Tetum)
- th (Thai)
- tr (Turkish)
- uk (Ukrainian)
- vi (Vietnamese)
- yo (Yoruba)
- zh (Chinese)

And many regional variations like es_CO (Colombian Spanish), pt_BR (Brazilian Portuguese), etc.

## Improvements over Original num2words

### Maintenance & Community
- **Active Maintenance**: Regular updates aligned with AI/ML ecosystem needs
- **Rapid Bug Resolution**: Issues are addressed promptly, not left open for months/years
- **Modern Development**: Updated CI/CD, comprehensive testing, automated dependency management
- **Community-Driven**: Open to contributions and feature requests from the AI/speech community

### Technical Improvements
- **Critical Bug Fixes**: Resolved issues with negative decimal handling, float comparisons, and type conversions affecting ML pipelines
- **Enhanced Language Support**: Added Armenian (hy), Mongolian (mn), Shona (sn) and improved existing language modules
- **LLM Optimization**: Better handling of edge cases common in large-scale text processing
- **Type Safety**: Improved type handling and error messages for better integration with ML frameworks
- **Performance**: Optimizations for batch processing scenarios common in AI applications

### AI/ML Specific Features
- **Consistent Output**: More predictable text generation for training datasets
- **Edge Case Handling**: Better support for unusual number formats found in real-world data
- **Multilingual Robustness**: Enhanced support for code-switching and multilingual AI models

## Migration from num2words

`num2words2` is designed as a drop-in replacement for `num2words` with full backward compatibility.

### 🤖 Automated Migration (Recommended)

We provide a migration script to automatically update your codebase:

```bash
# Download and run the migration script
curl -O https://raw.githubusercontent.com/jqueguiner/num2words/master/migrate_to_num2words2.py
python migrate_to_num2words2.py /path/to/your/project

# Or just scan current directory
python migrate_to_num2words2.py .

# Dry run to see what would change (recommended first step)
python migrate_to_num2words2.py --dry-run .
```

The script will:
- 🔍 Find all Python files with `num2words` imports
- 💾 Create backups of original files
- 🔄 Update imports to use `num2words2`
- 📝 Provide a detailed summary of changes

### 📝 Manual Migration

If you prefer manual migration, simply update your imports:

```python
# Before
from num2words import num2words

# After  
from num2words2 import num2words
```

For backward compatibility during transition:

```python
try:
    from num2words2 import num2words
except ImportError:
    from num2words import num2words
```

### 📦 Update Dependencies

Update your dependency files:

```bash
# requirements.txt
- num2words>=0.5.12
+ num2words2>=0.5.15

# pyproject.toml
dependencies = [
-    "num2words>=0.5.12",
+    "num2words2>=0.5.15",
]

# setup.py
install_requires=[
-    "num2words>=0.5.12",
+    "num2words2>=0.5.15",
],
```

### 🧪 Testing Your Migration

After migration, test your application:

```python
# Test basic functionality
from num2words2 import num2words

# These should work exactly as before
assert num2words(42) == "forty-two"
assert num2words(42, lang='es') == "cuarenta y dos"
assert num2words(42, to='ordinal') == "forty-second"
```

### 🚀 Installation

```bash
# Install num2words2
pip install num2words2

# If you were using num2words, you can remove it
pip uninstall num2words
```

### ⚠️ Breaking Changes

`num2words2` maintains full backward compatibility. However, if you experience any issues:

1. **Check version compatibility** - Ensure you're using `num2words2>=0.5.15`
2. **Report issues** - Create an issue at https://github.com/jqueguiner/num2words/issues
3. **Rollback if needed** - The migration script creates backups for easy rollback

### 🔄 Rollback Migration

If you need to rollback:

```bash
# The migration script creates .num2words_backup files
# Restore them if needed
for file in $(find . -name "*.num2words_backup"); do
    original="${file%.num2words_backup}"
    cp "$file" "$original"
    echo "Restored $original"
done
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-test.txt

# Run tests
python -m pytest tests/

# Run tests with coverage
python -m pytest tests/ --cov=num2words2
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the GNU Lesser General Public License v2.1 - see the LICENSE file for details.

## Credits

`num2words2` is based on the original [num2words](https://github.com/savoirfairelinux/num2words) project by Savoir-faire Linux inc.

**Original Library History:**
- **pynum2word** (2003) - Created by Taro Ogawa
- **Lithuanian support** (2011) - Added by Marius Grigaitis  
- **num2words** - Re-published by Virgil Dupras, Savoir-faire Linux
- **num2words2** (2025) - Modern fork by Jean-Louis Queguiner for AI/ML applications

## Author

Maintained by Jean-Louis Queguiner

## Links

- [PyPI Package](https://pypi.org/project/num2words2/)
- [GitHub Repository](https://github.com/jqueguiner/num2words)
- [Issue Tracker](https://github.com/jqueguiner/num2words/issues)