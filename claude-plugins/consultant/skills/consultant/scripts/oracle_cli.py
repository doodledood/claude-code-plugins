#!/usr/bin/env python3
"""
Oracle CLI - In-house implementation using LiteLLM
Supports async invocation, custom base URLs, and flexible model selection
"""

import sys
import argparse
import json
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

import config
from session_manager import SessionManager
from litellm_client import LiteLLMClient
from model_selector import ModelSelector


def validate_context_size(
    prompt: str,
    files: list,
    model: str,
    client: LiteLLMClient
) -> bool:
    """
    Validate that prompt + files fit in model context.
    Returns True if OK, raises ValueError if exceeds.
    """

    # Count tokens
    prompt_tokens = client.count_tokens(prompt, model)
    file_tokens = sum(f.get("tokens", 0) for f in files)
    total_tokens = prompt_tokens + file_tokens

    # Get limit
    max_tokens = client.get_max_tokens(model)

    # Reserve for response
    available_tokens = int(max_tokens * (1 - config.CONTEXT_RESERVE_RATIO))

    # Print summary
    print(f"\n📊 Token Usage:")
    print(f"- Prompt: {prompt_tokens:,} tokens")
    print(f"- Files: {file_tokens:,} tokens ({len(files)} files)")
    print(f"- Total: {total_tokens:,} tokens")
    print(f"- Limit: {max_tokens:,} tokens")
    print(f"- Available: {available_tokens:,} tokens ({int((available_tokens/max_tokens)*100)}%)\n")

    if total_tokens > max_tokens:
        raise ValueError(
            f"Input exceeds context limit!\n"
            f"  Input: {total_tokens:,} tokens\n"
            f"  Limit: {max_tokens:,} tokens\n"
            f"  Overage: {total_tokens - max_tokens:,} tokens\n\n"
            f"Suggestions:\n"
            f"1. Reduce number of files (currently {len(files)})\n"
            f"2. Use a model with larger context\n"
            f"3. Shorten the prompt"
        )

    if total_tokens > available_tokens:
        print(f"⚠️  WARNING: Using {int((total_tokens/max_tokens)*100)}% of context")
        print(f"   Consider reducing input size for better response quality\n")

    return True


def handle_invocation(args):
    """Handle main invocation command"""

    # Determine base URL: --base-url flag > OPENAI_BASE_URL env var > None
    base_url = args.base_url
    if not base_url:
        base_url = config.get_base_url()
        if base_url:
            print(f"Using base URL from OPENAI_BASE_URL: {base_url}")

    # Initialize components
    session_mgr = SessionManager()
    client = LiteLLMClient(
        base_url=base_url,
        api_key=args.api_key
    )

    # Validate and prepare files
    file_contents = []
    total_tokens = 0

    if args.files:
        for file_path in args.files:
            path = Path(file_path)
            if not path.exists():
                print(f"ERROR: File not found: {file_path}", file=sys.stderr)
                return 1

            if not path.is_file():
                print(f"ERROR: Not a file: {file_path}", file=sys.stderr)
                return 1

            try:
                content = path.read_text()
            except Exception as e:
                print(f"ERROR: Could not read {file_path}: {e}", file=sys.stderr)
                return 1

            tokens = client.count_tokens(content, args.model or config.DEFAULT_MODEL)
            file_contents.append({
                "path": str(file_path),
                "content": content,
                "tokens": tokens
            })
            total_tokens += tokens

    # Determine model
    if not args.model:
        print("No model specified. Discovering available models...")
        args.model = ModelSelector.select_best_model(base_url)
        print(f"Selected model: {args.model}")

    # Check context limits
    try:
        validate_context_size(args.prompt, file_contents, args.model, client)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # Create and start session
    session_id = session_mgr.create_session(
        slug=args.slug,
        prompt=args.prompt,
        files=file_contents,
        model=args.model,
        base_url=base_url,
        api_key=args.api_key
    )

    print(f"Session created: {session_id}")
    print(f"Reattach via: python3 {__file__} session {args.slug}")

    if args.wait:
        print("Waiting for completion...")
        try:
            result = session_mgr.wait_for_completion(session_id)

            if result.get("status") == "completed":
                print("\n" + "="*80)
                print(result.get("output", "No output available"))
                print("="*80)
                return 0
            else:
                print(f"\nSession ended with status: {result.get('status')}")
                if "error" in result:
                    print(f"Error: {result['error']}")
                return 1

        except TimeoutError as e:
            print(f"\nERROR: {e}", file=sys.stderr)
            return 1
    else:
        print("Session running in background.")

    return 0


def handle_session_status(args):
    """Handle session status check"""

    session_mgr = SessionManager()
    status = session_mgr.get_session_status(args.slug)

    if "error" in status and "No session found" in status["error"]:
        print(f"ERROR: {status['error']}", file=sys.stderr)
        return 1

    # Pretty print status
    print(json.dumps(status, indent=2))
    return 0


def handle_list_sessions(args):
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
            "calling_llm": "📞"
        }.get(s.get("status", ""), "❓")

        print(f"{status_icon} {s.get('slug', 'unknown')} - {s.get('status', 'unknown')}")
        print(f"   Created: {s.get('created_at', 'unknown')}")
        print(f"   Model: {s.get('model', 'unknown')}")
        if s.get("error"):
            print(f"   Error: {s['error'][:100]}...")
        print()

    return 0


def handle_list_models(args):
    """Handle list models command"""

    # Determine base URL: --base-url flag > OPENAI_BASE_URL env var > None
    base_url = args.base_url
    if not base_url:
        base_url = config.get_base_url()
        if base_url:
            print(f"Using base URL from OPENAI_BASE_URL: {base_url}")

    client = LiteLLMClient(base_url=base_url)
    models = ModelSelector.list_models(base_url)

    print(json.dumps(models, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Oracle CLI - LiteLLM-powered code analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start a consultation (runs in background)
  %(prog)s --prompt "Analyze this code" --file src/*.py --slug "review"

  # Wait for completion (blocking)
  %(prog)s --prompt "..." --file ... --slug "..." --wait

  # Check session status
  %(prog)s session review

  # List all sessions
  %(prog)s list

  # List available models
  %(prog)s models --base-url http://localhost:8000
"""
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Main invocation (default if no subcommand)
    parser.add_argument("-p", "--prompt", help="Analysis prompt")
    parser.add_argument("-f", "--file", action="append", dest="files",
                       help="Files to attach (can specify multiple times)")
    parser.add_argument("-s", "--slug", help="Session identifier")
    parser.add_argument("-m", "--model", help="Specific model to use")
    parser.add_argument("--base-url", help="Custom base URL for LiteLLM")
    parser.add_argument("--api-key", help="API key for the provider")
    parser.add_argument("--wait", action="store_true",
                       help="Wait for completion (blocking)")

    # Session status
    session_parser = subparsers.add_parser("session", help="Check session status")
    session_parser.add_argument("slug", help="Session slug to check")

    # List sessions
    list_parser = subparsers.add_parser("list", help="List all sessions")

    # List models
    models_parser = subparsers.add_parser("models", help="List available models")
    models_parser.add_argument("--base-url", help="Base URL to query models from")

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
