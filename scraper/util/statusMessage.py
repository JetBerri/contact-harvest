# logger.py

from datetime import datetime
from enum import Enum

from rich.console import Console

console = Console()

class MsgType(Enum):

    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    INFO = "INFO"


_STYLES: dict[MsgType, tuple[str, str]] = {
    MsgType.ERROR: ("bold red", "[ERROR]  "),
    MsgType.SUCCESS: ("bold green", "[SUCCESS]"),
    MsgType.WARNING: ("bold yellow", "[WARNING]"),
    MsgType.INFO: ("bold cyan", "[INFO]   "),
}

def print_log_msg(msg_type: MsgType, message: str) -> None:

    style, label = _STYLES[msg_type]
    timestamp = datetime.now().strftime("%H:%M:%S")

    console.print(f"[dim]{timestamp}[/dim]  [{style}]{label}[/{style}]  {message}")