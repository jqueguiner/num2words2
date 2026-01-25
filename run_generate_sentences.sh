#!/bin/bash
# Script to generate comprehensive sentence test cases for all languages

echo "Generating comprehensive test cases for num2words_sentence function"
echo "This will generate test cases for all supported languages"
echo ""

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set it with: export OPENAI_API_KEY='your-api-key'"
    exit 1
fi

# Start with a clean file
if [ -f "test_e2e_sentences_full.csv" ]; then
    echo "Backing up existing test_e2e_sentences_full.csv to test_e2e_sentences_full.csv.bak"
    cp test_e2e_sentences_full.csv test_e2e_sentences_full.csv.bak
fi

echo "Starting generation..."
echo ""

# Generate test cases for priority languages first (more tests each)
echo "=== Generating tests for high-priority languages (20 tests each) ==="
python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 20 \
    --languages en \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 20 \
    --languages fr es de it pt \
    --append \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 20 \
    --languages zh-cn ja ko ru ar \
    --append \
    --model gpt-4o-mini

echo ""
echo "=== Generating tests for medium-priority languages (10 tests each) ==="
python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 10 \
    --languages nl sv no da fi pl cs sk hu ro \
    --append \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 10 \
    --languages tr he hi bn ta te th vi id ms \
    --append \
    --model gpt-4o-mini

echo ""
echo "=== Generating tests for other languages (5 tests each) ==="
python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 5 \
    --languages el bg uk sr hr sl mk sq ka hy \
    --append \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 5 \
    --languages az kk uz tk tg mn fa ur ps sd \
    --append \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 5 \
    --languages pa gu mr kn ml si ne as km lo \
    --append \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 5 \
    --languages my bo am ha yo sw sn af jw tl \
    --append \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 5 \
    --languages haw mi mg mt cy gl eu ca oc br \
    --append \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 5 \
    --languages fo lb yi eo la sa tet ht wo ln \
    --append \
    --model gpt-4o-mini

python generate_test_e2e_sentences.py \
    --output test_e2e_sentences_full.csv \
    --count 5 \
    --languages so su ce ba tt bs nn kz \
    --append \
    --model gpt-4o-mini

echo ""
echo "=== Generation complete ==="
echo "Test cases have been saved to: test_e2e_sentences_full.csv"
echo ""
echo "To run the tests, use:"
echo "  python tests/test_e2e_sentences.py"
echo ""
echo "To view the CSV file:"
echo "  head -20 test_e2e_sentences_full.csv"
