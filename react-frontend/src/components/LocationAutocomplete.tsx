import { useState } from 'react';
import { Input, List, ListItem, Spinner } from '@chakra-ui/react';

// Mock data for development until the API is ready
const MOCK_LOCATIONS = [
  'Sydney NSW 2000',
  'Pyrmont NSW 2009',
  'Ultimo NSW 2007',
  'Surry Hills NSW 2010',
  'Darlinghurst NSW 2010',
  'Haymarket NSW 2000',
];

const LocationAutocomplete = () => {
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setInputValue(value);

    if (value.length > 2) {
      setIsLoading(true);
      // Simulate API call with debounce
      setTimeout(() => {
        const filteredLocations = MOCK_LOCATIONS.filter((location) =>
          location.toLowerCase().includes(value.toLowerCase())
        );
        setSuggestions(filteredLocations);
        setIsLoading(false);
      }, 300); // 300ms debounce
    } else {
      setSuggestions([]);
    }
  };

  return (
    <div>
      <Input
        placeholder="Search for a suburb, e.g., 'Sydney NSW 2000'"
        value={inputValue}
        onChange={handleInputChange}
      />
      {isLoading && <Spinner size="sm" />}
      {suggestions.length > 0 && (
        <List borderWidth="1px" borderRadius="md" mt={1}>
          {suggestions.map((suggestion, index) => (
            <ListItem key={index} p={2} _hover={{ bg: 'gray.100' }}>
              {suggestion}
            </ListItem>
          ))}
        </List>
      )}
    </div>
  );
};

export default LocationAutocomplete;
