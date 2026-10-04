<script setup lang="ts">
import { computed, ref } from 'vue'
import data from '../data/compare.json'

// Loss curve RNN vs LSTM trên Adding Problem (số liệu thật, sinh bởi experiment/compare_rnn_lstm.py)
const T = ref('100')
const showRnn = ref(true)
const showLstm = ref(true)

const W = 600, H = 260, PL = 50, PB = 36, PT = 22, PR = 24
const YMAX = 0.25
const run = computed(() => (data as any).runs[T.value])
const steps = (data as any).config.steps
const baseline = (data as any).config.baseline_mse
const xs = (s: number) => PL + (s / steps) * (W - PL - PR)
const ys = (v: number) => PT + (1 - Math.min(v, YMAX) / YMAX) * (H - PT - PB)
const path = (curve: number[][]) => curve.map((p, k) => `${k ? 'L' : 'M'}${xs(p[0]).toFixed(1)},${ys(p[1]).toFixed(1)}`).join('')
const yticks = [0, 0.05, 0.1, 0.15, 0.2, 0.25]
const xticks = computed(() => [0, 1, 2, 3, 4].map(k => Math.round((steps * k) / 4)))
</script>

<template>
  <div class="cc" data-no-nav>
    <svg :viewBox="`0 0 ${W} ${H}`" class="plot">
      <g v-for="t in yticks" :key="t">
        <line :x1="PL" :x2="W - PR" :y1="ys(t)" :y2="ys(t)" class="grid" />
        <text :x="PL - 6" :y="ys(t) + 4" class="tick" text-anchor="end">{{ t.toFixed(2) }}</text>
      </g>
      <text v-for="s in xticks" :key="s" :x="xs(s)" :y="H - PB + 16" class="tick" text-anchor="middle">{{ s }}</text>
      <text :x="(PL + W) / 2" :y="H - 2" class="tick" text-anchor="middle">bước huấn luyện</text>
      <text :x="PL" :y="PT - 10" class="tick" text-anchor="middle">MSE</text>
      <line :x1="PL" :x2="W - PR" :y1="ys(baseline)" :y2="ys(baseline)" class="base" />
      <text :x="W - PR - 4" :y="ys(baseline) - 6" class="tick" text-anchor="end">đoán bừa ≈ 0.167</text>
      <path v-if="showRnn" :d="path(run.rnn.curve)" class="rnn" />
      <path v-if="showLstm" :d="path(run.lstm.curve)" class="lstm" />
    </svg>
    <div class="ctrl">
      <div class="seg">
        <button :class="{ sel: T === '10' }" @click="T = '10'">T = 10</button>
        <button :class="{ sel: T === '100' }" @click="T = '100'">T = 100</button>
      </div>
      <label class="crnn"><input type="checkbox" v-model="showRnn"> RNN</label>
      <label class="clstm"><input type="checkbox" v-model="showLstm"> LSTM</label>
      <table><tbody>
        <tr><th></th><th>Test MSE</th><th>Tham số</th><th>Thời gian</th></tr>
        <tr class="crnn"><td>RNN</td><td>{{ run.rnn.test_mse.toFixed(4) }}</td><td>{{ run.rnn.params }}</td><td>{{ run.rnn.seconds }}s</td></tr>
        <tr class="clstm"><td>LSTM</td><td>{{ run.lstm.test_mse.toFixed(4) }}</td><td>{{ run.lstm.params }}</td><td>{{ run.lstm.seconds }}s</td></tr>
      </tbody></table>
    </div>
  </div>
</template>

<style scoped>
.cc { display: grid; grid-template-columns: 1.7fr 1fr; gap: 1rem; align-items: center; }
.plot { width: 100%; }
.grid { stroke: #e2e8f0; }
.base { stroke: #64748b; stroke-dasharray: 5 4; }
.tick { font-size: 11px; fill: #64748b; }
.rnn { fill: none; stroke: #ea580c; stroke-width: 2.5; }
.lstm { fill: none; stroke: #2563eb; stroke-width: 2.5; }
.ctrl { font-size: .8rem; }
.ctrl label { display: block; margin: .2rem 0; }
.seg { display: flex; gap: .4rem; margin-bottom: .5rem; }
.seg button { padding: .2rem .7rem; border-radius: 6px; border: 1px solid #94a3b8; }
.seg button.sel { background: #2563eb; color: #fff; border-color: #2563eb; }
table { font-size: .7rem; margin-top: .5rem; }
td, th { padding: 2px 6px !important; }
.crnn { color: #ea580c; } .clstm { color: #2563eb; }
</style>
