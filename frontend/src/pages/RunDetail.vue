<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const props = defineProps({ id: String })
const r = ref(null)
onMounted(async () => { r.value = await getJSON(`/api/runs/${props.id}`) })
</script>
<template><div class="page" v-if="r"><h1>记录 #{{ r.id }}</h1>
<p>{{ r.window_name }} / {{ r.fabric_name }}（{{ r.created_at }}）</p>
<p>布米 {{ r.result?.meters }} m（{{ r.result?.panels }} 幅 × {{ r.result?.cut_height }} m）</p>
<p v-if="r.result?.motor_track">电动轨 {{ r.result.track_length ?? "—" }} m（左外延 {{ r.result.track_ext_left }} m，右外延 {{ r.result.track_ext_right }} m）</p>
<p v-else>未开电动轨</p>
</div></template>
