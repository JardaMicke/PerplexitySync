def build_prompt(file_type, user_instruction, project_context, coding_guidelines):
    return f"""[INST] Generate {file_type} code for: {user_instruction}\nContext: {project_context}\nStyle guide: {coding_guidelines} [/INST]"""
