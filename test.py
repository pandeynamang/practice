import re


class SchemaReplacer:
    def __init__(self, source_schema, target_schema):
        self.SourceSchema = source_schema
        self.TargetSchema = target_schema

    def replace_schema_names(self, files):
        """
        Replaces source schema names with target schema and performs case-sensitive replacements for specific strings.

        Parameters:
        files (dict): Dictionary where keys are file path and values are file contents

        Returns:
        dict: Dictionary with updated file contents.
        """
        updated_files = {}

        for file_name, content in files.items():
            schema_names = self.getSchemasFromSQLScript(content)
            updated_content = content

            # Replace schema names
            for schema_name in schema_names:
                updated_schema = schema_name.replace(self.SourceSchema, self.TargetSchema)
                updated_content = re.sub(r'\b' + re.escape(schema_name) + r'\b', updated_schema, updated_content)

            # Perform additional replacements for standalone strings
            updated_content = self.case_sensitive_replace(updated_content, 'SIT2', 'UAT2')
            updated_content = self.case_sensitive_replace(updated_content, 'sit2', 'uat2')

            updated_files[file_name] = updated_content

        return updated_files

    def getSchemasFromSQLScript(self, s):
        """
        Parses and extracts schema names using regex.

        Args:
        s (string): Script for parsing

        Returns:
        list: List of schema names
        """
        sqlScript = s.replace("[", "").replace("]", "")  # remove chars '[]' for regex parsing
        p = re.compile(r'(\w+[-]\w+)', re.IGNORECASE)
        resplist = p.findall(sqlScript)
        SchemasList = []

        for item in resplist:
            parts = item.split(".")
            if len(parts) == 2:  # schema.table - 2 part format
                # handle dups
                if item.split(".")[0] not in SchemasList:
                    SchemasList.append(item.split(".")[0])
            elif len(parts) == 3:  # db.schema.table - 3 part format
                if item.split(".")[1] not in SchemasList:  # handle dups
                    SchemasList.append(item.split(".")[1])

        # remove system schemas
        for sch in ['dbo', 'INFORMATION_SCHEMA', 'sys', 'sysdiag', 'DBO', 'information_schema', 'SYS', 'guest']:
            if sch in SchemasList:
                SchemasList.remove(sch)

        return SchemasList

    def case_sensitive_replace(self, text, old, new):
        """
        Replaces all occurrences of 'old' with 'new' in 'text', case-sensitively.

        Args:
        text (string): The text to perform replacements on.
        old (string): The string to be replaced.
        new (string): The string to replace with.

        Returns:
        string: The updated text with replacements.
        """
        pattern = re.compile(re.escape(old))
        return pattern.sub(new, text)


# Example usage:
files = {
    'example.sql': """
    CREATE PROCEDURE 'SIT2_abc' AS
    BEGIN
        SELECT sa.* FROM [uat2_qnext].[sefe_table1 sa]
        INNER JOIN [uat2_testsit].[qefe_sit2_abc] sa2
        ON sa.id = sa2.id
    END;
    """
}

replacer = SchemaReplacer('source_schema', 'target_schema')
updated_files = replacer.replace_schema_names(files)
for file_name, content in updated_files.items():
    print(f"Updated content of {file_name}:\n{content}")
