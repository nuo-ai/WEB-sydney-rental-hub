## Brief overview
This rule file defines the specific guidelines for using shadcn components in the Sydney Rental Hub project. These rules ensure consistent usage of the shadcn UI library through the MCP server integration.

## Usage Rule
- When asked to use shadcn components, always use the MCP server to retrieve component code and demos
- Never manually write shadcn component code from memory
- Always verify component implementation through MCP-provided examples

## Planning Rule
- When asked to plan using anything related to shadcn:
  - Use the MCP server during planning phase to explore available components
  - Apply components wherever components are applicable in the design
  - Use whole blocks where possible (e.g., login page, calendar, dashboard sections)
  - Research component capabilities and limitations before finalizing plans

## Implementation Rule
- When implementing shadcn components:
  - First call the demo tool to see how the component is used
  - Study the demo code to understand proper implementation patterns
  - Then implement it so that it is implemented correctly
  - Ensure all required dependencies are properly installed
  - Follow the exact usage patterns shown in the demo code