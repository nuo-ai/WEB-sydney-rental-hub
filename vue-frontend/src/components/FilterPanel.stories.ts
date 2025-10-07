import type { Meta, StoryObj } from '@storybook/vue3'
import { ref } from 'vue'
import FilterPanel from './FilterPanel.vue'
import { usePropertiesStore } from '@/stores/properties'

const sampleAreas = [
  {
    id: 'suburb_ULTIMO',
    type: 'suburb',
    name: 'Ultimo',
    postcode: '2007',
    fullName: 'Ultimo NSW 2007',
  },
  {
    id: 'suburb_ZETLAND',
    type: 'suburb',
    name: 'Zetland',
    postcode: '2017',
    fullName: 'Zetland NSW 2017',
  },
  {
    id: 'suburb_CHATSWOOD',
    type: 'suburb',
    name: 'Chatswood',
    postcode: '2067',
    fullName: 'Chatswood NSW 2067',
  },
  {
    id: 'suburb_EPPING',
    type: 'suburb',
    name: 'Epping',
    postcode: '2121',
    fullName: 'Epping NSW 2121',
  },
]

const meta: Meta<typeof FilterPanel> = {
  title: 'Components/Filter/FilterPanel',
  component: FilterPanel,
  parameters: {
    layout: 'fullscreen',
  },
}
export default meta

type Story = StoryObj<typeof meta>

export const DefaultOpen: Story = {
  name: '移动筛选面板',
  render: () => ({
    components: { FilterPanel },
    setup() {
      const visible = ref(true)
      const store = usePropertiesStore() as any

      if (!store.__storybookInitializedFilterPanel) {
        store.$patch((state: any) => {
          state.selectedLocations = []
          state.draftSelectedLocations = []
          state.currentFilterParams = {}
          state.previewDraftSections = {}
          state.totalCount = 256
        })

        store.currentFilters = {}
        store.getAllAreas = async () => sampleAreas
        store.getFilteredCount = async () => 256
        store.applyFiltersFromDraft = async (draft: unknown) => {
          // eslint-disable-next-line no-console
          console.log('applyFiltersFromDraft', draft)
        }
        store.getAllAreas?.()
        store.__storybookInitializedFilterPanel = true
      }

      const handleVisibility = (value: boolean) => {
        visible.value = value
      }

      const handleFiltersChanged = (draft: unknown) => {
        // eslint-disable-next-line no-console
        console.log('filtersChanged', draft)
      }

      return {
        visible,
        handleVisibility,
        handleFiltersChanged,
      }
    },
    template: `
      <div style="min-height: 720px; background: var(--color-bg-page); padding: 24px; display:flex; justify-content:flex-end;">
        <FilterPanel
          v-model="visible"
          @update:modelValue="handleVisibility"
          @filtersChanged="handleFiltersChanged"
        />
      </div>
    `,
  }),
}
