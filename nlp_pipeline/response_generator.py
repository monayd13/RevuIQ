"""
Response Generation Module
Uses Flan-T5 for generating brand-consistent, empathetic replies
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class ResponseGenerator:
    """
    Generates AI-powered responses to customer reviews.
    
    Uses prompt engineering to create:
    - Empathetic and professional tone
    - Brand-consistent messaging
    - Appropriate length (2-3 sentences)
    """
    
    def __init__(self, model_name="google/flan-t5-base"):
        """
        Initialize response generator with T5 model.
        
        Args:
            model_name: Hugging Face model identifier
        """
        print(f"Loading response generation model: {model_name}")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
        
        print("✓ Response generator ready!")
    
    def _create_prompt(self, review, sentiment, emotion=None, business_name="our business"):
        """
        Create a structured prompt for the model.
        
        Args:
            review (str): Customer review text
            sentiment (str): POSITIVE, NEUTRAL, or NEGATIVE
            emotion (str): Primary emotion detected
            business_name (str): Name of the business
            
        Returns:
            str: Formatted prompt
        """
        # Base instruction
        instruction = f"You are a professional customer service representative for {business_name}. "
        
        # Tone guidance based on sentiment
        if sentiment == "POSITIVE":
            instruction += "Write a grateful and warm response. "
        elif sentiment == "NEGATIVE":
            instruction += "Write an apologetic and solution-focused response. "
        else:
            instruction += "Write a friendly and helpful response. "
        
        # Add emotion context if available
        if emotion:
            instruction += f"The customer seems to feel {emotion}. "
        
        # Formatting requirements
        instruction += "Keep it brief (2-3 sentences), professional, and empathetic.\n\n"
        
        # The actual task
        prompt = f"{instruction}Customer Review: \"{review}\"\n\nYour Response:"
        
        return prompt
    
    def generate(self, review, sentiment="NEUTRAL", emotion=None, 
                 business_name="our business", max_length=100, temperature=0.7):
        """
        Generate a response to a customer review.
        
        Args:
            review (str): Customer review text
            sentiment (str): Sentiment label (POSITIVE/NEUTRAL/NEGATIVE)
            emotion (str): Primary emotion detected (optional)
            business_name (str): Name of the business
            max_length (int): Maximum response length in tokens
            temperature (float): Sampling temperature (higher = more creative)
            
        Returns:
            dict: {
                'response': generated reply text,
                'prompt': the prompt used,
                'metadata': generation parameters
            }
        """
        if not review or not review.strip():
            return {
                'response': "Thank you for your feedback!",
                'prompt': None,
                'error': 'Empty review'
            }
        
        try:
            # Create prompt
            prompt = self._create_prompt(review, sentiment, emotion, business_name)
            
            # Tokenize
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True
            ).to(self.device)
            
            # Generate response
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                num_return_sequences=1
            )
            
            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up response
            response = response.strip()
            if not response.endswith(('.', '!', '?')):
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
        """
        Generate multiple response variations for human selection.
        
        Args:
            review (str): Customer review text
            sentiment (str): Sentiment label
            emotion (str): Primary emotion
            business_name (str): Business name
            num_variations (int): Number of variations to generate
            
        Returns:
            list: List of response dictionaries
        """
        responses = []
        
        for i in range(num_variations):
            # Vary temperature for diversity
            temp = 0.7 + (i * 0.1)
            result = self.generate(
                review, sentiment, emotion, business_name, temperature=temp
            )
            responses.append(result)
        
        return responses


def generate_response(review, sentiment="NEUTRAL", emotion=None):
    """
    Convenience function for quick response generation.
    
    Args:
        review (str): Customer review text
        sentiment (str): Sentiment label
        emotion (str): Primary emotion
        
    Returns:
        str: Generated response text
    """
    generator = ResponseGenerator()
    result = generator.generate(review, sentiment, emotion)
    return result['response']


# Example usage
if __name__ == "__main__":
    # Test the response generator
    generator = ResponseGenerator()
    
    test_cases = [
        {
            'review': "The coffee was amazing! Best I've ever had.",
            'sentiment': 'POSITIVE',
            'emotion': 'joy'
        },
        {
            'review': "Service was terrible and the food was cold.",
            'sentiment': 'NEGATIVE',
            'emotion': 'anger'
        },
        {
            'review': "It was okay, nothing special.",
            'sentiment': 'NEUTRAL',
            'emotion': 'neutral'
        },
        {
            'review': "Great food but the wait was too long.",
            'sentiment': 'NEUTRAL',
            'emotion': 'disappointment'
        }
    ]
    
    print("\n" + "="*70)
    print("RESPONSE GENERATION DEMO")
    print("="*70 + "\n")
    
    for case in test_cases:
        result = generator.generate(
            case['review'],
            case['sentiment'],
            case['emotion'],
            business_name="Starbucks"
        )
        
        print(f"Review: {case['review']}")
        print(f"Sentiment: {case['sentiment']} | Emotion: {case['emotion']}")
        print(f"AI Response: {result['response']}")
        print("-" * 70)
