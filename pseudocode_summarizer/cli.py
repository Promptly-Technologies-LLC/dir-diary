from .summarize import summarize_project_folder
import click

@click.command()
@click.option('--startpath', default=".", help='Path to the project folder.')
@click.option('--pseudocode_file', default="pseudocode/pseudocode.md", help='Path to the pseudocode file.')
@click.option('--project_map_file', default="pseudocode/project_map.json", help='Path to the project map file.')
@click.option('--include', default=["source", "utility scripts"], multiple=True, help='Types of files to include.')
@click.option('--api_key', default=None, help='API key for OpenAI.')
@click.option('--model_name', default="gpt-3.5-turbo", help='Name of the OpenAI model.')
@click.option('--long_context_fallback', default="gpt-3.5-turbo-16k", help='Fallback model for long context.')
@click.option('--temperature', default=0, help='Temperature for the OpenAI model.')
def cli(startpath, pseudocode_file, project_map_file, include, api_key, model_name, long_context_fallback, temperature) -> None:
    """Summarize a project folder using pseudocode."""
    summarize_project_folder(startpath=startpath, pseudocode_file=pseudocode_file, project_map_file=project_map_file, include=include, api_key=api_key, model_name=model_name, long_context_fallback=long_context_fallback, temperature=temperature)