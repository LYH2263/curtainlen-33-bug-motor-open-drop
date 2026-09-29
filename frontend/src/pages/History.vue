<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">
<router-link :to="`/runs/${r.id}`">#{{ r.id }}</router-link> {{ r.window_name }} {{ r.result?.meters }}m
<template v-if="r.result?.motor_track"> 轨 {{ r.result.track_length ?? '—' }}m</template>
</li></ul>
<p class="hint">轨长与布米均为写入时快照；此后修改默认外延不影响历史单。</p>
</div></template>
