import { mount, createLocalVue, shallowMount } from '@vue/test-utils'

import { listResources } from '../helpers/mocks'
import { stubs } from '../helpers/stubs'

import FilePicker from '@/components/FilePicker.vue'

const localVue = createLocalVue()

localVue.prototype.$client = {
  files: {
    list: listResources
  }
}

describe('File picker', () => {
  const waitTillItemsLoaded = async (wrapper) => {
    // Wait twice to give the list of resources enough time to render
    await wrapper.vm.$nextTick()
    await wrapper.vm.$nextTick()
  }

  it('renders a list of resources', async () => {
    const wrapper = mount(FilePicker, {
      localVue,
      propsData: {
        variation: 'resource'
      },
      stubs
    })

    await waitTillItemsLoaded(wrapper)

    expect(wrapper.findAll('[filename="ownCloud Manual.pdf"]').length).toEqual(1)
  })

  it('renders the select button with the provided label', () => {
    const wrapper = mount(FilePicker, {
      localVue,
      propsData: {
        variation: 'resource',
        selectBtnLabel: 'TestLabel'
      },
      stubs
    })

    expect(wrapper.findAll('.file-picker-btn-select-resources').length).toBe(1)
    expect(wrapper.find('.file-picker-btn-select-resources').text()).toBe('TestLabel')
  })

  it('emits selected resources', async () => {
    const wrapper = mount(FilePicker, {
      localVue,
      propsData: {
        variation: 'resource'
      },
      stubs
    })

    await waitTillItemsLoaded(wrapper)

    // For test purpose set only the folder name instead of the whole object
    await wrapper.setData({ selectedResources: 'Documents' })

    // Emit click event instead of calling `trigger()` due to stubbed component
    wrapper.find('.file-picker-btn-select-resources').vm.$emit('click')

    await wrapper.vm.$nextTick()

    // Need to access nested array
    expect(wrapper.emitted().select[0][0]).toContain('Documents')
  })

  it('emits a cancel event on button click', async () => {
    const wrapper = mount(FilePicker, {
      localVue,
      propsData: {
        variation: 'resource',
        cancelBtnLabel: 'Cancel'
      },
      stubs
    })

    // Emit click event instead of calling `trigger()` due to stubbed component
    wrapper.find('.file-picker-btn-cancel').vm.$emit('click')

    await wrapper.vm.$nextTick()

    expect(wrapper.emitted().cancel).toBeTruthy()
  })

  describe('emits events after loading folders in location variant', () => {
    const createWrapper = () =>
      shallowMount(FilePicker, {
        localVue,
        propsData: {
          variation: 'location'
        },
        stubs
      })

    it('emits "update" with argument of type array', async () => {
      const wrapper = createWrapper()

      await waitTillItemsLoaded(wrapper)

      expect(Array.isArray(wrapper.emitted().update[0][0])).toBe(true)
    })

    it('emits "folderLoaded" with current folder as an argument', async () => {
      const wrapper = createWrapper()

      await waitTillItemsLoaded(wrapper)

      expect(wrapper.emitted().folderLoaded[0][0].id).toEqual('144055')
    })
  })

  describe('has focus management', () => {
    describe('initial folder load', () => {
      it('does not focus last breadcrumb item if initial focus is disabled', async () => {
        const wrapper = shallowMount(FilePicker, {
          localVue,
          propsData: {
            variation: 'resource'
          },
          stubs
        })

        wrapper.vm.$_accessibility_focusAndAnnounceBreadcrumb = jest.fn()

        await waitTillItemsLoaded(wrapper)

        expect(wrapper.vm.$_accessibility_focusAndAnnounceBreadcrumb).not.toHaveBeenCalled()
      })

      it('focuses last breadcrumb item if initial focus is disabled', async () => {
        const wrapper = shallowMount(FilePicker, {
          localVue,
          propsData: {
            variation: 'resource',
            isInitialFocusEnabled: true
          },
          stubs
        })

        wrapper.vm.$_accessibility_focusAndAnnounceBreadcrumb = jest.fn()

        await waitTillItemsLoaded(wrapper)

        expect(wrapper.vm.$_accessibility_focusAndAnnounceBreadcrumb).toHaveBeenCalled()
      })
    })
  })
})
