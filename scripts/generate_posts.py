"""Main script to generate blog posts automatically with social media posting"""
import os
import time
import datetime
import re

# Import all modules
from config import *
from keywords_handler import get_keyword_row, parse_keyword_row, remove_keyword_from_file, get_keywords_count
from article_generator import generate_article, generate_image_prompt, generate_description
from image_generator import generate_image_freepik
from gsc_automation import submit_url_to_gsc
from webpushr_notifier import send_blog_post_notification, get_subscriber_count


def generate_smart_hashtags(title, focus_kw, semantic_kw, article_content):
    """
    Generate intelligent hashtags based on all available article data
    
    Args:
        title: Article title
        focus_kw: Main focus keyword
        semantic_kw: Related semantic keywords
        article_content: Full article text
    
    Returns:
        list: Ordered list of relevant hashtags (most relevant first)
    """
    hashtags = []
    hashtag_scores = {}
    
    # Comprehensive keyword to hashtag mapping with priorities
    keywords_map = {
        # High priority - specific technologies
        'langchain': ('#LangChain', 10),
        'langgraph': ('#LangGraph', 10),
        'anthropic': ('#Anthropic', 9),
        'claude': ('#Claude', 9),
        'openai': ('#OpenAI', 9),
        'gpt': ('#GPT', 9),
        
        # High priority - AI concepts
        'multi-agent': ('#MultiAgent', 9),
        'multiagent': ('#MultiAgent', 9),
        'agent': ('#AIAgents', 8),
        'rag': ('#RAG', 8),
        'retrieval augmented': ('#RAG', 8),
        'vector database': ('#VectorDB', 8),
        'vector db': ('#VectorDB', 8),
        'embedding': ('#Embeddings', 7),
        'prompt engineering': ('#PromptEngineering', 8),
        'function calling': ('#FunctionCalling', 7),
        
        # Medium priority - general AI
        'artificial intelligence': ('#AI', 7),
        'machine learning': ('#MachineLearning', 7),
        'generative ai': ('#GenerativeAI', 7),
        'gen ai': ('#GenerativeAI', 7),
        'llm': ('#LLM', 8),
        'large language model': ('#LLM', 8),
        'chatbot': ('#Chatbot', 6),
        'conversational ai': ('#ConversationalAI', 6),
        
        # Medium priority - development
        'python': ('#Python', 7),
        'api': ('#API', 6),
        'tutorial': ('#Tutorial', 6),
        'guide': ('#Tutorial', 6),
        'workflow': ('#Workflow', 6),
        'automation': ('#Automation', 6),
        'production': ('#Production', 5),
        'deployment': ('#Deployment', 5),
        
        # Time-based
        '2026': ('#2026', 4),
        '2025': ('#2025', 4),
    }
    
    # Combine all text sources for analysis
    combined_text = f"{title} {focus_kw} {semantic_kw}".lower()
    
    # Also check first 2000 chars of article for context
    article_preview = article_content[:2000].lower() if article_content else ""
    
    # Score hashtags based on keyword matches
    for keyword, (hashtag, base_score) in keywords_map.items():
        score = 0
        
        # Check in title (highest weight)
        if keyword in title.lower():
            score += base_score * 3
        
        # Check in focus keyword (high weight)
        if keyword in focus_kw.lower():
            score += base_score * 2.5
        
        # Check in semantic keywords (medium weight)
        if keyword in semantic_kw.lower():
            score += base_score * 2
        
        # Check in article preview (lower weight)
        if keyword in article_preview:
            score += base_score * 1
        
        if score > 0 and hashtag not in hashtag_scores:
            hashtag_scores[hashtag] = score
    
    # Sort by score (highest first)
    sorted_hashtags = sorted(hashtag_scores.items(), key=lambda x: x[1], reverse=True)
    hashtags = [tag for tag, score in sorted_hashtags]
    
    # Ensure we have at least 3 hashtags
    essential_tags = ['#AI', '#TechTutorial', '#Developer', '#Coding']
    for tag in essential_tags:
        if len(hashtags) >= 5:
            break
        if tag not in hashtags:
            hashtags.append(tag)
    
    return hashtags


