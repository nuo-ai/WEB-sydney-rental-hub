import React, { useState, useEffect } from 'react';
import { View, Text, Button } from '@tarojs/components';
import { Modal } from './Modal';

// --- Placeholder Components for Filter Controls ---
const FilterSection = ({ title, children }) => (
  <View className='mb-6'>
    <Text className='block text-base font-semibold text-grey-darker mb-3'>{title}</Text>
    {children}
  </View>
);

const UniversitySelector = () => <View><Text>[University Selector Placeholder]</Text></View>;
const PriceRangeSlider = () => <View><Text>[Price Range Slider Placeholder]</Text></View>;
const PropertyTypeSelector = () => <View><Text>[Property Type Selector Placeholder]</Text></View>;
const BedroomSelector = () => <View><Text>[Bedroom Selector Placeholder]</Text></View>;
const FurnishedToggle = () => <View><Text>[Furnished Toggle Placeholder]</Text></View>;
// --- End Placeholder Components ---

export interface FilterValues {
  university: string | null;
  priceMin: number;
  priceMax: number;
  propertyType: string[];
  bedrooms: number[];
  furnished: boolean;
}

interface FilterModalProps {
  isOpen: boolean;
  onClose: () => void;
  onApplyFilters: (filters: FilterValues) => void;
  initialFilters: FilterValues;
}

export const INITIAL_FILTERS: FilterValues = {
  university: null,
  priceMin: 100,
  priceMax: 2000,
  propertyType: [],
  bedrooms: [],
  furnished: false,
};

export const FilterModal: React.FC<FilterModalProps> = ({
  isOpen,
  onClose,
  onApplyFilters,
  initialFilters,
}) => {
  const [filters, setFilters] = useState<FilterValues>(initialFilters);

  // Sync internal state if the initial filters from parent change
  useEffect(() => {
    setFilters(initialFilters);
  }, [initialFilters]);

  const handleApply = () => {
    onApplyFilters(filters);
    onClose();
  };

  const handleReset = () => {
    setFilters(INITIAL_FILTERS);
  };

  const footer = (
    <View className='flex items-center gap-4'>
      <Button
        className='flex-1 bg-white border border-grey-base text-grey-darker rounded-md py-3'
        onClick={handleReset}
      >
        重置
      </Button>
      <Button
        className='flex-1 bg-primary text-white font-semibold rounded-md py-3'
        onClick={handleApply}
      >
        查看房源
      </Button>
    </View>
  );

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title='筛选条件'
      footer={footer}
    >
      <FilterSection title='学校选择'>
        <UniversitySelector />
      </FilterSection>
      <FilterSection title='价格区间'>
        <PriceRangeSlider />
      </FilterSection>
      <FilterSection title='房屋类型'>
        <PropertyTypeSelector />
      </FilterSection>
      <FilterSection title='卧室数量'>
        <BedroomSelector />
      </FilterSection>
      <FilterSection title='是否带家具'>
        <FurnishedToggle />
      </FilterSection>
    </Modal>
  );
};
