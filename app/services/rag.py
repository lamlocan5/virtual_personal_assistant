from typing import Optional
import logging
from openai import AsyncOpenAI
import yaml
from pathlib import Path

logger = logging.getLogger('app')

class RAGService:
    def __init__(self):
        # Load configuration
        config_path = Path('config/config.yaml')
        with config_path.open() as f:
            self.config = yaml.safe_load(f)
        
        # Initialize OpenAI client
        self.client = AsyncOpenAI(
            api_key=self.config['services']['openai']['api_key']
        )

    async def process_question(
        self,
        question: str,
        context: Optional[str] = None
    ) -> str:
        """
        Process a question using RAG (Retrieval Augmented Generation)
        """
        try:
            # Demo implementation - In practice, this would include:
            # 1. Vector search for relevant context
            # 2. Prompt engineering with context
            # 3. LLM call for answer generation
            
            system_prompt = "You are a helpful assistant with access to context."
            user_prompt = f"Question: {question}\nContext: {context if context else 'No additional context provided'}"
            
            response = await self.client.chat.completions.create(
                model=self.config['services']['openai']['model'],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in RAG processing: {str(e)}")
            raise Exception("Failed to process question")

    async def update_knowledge_base(self, new_data: str) -> bool:
        """
        Update the knowledge base with new information
        """
        # Demo implementation - would typically update vector store
        logger.info("Knowledge base update requested")
        return True