#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "litellm",
#     "requests>=2.31.0",
#     "tenacity",
#     "markitdown>=0.1.0",
#     "fastapi",
#     "orjson",
# ]
# ///
"""
Consultant CLI - LiteLLM-powered LLM consultation tool
Supports async invocation, custom base URLs, and flexible model selection

Run with: uvx consultant_cli.py [args]
This automatically installs/updates dependencies (litellm, requests) on first run.
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

import config
from file_handler import (
    FileHandler,
    build_multimodal_content,
    build_prompt_with_references,
    has_images,
    validate_vision_support,
)
from litellm_client import LiteLLMClient
from model_selector import ModelSelector
from session_manager import SessionManager


def validate_context_size(
    full_prompt: str, model: str, client: LiteLLMClient, num_files: int
) -> bool:
    """
    Validate that full prompt fits in model context.
    Returns True if OK, raises ValueError if exceeds.
    """

    # Count tokens for the complete prompt
    total_tokens = client.count_tokens(full_prompt, model)

    # Get limit
    max_tokens = client.get_max_tokens(model)

    # Reserve for response
    available_tokens = int(max_tokens * (1 - config.CONTEXT_RESERVE_RATIO))

    # Print summary
    print("\n📊 Token Usage:")
    print(f"- Input: {total_tokens:,} tokens ({num_files} files)")
    print(f"- Limit: {max_tokens:,} tokens")
    print(
        f"- Available: {available_tokens:,} tokens ({int((available_tokens/max_tokens)*100)}%)\n"
    )

    if total_tokens > max_tokens:
        raise ValueError(
            f"Input exceeds context limit!\n"
            f"  Input: {total_tokens:,} tokens\n"
            f"  Limit: {max_tokens:,} tokens\n"
            f"  Overage: {total_tokens - max_tokens:,} tokens\n\n"
            f"Suggestions:\n"
            f"1. Reduce number of files (currently {num_files})\n"
            f"2. Use a model with larger context\n"
            f"3. Shorten the prompt"
        )

    if total_tokens > available_tokens:
        print(f"⚠️  WARNING: Using {int((total_tokens/max_tokens)*100)}% of context")
        print("   Consider reducing input size for better response quality\n")

    return True


def handle_invocation(args: argparse.Namespace) -> int:
    """Handle main invocation command"""

    # Determine base URL: --base-url flag > OPENAI_BASE_URL env var > None
    base_url = args.base_url
    if not base_url:
        base_url = config.get_base_url()
        if base_url:
            print(f"Using base URL from OPENAI_BASE_URL: {base_url}")

    # Initialize components
    session_mgr = SessionManager()
    client = LiteLLMClient(base_url=base_url, api_key=args.api_key)

    # Process files using FileHandler
    file_handler = FileHandler()
    processed_files = []
    multimodal_content = None

    if args.files:
        processed_files, file_errors = file_handler.process_files(args.files)

        # If any files failed, report errors and exit
        if file_errors:
            print("\nERROR: Some files could not be processed:", file=sys.stderr)
            for err in file_errors:
                print(f"  - {err.path}: {err.reason}", file=sys.stderr)
            print(
                "\nPlease fix or remove the problematic files and try again.",
                file=sys.stderr,
            )
            return 1

        # Validate vision support if images present
        if has_images(processed_files):
            validate_vision_support(args.model, has_images=True)

        # Print file processing summary
        text_count = sum(1 for f in processed_files if f.category.value == "text")
        office_count = sum(1 for f in processed_files if f.category.value == "office")
        image_count = sum(1 for f in processed_files if f.category.value == "image")

        print("\nFile Processing Summary:")
        print(f"  - Text files: {text_count}")
        print(f"  - Office documents (converted): {office_count}")
        print(f"  - Images: {image_count}")

    # Log model being used
    print(f"Using model: {args.model}")

    # Validate environment variables (only if no custom base URL)
    if not base_url:
        env_status = client.validate_environment(args.model)
        if not env_status.get("keys_in_environment", False):
            missing = env_status.get("missing_keys", [])
            error = env_status.get("error", "")

            print(
                f"\n❌ ERROR: Missing required environment variables for model '{args.model}'",
                file=sys.stderr,
            )
            print(f"\nMissing keys: {', '.join(missing)}", file=sys.stderr)

            if error:
                print(f"\nDetails: {error}", file=sys.stderr)

            print("\n💡 To fix this:", file=sys.stderr)
            print("   1. Set the required environment variable(s):", file=sys.stderr)
            for key in missing:
                print(f"      export {key}=your-api-key", file=sys.stderr)
            print(
                "   2. Or use --base-url to specify a custom LiteLLM endpoint",
                file=sys.stderr,
            )
            print(
                "   3. Or use --model to specify a different model\n", file=sys.stderr
            )

            return 1

    # Build full prompt with reference files section
    full_prompt = build_prompt_with_references(args.prompt, processed_files)

    # Build multimodal content if we have images
    if has_images(processed_files):
        multimodal_content = build_multimodal_content(full_prompt, processed_files)

    # Check context limits on the full prompt
    try:
        validate_context_size(full_prompt, args.model, client, len(processed_files))
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # Create and start session
    session_id = session_mgr.create_session(
        slug=args.slug,
        prompt=full_prompt,
        model=args.model,
        base_url=base_url,
        api_key=args.api_key,
        reasoning_effort=args.reasoning_effort,
        multimodal_content=multimodal_content,
    )

    print(f"Session created: {session_id}")
    print(f"Reattach via: python3 {__file__} session {args.slug}")
    print("Waiting for completion...")

    try:
        result = session_mgr.wait_for_completion(session_id)

        if result.get("status") == "completed":
            print("\n" + "=" * 80)
            print("RESPONSE:")
            print("=" * 80)
            print(result.get("output", "No output available"))
            print("=" * 80)

            # Print metadata section (model, reasoning effort, tokens, cost)
            print("\n" + "=" * 80)
            print("METADATA:")
            print("=" * 80)

            # Model info
            print(f"model: {result.get('model', args.model)}")
            print(
                f"reasoning_effort: {result.get('reasoning_effort', args.reasoning_effort)}"
            )

            # Token usage and cost
            usage = result.get("usage")
            cost_info = result.get("cost_info")

            if cost_info:
                print(f"input_tokens: {cost_info.get('input_tokens', 0)}")
                print(f"output_tokens: {cost_info.get('output_tokens', 0)}")
                print(
                    f"total_tokens: {cost_info.get('input_tokens', 0) + cost_info.get('output_tokens', 0)}"
                )
                print(f"input_cost_usd: {cost_info.get('input_cost', 0):.6f}")
                print(f"output_cost_usd: {cost_info.get('output_cost', 0):.6f}")
                print(f"total_cost_usd: {cost_info.get('total_cost', 0):.6f}")
            elif usage:
                input_tokens = usage.get("prompt_tokens") or usage.get(
                    "input_tokens", 0
                )
                output_tokens = usage.get("completion_tokens") or usage.get(
                    "output_tokens", 0
                )
                print(f"input_tokens: {input_tokens}")
                print(f"output_tokens: {output_tokens}")
                print(f"total_tokens: {input_tokens + output_tokens}")

            print("=" * 80)

            return 0
        else:
            print(f"\nSession ended with status: {result.get('status')}")
            if "error" in result:
                print(f"Error: {result['error']}")
            return 1

    except TimeoutError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 1


def handle_session_status(args: argparse.Namespace) -> int:
    """Handle session status check"""

    session_mgr = SessionManager()
    status = session_mgr.get_session_status(args.slug)

    if "error" in status and "No session found" in status["error"]:
        print(f"ERROR: {status['error']}", file=sys.stderr)
        return 1

    # Pretty print status
    print(json.dumps(status, indent=2))
    return 0


def handle_list_sessions(args: argparse.Namespace) -> int:
    """Handle list sessions command"""

    session_mgr = SessionManager()
    sessions = session_mgr.list_sessions()

    if not sessions:
        print("No sessions found.")
        return 0

    print(f"\nFound {len(sessions)} session(s):\n")
    for s in sessions:
        status_icon = {
            "running": "🔄",
            "completed": "✅",
            "error": "❌",
            "calling_llm": "📞",
        }.get(s.get("status", ""), "❓")

        print(
            f"{status_icon} {s.get('slug', 'unknown')} - {s.get('status', 'unknown')}"
        )
        print(f"   Created: {s.get('created_at', 'unknown')}")
        print(f"   Model: {s.get('model', 'unknown')}")
        if s.get("error"):
            print(f"   Error: {s['error'][:100]}...")
        print()

    return 0


def handle_list_models(args: argparse.Namespace) -> int:
    """Handle list models command"""

    # Determine base URL: --base-url flag > OPENAI_BASE_URL env var > None
    base_url = args.base_url
    if not base_url:
        base_url = config.get_base_url()
        if base_url:
            print(f"Using base URL from OPENAI_BASE_URL: {base_url}")

    LiteLLMClient(base_url=base_url)
    models = ModelSelector.list_models(base_url)

    print(json.dumps(models, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="""
