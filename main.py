import requests
import json
import random
import logging
import time


def setup_logger(log_file):
    logger = logging.getLogger("GraphQLFuzzer")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def send_query(query, url, headers):
    try:
        response = requests.post(
            url, json={"query": query}, headers=headers, timeout=10
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def discover_schema(url, headers, logger):
    introspection_query = """
    {
      __schema {
        queryType { name }
        mutationType { name }
        types {
          name
          fields {
            name
          }
        }
      }
    }
    """
    schema_response = send_query(introspection_query, url, headers)
    if "errors" in schema_response:
        logger.error(f"Failed to discover schema: {schema_response['errors']}")
    else:
        logger.info("Schema discovery successful.")
    return schema_response


def generate_query(schema, depth=1):
    types = schema["data"]["__schema"]["types"]
    random_type = random.choice(types)

    query = f'{{ {random_type["name"]} {{ '
    for _ in range(depth):
        random_field = random.choice(random_type.get("fields", []))
        if random_field:
            query += f'{random_field["name"]} '
    query += "} }}"

    return query


def fuzz_query(query):
    mutations = ['"', "'", ";", "{}", "[]", "null", "true", "false", "123456789"]
    fuzzed_query = query + random.choice(mutations)
    return fuzzed_query


def process_response(query, response, start_time, logger):
    duration = time.time() - start_time
    response_type = "valid" if "data" in response else "error"

    if "errors" in response:
        logger.error(f"Error in response: {response['errors']}")
        response_type = "error"
    else:
        logger.info(f"Valid response received.")

    logger.debug(
        {
            "query": query,
            "response_type": response_type,
            "response_time": duration,
            "response": response,
        }
    )

    print(
        f"\nQuery: {query}\nType: {response_type}\nTime: {duration}s\nResponse: {response}\n"
    )


def fuzz_graphql(url, headers, iterations=10, depth=1, log_file="fuzz_results.log"):
    logger = setup_logger(log_file)

    logger.info("Starting schema discovery...")
    schema = discover_schema(url, headers, logger)
    if "errors" in schema:
        logger.error("Schema discovery failed. Exiting fuzzing process.")
        return

    logger.info(f"Starting fuzzing with {iterations} iterations.")

    for i in range(iterations):
        query = generate_query(schema, depth)
        logger.info(f"Generated Query {i+1}: {query}")

        fuzzed_query = fuzz_query(query)
        logger.info(f"Fuzzed Query {i+1}: {fuzzed_query}")

        start_time = time.time()
        response = send_query(fuzzed_query, url, headers)

        process_response(fuzzed_query, response, start_time, logger)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GraphQL Fuzzing Tool with Logging")
    parser.add_argument("--url", required=True, help="GraphQL endpoint URL")
    parser.add_argument(
        "--token", required=False, help="Bearer token for authentication"
    )
    parser.add_argument(
        "--iterations", type=int, default=10, help="Number of fuzzing iterations"
    )
    parser.add_argument(
        "--depth", type=int, default=1, help="Depth of generated queries"
    )
    parser.add_argument(
        "--log", type=str, default="fuzz_results.log", help="File to log responses"
    )

    args = parser.parse_args()

    headers = {}
    if args.token:
        headers["Authorization"] = f"Bearer {args.token}"

    fuzz_graphql(args.url, headers, args.iterations, args.depth, args.log)