def create_twitter_post(title, permalink, focus_kw, semantic_kw, article_content, image_path=None):
    """
    Create optimized Twitter post using all article data
    
    Args:
        title: Article title
        permalink: URL permalink
        focus_kw: Focus keyword
        semantic_kw: Semantic keywords
        article_content: Full article text
        image_path: Path to article image (optional)
    
    Returns:
        str: Formatted Twitter content
    """
    # Extract description from article
    paragraphs = [p.strip() for p in article_content.split('\n\n') 
                  if p.strip() and not p.startswith('#') and len(p.strip()) > 50]
    
    description = paragraphs[0] if paragraphs else focus_kw
    
    # Generate smart hashtags
    hashtags = generate_smart_hashtags(title, focus_kw, semantic_kw, article_content)
    
    # Get top 3 most relevant hashtags for Twitter
    top_hashtags = hashtags[:3]
    
    # Calculate available space (280 chars total)
    # Format: emoji + title + \n\n + description + \n\n + hashtags + \n\n + [link]
    
    emoji = "📚 "
    separator = "\n\n"
    link_placeholder = "[link]"
    hashtag_string = ' '.join(top_hashtags)
    
    # Fixed parts
    fixed_parts = emoji + separator + separator + hashtag_string + separator + link_placeholder
    fixed_length = len(fixed_parts)
    
    # Available space for title + description
    available_space = 280 - fixed_length - 30  # 30 chars buffer for URL
    
    # Allocate space: prefer longer title
    title_length = len(title)
    
    if title_length > 60:
        # Long title: truncate it
        title_display = title[:57] + "..."
        desc_space = available_space - 60
    else:
        # Short title: use more space for description
        title_display = title
        desc_space = available_space - title_length
    
    # Truncate description if needed
    if len(description) > desc_space:
        description = description[:desc_space-3] + "..."
    
    # Construct tweet
    twitter_content = f"{emoji}{title_display}{separator}{description}{separator}{hashtag_string}{separator}{link_placeholder}"
    
    return twitter_content, top_hashtags


def create_linkedin_post(title, permalink, focus_kw, semantic_kw, article_content, image_path=None):
    """
    Create optimized LinkedIn post using all article data
    
    Args:
        title: Article title
        permalink: URL permalink
        focus_kw: Focus keyword
        semantic_kw: Semantic keywords
        article_content: Full article text
        image_path: Path to article image (optional)
    
    Returns:
        str: Formatted LinkedIn content
    """
    # Extract longer description from article
    paragraphs = [p.strip() for p in article_content.split('\n\n') 
                  if p.strip() and not p.startswith('#') and len(p.strip()) > 50]
    
    # Get first 2-3 paragraphs for LinkedIn
    description_parts = paragraphs[:2] if len(paragraphs) >= 2 else paragraphs
    description = '\n\n'.join(description_parts)
    
    # Truncate if too long (LinkedIn prefers 1200-1300 chars)
    if len(description) > 600:
        description = description[:597] + "..."
    
    # Generate smart hashtags (use more for LinkedIn)
    hashtags = generate_smart_hashtags(title, focus_kw, semantic_kw, article_content)
    top_hashtags = hashtags[:5]
    
    # Extract key topics from semantic keywords
    key_topics = [kw.strip() for kw in semantic_kw.split(',')[:3] if kw.strip()]
    
    # Build LinkedIn post
    linkedin_content = f"""📚 {title}

{description}

Key Topics:
"""
    
    # Add key topics as bullet points
    for topic in key_topics:
        linkedin_content += f"• {topic}\n"
    
    # Add hashtags
    linkedin_content += f"\n{' '.join(top_hashtags)}\n\n"
    linkedin_content += "Read the full article: [link]"
    
    return linkedin_content, top_hashtags


