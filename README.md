
# GraphQL Fuzzing Tool

## Introduction
This GraphQL fuzzing tool is designed to test GraphQL APIs for potential vulnerabilities by sending randomly generated and fuzzed queries. It utilizes Python and provides a structured logging system to monitor responses and errors.

## Features
- Discover GraphQL schema using introspection.
- Generate random queries based on schema.
- Fuzz queries by introducing random mutations.
- Log results with response times and details.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/graphql-fuzzing-tool.git
   ```
   
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   The `requirements.txt` file should contain:
   ```
   requests
   ```

## Usage
1. Basic Fuzzing:
   ```
   python fuzz_tool.py --url https://example.com/graphql --token your_api_token
   ```

2. Options:
   - `--iterations`: Number of fuzzing iterations to perform (default: 10).
   - `--depth`: Max depth of the generated queries.
   - `--log`: Option to log the responses to a file.

   Example:
   ```
   python fuzz_tool.py --url https://example.com/graphql --iterations 20 --log fuzz_log.txt
   ```

## Logging
The tool logs the following:
- Query sent.
- Response time.
- Response type (valid/error).
- Full response content.

## Notes
- Ensure you have permission to fuzz the GraphQL endpoint.
- Only use this tool for ethical testing.
