<template>
  <div class="home">
    <MainFrame/>
  </div>
</template>

<script>
// @ is an alias to /src
import MainFrame from '@/components/MainFrame.vue';
import { Vue, Component } from 'vue-property-decorator';

@Component({
  components: {
    MainFrame,
  },
})
export default class Home extends Vue {
}
</script>
