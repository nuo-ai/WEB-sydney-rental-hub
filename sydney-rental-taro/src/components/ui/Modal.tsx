import React from 'react';
import { View, Text } from '@tarojs/components';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
}) => {
  if (!isOpen) {
    return null;
  }

  return (
    <View className='fixed inset-0 z-50 flex flex-col justify-end'>
      {/* Overlay */}
      <View
        className='absolute inset-0 bg-black/50 animate-fade-in'
        onClick={onClose}
      />

      {/* Modal Content */}
      <View className='relative bg-grey-lighter w-full rounded-t-lg shadow-lg animate-slide-up flex flex-col' style={{ maxHeight: '85vh' }}>
        {/* Header */}
        <View className='flex items-center justify-between p-4 border-b border-grey-base'>
          <View className='w-8 h-8' /> {/* Placeholder for spacing */}
          <Text className='text-lg font-semibold text-grey-darkest'>{title}</Text>
          <View onClick={onClose} className='p-1'>
            <X size={24} className='text-grey-dark' />
          </View>
        </View>

        {/* Body */}
        <View className='flex-1 overflow-y-auto p-4'>
          {children}
        </View>

        {/* Footer */}
        <View className='p-4 border-t border-grey-base'>
          {footer}
        </View>
      </View>
    </View>
  );
};

// Add animation keyframes to a global stylesheet or a style tag if needed
// For Taro, it's better to define animations in a .scss file and import it.
// Example in a global .scss file:
/*
@keyframes slide-up {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
.animate-slide-up {
  animation: slide-up 0.3s ease-out forwards;
}
.animate-fade-in {
  animation: fade-in 0.3s ease-out forwards;
}
*/
