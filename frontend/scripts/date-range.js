/**
 * @module date-range
 * @description Manages the date range filter component, including UI interactions, validation, and state management.
 */

// This debounce utility is assumed to be in a shared utils.js file.
// If not, it should be added there.
const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
};


const DOM = {
    startDateInput: null,
    endDateInput: null,
    clearButton: null,
    applyButton: null,
    errorContainer: null,
};

let onChangeCallback = () => {};
let onApplyCallback = () => {};

/**
 * Validates the selected date range.
 * If the end date is before the start date, it shows an error and disables the apply button.
 * @returns {boolean} - True if the date range is valid, false otherwise.
 */
function validateDates() {
    const start = DOM.startDateInput.value;
    const end = DOM.endDateInput.value;

    if (start && end && new Date(end) < new Date(start)) {
        DOM.errorContainer.classList.remove('hidden');
        DOM.applyButton.disabled = true;
        return false;
    }

    DOM.errorContainer.classList.add('hidden');
    DOM.applyButton.disabled = false;
    return true;
}

/**
 * Handles the date change event.
 * If the dates are valid, it triggers the onChange callback with the new date range.
 */
function handleDateChange() {
    if (validateDates()) {
        onChangeCallback(getDateRange());
    }
}

const debouncedDateChange = debounce(handleDateChange, 300);

/**
 * Initializes the date range filter component.
 * @param {object} options - The options for initialization.
 * @param {function} options.onChange - The callback function to be called when the date input changes.
 * @param {function} options.onApply - The callback function to be called when the apply button is clicked.
 */
export function initDateRange({ onChange, onApply }) {
    DOM.startDateInput = document.getElementById('start-date');
    DOM.endDateInput = document.getElementById('end-date');
    DOM.clearButton = document.getElementById('clear-date-range');
    DOM.applyButton = document.getElementById('apply-date-range');
    DOM.errorContainer = document.getElementById('date-range-error');
    
    if (!DOM.startDateInput) {
        console.error("Date range component's HTML structure not found in the DOM.");
        return;
    }

    onChangeCallback = onChange;
    onApplyCallback = onApply;

    DOM.startDateInput.addEventListener('input', debouncedDateChange);
    DOM.endDateInput.addEventListener('input', debouncedDateChange);
    
    DOM.applyButton.addEventListener('click', () => {
        if (validateDates()) {
            // First, ensure the latest values are passed to the state
            onChangeCallback(getDateRange());
            // Then, trigger the apply action
            onApplyCallback();
        }
    });

    DOM.clearButton.addEventListener('click', () => {
        setDateRange({ start: '', end: '' });
        // Immediately apply the cleared state
        onChangeCallback(getDateRange());
        onApplyCallback();
    });
    
    console.log('Date range component initialized.');
}

/**
 * Sets the date range values in the input fields.
 * @param {object} dateRange - The date range to set.
 * @param {string|null} dateRange.start - The start date in YYYY-MM-DD format.
 * @param {string|null} dateRange.end - The end date in YYYY-MM-DD format.
 */
export function setDateRange({ start, end }) {
    if (DOM.startDateInput) {
        DOM.startDateInput.value = start || '';
        DOM.endDateInput.value = end || '';
        validateDates();
    }
}

/**
 * Gets the current date range from the input fields.
 * @returns {{start: string|undefined, end: string|undefined}} - The current date range.
 */
export function getDateRange() {
    return {
        start: DOM.startDateInput.value || undefined,
        end: DOM.endDateInput.value || undefined,
    };
}