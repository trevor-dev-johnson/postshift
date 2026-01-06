import typer
from postshift.services.assessment import assess_energy

app = typer.Typer(help="PostShift — assess what you're actually capable of after a shift.")

@app.command()
def assess(
    hours_slept: float = typer.Option(..., help="Hours slept since last shift"),
    night_shift: bool = typer.Option(False, help="Was the last shift a night shift"),
    hours_since_shift_end: float = typer.Option(..., help="Hours since shift ended"),
    consecutive_shifts: int = typer.Option(1, help="Number of consecutive shifts worked"),
):
    result = assess_energy(
        hours_slept=hours_slept,
        night_shift=night_shift,
        hours_since_shift_end=hours_since_shift_end,
        consecutive_shifts=consecutive_shifts,
    )

    typer.echo(f"Energy state: {result.energy}")

    if result.warning:
        typer.echo(f"⚠ {result.warning}")


if __name__ == "__main__":
    app()
