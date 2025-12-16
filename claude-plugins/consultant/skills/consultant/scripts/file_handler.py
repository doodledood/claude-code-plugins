"""
File handling for consultant CLI.
Categorizes and processes files: images, office documents, and text files.
"""

import base64
import mimetypes
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from markitdown import MarkItDown


class FileCategory(Enum):
    """Categories of files the CLI can handle"""

    IMAGE = "image"
    OFFICE = "office"
    TEXT = "text"


@dataclass
class ProcessedFile:
    """Result of successfully processing a file"""

    path: str
    category: FileCategory
    content: str = ""  # For text/office: the text content
    base64_data: str = ""  # For images: base64 encoded data
    mime_type: str = ""  # For images: the MIME type


@dataclass
class FileError:
    """Error details for a file that failed processing"""

    path: str
    reason: str


# File extension constants
IMAGE_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp"})
OFFICE_EXTENSIONS = frozenset({".xls", ".xlsx", ".docx", ".pptx"})

# Size limits
MAX_IMAGE_SIZE_BYTES = 20 * 1024 * 1024  # 20MB


class FileHandler:
    """Main file processing coordinator"""

    def __init__(self) -> None:
        self._markitdown = MarkItDown()

    def process_files(
        self, file_paths: list[str]
    ) -> tuple[list[ProcessedFile], list[FileError]]:
        """
        Process a list of file paths and return categorized results.

        Returns:
            Tuple of (successfully processed files, errors)
        """
        processed: list[ProcessedFile] = []
        errors: list[FileError] = []

        for file_path in file_paths:
            path = Path(file_path)

            # Validate file exists
            if not path.exists():
                errors.append(FileError(path=str(path), reason="File not found"))
                continue

            if not path.is_file():
                errors.append(FileError(path=str(path), reason="Not a file"))
                continue

            # Categorize and process
            category = self._categorize(path)

            if category == FileCategory.IMAGE:
                result = self._process_image(path)
            elif category == FileCategory.OFFICE:
                result = self._process_office(path)
            else:  # FileCategory.TEXT
                result = self._process_text(path)

            if isinstance(result, FileError):
                errors.append(result)
            else:
                processed.append(result)

        return processed, errors

    def _categorize(self, path: Path) -> FileCategory:
        """Determine the category of a file based on extension"""
        suffix = path.suffix.lower()

        if suffix in IMAGE_EXTENSIONS:
            return FileCategory.IMAGE

        if suffix in OFFICE_EXTENSIONS:
            return FileCategory.OFFICE

        # Default: assume text, will validate during processing
        return FileCategory.TEXT

    def _process_image(self, path: Path) -> ProcessedFile | FileError:
        """Process an image file: validate size and encode to base64"""
        try:
            # Read binary content
            data = path.read_bytes()

            # Check size limit
            if len(data) > MAX_IMAGE_SIZE_BYTES:
                size_mb = len(data) / (1024 * 1024)
                max_mb = MAX_IMAGE_SIZE_BYTES / (1024 * 1024)
                return FileError(
                    path=str(path),
                    reason=f"Image too large: {size_mb:.1f}MB (max {max_mb:.0f}MB)",
                )

            # Encode to base64
            base64_data = base64.b64encode(data).decode("utf-8")

            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(str(path))
            if not mime_type:
                # Fallback based on extension
                ext = path.suffix.lower()
                mime_map = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".gif": "image/gif",
                    ".webp": "image/webp",
                }
                mime_type = mime_map.get(ext, "application/octet-stream")

            return ProcessedFile(
                path=str(path),
                category=FileCategory.IMAGE,
                base64_data=base64_data,
                mime_type=mime_type,
            )
        except Exception as e:
            return FileError(path=str(path), reason=f"Failed to process image: {e}")

    def _process_office(self, path: Path) -> ProcessedFile | FileError:
        """Process an office document using markitdown"""
        try:
            result = self._markitdown.convert(str(path))
            content = result.text_content

            if not content or not content.strip():
                return FileError(
                    path=str(path), reason="markitdown returned empty content"
                )

            return ProcessedFile(
                path=str(path),
                category=FileCategory.OFFICE,
                content=content,
            )
        except Exception as e:
            return FileError(
                path=str(path), reason=f"markitdown conversion failed: {e}"
            )

    def _process_text(self, path: Path) -> ProcessedFile | FileError:
        """Process a text file: attempt UTF-8 decode"""
        try:
            content = path.read_text(encoding="utf-8")

            # Check for empty or whitespace-only files
            if not content or not content.strip():
                return FileError(
                    path=str(path),
                    reason="File is empty or contains only whitespace",
                )

            return ProcessedFile(
                path=str(path),
                category=FileCategory.TEXT,
                content=content,
            )
        except UnicodeDecodeError as e:
            return FileError(
                path=str(path),
                reason=f"Not a valid UTF-8 text file: {e}",
            )
        except Exception as e:
            return FileError(path=str(path), reason=f"Failed to read file: {e}")


