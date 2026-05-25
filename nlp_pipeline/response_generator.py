"""
Response Generation Module
Uses Groq API (llama-3.3-70b-versatile) — no GPU/torch needed
"""

import os
from groq import Groq


class ResponseGenerator:
    """
    Generates AI-powered responses to customer reviews via Groq API.
    """

    def __init__(self, model_name=None):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is not set")
        self._client = Groq(api_key=api_key)
        self._model = "llama-3.3-70b-versatile"
        print("✓ Response generator ready!")

    def _create_prompt(self, review, sentiment, emotion=None, business_name="our business"):
        if sentiment == "POSITIVE":
            tone = "grateful and warm"
        elif sentiment == "NEGATIVE":
            tone = "apologetic and solution-focused"
        else:
            tone = "friendly and helpful"

        emotion_line = f" The customer seems to feel {emotion}." if emotion else ""

        return (
            f"You are a professional customer service representative for {business_name}. "
            f"Write a {tone} response to the review below.{emotion_line} "
            f"Keep it brief (2-3 sentences), professional, and empathetic.\n\n"
            f'Customer Review: "{review}"\n\nYour Response:'
        )

    def generate(self, review, sentiment="NEUTRAL", emotion=None,
                 business_name="our business", max_length=150, temperature=0.7):
        if not review or not review.strip():
            return {'response': "Thank you for your feedback!", 'prompt': None, 'error': 'Empty review'}

        try:
            prompt = self._create_prompt(review, sentiment, emotion, business_name)

            completion = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_length,
                temperature=temperature,
            )

            response = completion.choices[0].message.content.strip()
            if response and not response[-1] in '.!?':
                response += '.'

            return {
                'response': response,
                'prompt': prompt,
                'metadata': {
                    'sentiment': sentiment,
                    'emotion': emotion,
                    'temperature': temperature,
                    'max_length': max_length
                }
            }
        except Exception as e:
            return {
                'response': "Thank you for your feedback. We appreciate your input!",
                'prompt': None,
                'error': str(e)
            }

    def generate_multiple(self, review, sentiment="NEUTRAL", emotion=None,
                          business_name="our business", num_variations=3):
        responses = []
        for i in range(num_variations):
            temp = 0.7 + (i * 0.1)
            result = self.generate(review, sentiment, emotion, business_name, temperature=temp)
            responses.append(result)
        return responses


def generate_response(review, sentiment="NEUTRAL", emotion=None):
    generator = ResponseGenerator()
    result = generator.generate(review, sentiment, emotion)
    return result['response']
