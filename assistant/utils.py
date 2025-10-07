from rich.console import Console
from datetime import datetime

console = Console()

def log(message, level="info"):
    colors = {
        "info": "cyan",
        "success": "green",
        "warning": "yellow",
        "error": "red"
    }
    console.print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}", style=colors.get(level, "white"))

