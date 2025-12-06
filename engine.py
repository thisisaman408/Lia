from abc import ABC, abstractmethod
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Dict, Tuple

class SentimentEngine(ABC):
    @abstractmethod
    def analyze_message(self, text: str) -> Tuple[str, float]:
        pass

    @abstractmethod
    def analyze_conversation(self, messages: List[Dict]) -> Dict[str, str]:
        pass

class VaderSentimentEngine(SentimentEngine):
   
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_message(self, text: str) -> Tuple[str, float]:
        return self._get_score(text)

    def _get_score(self, text: str) -> Tuple[str, float]:
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        if compound >= 0.05: return "Positive", compound
        elif compound <= -0.05: return "Negative", compound
        return "Neutral", compound

    def analyze_conversation(self, messages: List[Dict]) -> Dict[str, str]:
        # Standard implementation needed for inheritance/fallback
        if not messages: return {"overall_sentiment": "Neutral", "trend": "Stable"}
        scores = [msg.get('sentiment_score', 0) for msg in messages if msg.get('sender') == 'user']
        if not scores: return {"overall_sentiment": "Neutral", "trend": "Stable"}
        
        avg_score = sum(scores) / len(scores)
        trend = self._calculate_trend(scores)
        
        if avg_score >= 0.05: overall = "Positive"
        elif avg_score <= -0.05: overall = "Negative"
        else: overall = "Neutral"
        return {"overall_sentiment": overall, "trend": trend}

    def _calculate_trend(self, scores: List[float]) -> str:
        if len(scores) < 2: return "Stable"
        mid = len(scores) // 2
        first = sum(scores[:mid]) / len(scores[:mid])
        second = sum(scores[mid:]) / len(scores[mid:])
        diff = second - first
        if diff > 0.1: return "Improving"
        elif diff < -0.1: return "Declining"
        return "Stable"


class ContentAwareLinguisticEngine(VaderSentimentEngine):
   
    def __init__(self):
        super().__init__()
        
        custom_lexicon = {
          
            'suicide': -4.0, 'kill myself': -4.0, 'hang myself': -4.0, 'die': -3.5,
            'dead': -3.5, 'worthless': -3.5, 'hopeless': -3.0, 'pain': -2.5,
            
           
            'blowjob': 1.5, 'fire': 2.8, 'lit': 2.5, 'goat': 3.0, 'mid': -1.5,
            
          
            'amazing': 3.5, 'love': 3.5, 'fantastic': 3.4
        }
        self.analyzer.lexicon.update(custom_lexicon)

    def analyze_message(self, text: str) -> Tuple[str, float]:
       
        label, score = super()._get_score(text)
        
       
        text_lower = text.lower()
        crisis_terms = ['suicide', 'kill myself', 'hang myself', 'die']
        if any(term in text_lower for term in crisis_terms):
           
            return "Negative", -0.95 

        return label, score



