import re

def read_sql_file(file_path):
    """Read SQL file and return its content."""
    with open(file_path, 'r') as file:
        return file.read()

def write_sql_file(file_path, content):
    """Write content to an SQL file."""
    with open(file_path, 'w') as file:
        file.write(content)

def replace_schema_names(content, replacements):

    def replacement_function(match):
        full_match = match.group(0)
        schema_name = match.group(1)
        if schema_name in replacements:
            return full_match.replace(schema_name, replacements[schema_name])
        return full_match

    pattern = re.compile(r'\[([^\]]+)\]\.')

    content = pattern.sub(replacement_function, content)

    pattern_simple_string = re.compile(r"'(\[?[^\]]+\])\.(?![^\]]+\])'")

    content = pattern_simple_string.sub(replacement_function, content)

    return content

def main():
    original_file_path = 'original.sql'
    new_file_path = 'modified.sql'

    sql_content = read_sql_file(original_file_path)

    replacements = {
        'Schema1': 'NewSchema1',
        'Schema2': 'NewSchema2'
    }

    modified_content = replace_schema_names(sql_content, replacements)

    write_sql_file(new_file_path, modified_content)
    print(f"Modified SQL file has been created at: {new_file_path}")

if __name__ == '__main__':
    main()