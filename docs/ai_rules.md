You are a senior AI Software Architect.

Your task is to create a file named `ai_rules.md`.

This document is NOT intended for human developers.
It is intended exclusively for AI models (ChatGPT, Claude, Gemini, DeepSeek Reasoner, etc.) that will generate, modify, or review this project's code.

The document must contain strict rules that every AI model must follow before generating any code.

Include the following sections.

1. Purpose
- Explain that this document is the highest-level instruction for AI.
- State that all other project documentation must be interpreted according to this file.

2. Documentation Reading Order
Specify the exact order in which every AI model must read project documentation before writing code.

For example:

1. ai_rules.md
2. project_overview.md
3. frontend_rules.md
4. telegram_guidelines.md
5. ui_style.md
6. components.md
7. animations.md
8. design_tokens.json
9. assets_description.md

The AI must never skip any document.

3. Documentation Priority

If multiple documents conflict, specify which one has higher priority.

4. Required Workflow

Describe the complete workflow that every AI model must follow before writing code.

For example:

- Read all documentation.
- Analyze project architecture.
- Analyze available assets.
- Analyze design tokens.
- Search existing components.
- Search existing hooks.
- Search existing stores.
- Search existing utilities.
- Reuse existing implementations whenever possible.
- Only create new code when no reusable implementation exists.
- Validate generated code against all project documentation.

5. Reuse Policy

The AI must:

- Prefer existing components.
- Prefer existing hooks.
- Prefer existing stores.
- Prefer existing utilities.
- Prefer composition over duplication.
- Never duplicate business logic.

6. Code Generation Rules

Describe strict requirements.

Examples:

- Never generate dead code.
- Never generate unused components.
- Never generate unused imports.
- Never hardcode colors.
- Never hardcode spacing.
- Never hardcode typography.
- Always use design tokens.
- Always follow the project's architecture.

7. Assets Rules

The AI must:

- Analyze assets_description.md before generating UI.
- Reuse existing artistic style.
- Never invent a new visual style.
- Never ignore available assets.
- Use assets as the primary inspiration for all new illustrations and UI.

8. Telegram Mini App Rules

Describe rules such as:

- Always use Telegram WebApp API correctly.
- Respect Safe Area.
- Support dark/light themes.
- Optimize for mobile.
- Keep animations lightweight.

9. Error Handling

If required information is missing:

- Never invent APIs.
- Never invent routes.
- Never invent database fields.
- Never invent backend behavior.
- Never invent assets.
- Ask for clarification.
- Use TODO only when appropriate.

10. AI Safety Rules

The AI must never:

- Change architecture.
- Rename folders.
- Rename components.
- Rename APIs.
- Modify documentation without request.
- Remove functionality.
- Introduce breaking changes.

11. Performance Rules

Always:

- Optimize rendering.
- Minimize bundle size.
- Lazy-load large assets.
- Memoize expensive calculations.
- Avoid unnecessary re-renders.

12. Code Quality Checklist

Before finishing any task the AI must verify:

✓ Documentation followed
✓ Existing code reused
✓ No duplicated logic
✓ No hardcoded values
✓ Correct TypeScript types
✓ Responsive layout
✓ Telegram compatibility
✓ Accessibility considered
✓ Performance optimized

13. Final Rule

State that this document overrides the AI's default assumptions.

If project documentation exists, the AI must always trust project documentation over its own assumptions.

Write the entire document in professional Markdown.

Use headings, lists, warning blocks, notes, examples and checklists.

The resulting document should be suitable for long-term use in a professional software project and should maximize consistency across different AI models.