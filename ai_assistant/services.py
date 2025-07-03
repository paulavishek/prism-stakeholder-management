import google.generativeai as genai
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not configured")
    
    def is_available(self):
        return self.model is not None
    
    def generate_stakeholder_profile(self, basic_info):
        """
        Generate comprehensive stakeholder profile from basic information
        """
        if not self.is_available():
            return "AI service not available"
        
        prompt = f"""
        Based on the following basic stakeholder information, generate a comprehensive analysis:
        
        Name: {basic_info.get('name', 'N/A')}
        Title: {basic_info.get('title', 'N/A')}
        Organization: {basic_info.get('organization', 'N/A')}
        Department: {basic_info.get('department', 'N/A')}
        Category: {basic_info.get('category', 'N/A')}
        
        Please provide:
        1. Likely influence level and reasons
        2. Potential interests and concerns
        3. Recommended engagement strategies
        4. Potential risks or challenges
        5. Communication preferences
        6. Key talking points for meetings
        
        Format your response as a structured analysis.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating stakeholder profile: {e}")
            return f"Error generating profile: {str(e)}"
    
    def draft_communication(self, stakeholder_info, communication_type, purpose):
        """
        Draft communication for stakeholder
        """
        if not self.is_available():
            return "AI service not available"
        
        prompt = f"""
        Draft a {communication_type} for the following stakeholder:
        
        Stakeholder: {stakeholder_info.get('name', 'N/A')} - {stakeholder_info.get('title', 'N/A')}
        Organization: {stakeholder_info.get('organization', 'N/A')}
        Purpose: {purpose}
        
        Consider their:
        - Influence level: {stakeholder_info.get('influence', 'medium')}
        - Interest level: {stakeholder_info.get('interest', 'medium')}
        - Category: {stakeholder_info.get('category', 'internal')}
        
        Please draft a professional {communication_type} that:
        1. Uses appropriate tone for their position
        2. Is concise and respectful of their time
        3. Clearly states the purpose
        4. Includes a clear call to action if needed
        5. Maintains professional relationships
        """        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error drafting communication: {e}")
            return f"Error drafting communication: {str(e)}"
    
    def summarize_meeting(self, meeting_notes, stakeholder_info):
        """
        Generate meeting summary and extract action items        """
        if not self.is_available():
            return {"summary": "AI service not available", "action_items": "", "sentiment": "neutral", "risks": "", "follow_up": ""}
        
        prompt = f"""
        Analyze the following meeting notes with stakeholder {stakeholder_info.get('name', 'N/A')}:
        
        Meeting Notes:
        {meeting_notes}
        
        Please provide your analysis in the following JSON format ONLY. Do not include any other text or formatting:
        
        {{
            "summary": "A concise summary of key discussion points",
            "action_items": "List of action items with responsible parties and deadlines",
            "sentiment": "positive, neutral, or negative (lowercase only)",
            "risks": "Any risks or concerns identified",
            "follow_up": "Suggested follow-up actions"
        }}
        
        Requirements:
        1. Use only "positive", "neutral", or "negative" (lowercase) for sentiment
        2. If no specific information is available for a field, use an empty string ""
        3. Do not include any markdown formatting or code blocks
        4. Return only valid JSON
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Try to parse as JSON, with better fallback handling
            try:
                parsed_response = json.loads(response.text)
                # Ensure all required keys exist and normalize sentiment
                result = {
                    "summary": parsed_response.get("summary", ""),
                    "action_items": parsed_response.get("action_items", ""),
                    "sentiment": parsed_response.get("sentiment", "neutral").lower(),
                    "risks": parsed_response.get("risks", ""),
                    "follow_up": parsed_response.get("follow_up", "")
                }
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract information from text
                text_response = response.text
                logger.warning(f"Failed to parse JSON response, processing as text: {text_response[:100]}...")
                
                # Try to extract JSON from the text if it's wrapped in markdown or other formatting
                import re
                json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
                if json_match:
                    try:
                        parsed_response = json.loads(json_match.group())
                        result = {
                            "summary": parsed_response.get("summary", ""),
                            "action_items": parsed_response.get("action_items", ""),
                            "sentiment": parsed_response.get("sentiment", "neutral").lower(),
                            "risks": parsed_response.get("risks", ""),
                            "follow_up": parsed_response.get("follow_up", "")
                        }
                        return result
                    except json.JSONDecodeError:
                        pass
                
                # If all JSON parsing attempts fail, return the text as summary
                return {
                    "summary": text_response,
                    "action_items": "Unable to extract structured action items from response",
                    "sentiment": "neutral",
                    "risks": "Unable to extract structured risks from response",
                    "follow_up": "Unable to extract structured follow-up actions from response"
                }
        except Exception as e:
            logger.error(f"Error summarizing meeting: {e}")
            return {
                "summary": f"Error summarizing meeting: {str(e)}",
                "action_items": "",
                "sentiment": "neutral",
                "risks": "",
                "follow_up": ""
            }
    
    def analyze_stakeholder_sentiment(self, text_content):
        """
        Analyze sentiment from stakeholder communications
        """
        if not self.is_available():
            return "neutral"
        
        prompt = f"""
        Analyze the sentiment of the following stakeholder communication:
        
        "{text_content}"
        
        Classify the sentiment as: positive, neutral, or negative
        Provide reasoning for your classification.
        
        Respond with just the sentiment classification (positive/neutral/negative) followed by a brief explanation.
        """
        
        try:
            response = self.model.generate_content(prompt)
            sentiment_text = response.text.lower()
            
            if 'positive' in sentiment_text:
                return 'positive'
            elif 'negative' in sentiment_text:
                return 'negative'
            else:
                return 'neutral'
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return 'neutral'
    
    def suggest_engagement_strategy(self, stakeholder_data, engagement_history=None):
        """
        Suggest optimal engagement strategy for stakeholder
        """
        if not self.is_available():
            return "AI service not available"
        
        prompt = f"""
        Based on the stakeholder profile and engagement history, suggest an optimal engagement strategy:
        
        Stakeholder Profile:
        - Name: {stakeholder_data.get('name', 'N/A')}
        - Influence: {stakeholder_data.get('influence', 'medium')}
        - Interest: {stakeholder_data.get('interest', 'medium')}
        - Category: {stakeholder_data.get('category', 'internal')}
        - Notes: {stakeholder_data.get('notes', 'N/A')}
        
        Recent Engagement History:
        {engagement_history or 'No recent engagements'}
        
        Please recommend:
        1. Optimal frequency of engagement
        2. Best communication channels
        3. Key topics to focus on
        4. Timing considerations
        5. Specific tactics for building relationships
        6. Warning signs to watch for
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating engagement strategy: {e}")
            return f"Error generating strategy: {str(e)}"
    
    def extract_action_items(self, text_content):
        """
        Extract action items from meeting notes or communications
        """
        if not self.is_available():
            return "AI service not available"
        
        prompt = f"""
        Extract action items from the following text:
        
        "{text_content}"
        
        Format each action item as:
        - Action: [what needs to be done]
        - Owner: [who is responsible]
        - Deadline: [when it's due, if mentioned]
        - Priority: [high/medium/low based on context]
        
        Only extract clear, actionable items. If no action items are found, respond with "No specific action items identified."
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error extracting action items: {e}")
            return f"Error extracting action items: {str(e)}"
