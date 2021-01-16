import { shallowMount } from '@vue/test-utils';
import Home from '@/views/Home.vue';
import Vuetify from 'vuetify';
import Vue from 'vue';

Vue.use(Vuetify);
describe('Home.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message';
    const wrapper = shallowMount(Home, {
      propsData: { msg },
    });
    expect(wrapper.text()).toMatch(msg);
  });
});
