#!/usr/bin/env python3
"""
AI Transformer Service for PravdaPlus
Transforms news articles into satirical/fun versions using OpenAI
"""

import os
import asyncio
from datetime import datetime
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import openai
import httpx

# Models
class NewsItem(BaseModel):
    title: str
    description: str
    link: str
    pub_date: str
    category: str

class TransformRequest(BaseModel):
    article: NewsItem
    style: str = "satirical"  # satirical, funny, absurd

class TransformResponse(BaseModel):
    original: NewsItem
    transformed: Dict[str, str]  # {title, description, content}
    style: str
    timestamp: str
    status: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    openai_configured: bool

# App setup
app = FastAPI(
    title="PravdaPlus Transformer",
    description="AI-powered news transformation service",
    version="1.0.0"
)

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY", "")
if openai_api_key and openai_api_key != "sk-your-openai-api-key-here":
    openai.api_key = openai_api_key
    OPENAI_CONFIGURED = True
else:
    OPENAI_CONFIGURED = False
    print("⚠️  OpenAI API key not configured. Transformation will use mock responses.")

async def transform_with_openai(article: NewsItem, style: str) -> Dict[str, str]:
    """Transform article using OpenAI API"""
    if not OPENAI_CONFIGURED:
        # Generate unique mock transformation based on the actual article
        import hashlib
        import random
        
        # Create a seed based on the article title for consistent but unique results
        seed = int(hashlib.md5(article.title.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Generate article-specific satirical content
        satirical_angles = [
            "Local Area Experts Baffled by Predictable Turn of Events",
            "Scientists Discover That Things Continue to Happen, More at 11",
            "Breaking: World Still Spinning, Residents Unimpressed", 
            "Researchers Confirm Reality Still Operating Within Normal Parameters",
            "Local Person Shocked to Learn Universe Follows Established Patterns",
            "Area Officials Announce That Time Continues Moving Forward",
            "Experts Puzzled by Occurrence of Scheduled Event",
            "Community Leaders Perplexed by Entirely Foreseeable Development"
        ]
        
        # Select title based on article content
        if "trump" in article.title.lower() or "president" in article.title.lower():
            mock_title = "Local Man Discovers Politicians Still Doing Politics, Experts Stunned"
        elif "health" in article.category.lower() or "medical" in article.title.lower():
            mock_title = "Area Residents Shocked to Learn Bodies Still Require Maintenance"
        elif "business" in article.category.lower() or "finance" in article.title.lower():
            mock_title = "Money Continues to Exist Despite Public's Best Efforts to Ignore It"
        elif "technology" in article.category.lower():
            mock_title = "Scientists Confirm: Computers Still Computing, Public Bewildered"
        else:
            mock_title = random.choice(satirical_angles)
        
        # Generate description
        descriptors = [
            "startling revelation", "shocking development", "unprecedented occurrence",
            "mind-bending discovery", "earth-shattering news", "reality-defying event"
        ]
        
        mock_description = f"In a {random.choice(descriptors)} that has left experts frantically updating their textbooks, recent events have confirmed what many suspected all along: things continue to happen in the world."
        
        # Generate unique content based on article
        expert_names = ["Dr. Sarah Mitchell", "Professor Bob Thompson", "Dr. Jennifer Walsh", "Professor Mike Stevens", "Dr. Lisa Chen", "Professor David Kumar"]
        institutions = ["University of Common Sense", "Institute of Obvious Studies", "College of Predictable Outcomes", "Academy of Expected Results"]
        resident_names = ["Karen Johnson", "Mike Davis", "Jennifer Smith", "Bob Wilson", "Sarah Brown", "Tom Anderson"]
        
        expert = random.choice(expert_names)
        institution = random.choice(institutions)
        resident = random.choice(resident_names)
        resident_age = random.randint(25, 65)
        
        # Create article-specific satirical scenarios
        if "technology" in article.category.lower():
            scenario = f"the latest technological development continues to perplex humanity"
            expert_quote = "We've been studying human-computer interaction for decades, and yet people still act surprised when technology does exactly what it was designed to do."
            resident_quote = f"I had no idea that pressing buttons would make things happen on screens."
        elif "health" in article.category.lower():
            scenario = f"people are discovering that their bodies still require basic maintenance"
            expert_quote = "After years of research, we've confirmed that the human body continues to function according to established biological principles."
            resident_quote = f"Who could have predicted that what I eat and how much I exercise would affect my health?"
        elif "business" in article.category.lower():
            scenario = f"economic principles continue to operate as economists predicted"
            expert_quote = "Our extensive research has revealed that supply, demand, and market forces are still functioning exactly as textbooks describe."
            resident_quote = f"I'm shocked to learn that businesses exist to make money."
        else:
            scenario = f"current events continue to unfold in a logical sequence"
            expert_quote = "We've been observing cause-and-effect relationships for years, yet people remain surprised when actions have consequences."
            resident_quote = f"I had no idea that today would be followed by tomorrow."
        
        mock_content = f"""
{article.category.upper()} - In a development that has left researchers at the {institution} scrambling to update their "Encyclopedia of Predictable Outcomes," recent events have confirmed that {scenario}.

{expert}, Professor of Stating the Obvious at {institution}, expressed measured bewilderment at the public's reaction: "{expert_quote} It's like being surprised that gravity makes things fall down."

The discovery came after extensive research involving careful observation of reality and occasionally checking the news. "The evidence was overwhelming," said lead researcher Dr. Amanda Foster, who spent nearly four minutes analyzing the situation before reaching her groundbreaking conclusion.

Local resident {resident}, {resident_age}, was reportedly "stunned" by this revelation. "{resident_quote}" she said while simultaneously demonstrating a complete understanding of exactly how these things work.

Meanwhile, experts continue to analyze the situation with the same level of accuracy they've maintained since the invention of expertise. "We're confident that things will continue to happen in roughly the order they happen," announced analyst Dr. Patricia Moore, before immediately being proven correct by the passage of time.

The international community has responded with its customary level of measured confusion, with world leaders issuing statements that can best be summarized as "We acknowledge that events occurred and will probably continue occurring."

In related news, the sun rose this morning as scheduled, water remains wet, and people continue to have opinions about things.

This story is developing, assuming anyone can agree on what 'developing' means when applied to the unstoppable march of causality itself.
"""
        
        return {
            "title": mock_title,
            "description": mock_description,
            "content": mock_content.strip()
        }
    
    try:
        prompt = f"""You are a brilliant satirical news writer in the style of The Onion, creating clever, witty, and genuinely funny content. Transform this real news story into a masterpiece of satirical journalism.

**Your mission**: Create a completely rewritten article that is:
- Genuinely hilarious and clever
- Satirical but not mean-spirited
- Uses absurd hypothetical scenarios and exaggerated quotes
- Maintains some connection to the original facts but takes creative liberties
- Written like a professional news article but with satirical content
- Family-friendly and avoids offensive content

**Original Article:**
Title: {article.title}
Description: {article.description}

**Instructions:**
1. Create a NEW satirical headline that's completely different but somehow relates to the original story
2. Write a NEW brief description (2-3 sentences) that sets up the satirical angle  
3. Write a FULL satirical article (400-600 words) with:
   - Fictional but believable quotes from made-up experts
   - Absurd statistics or studies
   - Creative scenarios that exaggerate the situation
   - A professional news article structure (location, quotes, context)
   - Subtle humor throughout, not just obvious jokes

**Output Format:**
TITLE: [Your satirical headline]
DESCRIPTION: [Your satirical description]
CONTENT: [Your full satirical article]

Remember: This should read like a real news article that just happens to be completely absurd and funny. Think "The Onion" quality."""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "system", "content": "You are a world-class satirical news writer with the wit of The Onion and the creativity of Douglas Adams. Your job is to transform mundane news into hilarious, absurd, yet professionally written satirical articles that make people laugh out loud."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1500,
                    "temperature": 0.9
                },
                timeout=30.0
            )
            
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {response.status_code}")
            
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Parse the response to extract title, description, and content
        lines = content.strip().split('\n')
        transformed_title = ""
        transformed_description = ""
        transformed_content = ""
        
        current_section = None
        content_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("TITLE:"):
                current_section = "title"
                transformed_title = line_stripped.replace("TITLE:", "").strip()
            elif line_stripped.startswith("DESCRIPTION:"):
                current_section = "description"
                transformed_description = line_stripped.replace("DESCRIPTION:", "").strip()
            elif line_stripped.startswith("CONTENT:"):
                current_section = "content"
                transformed_content = line_stripped.replace("CONTENT:", "").strip()
            elif current_section == "description" and line_stripped and not line_stripped.startswith("CONTENT:"):
                transformed_description += " " + line_stripped
            elif current_section == "content" and line.strip():
                content_lines.append(line.strip())
        
        if content_lines:
            transformed_content = "\n".join(content_lines)
        
        # Fallback parsing if format is different
        if not transformed_title or not transformed_description:
            sections = content.split('\n\n')
            if len(sections) >= 3:
                transformed_title = sections[0].replace("TITLE:", "").strip()
                transformed_description = sections[1].replace("DESCRIPTION:", "").strip()
                transformed_content = sections[2].replace("CONTENT:", "").strip()
            else:
                transformed_title = f"Breaking: Local News Still Happening, Experts Baffled"
                transformed_description = "In a shocking turn of events, things continue to occur in the world."
                transformed_content = content.strip()
        
        return {
            "title": transformed_title or "Breaking: Local News Still Happening, Experts Baffled",
            "description": transformed_description or "In a shocking turn of events, things continue to occur in the world.",
            "content": transformed_content or content.strip()
        }
        
    except Exception as e:
        print(f"OpenAI transformation error: {e}")
        # Fallback to mock response
        return {
            "title": f"Local News Event Occurs, Area Residents Moderately Concerned",
            "description": f"[AI Transformation temporarily unavailable] Scientists baffled by yet another thing happening.",
            "content": f"BREAKING - In what experts are calling 'a thing that happened,' local events continue to unfold at the pace of reality itself. More details as they develop, or don't."
        }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        openai_configured=OPENAI_CONFIGURED
    )

@app.post("/transform")
async def transform_article(request: TransformRequest):
    """Transform a news article using AI"""
    try:
        transformed = await transform_with_openai(request.article, request.style)
        
        # Return a plain dict to avoid serialization issues
        return {
            "original": request.article.dict(),
            "transformed": transformed,
            "style": request.style,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "PravdaPlus Transformer",
        "version": "1.0.0",
        "openai_configured": OPENAI_CONFIGURED,
        "endpoints": [
            "/health",
            "/transform",
            "/docs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)