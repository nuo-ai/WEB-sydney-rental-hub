# Implementation Plan

[Overview]
This plan outlines the steps to comprehensively fix and enhance the Property Detail page. The core goal is to ensure the page fetches all necessary data via the project's REST API, displays this information accurately and completely, and aligns with the established UI/UX patterns. This effort corrects a previous misunderstanding of the data flow and addresses a range of UI bugs and missing features, leading to a robust and user-friendly detail view.

[Types]
No new types, classes, or data structures will be introduced at the data contract level; this plan focuses on correctly utilizing the existing REST API data structures.

[Files]
This implementation will modify two key files and create this planning document.

- **backend/crud/properties_crud.py** (Modified):
  - The `get_property_by_id_from_db` function will be updated. Its SQL `SELECT` statement will be expanded to include the `description` and `property_features` columns from the `properties` table, which are currently missing.
  - The `Property` object instantiation within this function will be updated to map these newly queried columns to the corresponding object fields.

- **vue-frontend/src/views/PropertyDetail.vue** (Modified):
  - **Data Display**: The template will be updated to correctly render the `description` and `property_features` (as a list of tags). It will also ensure other previously missing fields like `bond` are displayed.
  - **UI Cleanup**: The redundant suburb and postcode paragraph below the main address will be removed.
  - **Iconography**: All Font Awesome `<i>` tag icons will be replaced with native Element Plus icon components (`<el-icon>`) for consistency. The bed/bath/parking specs will be changed from text labels to an "icon + number" format.
  - **Logic Fix**: The `isFavorite` computed property and `toggleFavorite` method will be corrected to use the appropriate property ID, resolving the non-functional favorite button.

- **implementation_plan.md** (New File):
  - This document, serving as the single source of truth for the implementation.

[Functions]
The following functions will be modified to ensure the correct data flow and UI representation.

- **get_property_by_id_from_db** (in `backend/crud/properties_crud.py`):
  - **Change**: Modify its internal SQL query to fetch additional fields (`description`, `property_features`).
  - **Purpose**: To ensure the REST API endpoint `/api/properties/{id}` returns all data required by the frontend.

- **propertySpecsText (computed)** (in `vue-frontend/src/views/PropertyDetail.vue`):
  - **Change**: The logic will be completely overhauled. It will no longer include the `property_type` string. Instead, it will generate a structure suitable for rendering specs with icons.
  - **Purpose**: To change the presentation of property specs from "2 bed • 1 bath" to a richer icon-based format.

- **isFavorite (computed)** (in `vue-frontend/src/views/PropertyDetail.vue`):
  - **Change**: The logic will be updated to use the correct identifier (`property.listing_id`) when checking against the `propertiesStore.favoriteIds` array.
  - **Purpose**: To accurately reflect the property's favorite status.

- **toggleFavorite (method)** (in `vue-frontend/src/views/PropertyDetail.vue`):
  - **Change**: Will be updated to pass the correct identifier to the store's `addFavorite` and `removeFavorite` actions.
  - **Purpose**: To make the "favorite" button functional.

[Classes]
No new classes will be created or modified.

[Dependencies]
No new dependencies are required for this task.

[Testing]
The implementation will be validated through manual end-to-end testing.

- **Backend**: After modifying the CRUD function, directly query the `/api/properties/{id}` REST endpoint (using `curl` or a browser) for a property with a known description and features to confirm the new fields are present in the JSON response.
- **Frontend**: After frontend changes, load the corresponding property detail page in the browser.
  - Verify that the description and features are displayed correctly.
  - Verify that the address is no longer duplicated.
  - Verify that bed/bath/parking specs are now icons.
  - Verify that all icons (favorite, share, copy) are displayed correctly.
  - Test the favorite button's add/remove functionality and confirm the state persists on page refresh (via localStorage).

[Implementation Order]
The task will be executed in a backend-first sequence to ensure the data pipeline is fixed before the frontend is adapted.

1.  **Update Backend**: Modify `backend/crud/properties_crud.py` to include `description` and `property_features` in the data payload for a single property.
2.  **Update Frontend**: Modify `vue-frontend/src/views/PropertyDetail.vue` to consume the new data fields and implement all planned UI and logic fixes simultaneously.
3.  **Update Documentation**: Update `memory-bank/activeContext.md` and `memory-bank/progress.md` to reflect the changes.
4.  **Final Verification**: Perform manual end-to-end testing as described in the [Testing] section.
