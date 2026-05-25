"""
Emotion Detection Module
Uses keyword-based detection (lightweight, no GPU/torch needed)
"""


# Keyword sets per emotion
_EMOTION_KEYWORDS = {
    'joy':            ['love', 'amazing', 'fantastic', 'wonderful', 'great', 'excellent',
                       'happy', 'best', 'perfect', 'awesome', 'delightful', 'thrilled'],
    'gratitude':      ['thank', 'thanks', 'grateful', 'appreciate', 'appreciated', 'thankful'],
    'anger':          ['angry', 'furious', 'outraged', 'terrible', 'horrible', 'worst',
                       'disgusting', 'unacceptable', 'ridiculous', 'awful'],
    'disappointment': ['disappointed', 'disappointing', 'letdown', 'expected more',
                       'not what i expected', 'underwhelming', 'mediocre'],
    'sadness':        ['sad', 'upset', 'unhappy', 'unfortunate', 'regret', 'sorry', 'miss'],
    'disgust':        ['disgusting', 'gross', 'revolting', 'nasty', 'filthy', 'dirty'],
    'surprise':       ['surprised', 'unexpected', 'shocked', 'amazed', 'unbelievable', 'wow'],
    'fear':           ['scared', 'afraid', 'worried', 'nervous', 'anxious', 'concerned'],
    'confusion':      ['confused', 'confusing', 'unclear', "don't understand", 'weird', 'strange'],
    'admiration':     ['impressive', 'admire', 'outstanding', 'exceptional', 'remarkable'],
    'neutral':        [],
}


class EmotionDetector:
    """
    Detects emotions in customer reviews using keyword matching.
    """

    def __init__(self, model_name=None):
        print("✓ Emotion detector ready!")

    def detect(self, text, top_n=3, threshold=0.1):
        if not text or not text.strip():
            return {'primary_emotion': 'neutral', 'emotions': [], 'all_scores': {}, 'error': 'Empty text'}

        try:
            lower = text.lower()
            scores = {}
            for emotion, keywords in _EMOTION_KEYWORDS.items():
                if not keywords:
                    continue
                hits = sum(1 for kw in keywords if kw in lower)
                if hits:
                    scores[emotion] = round(hits / len(keywords), 4)

            if not scores:
                scores['neutral'] = 1.0

            sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            significant = [
                {'label': e, 'score': s}
                for e, s in sorted_emotions
                if s >= threshold
            ][:top_n]

            primary = sorted_emotions[0][0] if sorted_emotions else 'neutral'

            return {
                'primary_emotion': primary,
                'emotions': significant,
                'all_scores': scores
            }
        except Exception as e:
            return {'primary_emotion': 'neutral', 'emotions': [], 'all_scores': {}, 'error': str(e)}

    def detect_batch(self, texts, top_n=3, threshold=0.1):
        return [self.detect(text, top_n, threshold) for text in texts]

    def get_emotion_summary(self, text):
        result = self.detect(text)
        if result.get('error'):
            return "Unable to detect emotions"
        emotions = result['emotions']
        if not emotions:
            return "Neutral tone"
        return ", ".join([f"{e['label']} ({e['score']:.0%})" for e in emotions])


def detect_emotion(text):
    detector = EmotionDetector()
    return detector.detect(text)
