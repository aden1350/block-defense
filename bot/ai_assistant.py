#!/usr/bin/env python3
"""
AI Assistant Bot - Test Version
Uses knowledge base and search to answer questions
"""

import json
import os
import re
from datetime import datetime
from ddgs import DDGS

# Knowledge base path
KNOWLEDGE_DIR = "/root/.openclaw/workspace/memory"

def search_knowledge(query):
    """Search knowledge base"""
    results = []
    seen = set()
    
    # Knowledge base files with priority
    files = [
        ("AI研究", "ai_agent_knowledge.md"),
        ("热点", "xiaohongshu_agent_knowledge.md"),
        ("股市", "stock_agent_knowledge.md"),
        ("探索", "exploration.md")
    ]
    
    for category, fname in files:
        fpath = os.path.join(KNOWLEDGE_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                content = f.read()
                # Split into sentences/paragraphs
                paragraphs = re.split(r'\n\n+', content)
                
                for para in paragraphs:
                    # Check if query keywords appear
                    query_lower = query.lower()
                    if any(kw.lower() in para.lower() for kw in [query_lower, query_lower[:2] if len(query) > 1 else query]):
                        # Clean and truncate
                        clean_para = ' '.join(para.split())[:150]
                        if clean_para not in seen and len(clean_para) > 20:
                            results.append(f"[{category}] {clean_para}")
                            seen.add(clean_para)
    
    return results[:5]

def web_search(query):
    """Search the web for information"""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=3)
        return [r['title'] for r in results]
    except Exception as e:
        print(f"Search error: {e}")
        return []

def format_response(query, knowledge_results, web_results=None):
    """Format response"""
    response = f"=== {query} ===\n\n"
    
    if knowledge_results:
        response += "[Knowledge Base Results]\n"
        for i, r in enumerate(knowledge_results[:3], 1):
            response += f"{i}. {r}\n\n"
    
    if web_results:
        response += "[Web Results]\n"
        for i, r in enumerate(web_results[:2], 1):
            response += f"- {r}\n"
    
    if not knowledge_results and not web_results:
        response += "No relevant information found.\n"
    
    response += f"\n{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    return response

def answer_question(query):
    """Answer question using knowledge base + web search"""
    # Search knowledge base
    knowledge_results = search_knowledge(query)
    
    # If no knowledge results, search web
    web_results = None
    if not knowledge_results:
        web_results = web_search(query)
    
    return format_response(query, knowledge_results, web_results)

# Test
if __name__ == "__main__":
    test_queries = [
        "AI",
        "机器人", 
        "股票",
        "小红书",
        "具身智能",
        "量子计算"
    ]
    
    print("="*50)
    print("AI Assistant Bot - Test Results")
    print("="*50)
    
    for q in test_queries:
        result = answer_question(q)
        print(f"\n{result}")
        print("-"*50)
