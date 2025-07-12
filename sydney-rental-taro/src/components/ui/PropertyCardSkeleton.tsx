import React from 'react';
import { View } from '@tarojs/components';
import { Card } from './Card';

export const PropertyCardSkeleton: React.FC = () => {
  return (
    <Card className='w-full max-w-sm overflow-hidden'>
      <View className='animate-pulse'>
        {/* Image Placeholder */}
        <View className='w-full h-48 bg-grey-light rounded-t-md'></View>
        
        <View className='p-4'>
          {/* Price Placeholder */}
          <View className='h-8 w-3/4 bg-grey-light rounded'></View>
          <View className='h-4 w-1/2 bg-grey-light rounded mt-1'></View>

          {/* Specs Placeholder */}
          <View className='flex items-center gap-4 mt-3'>
            <View className='h-5 w-1/4 bg-grey-light rounded'></View>
            <View className='h-5 w-1/4 bg-grey-light rounded'></View>
            <View className='h-5 w-1/4 bg-grey-light rounded'></View>
          </View>

          {/* Address Placeholder */}
          <View className='h-4 w-full bg-grey-light rounded mt-3'></View>
        </View>
      </View>
    </Card>
  );
};
