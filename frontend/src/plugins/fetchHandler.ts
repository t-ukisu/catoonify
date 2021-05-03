import Vue from 'vue';
import FetchHandler from '@/common/libs/fetchHandler/fetchHandler';

declare module 'vue/types/vue' {
  interface Vue {
    $fetch: FetchHandler;
  }

  interface VueConstructor {
    $fetch: FetchHandler;
  }
}

const baseUrl = process.env.VUE_APP_API_URL_BASE;
Vue.use(new FetchHandler(baseUrl));
