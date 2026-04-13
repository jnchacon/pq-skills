# PQ Skills agents instructions

## General Instructions

- Always respond in the same language as the user.
- Always write the skill in english.
- Always write the evals in english.

## Skill Authoring Best Practices

When creating or modifying skills in this repository, rigidly adhere to these best practices derived from official guides:

1. **Naming & Metadata**: Folders and `name` must be `kebab-case`. The `description` field MUST clearly state BOTH *what* the skill does and *when* to invoke it (trigger phrases). Do not use XML tags (`< >`) in descriptions.
2. **Progressive Disclosure**: Keep `SKILL.md` concise. Complex background docs belong in `references/` and formatting templates in `assets/`. Instruct the LLM to read them only when needed.
3. **Workflow Orchestration**: For complex goals, use sequential steps (`--# Step 1: ...`, `--# Step 2: ...`) with validation gates to prevent the agent from rushing the process.
4. **Domain-Specific Expert Intelligence**: Don't execute tools blindly. Add domain expert warnings before execution (e.g. check for engineering safety rules or best practices) to inform the user.
5. **Deterministic Execution**: Delegate complex logic, rendering, or mathematical calculations to executable scripts (e.g. `scripts/*.py`). The LLM should act merely as a bridge to execute them and format the data.
6. **Strict Error Handling**: Always include a `--# Troubleshooting` section outlining what to do when a script fails.
7. **Focused Scope**: Build one skill per clear workflow. Do not merge fundamentally different tasks into one massive skill file.
8. **Constraint Enforcements**: If the skill strictly requires text-only output or specific formatting (e.g. `do not generate images`), explicitly instruct the agent via a `**STRICT CONSTRAINT:**` or `**STRICT RULE:**` block.

## Evals

Siempre que se cree una nueva skill, se debe crear un archivo en la carpeta `evals` con el siguiente formato:

```json
{
  "skill_name": "<nombre_de_la_skill>",
  "evals": [
    {
      "id": 1,
      "prompt": "<prompt>",
      "expected_output": "<expected_output>",
      "files": []
    }
  ]
}
```
