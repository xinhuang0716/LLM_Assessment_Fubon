from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


def display_scores_table(all_scores: dict[str, dict]) -> None:
    """Display BBQ evaluation results with rich formatting.
    
    Args:
        all_scores (dict[str, dict]): Dictionary mapping bias types to their scores.
    """
    console = Console()
    
    # Header
    console.print(Panel.fit("[bold cyan]🎯 BBQ Bias Benchmark Evaluation[/bold cyan]", border_style="cyan"))
    console.print()

    # Create results table
    table = Table(
        title="📊 Bias Type Results",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Bias Type", style="cyan", no_wrap=True)
    table.add_column("Total", justify="right", style="white")
    table.add_column("Correct", justify="right", style="green")
    table.add_column("Incorrect", justify="right", style="red")
    table.add_column("Failed Format", justify="right", style="yellow")
    table.add_column("Accuracy", justify="right", style="bold blue")

    # Add rows for each bias type
    for bias_type, scores in all_scores.items():
        accuracy = scores["accuracy"]
        if accuracy >= 0.8:
            accuracy_str = f"[bold green]{accuracy:.2%}[/bold green]"
        elif accuracy >= 0.6:
            accuracy_str = f"[yellow]{accuracy:.2%}[/yellow]"
        else:
            accuracy_str = f"[bold red]{accuracy:.2%}[/bold red]"

        table.add_row(
            bias_type.replace("_", " "),
            str(scores["total_num"]),
            str(scores["correct_num"]),
            str(scores["incorrect_num"]),
            str(scores["failed_format_num"]),
            accuracy_str,
        )

    console.print(table)
    console.print()


def display_overall_scores(overall_scores: dict) -> None:
    """Display overall BBQ scores with rich formatting.
    
    Args:
        overall_scores (dict): Dictionary containing overall scoring metrics.
    """
    console = Console()
    
    overall_accuracy = overall_scores["accuracy"]
    if overall_accuracy >= 0.8:
        emoji = "🎉"
        color = "green"
    elif overall_accuracy >= 0.6:
        emoji = "👍"
        color = "yellow"
    else:
        emoji = "⚠️"
        color = "red"

    overall_panel = Panel(
        f"[bold]Total:[/bold] {overall_scores['total_num']}\n"
        f"[bold green]Correct:[/bold green] {overall_scores['correct_num']}\n"
        f"[bold red]Incorrect:[/bold red] {overall_scores['incorrect_num']}\n"
        f"[bold yellow]Failed Format:[/bold yellow] {overall_scores['failed_format_num']}\n"
        f"[bold {color}]Accuracy:[/bold {color}] {overall_accuracy:.2%} {emoji}",
        title="[bold cyan]📈 Overall BBQ Scores[/bold cyan]",
        border_style=color,
        box=box.DOUBLE,
    )
    console.print(overall_panel)
