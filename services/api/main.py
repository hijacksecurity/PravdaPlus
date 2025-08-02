#!/usr/bin/env python3
"""
Simple FastAPI application for PravdaPlus API service.
Minimal working version for local Kubernetes deployment.
"""

import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Models
class NewsItem(BaseModel):
    title: str
    description: str
    link: str
    pub_date: datetime
    category: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

# App Configuration
app = FastAPI(
    title="PravdaPlus API",
    description="Simple news transformation API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# BBC RSS Feed URLs
BBC_FEEDS = {
    "world": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "uk": "http://feeds.bbci.co.uk/news/uk/rss.xml", 
    "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "health": "http://feeds.bbci.co.uk/news/health/rss.xml",
}

async def fetch_bbc_feed(session: aiohttp.ClientSession, category: str, feed_url: str, max_articles: int = 10) -> List[NewsItem]:
    """Fetch articles from a BBC RSS feed."""
    try:
        async with session.get(feed_url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status != 200:
                return []
            xml_content = await response.text()
            root = ET.fromstring(xml_content)
            
            items = root.findall(".//item")
            articles = []
            
            for item in items[:max_articles]:
                title = item.find("title")
                description = item.find("description")
                link = item.find("link")
                pub_date = item.find("pubDate")
                
                if title is not None and description is not None and link is not None:
                    # Parse date
                    date_str = pub_date.text if pub_date is not None else None
                    try:
                        # BBC uses RFC 2822 format
                        parsed_date = datetime.strptime(date_str[:25], "%a, %d %b %Y %H:%M:%S") if date_str else datetime.now()
                    except:
                        parsed_date = datetime.now()
                    
                    articles.append(NewsItem(
                        title=title.text.strip(),
                        description=description.text.strip(),
                        link=link.text.strip(),
                        pub_date=parsed_date,
                        category=category
                    ))
            
            return articles
    except Exception as e:
        print(f"Error fetching {category} feed: {e}")
        return []

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.get("/news/{category}", response_model=List[NewsItem])
async def get_news_by_category(category: str, limit: int = 10):
    """Get news articles by category."""
    if category not in BBC_FEEDS:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    
    async with aiohttp.ClientSession() as session:
        articles = await fetch_bbc_feed(session, category, BBC_FEEDS[category], limit)
        return articles

@app.get("/news", response_model=Dict[str, List[NewsItem]])
async def get_all_news(limit: int = 5):
    """Get news from all categories."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for category, feed_url in BBC_FEEDS.items():
            tasks.append(fetch_bbc_feed(session, category, feed_url, limit))
        
        results = await asyncio.gather(*tasks)
        
        return {
            category: articles
            for category, articles in zip(BBC_FEEDS.keys(), results)
        }

class TransformRequest(BaseModel):
    article: NewsItem
    style: str = "satirical"

@app.post("/transform")
async def transform_article(request: TransformRequest):
    """Transform a news article using the AI transformer service."""
    try:
        transformer_url = os.getenv("TRANSFORMER_URL", "http://transformer-service:8002")
        
        async with aiohttp.ClientSession() as session:
            article_data = request.article.dict()
            # Convert datetime to string for JSON serialization
            article_data["pub_date"] = article_data["pub_date"].isoformat()
            
            payload = {
                "article": article_data,
                "style": request.style
            }
            
            async with session.post(
                f"{transformer_url}/transform",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Transformer service error: {error_text}"
                    )
                    
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Transformer service timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PravdaPlus API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/news",
            "/news/{category}",
            "/transform",
            "/docs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)