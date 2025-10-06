// Google Places Service for Sydney Rental Hub

class PlacesService {
  constructor() {
    this.isLoaded = false
    this.loadPromise = null
    this.service = null
    this.autocompleteService = null
    this.geocoder = null

    // Development mode flag - set to false when you have a real API key
    this.devMode = import.meta.env.VITE_GOOGLE_PLACES_DEV_MODE !== 'false'

    // API Key configuration
    this.apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
  }

  // Load Google Maps JavaScript API
  async loadGoogleMaps() {
    if (this.isLoaded) return true

    if (this.loadPromise) return this.loadPromise

    this.loadPromise = new Promise((resolve, reject) => {
      // Check if already loaded
      if (window.google && window.google.maps) {
        this.initializeServices()
        this.isLoaded = true
        resolve(true)
        return
      }

      // Development mode - don't load real API
      if (this.devMode || !this.apiKey) {
        // 开发模式：使用模拟数据避免Google API调用
        this.isLoaded = true
        resolve(true)
        return
      }

      // Create script tag
      const script = document.createElement('script')
      script.async = true
      script.defer = true
      script.src = `https://maps.googleapis.com/maps/api/js?key=${this.apiKey}&libraries=places&language=en&region=AU`

      script.onload = () => {
        this.initializeServices()
        this.isLoaded = true
        resolve(true)
      }

      script.onerror = () => {
        console.error('[Places Service] Failed to load Google Maps API')
        reject(new Error('Failed to load Google Maps API'))
      }

      document.head.appendChild(script)
    })

    return this.loadPromise
  }

  // Initialize Google Maps services
  initializeServices() {
    if (window.google && window.google.maps) {
      this.autocompleteService = new google.maps.places.AutocompleteService()
      this.service = new google.maps.places.PlacesService(document.createElement('div'))
      this.geocoder = new google.maps.Geocoder()
    }
  }

