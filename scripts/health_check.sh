#!/bin/bash

# PravdaPlus Health Check Script
# Comprehensive testing for frontend, API, and transformation pipeline

set -e  # Exit on any error

echo "🔍 Starting PravdaPlus Health Check..."
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0

check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
    ((PASS_COUNT++))
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
    ((FAIL_COUNT++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test 1: API Health
echo ""
echo "📡 Testing API Health..."
if curl -s -f http://localhost:8000/health > /dev/null; then
    API_HEALTH=$(curl -s http://localhost:8000/health)
    check_pass "API Health endpoint accessible: $API_HEALTH"
else
    check_fail "API Health endpoint not accessible"
fi

# Test 2: Frontend Accessibility
echo ""
echo "🌐 Testing Frontend Access..."
if curl -s -f http://localhost:3001 > /dev/null; then
    FRONTEND_TITLE=$(curl -s http://localhost:3001 | grep -o '<title>.*</title>' || echo "No title found")
    check_pass "Frontend accessible: $FRONTEND_TITLE"
else
    check_fail "Frontend not accessible at localhost:3001"
fi

# Test 3: News API
echo ""
echo "📰 Testing News API..."
NEWS_RESPONSE=$(curl -s -w "%{http_code}" http://localhost:8000/news?limit=2)
HTTP_CODE="${NEWS_RESPONSE: -3}"
if [ "$HTTP_CODE" = "200" ]; then
    # Count articles in response
    ARTICLE_COUNT=$(echo "${NEWS_RESPONSE%???}" | grep -o '"title"' | wc -l || echo "0")
    check_pass "News API working: Retrieved $ARTICLE_COUNT articles"
else
    check_fail "News API failed with HTTP code: $HTTP_CODE"
fi

# Test 4: Frontend API Proxy
echo ""
echo "🔗 Testing Frontend API Proxy..."
if curl -s -f http://localhost:3001/api/health > /dev/null; then
    check_pass "Frontend API proxy working"
else
    check_fail "Frontend API proxy not working"
fi

# Test 5: Transformation Pipeline
echo ""
echo "🎭 Testing Transformation Pipeline..."

# Get a sample article first
SAMPLE_ARTICLE=$(curl -s "http://localhost:8000/news/world?limit=1")
if [ $? -eq 0 ] && [ ! -z "$SAMPLE_ARTICLE" ] && [ "$SAMPLE_ARTICLE" != "[]" ]; then
    check_pass "Sample article retrieved for transformation test"
    
    # Create a simple test transformation payload
    TEST_PAYLOAD='{
        "article": {
            "title": "Test Article Title",
            "description": "Test article description for transformation",
            "link": "https://example.com/test",
            "pub_date": "2025-08-02T06:00:00",
            "category": "world"
        },
        "style": "satirical"
    }'
    
    # Test transformation
    TRANSFORM_RESPONSE=$(curl -s -w "%{http_code}" -X POST \
        -H "Content-Type: application/json" \
        -d "$TEST_PAYLOAD" \
        http://localhost:8000/transform)
    
    TRANSFORM_HTTP_CODE="${TRANSFORM_RESPONSE: -3}"
    if [ "$TRANSFORM_HTTP_CODE" = "200" ]; then
        # Check if response contains expected fields
        RESPONSE_BODY="${TRANSFORM_RESPONSE%???}"
        if echo "$RESPONSE_BODY" | grep -q '"transformed"' && echo "$RESPONSE_BODY" | grep -q '"title"' && echo "$RESPONSE_BODY" | grep -q '"content"'; then
            check_pass "Transformation pipeline working: Response contains expected fields"
            
            # Check content length
            CONTENT_LENGTH=$(echo "$RESPONSE_BODY" | grep -o '"content":"[^"]*"' | wc -c)
            if [ "$CONTENT_LENGTH" -gt 100 ]; then
                check_pass "Generated content has reasonable length ($CONTENT_LENGTH characters)"
            else
                check_warn "Generated content seems short ($CONTENT_LENGTH characters)"
            fi
        else
            check_fail "Transformation response missing expected fields"
        fi
    else
        check_fail "Transformation failed with HTTP code: $TRANSFORM_HTTP_CODE"
    fi
else
    check_fail "Cannot retrieve sample article for transformation test"
fi

# Test 6: Kubernetes Pods Status
echo ""
echo "☸️  Testing Kubernetes Pod Status..."
if command -v kubectl &> /dev/null; then
    RUNNING_PODS=$(kubectl get pods -n pravda-system --field-selector=status.phase=Running --no-headers | wc -l)
    TOTAL_PODS=$(kubectl get pods -n pravda-system --no-headers | wc -l)
    
    if [ "$RUNNING_PODS" -eq "$TOTAL_PODS" ] && [ "$TOTAL_PODS" -gt 0 ]; then
        check_pass "All Kubernetes pods running ($RUNNING_PODS/$TOTAL_PODS)"
    else
        check_fail "Some Kubernetes pods not running ($RUNNING_PODS/$TOTAL_PODS)"
        kubectl get pods -n pravda-system
    fi
else
    check_warn "kubectl not available, skipping pod status check"
fi

# Summary
echo ""
echo "=================================================="
echo "📊 HEALTH CHECK SUMMARY"
echo "=================================================="
echo -e "${GREEN}✅ Passed: $PASS_COUNT${NC}"
echo -e "${RED}❌ Failed: $FAIL_COUNT${NC}"

TOTAL_CHECKS=$((PASS_COUNT + FAIL_COUNT))
if [ "$FAIL_COUNT" -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 ALL CHECKS PASSED! PravdaPlus is fully operational.${NC}"
    echo ""
    echo "🌐 Frontend: http://localhost:3001"
    echo "🔗 API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    exit 0
else
    echo ""
    echo -e "${RED}⚠️  $FAIL_COUNT/$TOTAL_CHECKS checks failed. Please review the issues above.${NC}"
    exit 1
fi