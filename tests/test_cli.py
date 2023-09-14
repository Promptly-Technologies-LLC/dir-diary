from click.testing import CliRunner
from dir_diary.cli import cli


def test_cli_entry_point(mocker) -> None:
    # Since the import of cli has already imported summarize_project_folder
    # into the dir_diary.cli namespace, we need to mock it in that namespace
    mock_summarize = mocker.patch('dir_diary.cli.summarize_project_folder', return_value=None)

    print(f"Mock object: {mock_summarize}")
    
    # Run the CLI command
    runner = CliRunner()
    result = runner.invoke(cli=cli, args=[
        '--startpath', '.', 
        '--destination', 'docs',
        '--include', 'source',
        '--include', 'utility scripts',
        '--summary_types', 'pseudocode',
        '--api_key', 'some_key',
        '--model_name', 'gpt-3.5-turbo',
        '--long_context_fallback', 'gpt-3.5-turbo-16k',
        '--temperature', '0'
    ])

    # Check that the CLI command succeeded
    assert result.exit_code == 0

    # Check that summarize_project_folder was called with the expected arguments
    mock_summarize.assert_called_once_with(
        startpath='.',
        destination='docs',
        summary_types=('pseudocode',),
        include=('source', 'utility scripts'),
        api_key='some_key',
        model_name='gpt-3.5-turbo',
        long_context_fallback='gpt-3.5-turbo-16k',
        temperature=0
    )
