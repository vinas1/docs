CRITICAL OVERRIDE FOR TOOL CALLS:
You MUST NOT output code changes, file edits, or completed steps as plain conversational text or markdown blocks inside the chat.

When making file modifications, you MUST format your output strictly using Anthropic-style XML tool tags as expected by Cline:

<replace_in_file>
<path>relative/path/to/file.ext</path>
<diff>
<<<<<<< SEARCH
code to find
=======
code to replace
>>>>>>> REPLACE
</diff>
</replace_in_file>

Or to write a file completely:

<write_to_file>
<path>relative/path/to/file.ext</path>
<content>
file contents here
</content>
</write_to_file>

Always output the raw tool XML tags so Cline can parse and apply the changes to the file system automatically.