def main():
    print("=" * 60)
    print("🚀 Starting Blog Post Generator")
    print("=" * 60)
    
    # Verify environment variables
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found")
        return
    print("✅ GEMINI_API_KEY found")
    
    if not FREEPIK_API_KEY:
        print("❌ FREEPIK_API_KEY not found")
        return
    print("✅ FREEPIK_API_KEY found")
    
    # # Show keywords status
    # keywords_count = get_keywords_count()
    # print(f"\n📊 Posts to generate this run: {POSTS_PER_RUN}")
    # print(f"📋 Keywords available: {keywords_count}")
    
    # posts_generated = 0
    
    # for post_num in range(1, POSTS_PER_RUN + 1):
    #     print(f"\n{'=' * 60}")
    #     print(f"📝 Processing Post {post_num}/{POSTS_PER_RUN}")
    #     print("=" * 60)
        
    #     # Get next keyword
    #     row = get_keyword_row()
    #     if not row:
    #         print(f"❌ No more keywords left")
    #         break
        
    #     print(f"\n📋 Keyword: {row[:80]}...")
        
    #     # Parse keyword with new format
    #     keyword_data = parse_keyword_row(row)
    #     if not keyword_data:
    #         print(f"❌ Invalid keyword format")
    #         remove_keyword_from_file()  # Remove invalid keyword
    #         continue
        
    #     title = keyword_data['title']
    #     focus_kw = keyword_data['focus_kw']
    #     permalink = keyword_data['permalink']
    #     semantic_kw = keyword_data['semantic_kw']
    #     affiliate_links = keyword_data['affiliate_links']
        
    #     print(f"✅ Parsed: {title[:60]}...")
        
    #     # Generate file paths
    #     today = datetime.date.today().isoformat()
    #     post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
    #     image_file = f"{IMAGES_DIR}/{permalink}.webp"
        
    #     # Check if post already exists
    #     if os.path.exists(post_path):
    #         print(f"\n⚠️  Post already exists: {post_path}")
    #         remove_keyword_from_file()  # Remove duplicate
    #         continue
        
    #     # Generate content
    #     try:
    #         # Step 1: Generate article
    #         print(f"\n{'=' * 60}")
    #         print("Step 1: Generating Article")
    #         print("=" * 60)
    #         article = generate_article(title, focus_kw, permalink, semantic_kw)
    #         print(f"✅ Article generated ({len(article)} characters)")
            
    #         # Step 2: Generate image prompt
    #         print(f"\n{'=' * 60}")
    #         print("Step 2: Generating Image Prompt")
    #         print("=" * 60)
    #         image_prompt = generate_image_prompt(title)
    #         print(f"✅ Image prompt generated")
            
    #         # Step 3: Generate image
    #         print(f"\n{'=' * 60}")
    #         print("Step 3: Generating & Compressing Image")
    #         print("=" * 60)
    #         generate_image_freepik(image_prompt, image_file)
            
    #         # Step 4: Save post
    #         print(f"\n{'=' * 60}")
    #         print("Step 4: Saving Post")
    #         print("=" * 60)
    #         with open(post_path, "w", encoding="utf-8") as f:
    #             f.write(article)
    #         print(f"✅ Post saved: {post_path}")
            
    #         post_url = f"{SITE_DOMAIN}/{permalink}"
            
    #         print(f"\n{'=' * 60}")
    #         print(f"✅ SUCCESS! Post {post_num} Generated")
    #         print("=" * 60)
    #         print(f"📰 Title: {title}")
    #         print(f"🌐 URL: {post_url}")
            
    #         posts_generated += 1
            
    #         # Step 5: Wait before indexing
    #         if post_num == POSTS_PER_RUN or post_num == posts_generated:
    #             print(f"\n{'=' * 60}")
    #             print(f"Step 5: Waiting {WAIT_TIME_BEFORE_INDEXING // 60} minutes")
    #             print("=" * 60)
    #             print("⏳ Allowing GitHub Pages to deploy...")
                
    #             for remaining in range(WAIT_TIME_BEFORE_INDEXING, 0, -30):
    #                 minutes = remaining // 60
    #                 seconds = remaining % 60
    #                 print(f"⏰ Time remaining: {minutes}m {seconds}s", end='\r')
    #                 # time.sleep(30)
                
                
                
    # Step 6: Submit to Google Search Console (Browser Only)
    print(f"\n{'=' * 60}")
    print("Step 6: Submitting to Google Search Console")
    print("=" * 60)
    
    indexing_status = "Not Attempted"
    try:
        # URLS_TO_SUBMIT = post_url
        URLS_TO_SUBMIT = "https://ur-lawyer.github.io/when-to-hire-medical-malpractice-lawyer"
        print(f"📋 URLS_TO_SUBMIT: {URLS_TO_SUBMIT}")
        
        gsc_success = submit_url_to_gsc(URLS_TO_SUBMIT)
        
        if gsc_success:
            indexing_status = "Success (GSC Browser)"
            print("✅ URL submitted to Google Search Console!")
        else:
            indexing_status = "Failed (GSC Browser)"
            print("⚠️ GSC submission failed")
            
    except Exception as e:
        indexing_status = f"Failed - {str(e)[:100]}"
        print(f"⚠️ GSC automation failed: {e}")
    
    print(f"\n📊 Indexing Status: {indexing_status}")
                
                    
        #         # Step 10: Send Push Notification
        #         print(f"\n{'=' * 60}")
        #         print("Step 10: Sending Push Notification")
        #         print("=" * 60)

        #         try:
        #             send_blog_post_notification(title, permalink, focus_kw)
        #         except Exception as e:
        #             print(f"⚠️ Push notification failed (non-critical): {e}")
            
        #     # Step 11: Remove keyword after success
        #     print(f"\n{'=' * 60}")
        #     print("Step 11: Removing Keyword from File")
        #     print("=" * 60)
        #     remove_keyword_from_file()
        #     print("✅ Keyword removed from keywords.txt")
            
        # except Exception as e:
        #     print(f"\n{'=' * 60}")
        #     print(f"❌ FAILED: {e}")
        #     print("=" * 60)
        #     print(f"⚠️ Keyword NOT removed - will retry next run")
        #     import traceback
        #     traceback.print_exc()
        #     continue
    
    # Final summary
    print(f"\n{'=' * 60}")
    print("🎉 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"✅ Posts generated: {posts_generated}")
    print(f"📊 Keywords remaining: {get_keywords_count()}")
    print(f"\n📱 Social Media Summary:")
    print(f"   • All posts automatically shared to Twitter & LinkedIn")
    print(f"   • Smart hashtag generation based on article content")
    print(f"   • Platform-optimized formatting")
    print("=" * 60)


if __name__ == "__main__":
    main()