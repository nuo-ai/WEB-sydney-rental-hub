import React from 'react';
import { View } from '@tarojs/components';

// Helper function to mimic clsx for this simple case
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
}

interface CardProps extends React.ComponentProps<typeof View> {
  children: React.ReactNode;
  className?: string;
}

const Card = React.forwardRef<typeof View, CardProps>(
  ({ className, children, ...props }, ref) => (
    <View
      ref={ref}
      className={cn(
        'bg-white border border-grey-base rounded-md shadow-DEFAULT',
        className
      )}
      {...props}
    >
      {children}
    </View>
  )
);

Card.displayName = 'Card';

export { Card };
