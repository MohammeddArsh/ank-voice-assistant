import json
import csv
import os
import time
import io
from datetime import datetime


class SessionLogger:
    """
    Logs each conversation session for research and analysis.
    Tracks turns, response times, and session metadata.
    Supports export as JSON and CSV.
    """

    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_start = time.time()
        self.turns = []
        self.log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(self.log_dir, exist_ok=True)

    def log_turn(self, user_text: str, assistant_reply: str, response_time_ms: float):
        self.turns.append({
            "turn": len(self.turns) + 1,
            "timestamp": datetime.now().isoformat(),
            "user": user_text,
            "assistant": assistant_reply,
            "response_time_ms": round(response_time_ms, 2)
        })

    def get_analytics(self) -> dict:
        if not self.turns:
            return {}
        response_times = [t["response_time_ms"] for t in self.turns]
        return {
            "session_id": self.session_id,
            "session_duration_s": round(time.time() - self.session_start, 2),
            "total_turns": len(self.turns),
            "avg_response_time_ms": round(sum(response_times) / len(response_times), 2),
            "min_response_time_ms": round(min(response_times), 2),
            "max_response_time_ms": round(max(response_times), 2),
        }

    def export_json(self) -> str:
        """Returns session data as a JSON string."""
        data = {
            "metadata": self.get_analytics(),
            "turns": self.turns
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def export_csv(self) -> str:
        """Returns session turns as a CSV string."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["turn", "timestamp", "user", "assistant", "response_time_ms"])
        writer.writeheader()
        writer.writerows(self.turns)
        return output.getvalue()

    def save(self):
        if not self.turns:
            return
        path = os.path.join(self.log_dir, f"session_{self.session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.export_json())
        print(f"Session saved to {path}")

    def reset(self):
        self.save()
        self.__init__()