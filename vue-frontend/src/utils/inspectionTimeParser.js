/**
 * @typedef {object} ParsedInspectionTime
 * @property {string} date - The formatted date part, e.g., "Thursday, 21 Aug"
 * @property {string} time - The formatted time part, e.g., "5:00pm - 5:15pm" or "By Appointment"
 */

/**
 * Parses a variety of inconsistent inspection time strings into a structured object.
 * Handles formats like "Thursday Details", "21 Aug", "Inspection 5:00pm - 5:15pm", and "By Appointment".
 *
 * @param {string} timeStr - The raw inspection time string from the API.
 * @returns {ParsedInspectionTime} A structured object with date and time properties.
 */
export function parseInspectionTime(timeStr) {
  if (!timeStr || typeof timeStr !== 'string') {
    return { date: 'N/A', time: 'Contact Agent' };
  }

  // Normalize the string by removing "Details" and other noise, then trimming.
  let cleanedStr = timeStr.replace(/Details/gi, '').trim();

  if (!cleanedStr) {
      return { date: 'Inspection', time: 'By Appointment' };
  }

  if (cleanedStr.toLowerCase().includes('by appointment')) {
    return { date: 'By Appointment', time: '' };
  }

  if (cleanedStr.toLowerCase().includes('cancelled')) {
    return { date: 'Cancelled', time: '' };
  }

  // Regex to find time-like patterns (e.g., "5:00pm - 5:15pm", "10:30am", "1pm")
  const timeRegex = /(\d{1,2}:\d{2}\s*(?:am|pm)?\s*-\s*\d{1,2}:\d{2}\s*(?:am|pm)?|\d{1,2}(?::\d{2})?\s*(?:am|pm))/i;
  const timeMatch = cleanedStr.match(timeRegex);

  let datePart = '';
  let timePart = '';

  if (timeMatch) {
    timePart = timeMatch[0].trim();
    // The date is everything else in the string.
    datePart = cleanedStr.replace(timeMatch[0], '').replace('Inspection', '').trim();
    if (!datePart) {
        // If nothing is left, it's just a time, so the date is "Inspection".
        datePart = 'Inspection';
    }
  } else {
    // If no time is found, the entire string is considered the date part.
    datePart = cleanedStr;
    timePart = 'Details';
  }

  // Final cleanup for a cleaner display
  datePart = datePart.replace(/,$/, '').trim();

  return {
    date: datePart || 'Inspection', // Fallback
    time: timePart,
  };
}