Consultant CLI - LiteLLM-powered LLM consultation tool

This CLI tool allows you to consult powerful LLM models for code analysis,
reviews, architectural decisions, and complex technical questions. It supports
100+ LLM providers via LiteLLM with custom base URLs.

CORE WORKFLOW:
  1. Provide a prompt describing your analysis task
  2. Attach relevant files for context
  3. The CLI sends everything to the LLM and waits for completion
  4. Results are printed with full metadata (model, tokens, cost)

OUTPUT FORMAT:
  The CLI prints structured output with clear sections:
  - RESPONSE: The LLM's analysis/response
  - METADATA: Model used, reasoning effort, token counts, costs

ENVIRONMENT VARIABLES:
  LITELLM_API_KEY      Primary API key (checked first)
  OPENAI_API_KEY       OpenAI API key (fallback)
  ANTHROPIC_API_KEY    Anthropic API key (fallback)
  OPENAI_BASE_URL      Default base URL for custom LiteLLM proxy
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:

  Basic consultation with prompt and files:
    %(prog)s -p "Review this code for bugs" -f src/main.py -s code-review

  Multiple files:
    %(prog)s -p "Analyze architecture" -f src/api.py -f src/db.py -f src/models.py -s arch-review

  Specify model explicitly:
    %(prog)s -p "Security audit" -f auth.py -s security -m claude-3-5-sonnet-20241022

  Use custom LiteLLM proxy:
    %(prog)s -p "Code review" -f app.py -s review --base-url http://localhost:8000

  Lower reasoning effort (faster, cheaper):
    %(prog)s -p "Quick check" -f code.py -s quick --reasoning-effort low

  Check session status:
    %(prog)s session my-review

  List all sessions:
    %(prog)s list

  List available models from proxy:
    %(prog)s models --base-url http://localhost:8000

