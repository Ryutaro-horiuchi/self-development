import { mount } from '@vue/test-utils'
import Counter from '@/components/Counter.vue'

test('emits an event when clicked', () => {
  const wrapper = mount(Counter)
  wrapper.get('button').trigger('click')
  wrapper.get('button').trigger('click')

  const incrementEvent = wrapper.emitted('increment')
  console.log(wrapper.vm.count)

  expect(incrementEvent[0][0]).toBe(1)
})
