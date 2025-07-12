import React, { useState, useEffect } from 'react';
import { View, Button, Text } from '@tarojs/components';
import Taro from '@tarojs/taro';
import { Filter } from 'lucide-react';
import { PropertyCard, PropertyCardProps } from '../../components/ui/PropertyCard';
import { PropertyCardSkeleton } from '../../components/ui/PropertyCardSkeleton';
import { FilterModal, FilterValues, INITIAL_FILTERS } from '../../components/ui/FilterModal';

// Helper to build query string from filters
const buildQueryString = (filters: FilterValues) => {
  const params = new URLSearchParams();
  if (filters.university) params.append('university', filters.university);
  if (filters.priceMin) params.append('min_rent_pw', String(filters.priceMin));
  if (filters.priceMax) params.append('max_rent_pw', String(filters.priceMax));
  if (filters.propertyType.length > 0) params.append('property_type', filters.propertyType.join(','));
  if (filters.bedrooms.length > 0) params.append('bedrooms', filters.bedrooms.join(','));
  if (filters.furnished) params.append('furnished', String(filters.furnished));
  return params.toString();
};

export default function Index() {
  const [properties, setProperties] = useState<PropertyCardProps[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isFilterModalOpen, setIsFilterModalOpen] = useState(false);
  const [activeFilters, setActiveFilters] = useState<FilterValues>(INITIAL_FILTERS);

  // useEffect to fetch data when activeFilters change
  useEffect(() => {
    console.log('Filters changed, fetching properties...', activeFilters);
    fetchProperties();
  }, [activeFilters]);

  const handleApplyFilters = (newFilters: FilterValues) => {
    setActiveFilters(newFilters);
  };

  const fetchProperties = async () => {
    setIsLoading(true);
    const queryString = buildQueryString(activeFilters);
    const isDefaultFilters = JSON.stringify(activeFilters) === JSON.stringify(INITIAL_FILTERS);
    
    // Use featured endpoint for default filters, search endpoint otherwise
    const endpoint = isDefaultFilters 
      ? 'http://127.0.0.1:8000/api/v1/properties/featured'
      : `http://127.0.0.1:8000/api/v1/properties/search?${queryString}`;

    try {
      const res = await Taro.request({
        url: endpoint,
        method: 'GET',
      });
      if (res.statusCode === 200 && res.data) {
        const propertyData = res.data.data || [];
        const formattedProperties = propertyData.map(p => ({
          imageUrl: p.image_urls[0] || 'https://via.placeholder.com/300x200',
          price: p.price,
          address: p.address,
          bedrooms: p.bedrooms,
          bathrooms: p.bathrooms,
          carspots: p.car_spaces,
          isFavorited: false,
        }));
        setProperties(formattedProperties);
      } else {
        console.error('Failed to fetch properties:', res);
        setProperties([]); // Clear properties on error
      }
    } catch (error) {
      console.error('Error fetching properties:', error);
      setProperties([]); // Clear properties on error
    } finally {
      setIsLoading(false);
    }
  };

  const renderSkeleton = () => (
    <>
      {[...Array(4)].map((_, index) => (
        <View key={index} className='mb-4'>
          <PropertyCardSkeleton />
        </View>
      ))}
    </>
  );

  return (
    <View className='index bg-grey-lighter min-h-screen p-4'>
      <View className='mb-4'>
        <Button 
          className='bg-white border border-grey-base text-grey-darker flex items-center justify-center w-full py-2 rounded-md shadow-sm'
          onClick={() => setIsFilterModalOpen(true)}
        >
          <Filter size={18} className='mr-2' />
          筛选
        </Button>
      </View>

      <View className='space-y-4'>
        {isLoading
          ? renderSkeleton()
          : properties.length > 0
            ? properties.map((prop, index) => (
                <PropertyCard key={index} {...prop} />
              ))
            : <Text>No properties found for the selected filters.</Text>}
      </View>
      
      <FilterModal
        isOpen={isFilterModalOpen}
        onClose={() => setIsFilterModalOpen(false)}
        onApplyFilters={handleApplyFilters}
        initialFilters={activeFilters}
      />
    </View>
  );
}
