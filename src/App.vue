<template>
  <v-app>

    <v-main>
      <MainFrame/>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import MainFrame from '@/components/MainFrame.vue';

@Component({
  components: {
    MainFrame,
  },
  data: () => ({
    //
  }),
})
export default class App extends Vue {
}
</script>
