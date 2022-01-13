import { shallowMount } from '@vue/test-utils'

import { stubs } from '../helpers/stubs'

import ListHeader from '@/components/ListHeader.vue'

const defaultProps = {
  currentFolder: {
    path: '/Documents/PDF'
  },
  isSelectBtnEnabled: true,
  isLocationPicker: false
}

describe('List header', () => {
  it('builds correct path for breadcrumbs', async () => {
    const wrapper = shallowMount(ListHeader, {
      propsData: defaultProps,
      stubs
    })

    expect(wrapper.vm.breadcrumbsItems.length).toEqual(3)
    expect(wrapper.vm.breadcrumbsItems[2].text).toEqual('PDF')
  })

  it('hides select btn if it is hidden by a prop', () => {
    const wrapper = shallowMount(ListHeader, {
      propsData: {
        ...defaultProps,
        isSelectBtnDisplayed: false
      },
      stubs
    })

    expect(wrapper.findAll('[data-testid="list-header-btn-select"]').length).toBe(0)
  })

  it('renders a cancel button if a label is provided', () => {
    const wrapper = shallowMount(ListHeader, {
      propsData: {
        ...defaultProps,
        cancelBtnLabel: 'Cancel'
      },
      stubs
    })

    expect(wrapper.find('[data-testid="list-header-btn-cancel"]').exists()).toBeTruthy()
    expect(wrapper.find('[data-testid="list-header-btn-cancel"]').text()).toBe('Cancel')
  })

  it('hides cancel button by default', () => {
    const wrapper = shallowMount(ListHeader, {
      propsData: defaultProps,
      stubs
    })

    expect(wrapper.find('[data-testid="list-header-btn-cancel"]').exists()).toBeFalsy()
  })

  it("doesn't insert last breadcrumb item as interactible element", () => {
    const wrapper = shallowMount(ListHeader, {
      propsData: defaultProps,
      stubs
    })

    expect(typeof wrapper.vm.breadcrumbsItems[0].onClick).toEqual('function')
    expect(typeof wrapper.vm.breadcrumbsItems[1].onClick).toEqual('function')
    expect(wrapper.vm.breadcrumbsItems[2].onClick).toEqual(undefined)
  })
})
