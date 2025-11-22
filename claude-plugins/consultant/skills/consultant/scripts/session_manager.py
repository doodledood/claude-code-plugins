"""
Session management for async oracle executions
Handles background processes, session persistence, and status tracking
"""

import json
import time
import multiprocessing
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

import config


class SessionManager:
    """Manages oracle consultation sessions with async execution"""

    def __init__(self, sessions_dir: Optional[Path] = None):
        self.sessions_dir = sessions_dir or config.DEFAULT_SESSIONS_DIR
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def create_session(
        self,
        slug: str,
        prompt: str,
        model: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None
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
            "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt
        }

        metadata_file = session_dir / "metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))

        # Save full prompt
        prompt_file = session_dir / "prompt.txt"
        prompt_file.write_text(prompt)

        # Start background process
        process = multiprocessing.Process(
            target=self._execute_session,
            args=(session_id, prompt, model, base_url, api_key)
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
        base_url: Optional[str],
        api_key: Optional[str]
    ):
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
                session_dir=session_dir  # Enables background job resumption if supported
            )

            full_response = result.get("content", "")
            usage = result.get("usage")

            # Save response to file
            output_file = session_dir / "output.txt"
            output_file.write_text(full_response)

            # Calculate cost if usage info available
            cost_info = None
            if usage:
                cost_info = client.calculate_cost(model, usage)

            # Update metadata with usage and cost
            self._update_status(
                session_id,
                "completed",
                response=full_response,
                usage=usage,
                cost_info=cost_info
            )

        except Exception as e:
            error_msg = f"Error: {str(e)}\n\nType: {type(e).__name__}"
            (session_dir / "error.txt").write_text(error_msg)
            self._update_status(session_id, "error", error=error_msg)

    def _update_status(
        self,
        session_id: str,
        status: str,
        response: Optional[str] = None,
        error: Optional[str] = None,
        usage: Optional[Dict] = None,
        cost_info: Optional[Dict] = None
    ):
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

        metadata_file.write_text(json.dumps(metadata, indent=2))

    def get_session_status(self, slug: str) -> Dict:
        """Get current status of a session by slug"""

        # Find most recent session with this slug
        matching_sessions = sorted(
            [d for d in self.sessions_dir.iterdir()
             if d.is_dir() and d.name.startswith(slug)],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        if not matching_sessions:
            return {"error": f"No session found with slug: {slug}"}

        session_dir = matching_sessions[0]
        metadata_file = session_dir / "metadata.json"

        if not metadata_file.exists():
            return {"error": f"Session metadata not found: {slug}"}

        metadata = json.loads(metadata_file.read_text())

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

    def wait_for_completion(self, session_id: str, timeout: int = 3600):
        """Block until session completes or timeout"""

        start_time = time.time()

        while time.time() - start_time < timeout:
            session_dir = self.sessions_dir / session_id
            metadata_file = session_dir / "metadata.json"

            if not metadata_file.exists():
                time.sleep(1)
                continue

            metadata = json.loads(metadata_file.read_text())

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

    def list_sessions(self) -> List[Dict]:
        """List all sessions"""

        sessions = []
        for session_dir in self.sessions_dir.iterdir():
            if not session_dir.is_dir():
                continue

            metadata_file = session_dir / "metadata.json"
            if metadata_file.exists():
                try:
                    sessions.append(json.loads(metadata_file.read_text()))
                except:
                    pass

        return sorted(sessions, key=lambda x: x.get("created_at", ""), reverse=True)