SUBCOMMANDS:
  session <slug>    Check status of a session by its slug
  list              List all sessions with their status
  models            List available models (from proxy or known models)

For more information, see the consultant plugin documentation.
""",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Main invocation arguments
    parser.add_argument(
        "-p",
        "--prompt",
        metavar="TEXT",
        help="""The analysis prompt to send to the LLM. This should describe
                what you want the model to analyze or review. The prompt will
                be combined with any attached files to form the full request.
                REQUIRED for main invocation.""",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="append",
        dest="files",
        metavar="PATH",
        help="""File to attach for analysis. Can be specified multiple times
                to attach multiple files. Each file's contents will be included
                in the prompt sent to the LLM. Supports any text file format.
                Example: -f src/main.py -f src/utils.py -f README.md""",
    )
    parser.add_argument(
        "-s",
        "--slug",
        metavar="NAME",
        help="""Unique identifier for this session. Used to track and retrieve
                session results. Should be descriptive (e.g., "pr-review-123",
                "security-audit", "arch-analysis"). REQUIRED for main invocation.""",
    )
    parser.add_argument(
        "-m",
        "--model",
        metavar="MODEL_ID",
        default="gpt-5.2-pro",
        help="""Specific LLM model to use. Default: gpt-5.2-pro. Examples:
                "gpt-5.2", "claude-opus-4-5", "gemini/gemini-2.5-flash".
                Use the "models" subcommand to see available models.""",
    )
    parser.add_argument(
        "--base-url",
        metavar="URL",
        help="""Custom base URL for LiteLLM proxy server (e.g., "http://localhost:8000").
                When set, all API calls go through this proxy. The proxy's /v1/models
                endpoint will be queried for available models. If not set, uses
                direct provider APIs based on the model prefix.""",
    )
    parser.add_argument(
        "--api-key",
        metavar="KEY",
        help="""API key for the LLM provider. If not provided, the CLI will look
                for keys in environment variables: LITELLM_API_KEY, OPENAI_API_KEY,
                or ANTHROPIC_API_KEY (in that order).""",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high", "xhigh"],
        default="xhigh",
        metavar="LEVEL",
        help="""Reasoning effort level for the LLM. Higher effort = more thorough
                analysis but slower and more expensive. Choices: low, medium, high, xhigh.
                Default: xhigh. Use "low" for quick checks, "xhigh" for most thorough analysis.""",
    )

    # Session status subcommand
    session_parser = subparsers.add_parser(
        "session",
        help="Check the status of a session",
        description="""Check the current status of a consultation session.
                       Returns JSON with session metadata, status, and output if completed.""",
    )
    session_parser.add_argument(
        "slug", help="Session slug/identifier to check (the value passed to -s/--slug)"
    )

    # List sessions subcommand
    subparsers.add_parser(
        "list",
        help="List all consultation sessions",
        description="""List all consultation sessions with their status.
                       Shows session slug, status, creation time, model used, and any errors.""",
    )

    # List models subcommand
    models_parser = subparsers.add_parser(
        "models",
        help="List available LLM models",
        description="""List available LLM models. If --base-url is provided, queries
                       the proxy's /v1/models endpoint. Otherwise, returns known models
                       from LiteLLM's model registry.""",
    )
    models_parser.add_argument(
        "--base-url",
        metavar="URL",
        help="Base URL of LiteLLM proxy to query for available models",
    )

    args = parser.parse_args()

    # Handle commands
    if args.command == "session":
        return handle_session_status(args)

    elif args.command == "list":
        return handle_list_sessions(args)

    elif args.command == "models":
        return handle_list_models(args)

    else:
        # Main invocation
        if not args.prompt or not args.slug:
            parser.print_help()
            print("\nERROR: --prompt and --slug are required", file=sys.stderr)
            return 1

        return handle_invocation(args)


if __name__ == "__main__":
    sys.exit(main())
