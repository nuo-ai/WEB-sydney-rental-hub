import React, { useState } from 'react';
import { View, Image, Text } from '@tarojs/components';
import { Heart, Bed, Bath, Car } from 'lucide-react';
import { Card } from './Card';

// Data interface as per Work Order #003
export interface PropertyCardProps {
  imageUrl: string;
  price: string;
  address: string;
  bedrooms: number;
  bathrooms: number;
  carspots: number;
  isFavorited: boolean;
}

// Helper to render specification icons
const SpecItem = ({ icon, value, text }) => (
  <View className='flex items-center text-grey-dark'>
    {icon}
    <Text className='ml-1 text-sm font-normal'>{value} {text}</Text>
  </View>
);

export const PropertyCard: React.FC<PropertyCardProps> = ({
  imageUrl,
  price,
  address,
  bedrooms,
  bathrooms,
  carspots,
  isFavorited: initialIsFavorited,
}) => {
  const [isFavorited, setIsFavorited] = useState(initialIsFavorited);

  const handleFavoriteClick = (e) => {
    e.stopPropagation(); // Prevent card click event
    setIsFavorited(!isFavorited);
  };

  return (
    <Card className='w-full max-w-sm overflow-hidden'>
      <View className='relative'>
        <Image
          src={imageUrl}
          className='w-full h-48 object-cover rounded-t-md'
          mode='aspectFill'
          // Accessibility as per UI_RULES.md
          aria-label={`Rental property at ${address}`}
        />
        <View
          className='absolute top-2 right-2 bg-white/80 rounded-full p-2'
          onClick={handleFavoriteClick}
        >
          <Heart
            size={24}
            className={isFavorited ? 'text-primary fill-current' : 'text-grey-dark'}
          />
        </View>
      </View>
      
      {/* Information Section - Padding rule from UI_RULES.md */}
      <View className='p-4'>
        {/* Price - Typography rule from UI_RULES.md */}
        <Text className='text-2xl font-bold text-grey-darkest'>
          ${price}
        </Text>
        <Text className='text-sm text-grey-dark'> per week</Text>

        {/* Core Specs - Spacing and Typography rules */}
        <View className='flex items-center gap-4 mt-2'>
          <SpecItem icon={<Bed size={16} />} value={bedrooms} text='Beds' />
          <SpecItem icon={<Bath size={16} />} value={bathrooms} text='Baths' />
          <SpecItem icon={<Car size={16} />} value={carspots} text='Cars' />
        </View>

        {/* Address - Typography rule */}
        <Text className='block mt-2 text-xs text-grey-dark truncate'>
          {address}
        </Text>
      </View>
    </Card>
  );
};
