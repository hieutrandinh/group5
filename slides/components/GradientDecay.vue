<script setup lang="ts">
import { computed, ref } from 'vue'

// Đồ thị |gradient| ≈ γ^k (RNN) và ∏f = f^k (LSTM, đường trực tiếp) theo số bước k, thang log.
const props = withDefaults(defineProps<{ lstm?: boolean }>(), { lstm: false })

const gamma = ref(0.9)
const T = ref(50)
const f = ref(0.99)

const W = 560, H = 230, PL = 56, PB = 34, PT = 10
const LOGMIN = -12, LOGMAX = 4
const xs = (k: number) => PL + (k / T.value) * (W - PL - 10)
const ys = (v: number) => {
  const l = Math.min(LOGMAX, Math.max(LOGMIN, Math.log10(Math.max(v, 1e-300))))
  return PT + ((LOGMAX - l) / (LOGMAX - LOGMIN)) * (H - PT - PB)
}
const path = (base: number) => {
  let d = ''
  for (let k = 0; k <= T.value; k++) d += `${k ? 'L' : 'M'}${xs(k).toFixed(1)},${ys(Math.pow(base, k)).toFixed(1)}`
  return d
}
const ticks = [4, 0, -4, -8, -12]
const fmt = (v: number) => (v >= 1e4 || v < 1e-3 ? v.toExponential(1) : v.toFixed(4))
const rnnEnd = computed(() => Math.pow(gamma.value, T.value))
const lstmEnd = computed(() => Math.pow(f.value, T.value))
</script>

<template>
  <div class="gd" data-no-nav>
    <svg :viewBox="`0 0 ${W} ${H}`" class="plot">
      <g v-for="t in ticks" :key="t">
        <line :x1="PL" :x2="W - 10" :y1="ys(10 ** t)" :y2="ys(10 ** t)" class="grid" />
        <text :x="PL - 6" :y="ys(10 ** t) + 4" class="tick" text-anchor="end">1e{{ t }}</text>
      </g>
      <line :x1="PL" :x2="W - 10" :y1="ys(1)" :y2="ys(1)" class="one" />
      <text :x="(PL + W) / 2" :y="H - 4" class="tick" text-anchor="middle">số bước lan truyền ngược k (0 → T = {{ T }})</text>
      <path :d="path(gamma)" class="rnn" />
      <path v-if="props.lstm" :d="path(f)" class="lstm" />
    </svg>
    <div class="ctrl">
      <label class="crnn">RNN: γ = ‖W<sub>h</sub>‖·tanh′ = {{ gamma.toFixed(2) }}
        <input type="range" min="0.5" max="1.2" step="0.01" v-model.number="gamma"></label>
      <label v-if="props.lstm" class="clstm">LSTM: f<sub>t</sub> = {{ f.toFixed(3) }}
        <input type="range" min="0.5" max="1" step="0.001" v-model.number="f"></label>
      <label>T = {{ T }}<input type="range" min="1" max="100" step="1" v-model.number="T"></label>
      <div class="out">
        <div class="crnn">RNN: γ<sup>T</sup> = <b>{{ fmt(rnnEnd) }}</b></div>
        <div v-if="props.lstm" class="clstm">LSTM: f<sup>T</sup> = <b>{{ fmt(lstmEnd) }}</b></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gd { display: grid; grid-template-columns: 1.7fr 1fr; gap: 1rem; align-items: center; }
.plot { width: 100%; }
.grid { stroke: #e2e8f0; }
.one { stroke: #94a3b8; stroke-dasharray: 4 4; }
.tick { font-size: 11px; fill: #64748b; }
.rnn { fill: none; stroke: #ea580c; stroke-width: 3; }
.lstm { fill: none; stroke: #2563eb; stroke-width: 3; }
.ctrl { font-size: .8rem; }
.ctrl label { display: block; margin-bottom: .6rem; }
.ctrl input { width: 100%; display: block; }
.out { font-family: ui-monospace, monospace; font-size: .85rem; margin-top: .4rem; }
.crnn { color: #ea580c; } .clstm { color: #2563eb; }
</style>
