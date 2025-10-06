# Google Maps API Setup

Follow these steps to enable Google Maps features.

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project or select an existing one.
3. Enable the **Maps JavaScript API**.
4. Generate an API key and restrict it to approved domains or IPs.
5. Store the key in environment variables:
   - Backend: `GOOGLE_MAPS_API_KEY=your_key`
   - MCP Server: `apps/mcp-server/.env` with `GOOGLE_MAPS_API_KEY=your_key`
   - Frontend: `.env` with `VITE_GOOGLE_MAPS_API_KEY=your_key`
6. Load the script in the front end:
```ts
const url = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}&libraries=places`;
```
7. Do not commit real keys; use `.env.example` placeholders.
8. See `SECURITY_CHECKLIST.md` for protecting credentials.