def validate_vision_support(model: str, has_images: bool) -> None:
    """
    Validate that the model supports vision if images are present.
    Exits with code 2 if validation fails.
    """
    if not has_images:
        return

    from litellm import supports_vision

    if not supports_vision(model=model):
        print(
            f"\nERROR: Model '{model}' does not support vision/images.\n",
            file=sys.stderr,
        )
        print(
            "Image files were provided but the selected model cannot process them.",
            file=sys.stderr,
        )
        print("\nSuggestions:", file=sys.stderr)
        print("  1. Use a vision-capable model:", file=sys.stderr)
        print("     - gpt-5.2, gpt-5-vision (OpenAI)", file=sys.stderr)
        print(
            "     - claude-opus-4-5, claude-opus-4 (Anthropic)",
            file=sys.stderr,
        )
        print(
            "     - gemini/gemini-2.5-flash, gemini/gemini-3-pro-preview (Google)",
            file=sys.stderr,
        )
        print("  2. Remove image files from the request", file=sys.stderr)
        print("  3. Convert images to text descriptions first\n", file=sys.stderr)
        sys.exit(2)


def build_prompt_with_references(prompt: str, files: list[ProcessedFile]) -> str:
    """
    Build the text portion of the prompt with Reference Files section.
    Does NOT include images (those go in the multimodal array).

    Args:
        prompt: The user's original prompt
        files: List of successfully processed files

    Returns:
        The full prompt with reference files section appended
    """
    # Filter to text and office files only (images handled separately)
    text_content_files = [
        f for f in files if f.category in (FileCategory.TEXT, FileCategory.OFFICE)
    ]

    # Also get image files for the note
    image_files = [f for f in files if f.category == FileCategory.IMAGE]

    if not text_content_files and not image_files:
        return prompt

    parts = [prompt]

    # Add reference files section if there are text/office files
    if text_content_files:
        parts.append("\n\n" + "=" * 80)
        parts.append("\n\n## Reference Files\n")

        for file in text_content_files:
            parts.append(f"\n### {file.path}\n")
            parts.append(f"```\n{file.content}\n```\n")

    # Add note about images if present
    if image_files:
        parts.append("\n\n" + "-" * 40)
        parts.append(
            f"\n*Note: {len(image_files)} image(s) attached for visual analysis.*\n"
        )
        for img in image_files:
            parts.append(f"- {img.path}\n")

    return "".join(parts)


def build_multimodal_content(
    text_prompt: str, files: list[ProcessedFile]
) -> list[dict[str, Any]]:
    """
    Build multimodal content array for LLM APIs.

    Uses the standard OpenAI Chat Completions format which is widely supported.
    Response strategies will convert to API-specific formats as needed.

    Format:
    - Text: {"type": "text", "text": "..."}
    - Image: {"type": "image_url", "image_url": {"url": "data:...", "detail": "auto"}}

    Args:
        text_prompt: The text portion of the prompt (with reference files)
        files: List of successfully processed files

    Returns:
        Multimodal content array
    """
    content: list[dict[str, Any]] = []

    # Text content
    content.append({"type": "text", "text": text_prompt})

    # Images with base64 data URLs
    for f in files:
        if f.category == FileCategory.IMAGE:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{f.mime_type};base64,{f.base64_data}",
                        "detail": "auto",
                    },
                }
            )

    return content


def has_images(files: list[ProcessedFile]) -> bool:
    """Check if any processed files are images"""
    return any(f.category == FileCategory.IMAGE for f in files)
