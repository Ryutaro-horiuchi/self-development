import { mount } from '@vue/test-utils'
import Form from '@/components/Form.vue'

test('sets the value', async () => {
  const wrapper = mount(Form)
  await wrapper.find('input').setValue('my@mail.com')
  await wrapper.find('button').trigger('click')
  expect(wrapper.emitted('submit')[0][0]).toBe('my@mail.com')
 })