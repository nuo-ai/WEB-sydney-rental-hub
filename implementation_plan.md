# Implementation Plan

[Overview]
This plan will comprehensively fix the incorrect display of property inspection times by creating a robust, centralized date utility function and refactoring the `PropertyDetail.vue` component to use it, ensuring all date and time formats are parsed and displayed correctly.

The core issue is that the current `parseInspectionTime` helper function inside `PropertyDetail.vue` is insufficient. It fails to handle the variety of inconsistent string formats for inspection times provided by the backend API, such as "Thursday Details", "21 Aug Details", and "5:00pm - 5:15pm Details". This results in the garbled UI you screenshotted. The solution is to centralize this parsing logic into a new, more powerful utility file, making it reusable and easier to maintain, while also simplifying the `PropertyDetail.vue` component.

[Types]
This implementation will introduce a new structured type for a parsed inspection time.

```typescript
// Defines the structured object for a parsed inspection time.
interface ParsedInspectionTime {
  date: string; // The formatted date part, e.g., "Thursday, 21 Aug"
  time: string; // The formatted time part, e.g., "5:00pm - 5:15pm" or "By Appointment"
}
```

[Files]
This plan involves creating one new file and modifying one existing file.

- **New File:** `vue-frontend/src/utils/inspectionTimeParser.js`
  - **Purpose:** To house the new, robust `parseInspectionTime` function. This centralizes the complex parsing logic, removing it from the component level and making it reusable for any other component that might need to parse inspection times in the future.

- **Modified File:** `vue-frontend/src/views/PropertyDetail.vue`
  - **Purpose:** To remove the now-obsolete local `parseInspectionTime` helper function and instead import and use the new centralized parser from `inspectionTimeParser.js`. This will simplify the component's script section and ensure it relies on the new, more reliable parsing logic.

- **Deleted File:** `vue-frontend/src/utils/dateUtils.js` was already deleted in a previous step, and this plan correctly avoids re-introducing it, instead creating a new, more specific utility.

[Functions]
This plan will create one new function and modify two existing computed properties.

- **New Function:** `parseInspectionTime(timeStr: string): ParsedInspectionTime`
  - **File Path:** `vue-frontend/src/utils/inspectionTimeParser.js`
  - **Purpose:** This function will be the core of the solution. It will take a raw inspection time string as input and use a series of regular expressions and conditional checks to robustly parse it into a `ParsedInspectionTime` object. It will correctly handle formats like "Day Date Mon", "Time-range", "By Appointment", and lone day/date strings by pairing them with appropriate defaults like "Details".

- **Modified Function:** `inspectionTimes()` (Computed Property)
  - **File Path:** `vue-frontend/src/views/PropertyDetail.vue`
  - **Changes:** The implementation will be simplified to a single `map` operation that calls the new `parseInspectionTime` utility for each raw time string. All complex inline parsing logic will be removed.

- **Modified Function:** `nextInspectionTime()` (Computed Property)
  - **File Path:** `vue-frontend/src/views/PropertyDetail.vue`
  - **Changes:** The logic will be updated to correctly use the new `ParsedInspectionTime` object returned by the `inspectionTimes` computed property. It will generate a concise summary, such as "Sat 10am" or "By Appt.", suitable for display on the overlay button.

[Classes]
No classes will be added, modified, or removed in this implementation.

[Dependencies]
No new dependencies will be added, and no existing dependency versions will be changed.

[Testing]
The primary validation will be through manual verification by you.

Given the visual nature of this bug, manual testing is the most effective way to confirm the fix. After I implement the changes, you will need to check the "Inspection times" section on the property detail page to confirm that all variants of inspection times now display correctly, with the date and time parts properly separated and formatted in their respective UI elements.

[Implementation Order]
The changes will be implemented in a logical, conflict-free sequence.

1.  **Create Utility File:** First, create the new file `vue-frontend/src/utils/inspectionTimeParser.js` and implement the robust `parseInspectionTime` function within it.
2.  **Refactor Component:** Second, modify `vue-frontend/src/views/PropertyDetail.vue`. Import the new `parseInspectionTime` function, remove the old local helper, and update the `inspectionTimes` and `nextInspectionTime` computed properties to use the new utility.
