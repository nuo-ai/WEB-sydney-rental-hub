# Implementation Plan

[Overview]
This plan will fix a bug where property inspection times disappear upon page refresh by correcting the data merge logic in the Pinia store.

The core issue is that the `fetchPropertyDetail` action in `properties.js` fetches data from two different endpoints. The second, more detailed endpoint (`getDetail`) unfortunately does not include the `inspection_times` field. The current implementation incorrectly overwrites the initially loaded property data (which contains inspection times) with the data from the second call, leading to data loss. This plan corrects the merge strategy to ensure data is supplemented, not overwritten, creating a more robust and predictable state management flow.

[Types]
No new types, interfaces, or data structures are required for this change. The existing `Property` type implicitly handles the `inspection_times` field, and this fix ensures that field is correctly preserved.

[Files]
This implementation will modify one existing file to correct the state management logic.

- **`vue-frontend/src/stores/properties.js`**: This file will be modified to change how property details are merged into the state.

[Functions]
The focus of this implementation is to modify a single function within the `properties` Pinia store.

- **`fetchPropertyDetail`** in `vue-frontend/src/stores/properties.js`: The merging logic within this action will be updated. Instead of a simple object spread that overwrites existing data, it will be changed to an intelligent merge that preserves the `inspection_times` from the initial fetch while supplementing other details from the second fetch.

[Classes]
No new classes will be created, and no existing classes will be modified or removed.

[Dependencies]
There are no changes to project dependencies. No new packages will be added, and no existing ones will be updated or removed.

[Testing]
Manual testing will be required to confirm the fix.

1.  Navigate directly to a property detail page that is known to have inspection times.
2.  Refresh the page.
3.  Verify that the inspection times are still visible after the refresh.
4.  Navigate from the home page to a property detail page and confirm inspection times are also visible.

[Implementation Order]
The implementation will be completed in a single, focused step.

1.  Modify the `fetchPropertyDetail` action in `vue-frontend/src/stores/properties.js` to implement the corrected data merging strategy.
