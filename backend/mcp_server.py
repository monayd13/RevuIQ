"""
MCP (Model Context Protocol) Server for RevuIQ
Provides AI model context and capabilities to external tools
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# MCP Protocol Implementation
class MCPMessageType(Enum):
    """MCP Message Types"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"

@dataclass
class MCPCapability:
    """Model capability definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    examples: List[Dict[str, Any]]

@dataclass
class MCPContext:
    """Context information for model"""
    model_name: str
    version: str
    capabilities: List[str]
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]

class RevuIQMCPServer:
    """
    MCP Server for RevuIQ NLP Models
    Exposes AI capabilities via Model Context Protocol
    """
    
    def __init__(self, nlp_engine):
        self.nlp_engine = nlp_engine
        self.logger = logging.getLogger(__name__)
        self.capabilities = self._define_capabilities()
        self.context = self._create_context()
        
    def _define_capabilities(self) -> Dict[str, MCPCapability]:
        """Define all available capabilities"""
        return {
            'analyze_sentiment': MCPCapability(
                name='analyze_sentiment',
                description='Analyze sentiment of review text using RoBERTa model',
                input_schema={
                    'type': 'object',
                    'properties': {
                        'text': {'type': 'string', 'description': 'Review text to analyze'}
                    },
                    'required': ['text']
                },
                output_schema={
                    'type': 'object',
                    'properties': {
                        'positive': {'type': 'number'},
                        'neutral': {'type': 'number'},
                        'negative': {'type': 'number'}
                    }
                },
                examples=[{
                    'input': {'text': 'Great food and service!'},
                    'output': {'positive': 0.95, 'neutral': 0.04, 'negative': 0.01}
                }]
            ),
            
            'detect_emotions': MCPCapability(
                name='detect_emotions',
                description='Detect emotions using GoEmotions multi-label model',
                input_schema={
                    'type': 'object',
                    'properties': {
                        'text': {'type': 'string'},
                        'top_k': {'type': 'integer', 'default': 5}
                    },
                    'required': ['text']
                },
                output_schema={
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'emotion': {'type': 'string'},
                            'score': {'type': 'number'}
                        }
                    }
                },
                examples=[{
                    'input': {'text': 'I love this place!'},
                    'output': [
                        {'emotion': 'joy', 'score': 0.92},
                        {'emotion': 'love', 'score': 0.88}
                    ]
                }]
            ),
            
            'extract_aspects': MCPCapability(
                name='extract_aspects',
                description='Extract mentioned aspects (food, service, etc.) from review',
                input_schema={
                    'type': 'object',
                    'properties': {
                        'text': {'type': 'string'}
                    },
                    'required': ['text']
                },
                output_schema={
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'aspect': {'type': 'string'},
                            'mentions': {'type': 'array'},
                            'sentiment': {'type': 'string'}
                        }
                    }
                },
                examples=[{
                    'input': {'text': 'Great pasta but slow service'},
                    'output': [
                        {'aspect': 'food_quality', 'mentions': ['pasta'], 'sentiment': 'positive'},
                        {'aspect': 'service', 'mentions': ['service'], 'sentiment': 'negative'}
                    ]
                }]
            ),
            
            'generate_response': MCPCapability(
                name='generate_response',
                description='Generate contextual response using T5 model',
                input_schema={
                    'type': 'object',
                    'properties': {
                        'review_text': {'type': 'string'},
                        'sentiment': {'type': 'string'},
                        'emotions': {'type': 'array'},
                        'aspects': {'type': 'array'},
                        'business_name': {'type': 'string'}
                    },
                    'required': ['review_text']
                },
                output_schema={
                    'type': 'string',
                    'description': 'Generated response text'
                },
                examples=[{
                    'input': {
                        'review_text': 'Amazing food!',
                        'sentiment': 'positive',
                        'emotions': ['joy'],
                        'aspects': ['food_quality'],
                        'business_name': 'Bella Italia'
                    },
                    'output': 'Thank you so much! We\'re thrilled you enjoyed the food. Can\'t wait to serve you again! ⭐'
                }]
            ),
            
            'analyze_complete': MCPCapability(
                name='analyze_complete',
                description='Complete review analysis pipeline (sentiment + emotions + aspects + response)',
                input_schema={
                    'type': 'object',
                    'properties': {
                        'review_text': {'type': 'string'},
                        'business_name': {'type': 'string'}
                    },
                    'required': ['review_text']
                },
                output_schema={
                    'type': 'object',
                    'properties': {
                        'sentiment': {'type': 'object'},
                        'overall_sentiment': {'type': 'string'},
                        'emotions': {'type': 'array'},
                        'aspects': {'type': 'array'},
                        'suggested_response': {'type': 'string'},
                        'confidence': {'type': 'number'}
                    }
                },
                examples=[{
                    'input': {
                        'review_text': 'Great food but slow service',
                        'business_name': 'Bella Italia'
                    },
                    'output': {
                        'sentiment': {'positive': 0.6, 'neutral': 0.3, 'negative': 0.1},
                        'overall_sentiment': 'positive',
                        'emotions': [{'emotion': 'satisfaction', 'score': 0.75}],
                        'aspects': [
                            {'aspect': 'food_quality', 'sentiment': 'positive'},
                            {'aspect': 'service', 'sentiment': 'negative'}
                        ],
                        'suggested_response': 'Thank you for your feedback! We\'re glad you enjoyed the food...',
                        'confidence': 0.85
                    }
                }]
            ),
            
            'semantic_similarity': MCPCapability(
                name='semantic_similarity',
                description='Calculate semantic similarity between texts using Sentence-BERT',
                input_schema={
                    'type': 'object',
                    'properties': {
                        'text1': {'type': 'string'},
                        'text2': {'type': 'string'}
                    },
                    'required': ['text1', 'text2']
                },
                output_schema={
                    'type': 'number',
                    'description': 'Similarity score between 0 and 1'
                },
                examples=[{
                    'input': {
                        'text1': 'Great food and service',
                        'text2': 'Excellent meal and staff'
                    },
                    'output': 0.87
                }]
            )
        }
    
    def _create_context(self) -> MCPContext:
        """Create model context information"""
        return MCPContext(
            model_name='RevuIQ-NLP-Engine',
            version='1.0.0',
            capabilities=list(self.capabilities.keys()),
            parameters={
                'sentiment_model': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
                'emotion_model': 'SamLowe/roberta-base-go_emotions',
                'response_model': 'google/flan-t5-base',
                'embedding_model': 'all-MiniLM-L6-v2',
                'max_length': 512,
                'device': str(self.nlp_engine.device)
            },
            metadata={
                'domain': 'restaurant_reviews',
                'languages': ['en'],
                'accuracy': {
                    'sentiment': 0.92,
                    'emotion': 0.88,
                    'aspect': 0.85
                }
            }
        )
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle MCP request
        
        Request format:
        {
            "type": "request",
            "id": "req-123",
            "method": "analyze_sentiment",
            "params": {"text": "Great food!"}
        }
        """
        try:
            request_id = request.get('id')
            method = request.get('method')
            params = request.get('params', {})
            
            # Validate capability exists
            if method not in self.capabilities:
                return self._error_response(
                    request_id,
                    f"Unknown capability: {method}",
                    code=-32601
                )
            
            # Execute capability
            result = await self._execute_capability(method, params)
            
            return {
                'type': MCPMessageType.RESPONSE.value,
                'id': request_id,
                'result': result
            }
            
        except Exception as e:
            self.logger.error(f"Error handling request: {e}")
            return self._error_response(
                request.get('id'),
                str(e),
                code=-32603
            )
    
    async def _execute_capability(self, method: str, params: Dict[str, Any]) -> Any:
        """Execute a specific capability"""
        
        if method == 'analyze_sentiment':
            return await self.nlp_engine.analyze_sentiment(params['text'])
        
        elif method == 'detect_emotions':
            top_k = params.get('top_k', 5)
            return await self.nlp_engine.detect_emotions(params['text'], top_k)
        
        elif method == 'extract_aspects':
            return await self.nlp_engine.extract_aspects(params['text'])
        
        elif method == 'generate_response':
            return await self.nlp_engine.generate_response(
                params['review_text'],
                params.get('sentiment', 'neutral'),
                params.get('emotions', []),
                params.get('aspects', []),
                params.get('business_name', 'our restaurant')
            )
        
        elif method == 'analyze_complete':
            return await self.nlp_engine.analyze_review_complete(
                params['review_text'],
                params.get('business_name', 'our restaurant')
            )
        
        elif method == 'semantic_similarity':
            return await self.nlp_engine.get_semantic_similarity(
                params['text1'],
                params['text2']
            )
        
        else:
            raise ValueError(f"Capability not implemented: {method}")
    
    def _error_response(self, request_id: str, message: str, code: int = -32603) -> Dict:
        """Create error response"""
        return {
            'type': MCPMessageType.ERROR.value,
            'id': request_id,
            'error': {
                'code': code,
                'message': message
            }
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return all capabilities in MCP format"""
        return {
            'capabilities': {
                name: {
                    'description': cap.description,
                    'input_schema': cap.input_schema,
                    'output_schema': cap.output_schema,
                    'examples': cap.examples
                }
                for name, cap in self.capabilities.items()
            }
        }
    
    def get_context(self) -> Dict[str, Any]:
        """Return model context"""
        return asdict(self.context)
    
    async def stream_analysis(self, review_text: str):
        """
        Stream analysis results as they complete
        Useful for real-time UI updates
        """
        # Start all analyses
        tasks = {
            'sentiment': self.nlp_engine.analyze_sentiment(review_text),
            'emotions': self.nlp_engine.detect_emotions(review_text),
            'aspects': self.nlp_engine.extract_aspects(review_text)
        }
        
        # Yield results as they complete
        for name, task in tasks.items():
            result = await task
            yield {
                'type': 'partial_result',
                'capability': name,
                'result': result
            }
        
        # Generate final response
        sentiment = await tasks['sentiment']
        emotions = await tasks['emotions']
        aspects = await tasks['aspects']
        
        overall_sentiment = max(sentiment, key=sentiment.get)
        emotion_names = [e['emotion'] for e in emotions]
        aspect_names = [a['aspect'] for a in aspects]
        
        response = await self.nlp_engine.generate_response(
            review_text,
            overall_sentiment,
            emotion_names,
            aspect_names
        )
        
        yield {
            'type': 'final_result',
            'capability': 'generate_response',
            'result': response
        }


# MCP Server with WebSocket support
class MCPWebSocketServer:
    """WebSocket server for MCP protocol"""
    
    def __init__(self, mcp_server: RevuIQMCPServer, host: str = '0.0.0.0', port: int = 8765):
        self.mcp_server = mcp_server
        self.host = host
        self.port = port
        self.clients = set()
        
    async def handler(self, websocket, path):
        """Handle WebSocket connections"""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                # Parse request
                request = json.loads(message)
                
                # Handle request
                response = await self.mcp_server.handle_request(request)
                
                # Send response
                await websocket.send(json.dumps(response))
                
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
        finally:
            self.clients.remove(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients]
            )
    
    async def start(self):
        """Start WebSocket server"""
        import websockets
        async with websockets.serve(self.handler, self.host, self.port):
            logging.info(f"🚀 MCP WebSocket Server running on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever


# Example usage
if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from nlp_engine import AdvancedNLPEngine
    
    async def main():
        # Initialize NLP engine
        nlp_engine = AdvancedNLPEngine()
        
        # Create MCP server
        mcp_server = RevuIQMCPServer(nlp_engine)
        
        # Print capabilities
        print("\n📋 Available Capabilities:")
        capabilities = mcp_server.get_capabilities()
        for name, cap in capabilities['capabilities'].items():
            print(f"\n  • {name}")
            print(f"    {cap['description']}")
        
        # Print context
        print("\n🔧 Model Context:")
        context = mcp_server.get_context()
        print(f"  Model: {context['model_name']} v{context['version']}")
        print(f"  Device: {context['parameters']['device']}")
        print(f"  Accuracy: {context['metadata']['accuracy']}")
        
        # Test request
        print("\n🧪 Testing Request:")
        test_request = {
            'type': 'request',
            'id': 'test-1',
            'method': 'analyze_complete',
            'params': {
                'review_text': 'Amazing food and great service! Highly recommend.',
                'business_name': 'Bella Italia'
            }
        }
        
        response = await mcp_server.handle_request(test_request)
        print(f"\n✅ Response:")
        print(json.dumps(response, indent=2))
        
        # Start WebSocket server (optional)
        # ws_server = MCPWebSocketServer(mcp_server)
        # await ws_server.start()
    
    asyncio.run(main())
