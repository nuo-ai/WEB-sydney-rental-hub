import type { Meta, StoryObj } from '@storybook/vue3'
import { reactive } from 'vue'
import PropertyCard from './PropertyCard.vue'
import { usePropertiesStore } from '@/stores/properties'

const mockProperty = reactive({
  listing_id: 3102,
  rent_pw: 820,
  address: '120 Defiance Road, Zetland NSW 2017',
  suburb: 'Zetland',
  postcode: 2017,
  bedrooms: 2,
  bathrooms: 2,
  parking_spaces: 1,
  available_date: '2025-02-01',
  inspection_times: 'Saturday 11:00 - 11:20 AM',
  images: [
    'https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=900&q=80',
  ],
})

const meta: Meta<typeof PropertyCard> = {
  title: 'Components/Property/PropertyCard',
  component: PropertyCard,
  parameters: {
    layout: 'centered',
    backgrounds: { default: 'light' },
  },
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  name: '标准房源卡片',
  render: () => ({
    components: { PropertyCard },
    setup() {
      const store = usePropertiesStore() as any

      if (!store.__storybookInitializedPropertyCard) {
        store.favoriteIds = Array.isArray(store.favoriteIds) ? [...store.favoriteIds] : []
        store.favoritePropertiesData = Array.isArray(store.favoritePropertiesData)
          ? [...store.favoritePropertiesData]
          : []

        const originalToggleFavorite = store.toggleFavorite?.bind(store)
        store.toggleFavorite = (propertyOrId: any) => {
          originalToggleFavorite?.(propertyOrId)
          const id =
            typeof propertyOrId === 'object'
              ? String(propertyOrId.listing_id)
              : String(propertyOrId)
          // eslint-disable-next-line no-console
          console.log('toggleFavorite', id, store.favoriteIds)
        }

        const originalHideProperty = store.hideProperty?.bind(store)
        store.hideProperty = (id: any) => {
          originalHideProperty?.(id)
          // eslint-disable-next-line no-console
          console.log('hideProperty', id)
        }

        store.__storybookInitializedPropertyCard = true
      }

      const handleClick = (property: unknown) => {
        // eslint-disable-next-line no-console
        console.log('PropertyCard click', property)
      }

      return {
        property: mockProperty,
        handleClick,
      }
    },
    template: `
      <div style="max-width: 580px;">
        <PropertyCard :property="property" @click="handleClick" />
      </div>
    `,
  }),
}
