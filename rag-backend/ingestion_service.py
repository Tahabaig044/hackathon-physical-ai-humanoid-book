import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any
import aiofiles

from rag_service import rag_service
from qdrant_service import qdrant_service

class IngestionService:
    def __init__(self):
        self.supported_extensions = {'.md', '.txt', '.html', '.rst'}

    async def ingest_from_directory(self, directory_path: str, recursive: bool = True) -> Dict[str, Any]:
        """
        Ingest all supported documents from a directory
        """
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            return {"error": f"Directory does not exist: {directory_path}"}

        # Find all supported files
        files_to_process = []
        if recursive:
            for ext in self.supported_extensions:
                files_to_process.extend(directory.rglob(f"*{ext}"))
        else:
            for ext in self.supported_extensions:
                files_to_process.extend(directory.glob(f"*{ext}"))

        # Process each file
        documents = []
        for file_path in files_to_process:
            try:
                content = await self._read_file(file_path)
                if content:
                    # Extract module and chapter from path
                    relative_path = file_path.relative_to(directory)
                    path_parts = str(relative_path).split('/')

                    # Default values
                    module = "unknown"
                    chapter = "unknown"

                    # Try to extract module and chapter from path
                    if len(path_parts) >= 2:
                        for part in path_parts:
                            if part.startswith('module'):
                                module = part
                                break
                        # Chapter is typically the filename without extension
                        chapter = file_path.stem

                    documents.append({
                        "title": file_path.name,
                        "content": content,
                        "source": str(relative_path),
                        "module": module,
                        "chapter": chapter
                    })
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")

        # Ingest all documents
        result = await rag_service.batch_ingest_documents(documents)
        return result

    async def _read_file(self, file_path: Path) -> str:
        """
        Read content from a file
        """
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()

                # For markdown files, we might want to extract just the content
                # Remove frontmatter if it exists
                if file_path.suffix.lower() == '.md':
                    content = self._extract_markdown_content(content)

                return content
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return ""

    def _extract_markdown_content(self, content: str) -> str:
        """
        Extract content from markdown, potentially removing frontmatter
        """
        lines = content.split('\n')

        # Check if there's frontmatter (starts and ends with ---)
        if len(lines) > 1 and lines[0].strip() == '---':
            # Find the end of frontmatter
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    # Return content after frontmatter
                    return '\n'.join(lines[i+1:])

        # If no frontmatter, return all content
        return content

    async def setup_document_collection(self):
        """
        Create the document collection in Qdrant if it doesn't exist
        """
        try:
            # Create collection with appropriate vector size for text embeddings
            # Using OpenAI's text-embedding-ada-002 which produces 1536-dimensional vectors
            qdrant_service.create_collection("textbook_documents", vector_size=1536)
            logging.info("Document collection set up successfully")
            return True
        except Exception as e:
            logging.error(f"Error setting up document collection: {e}")
            return False

    async def ingest_docusaurus_docs(self, docusaurus_docs_path: str) -> Dict[str, Any]:
        """
        Specialized method to ingest Docusaurus documentation
        """
        # First ensure the collection exists
        await self.setup_document_collection()

        # Process the Docusaurus docs directory
        result = await self.ingest_from_directory(docusaurus_docs_path)

        return result

# Create a global instance
ingestion_service = IngestionService()