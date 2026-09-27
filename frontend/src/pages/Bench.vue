<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1); const out = ref(null)
const track = ref(false); const extL = ref(0.2); const extR = ref(0.2); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  const s = await getJSON('/api/settings')
  const d = parseFloat(s.default_track_ext)
  if (!isNaN(d)) { extL.value = d; extR.value = d }
})
const num = v => { const n = parseFloat(v); return isNaN(n) ? 0 : n }
function trackQuery(){ return track.value ? `&motor_track=true&track_ext_left=${num(extL.value)}&track_ext_right=${num(extR.value)}` : '' }
function trackBody(){ return track.value ? { motor_track:true, track_ext_left:num(extL.value), track_ext_right:num(extR.value) } : {} }
async function go(save){
  err.value = ''
  try {
    out.value = save
      ? await postJSON('/api/estimate',{window_id:wid.value,fabric_id:fid.value,save:true,...trackBody()})
      : await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}${trackQuery()}`)
  } catch(e){ err.value = e.message; out.value = null }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label><input type="checkbox" v-model="track" /> 电动轨</label>
<template v-if="track">
  左外延 <input type="number" step="0.05" min="0" v-model.number="extL" style="width:5em" /> m
  右外延 <input type="number" step="0.05" min="0" v-model.number="extR" style="width:5em" /> m
</template>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="bad">{{ err }}</p>
<PanelCut v-if="out" :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" />
<p v-if="out && out.track_length != null">电动轨长 {{ out.track_length }} m（左外延 {{ out.track_ext_left }} m，右外延 {{ out.track_ext_right }} m）</p>
</div></template>
