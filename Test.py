import openai
import os
from pathlib import Path

class DocumentationGenerator:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.model = "gpt-3.5-turbo"
        self.template = {
            "system_message": "You are a technical documentation expert. Generate clear, concise, and comprehensive documentation.",
            "documentation_format": """
            # {filename} Documentation

            ## Overview
            {overview}

            ## Functions
            {functions}

            ## Usage Examples
            {examples}

            ## Dependencies
            {dependencies}
            """,
            "prompt_template": """Please provide detailed documentation for the following Python code.
            Follow this structure:
            1. Brief overview of the code's purpose
            2. Detailed function descriptions including:
               - Parameters and their types
               - Return values and types
               - Any exceptions raised
            3. Practical usage examples
            4. List of dependencies and requirements
            
            Code to document:
            {code_content}
            """
        }

    def generate_documentation(self, file_path):
        """Generate documentation for a Python file using OpenAI."""
        # Read the Python file
        with open(file_path, 'r') as file:
            code_content = file.read()

        # Create the prompt using template
        prompt = self.template["prompt_template"].format(
            code_content=code_content
        )

        try:
            # Make the API call
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.template["system_message"]},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # Add some creativity but keep it professional
                max_tokens=2000,  # Adjust based on your needs
                top_p=0.95,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            # Extract the documentation
            documentation = response.choices[0].message.content

            # Format the documentation using the template
            formatted_doc = self.template["documentation_format"].format(
                filename=Path(file_path).stem,
                overview="",  # These will be filled by the AI response
                functions="",
                examples="",
                dependencies=""
            )

            # Create markdown file path
            md_path = Path(file_path).with_suffix('.md')

            # Write documentation to markdown file
            with open(md_path, 'w') as md_file:
                md_file.write(documentation)

            return f"Documentation generated successfully: {md_path}"

        except Exception as e:
            return f"Error generating documentation: {str(e)}"

    def update_template(self, new_template):
        """
        Update the documentation template.
        
        Args:
            new_template (dict): New template with keys to update
        """
        self.template.update(new_template)

def main():
    # Get OpenAI API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    # Initialize the documentation generator
    doc_gen = DocumentationGenerator(api_key)

    # Example of updating the template (optional)
    # custom_template = {
    #     "system_message": "Your custom system message",
    #     "documentation_format": "Your custom format"
    # }
    # doc_gen.update_template(custom_template)

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
