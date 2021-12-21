import { createLocalVue, mount } from '@vue/test-utils'
import HelloWorld from '@/components/HelloWorld.vue'
import Vuetify from 'vuetify'

describe('HelloWorld.vue', () => {
  let localVue
  let vuetify

  beforeEach(() => {
    localVue = createLocalVue()
    vuetify = new Vuetify()
  })

  it('should work', () => {
    const wrapper = mount(HelloWorld, {
      localVue,
      vuetify,
    })

    expect(wrapper.html()).toMatchSnapshot()
  })
})

