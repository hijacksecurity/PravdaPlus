#!/bin/bash

# Final Validation Script for PravdaPlus
# Quick check to ensure all services are operational

echo "🚀 PravdaPlus Final Validation"
echo "============================="

# Check API
API_STATUS=$(curl -s http://localhost:8000/health | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$API_STATUS" = "healthy" ]; then
    echo "✅ API: Healthy"
else
    echo "❌ API: Not healthy"
    exit 1
fi

# Check Frontend
FRONTEND_CHECK=$(curl -s http://localhost:3001 | grep -c "PravdaPlus")
if [ "$FRONTEND_CHECK" -gt 0 ]; then
    echo "✅ Frontend: Accessible"
else
    echo "❌ Frontend: Not accessible"
    exit 1
fi

# Check News API
NEWS_COUNT=$(curl -s "http://localhost:8000/news?limit=1" | grep -o '"title"' | wc -l)
if [ "$NEWS_COUNT" -gt 0 ]; then
    echo "✅ News API: $NEWS_COUNT articles retrieved"
else
    echo "❌ News API: No articles"
    exit 1
fi

# Check Transformation
TRANSFORM_TEST='{"article":{"title":"Test","description":"Test","link":"http://test.com","pub_date":"2025-08-02T06:00:00","category":"world"},"style":"satirical"}'
TRANSFORM_RESULT=$(curl -s -X POST -H "Content-Type: application/json" -d "$TRANSFORM_TEST" http://localhost:8000/transform | grep -c '"transformed"')
if [ "$TRANSFORM_RESULT" -gt 0 ]; then
    echo "✅ Transformation: Working"
else
    echo "❌ Transformation: Failed"
    exit 1
fi

echo ""
echo "🎉 All systems operational!"
echo ""
echo "🌐 Frontend: http://localhost:3001"
echo "🔗 API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"