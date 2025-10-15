import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/en/components',
    component: ComponentCreator('/en/components', 'ae8'),
    exact: true
  },
  {
    path: '/en/tokens',
    component: ComponentCreator('/en/tokens', '1b6'),
    exact: true
  },
  {
    path: '/en/',
    component: ComponentCreator('/en/', '35f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
