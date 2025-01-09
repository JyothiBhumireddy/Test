import openai
import os
from pathlib import Path

class DocumentationGenerator:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.model = "gpt-3.5-turbo"

    def generate_documentation(self, file_path):
        """Generate documentation for a Python file using OpenAI."""
        # Read the Python file
        with open(file_path, 'r') as file:
            code_content = file.read()

        # Create the prompt for OpenAI
        prompt = f"""Please provide detailed documentation for the following Python code. 
        Include:
        - Overview of the code
        - Function descriptions
        - Parameters and return values
        - Usage examples
        
        Code:
        {code_content}
        """

        try:
            # Make the API call
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical documentation expert."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the documentation
            documentation = response.choices[0].message.content

            # Create markdown file path
            md_path = Path(file_path).with_suffix('.md')

            # Write documentation to markdown file
            with open(md_path, 'w') as md_file:
                md_file.write(documentation)

            return f"Documentation generated successfully: {md_path}"

        except Exception as e:
            return f"Error generating documentation: {str(e)}"

def main():
    # Get OpenAI API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    # Initialize the documentation generator
    doc_gen = DocumentationGenerator(api_key)

    # Get list of files from user input
    print("Enter the paths of Python files to document (one per line)")
    print("Press Enter twice to start processing")
    
    files_to_process = []
    while True:
        file_path = input().strip()
        if not file_path:
            break
        if not file_path.endswith('.py'):
            print(f"Warning: {file_path} is not a Python file. Skipping...")
            continue
        if not Path(file_path).exists():
            print(f"Warning: {file_path} does not exist. Skipping...")
            continue
        files_to_process.append(file_path)

    if not files_to_process:
        print("No valid files to process.")
        return

    # Process each specified file
    for file_path in files_to_process:
        print(f"\nProcessing {file_path}...")
        result = doc_gen.generate_documentation(file_path)
        print(result)

if __name__ == "__main__":
    main()
