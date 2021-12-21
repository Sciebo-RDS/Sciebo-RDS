import { mount } from '@vue/test-utils'

import resources from '../fixtures/resources'
import { stubs } from '../helpers/stubs'
import { buildResource } from '@/helpers/resources'

import ListResources from '@/components/ListResources.vue'

const _resources = resources['/'].map((resource) => buildResource(resource))

describe('List resources', () => {
  it('Resets resources selection on navigation', async () => {
    const wrapper = mount(ListResources, {
      propsData: {
        resources: _resources
      },
      stubs
    })

    await wrapper.setData({ selectedResources: _resources })

    wrapper.findAll('.file-picker-resource').at(0).vm.$emit('navigate')

    // Wait twice to give the list of resources enough time to render
    await wrapper.vm.$nextTick()

    // Need to access nested array
    expect(wrapper.emitted().selectResources[0][0].length).toEqual(0)
  })
})
