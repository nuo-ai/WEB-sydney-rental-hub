export const getCssVarValue = (name, fallback = '') => {
  if (!name) {
    return fallback
  }

  if (typeof window === 'undefined' || !window.document?.documentElement) {
    return fallback
  }

  const value = getComputedStyle(document.documentElement).getPropertyValue(name)
  return value && value.trim() ? value.trim() : fallback
}
