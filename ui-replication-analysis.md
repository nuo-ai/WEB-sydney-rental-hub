# Workflow: UI Component Replication via Code-Level Analysis

This workflow provides a systematic process for comparing a local UI component against a reference implementation (e.g., a production website) to identify and document all structural and stylistic differences.

## Pre-requisites
- A running local development server for the component being analyzed.
- A URL to the reference implementation.
- The `playwright` MCP server must be available.

---

## Phase 1: Data-driven Standard Extraction (Reference)

1.  **Identify Target URL**: State the URL of the reference website.
    ```xml
    <ask_followup_question>
    <question>Please provide the URL of the reference website containing the component to analyze.</question>
    </ask_followup_question>
    ```
2.  **Navigate and Trigger Component**: Use browser tools to navigate to the page and perform any actions needed to make the target component visible (e.g., click a button to open a modal or panel).
    ```xml
    <use_mcp_tool>
    <server_name>playwright</server_name>
    <tool_name>browser_navigate</tool_name>
    <arguments>
    {
      "url": "[URL from previous step]"
    }
    </arguments>
    </use_mcp_tool>
    <!-- Follow-up with browser_click if needed to expose the element -->
    ```
3.  **Execute Analysis Script**: Run a `browser_evaluate` script to extract the component's DOM structure and computed CSS styles into a structured JSON object. This provides a precise, data-driven snapshot of the target.
    ```xml
    <use_mcp_tool>
    <server_name>playwright</server_name>
    <tool_name>browser_evaluate</tool_name>
    <arguments>
    {
      "function": "async (selector) => { const element = document.querySelector(selector); if (!element) return null; const style = window.getComputedStyle(element); const styleJSON = {}; for (const prop of style) { styleJSON[prop] = style.getPropertyValue(prop); } return { tagName: element.tagName, innerHTML: element.innerHTML, computedStyle: styleJSON }; }",
      "element": "The target UI component on the reference page",
      "ref": "[CSS selector for the reference component]"
    }
    </arguments>
    </use_mcp_tool>
    ```
    *Note: The resulting JSON data will be stored internally as the "reference standard".*

---

## Phase 2: Data-driven Implementation Analysis (Local)

1.  **Identify Local URL**: State the URL of the local development server.
    ```xml
    <ask_followup_question>
    <question>Please provide the URL of your local development server (e.g., http://localhost:5174).</question>
    </ask_followup_question>
    ```
2.  **Navigate and Trigger Component**: Repeat the process from Phase 1 on the local application.
3.  **Execute Analysis Script**: Run the **exact same** `browser_evaluate` script on the local component to extract its data for comparison.

---

## Phase 3: Automated Gap Analysis

1.  **Load Data**: Internally load the JSON data from both the reference standard and the local implementation.
2.  **Compare Data**: Systematically compare the two JSON objects, identifying all discrepancies in:
    *   HTML structure (`tagName`, `innerHTML` differences).
    *   Computed CSS styles (mismatched properties like `box-shadow`, `border-radius`, `color`, etc.).
3.  **Generate Report**: Create a detailed, human-readable report in Markdown format summarizing all identified gaps, presented in a clear table.

---

## Phase 4: Precision Action Plan

1.  **Create Todo List**: Based on the gap analysis report, create a detailed checklist of actionable development tasks.
2.  **Request Approval**: Present the final action plan to the user for approval before switching to `ACT MODE` to implement the changes.
    ```xml
    <ask_followup_question>
    <question>I have completed the UI analysis and generated a detailed action plan. Please review the plan above. Shall I proceed with implementing these changes?</question>
    <options>["Yes, proceed with the plan.", "No, let's discuss some changes."]</options>
    </ask_followup_question>