  // Search for places with autocomplete
  async searchPlaces(query, sessionToken = null) {
    await this.loadGoogleMaps()

    // Development mode - return mock data
    if (this.devMode || !this.autocompleteService) {
      return this.getMockSearchResults(query)
    }

    return new Promise((resolve, reject) => {
      const request = {
        input: query,
        componentRestrictions: { country: 'au' }, // Restrict to Australia
        types: ['address', 'establishment'], // Focus on addresses and places
        sessionToken: sessionToken,
      }

      this.autocompleteService.getPlacePredictions(request, (predictions, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          resolve(
            predictions.map((p) => ({
              place_id: p.place_id,
              description: p.description,
              main_text: p.structured_formatting?.main_text,
              secondary_text: p.structured_formatting?.secondary_text,
              types: p.types,
            })),
          )
        } else if (status === google.maps.places.PlacesServiceStatus.ZERO_RESULTS) {
          resolve([])
        } else {
          console.error('[Places Service] Autocomplete error:', status)
          reject(new Error(`Autocomplete failed: ${status}`))
        }
      })
    })
  }

  // Get place details including coordinates
  async getPlaceDetails(placeId) {
    await this.loadGoogleMaps()

    // Development mode - return mock data
    if (this.devMode || !this.service) {
      return this.getMockPlaceDetails(placeId)
    }

    return new Promise((resolve, reject) => {
      const request = {
        placeId: placeId,
        fields: ['name', 'formatted_address', 'geometry', 'types', 'address_components'],
      }

      this.service.getDetails(request, (place, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          resolve({
            place_id: placeId,
            name: place.name,
            formatted_address: place.formatted_address,
            latitude: place.geometry.location.lat(),
            longitude: place.geometry.location.lng(),
            types: place.types,
            address_components: place.address_components,
          })
        } else {
          console.error('[Places Service] Place details error:', status)
          reject(new Error(`Place details failed: ${status}`))
        }
      })
    })
  }

  // Get coordinates from address
  async geocodeAddress(address) {
    await this.loadGoogleMaps()

    // Development mode - return mock data
    if (this.devMode || !this.geocoder) {
      return this.getMockGeocodeResult(address)
    }

    return new Promise((resolve, reject) => {
      this.geocoder.geocode(
        {
          address: address,
          region: 'AU', // Bias to Australia
        },
        (results, status) => {
          if (status === google.maps.GeocoderStatus.OK) {
            const result = results[0]
            resolve({
              formatted_address: result.formatted_address,
              latitude: result.geometry.location.lat(),
              longitude: result.geometry.location.lng(),
              place_id: result.place_id,
            })
          } else {
            console.error('[Places Service] Geocoding error:', status)
            reject(new Error(`Geocoding failed: ${status}`))
          }
        },
      )
    })
  }

  // Mock data for development
  getMockSearchResults(query) {
    const mockResults = [
      {
        place_id: 'ChIJ1-v38TeuEmsRKaDzrWLx5qQ',
        description: '83 Harbour St, Haymarket NSW 2000',
        main_text: '83 Harbour Street',
        secondary_text: 'Haymarket NSW 2000',
        types: ['street_address'],
      },
      {
        place_id: 'ChIJ2-v38TeuEmsRKaDzrWLx5qQ',
        description: '123 Pitt St, Sydney NSW 2000',
        main_text: '123 Pitt Street',
        secondary_text: 'Sydney NSW 2000',
        types: ['street_address'],
      },
      {
        place_id: 'ChIJ3-v38TeuEmsRKaDzrWLx5qQ',
        description: '456 George St, Sydney NSW 2000',
        main_text: '456 George Street',
        secondary_text: 'Sydney NSW 2000',
        types: ['street_address'],
      },
      {
        place_id: 'ChIJ4-v38TeuEmsRKaDzrWLx5qQ',
        description: '789 Kent St, Sydney NSW 2000',
        main_text: '789 Kent Street',
        secondary_text: 'Sydney NSW 2000',
        types: ['street_address'],
      },
      {
        place_id: 'ChIJ5-v38TeuEmsRKaDzrWLx5qQ',
        description: '321 Sussex St, Sydney NSW 2000',
        main_text: '321 Sussex Street',
        secondary_text: 'Sydney NSW 2000',
        types: ['street_address'],
      },
    ]

    // Filter by query
    const lowerQuery = query.toLowerCase()
    return mockResults.filter((r) => r.description.toLowerCase().includes(lowerQuery)).slice(0, 5)
  }

  getMockPlaceDetails(placeId) {
    const baseDetails = {
      place_id: placeId,
      name: 'Mock Address',
      formatted_address: '83 Harbour St, Haymarket NSW 2000',
      latitude: -33.8831 + (Math.random() - 0.5) * 0.02,
      longitude: 151.2065 + (Math.random() - 0.5) * 0.02,
      types: ['street_address'],
      address_components: [
        { long_name: '83', types: ['street_number'] },
        { long_name: 'Harbour Street', types: ['route'] },
        { long_name: 'Haymarket', types: ['locality'] },
        { long_name: 'NSW', types: ['administrative_area_level_1'] },
        { long_name: '2000', types: ['postal_code'] },
      ],
    }

    // Customize based on placeId for variety
    if (placeId.includes('2')) {
      baseDetails.name = 'Pitt Street Location'
      baseDetails.formatted_address = '123 Pitt St, Sydney NSW 2000'
    } else if (placeId.includes('3')) {
      baseDetails.name = 'George Street Location'
      baseDetails.formatted_address = '456 George St, Sydney NSW 2000'
    }

    return baseDetails
  }

  getMockGeocodeResult(address) {
    return {
      formatted_address: address + ', Australia',
      latitude: -33.8688 + (Math.random() - 0.5) * 0.1,
      longitude: 151.2093 + (Math.random() - 0.5) * 0.1,
      place_id: 'mock_' + Date.now(),
    }
  }

  // Get preset Sydney locations
  getPresetLocations() {
    return [
      {
        place_id: 'ChIJVXealLmuEmsRUduC5Wd-6XQ',
        name: 'University of Sydney (USYD)',
        formatted_address: 'Camperdown NSW 2006, Australia',
        latitude: -33.8886,
        longitude: 151.1873,
        type: 'university',
      },
      {
        place_id: 'ChIJTbYYkVOxEmsRAO6ykvoWKgI',
        name: 'University of New South Wales (UNSW)',
        formatted_address: 'Kensington NSW 2052, Australia',
        latitude: -33.9173,
        longitude: 151.2313,
        type: 'university',
      },
      {
        place_id: 'ChIJrRNl1jCuEmsRMOwrvs3vkLg',
        name: 'University of Technology Sydney (UTS)',
        formatted_address: 'Ultimo NSW 2007, Australia',
        latitude: -33.8832,
        longitude: 151.2005,
        type: 'university',
      },
      {
        place_id: 'ChIJaYGwoN6vEmsRCHhYJrz7JMo',
        name: 'Central Station',
        formatted_address: 'Sydney NSW 2000, Australia',
        latitude: -33.8831,
        longitude: 151.2065,
        type: 'station',
      },
      {
        place_id: 'ChIJi6C1MxquEmsR9-c-3O48ykI',
        name: 'Town Hall Station',
        formatted_address: 'Sydney NSW 2000, Australia',
        latitude: -33.8733,
        longitude: 151.207,
        type: 'station',
      },
      {
        place_id: 'ChIJDy-wPOauEmsRGQ4he8OZRj4',
        name: 'Macquarie University',
        formatted_address: 'Macquarie Park NSW 2109, Australia',
        latitude: -33.7738,
        longitude: 151.1126,
        type: 'university',
      },
      {
        place_id: 'ChIJP5iLHkCuEmsRwMwyFmh9AQU',
        name: 'Sydney Opera House',
        formatted_address: 'Bennelong Point, Sydney NSW 2000, Australia',
        latitude: -33.8568,
        longitude: 151.2153,
        type: 'landmark',
      },
      {
        place_id: 'ChIJN1t_tDeuEmsRdSZ7PKMHBUQ',
        name: 'Sydney CBD',
        formatted_address: 'Sydney NSW 2000, Australia',
        latitude: -33.8688,
        longitude: 151.2093,
        type: 'area',
      },
    ]
  }

  // Create a new session token for autocomplete billing optimization
  createSessionToken() {
    if (window.google && window.google.maps) {
      return new google.maps.places.AutocompleteSessionToken()
    }
    return 'mock-session-' + Date.now()
  }
}

// Export singleton instance
export default new PlacesService()
