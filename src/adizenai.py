#!/usr/bin/env python3
"""
AdiZenWorks AI Assistant
Gemini-powered security analysis and recommendations
Company: AdiZenWorks Inc.
"""

import json
from pathlib import Path
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AIAssistant:
    def __init__(self, api_key=None):
        """Initialize Gemini AI Assistant"""
        self.api_key = api_key
        self.model = None
        
        if not GEMINI_AVAILABLE:
            self.error = "google-generativeai not installed. Run: pip install google-generativeai"
            return
        
        if not api_key:
            # Try to load from config
            config_path = Path("adizen_config.json")
            if config_path.exists():
                with open(config_path) as f:
                    config = json.load(f)
                    self.api_key = config.get("gemini_api_key")
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.error = None
            except Exception as e:
                self.error = f"Failed to initialize Gemini: {str(e)}"
        else:
            self.error = "No API key found. Please configure adizen_config.json"
    
    def analyze_vulnerability(self, vulnerability_type, details):
        """
        Analyze a security vulnerability using AI
        
        Args:
            vulnerability_type: Type of vulnerability (XSS, SQLi, etc.)
            details: Details about the vulnerability
        
        Returns:
            dict with AI analysis
        """
        results = {
            "vulnerability_type": vulnerability_type,
            "timestamp": datetime.now().isoformat()
        }
        
        if not GEMINI_AVAILABLE:
            results["error"] = "Gemini AI not available. Install: pip install google-generativeai"
            return results
        
        if self.error:
            results["error"] = self.error
            return results
        
        try:
            # Create prompt
            prompt = f"""As a cybersecurity expert, analyze this vulnerability:

Vulnerability Type: {vulnerability_type}
Details: {details}

Provide:
1. Risk Assessment (Critical/High/Medium/Low)
2. Potential Impact
3. Exploitation Difficulty
4. Recommended Remediation Steps
5. Additional Security Considerations

Be concise but thorough."""

            # Generate response
            response = self.model.generate_content(prompt)
            
            results["analysis"] = response.text
            results["status"] = "success"
            
        except Exception as e:
            results["error"] = str(e)
            results["status"] = "failed"
        
        return results
    
    def analyze_scan_results(self, scan_data):
        """
        Analyze security scan results
        
        Args:
            scan_data: Dictionary containing scan results
        
        Returns:
            dict with AI analysis
        """
        results = {
            "timestamp": datetime.now().isoformat()
        }
        
        if not GEMINI_AVAILABLE:
            results["error"] = "Gemini AI not available"
            return results
        
        if self.error:
            results["error"] = self.error
            return results
        
        try:
            # Create analysis prompt
            prompt = f"""As a cybersecurity expert, analyze these scan results:

{json.dumps(scan_data, indent=2)}

Provide:
1. Overall Security Posture
2. Critical Findings
3. Priority Recommendations
4. Long-term Security Improvements

Be specific and actionable."""

            response = self.model.generate_content(prompt)
            
            results["analysis"] = response.text
            results["status"] = "success"
            
        except Exception as e:
            results["error"] = str(e)
            results["status"] = "failed"
        
        return results
    
    def get_security_advice(self, question):
        """
        Get security advice for a specific question
        
        Args:
            question: Security-related question
        
        Returns:
            dict with AI response
        """
        results = {
            "question": question,
            "timestamp": datetime.now().isoformat()
        }
        
        if not GEMINI_AVAILABLE:
            results["error"] = "Gemini AI not available"
            return results
        
        if self.error:
            results["error"] = self.error
            return results
        
        try:
            prompt = f"""As a cybersecurity expert at AdiZenWorks Inc., answer this question:

{question}

Provide expert, actionable advice."""

            response = self.model.generate_content(prompt)
            
            results["answer"] = response.text
            results["status"] = "success"
            
        except Exception as e:
            results["error"] = str(e)
            results["status"] = "failed"
        
        return results

# WRAPPER FUNCTION for compatibility
def analyze_with_ai(query_type, data):
    """
    Wrapper function for AI analysis
    
    Args:
        query_type: Type of analysis ('vulnerability', 'scan', 'advice')
        data: Data to analyze or question to answer
    
    Returns:
        dict with AI response
    """
    assistant = AIAssistant()
    
    if query_type == "vulnerability":
        return assistant.analyze_vulnerability(
            data.get("type", "Unknown"),
            data.get("details", "")
        )
    elif query_type == "scan":
        return assistant.analyze_scan_results(data)
    elif query_type == "advice":
        return assistant.get_security_advice(data)
    else:
        return {"error": f"Unknown query type: {query_type}"}

def main():
    """Test AI Assistant"""
    print("AdiZenWorks AI Assistant Test")
    print("-" * 50)
    
    assistant = AIAssistant()
    
    if assistant.error:
        print(f"Error: {assistant.error}")
        print("\nTo use AI Assistant:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Create adizen_config.json with:")
        print('   {"gemini_api_key": "YOUR_KEY_HERE"}')
        return
    
    # Test question
    question = "What are the top 3 security headers every website should have?"
    results = assistant.get_security_advice(question)
    
    print(f"Question: {question}")
    print(f"\nAnswer:\n{results.get('answer', 'No answer')}")
    
# Alias for Flask compatibility
AdiZenAI = AIAssistant

if __name__ == "__main__":
    main()
