## Brief overview
This Cline rule file contains specific guidelines for developing uni-app x projects using UTS language. These rules cover code style, project structure, platform compatibility, and best practices for cross-platform development.

## Code Style and Structure
- Write clean and understandable code with Chinese comments for complex logic
- Strict type matching without implicit conversions
- No variable or function hoisting - use variables and functions within clear scopes only
- Use conditional compilation for platform-specific code to avoid interference with other platforms

## Project Structure
- Follow uni-app x project structure and place generated files in correct directories
- Use .uvue as page file extension (similar to .vue but with minor differences)
- Place generated .uvue pages in project's pages directory and register them in pages.json
- Scrollable content must be within scroll containers (scroll-view, list-view, waterflow)
- When pages need scrolling, place scroll container as first-level child node with App conditional compilation

## UTS Language Rules
- Use cross-platform UTS language for generated script code
- UTS is a strong type language similar to TypeScript but with stricter type requirements
- No implicit type conversion - boolean type required for conditional statements
- Strictly distinguish between nullable and non-nullable types using `|null` or `?`
- Use safe call operator `?.` for nullable types, avoid `!.` assertion
- Use UTSJSONObject instead of object type
- No undefined - variables must be assigned before use
- Use `type` for object type definitions, not `interface`
- Use `let` and `const` for variable declarations, not `var`
- No JSX expressions or with statements
- No JavaScript prototype chain features
- Prefer `==` and `!=` over `===` and `!==`

## CSS Rules
- Use ucss (CSS subset) for cross-platform styling
- Layout: Only use flex layout or absolute positioning - no floats or grids
- Selectors: Only basic class selectors (.class) allowed
- Text styling: Place text in <text> or <button> components only
- Units: Only px, rpx, and percentages supported
- Use rpx only when width needs to adapt to screen width
- Use percentages only when length needs to adapt to parent container size

## Vue Support
- Use Vue 3 syntax only - avoid Vue 2
- Prefer Composition API for new pages
- Use easycom specification for components
- For non-easycom custom Vue components, use `$callMethod` to call component methods
- Avoid unsupported Vue plugins (pinia, vuex, i18n)
- Check uni-app x documentation for platform and version compatibility

## Conditional Compilation
- Use conditional compilation for platform-specific code
- Core syntax:
  ```
  // Platform basic judgment
  #ifdef APP || MP
  // Mini programs/APP common code
  #ifdef APP-ANDROID
      // Android-specific logic
  #endif
  #ifdef APP-IOS
      // IOS-specific logic
  #endif
  #endif
  ```
- Core platform identifiers: APP, APP-ANDROID, APP-IOS, APP-HARMONY, WEB, MP-WEIXIN, etc.

## API Usage
- Can use UTS APIs but check version and platform compatibility
- Can use uni-app x APIs but check version and platform compatibility
- Can use Vue 3 APIs but check version and platform compatibility
- Prefer calling system native APIs through UTS plugins rather than directly in .uvue pages
- Use conditional compilation for platform/version-specific code
- Query available plugins using MCP tools
- Use eventbus for cross-page communication
