<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({}); const fullness = ref(2.0); const trackExt = ref(0.2); const msg = ref(''); const err = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  fullness.value = parseFloat(s.value.default_fullness) || 2.0
  trackExt.value = parseFloat(s.value.default_track_ext) || 0
})
async function save(){
  msg.value = ''; err.value = ''
  try {
    s.value = await putJSON('/api/settings', { default_fullness: fullness.value, default_track_ext: trackExt.value })
    msg.value = '已保存'
  } catch(e){ err.value = e.message }
}
</script>
<template><div class="page"><h1>设置</h1>
<p>默认褶倍 <input type="number" step="0.1" min="0" v-model.number="fullness" style="width:5em" /></p>
<p>电动轨默认外延（单侧） <input type="number" step="0.05" min="0" v-model.number="trackExt" style="width:5em" /> m</p>
<button @click="save">保存</button>
<span v-if="msg">{{ msg }}</span><p v-if="err" class="bad">{{ err }}</p>
</div></template>
