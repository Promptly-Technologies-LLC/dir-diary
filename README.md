# pseudocode_summarizer

## Description



## To-do

- [ ] Write README
- [ ] Create a Github Action to run this on every commit
- [ ] Add tech stack summarization
- [ ] Add usage summarization
- [ ] Add support for LLMs other than OpenAI's

## Ideas

Instead of having separate `ProjectFile` and `FileClassification` data types, have a single class with `modified` and `role` both as optional fields. And instead of a `FileClassificationList` class, I could simplify in the pydantic parser as `[FileClassification]` and convert the `to_json` method to a function that takes a list of `FileClassification` objects. This would require removing the `files` attribute in the list comprehension in `classify_files`. However, this might still cause `modified` to show up in our JSON serialization, filling our LLM context with useless tokens.

Do I want to experiment with YAML instead of JSON to keep context length down?