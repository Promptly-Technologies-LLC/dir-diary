from .summarize import summarize_project_folder
import click

@click.command()
@click.option('--startpath', default=".", type=click.Path(), help='Path to the project folder.')
@click.option('--pseudocode_file', default="docs/pseudocode.md", type=click.Path(), help='Path to the pseudocode file.')
@click.option('--project_map_file', default="docs/project_map.json", type=click.Path(), help='Path to the project map file.')
@click.option('--include', default=["source", "utility scripts"], type=click.Choice([
                    "source", "configuration", "build or deployment",
                    "documentation", "testing", "database", "utility scripts",
                    "assets or data", "specialized"
                ]), multiple=True, help='Types of files to include.')
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
def cli(startpath: str, pseudocode_file: str, project_map_file: str, include: list[str], api_key: str, model_name: str, long_context_fallback: str, temperature: float) -> None:
    """Summarize a project folder using pseudocode."""
    summarize_project_folder(
        startpath=startpath, 
        pseudocode_file=pseudocode_file, 
        project_map_file=project_map_file, 
        include=include,
        api_key=api_key, 
        model_name=model_name, 
        long_context_fallback=long_context_fallback, 
        temperature=temperature
    )
