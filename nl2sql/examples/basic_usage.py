"""
Basic usage examples for the NL2SQL package.
"""

import os
from dotenv import load_dotenv
from nl2sql import NL2SQL

# Load environment variables
load_dotenv()

def main():
    """Basic usage examples."""
    
    # Database connection (example with SQLite)
    database_url = "sqlite:///example.db"
    
    # Initialize with OpenAI
    with NL2SQL(
        database_url=database_url,
        llm_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4"
    ) as nl2sql:
        
        # Example 1: Simple query
        print("=== Example 1: Simple Query ===")
        result = nl2sql.ask("Show me all customers from New York")
        print(f"Question: {result['question']}")
        print(f"Generated SQL: {result['sql_query']}")
        if result['results'] is not None:
            print(f"Results:\n{result['results']}")
        if result['error']:
            print(f"Error: {result['error']}")
        
        print("\n" + "="*50 + "\n")
        
        # Example 2: Query with explanation
        print("=== Example 2: Query with Explanation ===")
        result = nl2sql.ask(
            "What are the top 5 products by sales?",
            explain=True
        )
        print(f"Question: {result['question']}")
        print(f"Generated SQL: {result['sql_query']}")
        print(f"Explanation: {result['explanation']}")
        if result['results'] is not None:
            print(f"Results:\n{result['results']}")
        
        print("\n" + "="*50 + "\n")
        
        # Example 3: Query without execution (SQL generation only)
        print("=== Example 3: SQL Generation Only ===")
        result = nl2sql.ask(
            "Calculate average order value by customer",
            execute=False,
            explain=True
        )
        print(f"Question: {result['question']}")
        print(f"Generated SQL: {result['sql_query']}")
        print(f"Explanation: {result['explanation']}")
        
        print("\n" + "="*50 + "\n")
        
        # Example 4: Direct SQL execution
        print("=== Example 4: Direct SQL Execution ===")
        custom_sql = "SELECT COUNT(*) as total_records FROM customers"
        try:
            results = nl2sql.execute_sql(custom_sql)
            print(f"SQL: {custom_sql}")
            print(f"Results:\n{results}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Example 5: Schema exploration
        print("=== Example 5: Schema Information ===")
        tables = nl2sql.get_tables()
        print(f"Available tables: {tables}")
        
        # Get schema info (first 500 characters)
        schema_info = nl2sql.get_schema_info()
        print(f"Schema info preview:\n{schema_info[:500]}...")

def example_with_different_providers():
    """Examples using different LLM providers."""
    
    database_url = "sqlite:///example.db"
    
    # Example with Cohere
    print("=== Using Cohere Provider ===")
    try:
        with NL2SQL(
            database_url=database_url,
            llm_provider="cohere",
            api_key=os.getenv("COHERE_API_KEY")
        ) as nl2sql_cohere:
            
            result = nl2sql_cohere.ask("Show me customers who made orders in the last month")
            print(f"Cohere SQL: {result['sql_query']}")
    except Exception as e:
        print(f"Cohere example failed: {e}")
    
    print("\n" + "="*30 + "\n")
    
    # Example with Anthropic
    print("=== Using Anthropic Provider ===")
    try:
        with NL2SQL(
            database_url=database_url,
            llm_provider="anthropic",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        ) as nl2sql_anthropic:
            
            result = nl2sql_anthropic.ask("What's the revenue trend by month?")
            print(f"Anthropic SQL: {result['sql_query']}")
    except Exception as e:
        print(f"Anthropic example failed: {e}")

def advanced_usage_example():
    """Advanced usage examples with custom configurations."""
    
    database_url = "postgresql://user:pass@localhost/mydb"
    
    with NL2SQL(
        database_url=database_url,
        llm_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4",
        temperature=0.1,
        max_tokens=800
    ) as nl2sql:
        
        # Complex query example
        complex_question = """
        I want to see the monthly revenue trend for the last 6 months, 
        broken down by product category, and only include categories 
        that had more than $10,000 in total sales.
        """
        
        result = nl2sql.ask(
            complex_question,
            explain=True,
            validate=True,
            temperature=0.05  # Override default temperature for this query
        )
        
        print(f"Complex Question: {complex_question}")
        print(f"Generated SQL: {result['sql_query']}")
        print(f"Explanation: {result['explanation']}")
        
        if result['error']:
            print(f"Error: {result['error']}")
        elif result['results'] is not None:
            print(f"Results shape: {result['results'].shape}")
            print(f"First few results:\n{result['results'].head()}")

if __name__ == "__main__":
    main()
    print("\n" + "="*60 + "\n")
    example_with_different_providers()
    print("\n" + "="*60 + "\n")
    advanced_usage_example()
