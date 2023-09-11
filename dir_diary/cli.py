from .summarize import summarize_project_folder
import click

@click.command()
@click.option('--startpath', default=".", type=click.Path(), help='Path to the project folder.')
@click.option('--destination', default="docs", type=click.Path(), help='Destination folder for the generated files.')
@click.option('--include', default=["source", "utility scripts"], type=click.Choice([
                    "source", "configuration", "build or deployment",
                    "documentation", "testing", "database", "utility scripts",
                    "assets or data", "specialized"
                ]), multiple=True, help='Types of files to include.')
@click.option('--summary_types', default=["pseudocode"], type=click.Choice(["pseudocode", "usage", "tech stack"]), multiple=True, help='Types of summaries to generate.')
@click.option('--api_key', default=None, type=str, help='API key for OpenAI.')
@click.option('--model_name', default="gpt-3.5-turbo", type=click.Choice([
                    'gpt-3.5-turbo', 'gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613',
                    'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613', 'gpt-4',
                    'gpt-4-0314', 'gpt-4-0613'
                ]), help='Name of the OpenAI model.')
@click.option('--long_context_fallback', default="gpt-3.5-turbo-16k", type=click.Choice([
                    'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613'
                ]), help='Fallback model for long context.')
@click.option('--temperature', default=0, type=float, help='Temperature for the OpenAI model.')
def cli(startpath: str, destination: str, summary_types: list[str], include: list[str], api_key: str, model_name: str, long_context_fallback: str, temperature: float) -> None:
    """Summarize a project folder using pseudocode."""
    summarize_project_folder(
        startpath=startpath, 
        destination=destination,
        summary_types=summary_types,
        include=include,
        api_key=api_key, 
        model_name=model_name, 
        long_context_fallback=long_context_fallback, 
        temperature=temperature
    )
