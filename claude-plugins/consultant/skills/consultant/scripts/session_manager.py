"""
Session management for async consultant executions
Handles background processes, session persistence, and status tracking
"""

import builtins
import contextlib
import json
import multiprocessing
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import config


class SessionManager:
    """Manages consultant sessions with async execution"""

    def __init__(self, sessions_dir: Path | None = None) -> None:
        self.sessions_dir = sessions_dir or config.DEFAULT_SESSIONS_DIR
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def create_session(
        self,
        slug: str,
        prompt: str,
        model: str,
        base_url: str | None = None,
        api_key: str | None = None,
        reasoning_effort: str = "xhigh",
        multimodal_content: list[dict[str, Any]] | None = None,
    ) -> str:
        """Create a new session and start background execution"""

        session_id = f"{slug}-{int(time.time())}"
        session_dir = self.sessions_dir / session_id
        session_dir.mkdir(exist_ok=True)

        # Save session metadata
        metadata = {
            "id": session_id,
            "slug": slug,
            "created_at": datetime.now().isoformat(),
            "status": "running",
            "model": model,
            "base_url": base_url,
            "reasoning_effort": reasoning_effort,
            "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "has_images": multimodal_content is not None,
        }

        metadata_file = session_dir / "metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))

        # Save full prompt
        prompt_file = session_dir / "prompt.txt"
        prompt_file.write_text(prompt)

        # Start background process
        process = multiprocessing.Process(
            target=self._execute_session,
            args=(
                session_id,
                prompt,
                model,
                base_url,
                api_key,
                reasoning_effort,
                multimodal_content,
            ),
        )
        process.start()

        # Store PID for potential cleanup
        (session_dir / "pid").write_text(str(process.pid))

        return session_id

    def _execute_session(
        self,
        session_id: str,
        prompt: str,
        model: str,
        base_url: str | None,
        api_key: str | None,
        reasoning_effort: str = "xhigh",
        multimodal_content: list[dict[str, Any]] | None = None,
    ) -> None:
        """Background execution of LLM consultation"""

        session_dir = self.sessions_dir / session_id

        try:
            # Import here to avoid issues with multiprocessing
            from litellm_client import LiteLLMClient

            # Initialize client
            client = LiteLLMClient(base_url=base_url, api_key=api_key)

            # Make LLM call with the full prompt (already includes file contents)
            self._update_status(session_id, "calling_llm")

            # Get full response (pass session_dir for resumability support)
            result = client.complete(
                model=model,
                prompt=prompt,
                session_dir=session_dir,  # Enables background job resumption if supported
                reasoning_effort=reasoning_effort,
                multimodal_content=multimodal_content,
            )

            full_response = result.get("content", "")
            usage = result.get("usage")
            response_obj = result.get(
                "response"
            )  # Full response object for cost calculation

            # Save response to file
            output_file = session_dir / "output.txt"
            output_file.write_text(full_response)

            # Calculate cost using response object (preferred) or usage dict (fallback)
            cost_info = None
            if response_obj or usage:
                cost_info = client.calculate_cost(
                    model, response=response_obj, usage=usage
                )

            # Update metadata with usage and cost
            self._update_status(
                session_id,
                "completed",
                response=full_response,
                usage=usage,
                cost_info=cost_info,
                reasoning_effort=reasoning_effort,
            )

        except Exception as e:
            error_msg = f"Error: {str(e)}\n\nType: {type(e).__name__}"
            (session_dir / "error.txt").write_text(error_msg)
            self._update_status(session_id, "error", error=error_msg)

    def _update_status(
        self,
        session_id: str,
        status: str,
        response: str | None = None,
        error: str | None = None,
        usage: dict[str, Any] | None = None,
        cost_info: dict[str, Any] | None = None,
        reasoning_effort: str | None = None,
    ) -> None:
        """Update session status in metadata"""

        session_dir = self.sessions_dir / session_id
        metadata_file = session_dir / "metadata.json"

        if not metadata_file.exists():
            return

        metadata = json.loads(metadata_file.read_text())
        metadata["status"] = status
        metadata["updated_at"] = datetime.now().isoformat()

        if response:
            metadata["completed_at"] = datetime.now().isoformat()
            metadata["output_length"] = len(response)

        if error:
            metadata["error"] = error[:500]  # Truncate long errors

        if usage:
            metadata["usage"] = usage

        if cost_info:
            metadata["cost_info"] = cost_info

        if reasoning_effort:
            metadata["reasoning_effort"] = reasoning_effort

        metadata_file.write_text(json.dumps(metadata, indent=2))

    def get_session_status(self, slug: str) -> dict[str, Any]:
        """Get current status of a session by slug"""

        # Find most recent session with this slug
        matching_sessions = sorted(
            [
                d
                for d in self.sessions_dir.iterdir()
                if d.is_dir() and d.name.startswith(slug)
            ],
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )

        if not matching_sessions:
            return {"error": f"No session found with slug: {slug}"}

        session_dir = matching_sessions[0]
        metadata_file = session_dir / "metadata.json"

        if not metadata_file.exists():
            return {"error": f"Session metadata not found: {slug}"}

        metadata: dict[str, Any] = json.loads(metadata_file.read_text())

        # Add output if completed
        if metadata["status"] == "completed":
            output_file = session_dir / "output.txt"
            if output_file.exists():
                metadata["output"] = output_file.read_text()

        # Add error if failed
        if metadata["status"] == "error":
            error_file = session_dir / "error.txt"
            if error_file.exists():
                metadata["error_details"] = error_file.read_text()

        return metadata

    def wait_for_completion(
        self, session_id: str, timeout: int = 3600
    ) -> dict[str, Any]:
        """Block until session completes or timeout"""

        start_time = time.time()

        while time.time() - start_time < timeout:
            session_dir = self.sessions_dir / session_id
            metadata_file = session_dir / "metadata.json"

            if not metadata_file.exists():
                time.sleep(1)
                continue

            metadata: dict[str, Any] = json.loads(metadata_file.read_text())

            if metadata["status"] in ["completed", "error"]:
                # Add output if completed
                if metadata["status"] == "completed":
                    output_file = session_dir / "output.txt"
                    if output_file.exists():
                        metadata["output"] = output_file.read_text()

                # Add error if failed
                if metadata["status"] == "error":
                    error_file = session_dir / "error.txt"
                    if error_file.exists():
                        metadata["error_details"] = error_file.read_text()

                return metadata

            time.sleep(config.POLLING_INTERVAL_SECONDS)

        raise TimeoutError(f"Session {session_id} did not complete within {timeout}s")

    def list_sessions(self) -> list[dict[str, Any]]:
        """List all sessions"""

        sessions = []
        for session_dir in self.sessions_dir.iterdir():
            if not session_dir.is_dir():
                continue

            metadata_file = session_dir / "metadata.json"
            if metadata_file.exists():
                with contextlib.suppress(builtins.BaseException):
                    sessions.append(json.loads(metadata_file.read_text()))

        return sorted(sessions, key=lambda x: x.get("created_at", ""), reverse=True)
