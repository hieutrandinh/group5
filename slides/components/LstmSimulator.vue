<script setup lang="ts">
import { computed, ref } from 'vue'
import LstmCell from './LstmCell.vue'

// LSTM vô hướng (hidden size = 1), trọng số cố định để cả lớp tính tay được:
// f = σ(0.5h + 3x + 3)   i = σ(0.5h + 4x − 3)   c̃ = tanh(0.5h + 2x)   o = σ(0.5h + x + 1)
const sig = (z: number) => 1 / (1 + Math.exp(-z))

const x = ref(2)
const hPrev = ref(0)
const cPrev = ref(0)
const manual = ref(false)
const fM = ref(0.9)
const iM = ref(0.5)
const oM = ref(0.8)

const sequence = [2, 0, 0, 0, -2, 0]
const stepIdx = ref(0)
const history = ref<{ x: number; f: number; i: number; c: number; h: number }[]>([])

const r = computed(() => {
  const h0 = hPrev.value, x0 = x.value
  const f = manual.value ? fM.value : sig(0.5 * h0 + 3 * x0 + 3)
  const i = manual.value ? iM.value : sig(0.5 * h0 + 4 * x0 - 3)
  const g = Math.tanh(0.5 * h0 + 2 * x0)
  const o = manual.value ? oM.value : sig(0.5 * h0 + x0 + 1)
  const c = f * cPrev.value + i * g
  const h = o * Math.tanh(c)
  return { x: x0, hPrev: h0, cPrev: cPrev.value, f, i, g, o, c, h }
})

function step() {
  if (stepIdx.value >= sequence.length) return
  if (stepIdx.value > 0) { hPrev.value = r.value.h; cPrev.value = r.value.c }
  x.value = sequence[stepIdx.value]
  stepIdx.value++
  const s = r.value
  history.value.push({ x: s.x, f: s.f, i: s.i, c: s.c, h: s.h })
}
function reset() {
  stepIdx.value = 0; history.value = []
  x.value = 2; hPrev.value = 0; cPrev.value = 0; manual.value = false
}
const f2 = (n: number) => n.toFixed(2)
</script>

<template>
  <div class="sim" data-no-nav>
    <div class="left">
      <LstmCell :values="r" />
      <div class="eqs">
        <div><b class="cf">f</b> = σ(0.5·{{ f2(r.hPrev) }} + 3·{{ f2(r.x) }} + 3) = <b class="cf">{{ f2(r.f) }}</b><span v-if="manual"> (chỉnh tay)</span></div>
        <div><b class="ci">i</b> = σ(0.5·{{ f2(r.hPrev) }} + 4·{{ f2(r.x) }} − 3) = <b class="ci">{{ f2(r.i) }}</b><span v-if="manual"> (chỉnh tay)</span></div>
        <div><b class="ci">c̃</b> = tanh(0.5·{{ f2(r.hPrev) }} + 2·{{ f2(r.x) }}) = <b class="ci">{{ f2(r.g) }}</b></div>
        <div><b class="cs">c</b> = {{ f2(r.f) }}·{{ f2(r.cPrev) }} + {{ f2(r.i) }}·{{ f2(r.g) }} = <b class="cs">{{ f2(r.c) }}</b></div>
        <div><b class="co">h</b> = {{ f2(r.o) }}·tanh({{ f2(r.c) }}) = <b class="co">{{ f2(r.h) }}</b></div>
      </div>
    </div>
    <div class="right">
      <label>x<sub>t</sub> = {{ f2(x) }}<input type="range" min="-2" max="2" step="0.1" v-model.number="x"></label>
      <label>h<sub>t-1</sub> = {{ f2(hPrev) }}<input type="range" min="-1" max="1" step="0.05" v-model.number="hPrev"></label>
      <label>c<sub>t-1</sub> = {{ f2(cPrev) }}<input type="range" min="-2" max="2" step="0.05" v-model.number="cPrev"></label>
      <label class="chk"><input type="checkbox" v-model="manual"> Chỉnh trực tiếp các cổng</label>
      <template v-if="manual">
        <label class="cf">f = {{ f2(fM) }}<input type="range" min="0" max="1" step="0.01" v-model.number="fM"></label>
        <label class="ci">i = {{ f2(iM) }}<input type="range" min="0" max="1" step="0.01" v-model.number="iM"></label>
        <label class="co">o = {{ f2(oM) }}<input type="range" min="0" max="1" step="0.01" v-model.number="oM"></label>
      </template>
      <div class="btns">
        <button @click="step" :disabled="stepIdx >= sequence.length">Step ▶ ({{ stepIdx }}/{{ sequence.length }})</button>
        <button @click="reset">Reset</button>
      </div>
      <div class="seq">Chuỗi: x = [{{ sequence.join(', ') }}]</div>
      <table v-if="history.length"><tbody>
        <tr><th>t</th><th>x</th><th class="cf">f</th><th class="ci">i</th><th class="cs">c</th></tr>
        <tr v-for="(s, k) in history" :key="k">
          <td>{{ k + 1 }}</td><td>{{ s.x }}</td><td>{{ f2(s.f) }}</td><td>{{ f2(s.i) }}</td><td><b>{{ f2(s.c) }}</b></td>
        </tr>
      </tbody></table>
    </div>
  </div>
</template>

<style scoped>
.sim { display: grid; grid-template-columns: 1.55fr 1fr; gap: 1rem; font-size: 0.8rem; }
.eqs { font-family: ui-monospace, monospace; font-size: 0.72rem; line-height: 1.5; margin-top: .3rem; }
.right label { display: block; margin-bottom: .35rem; }
.right input[type=range] { width: 100%; display: block; }
.chk { margin-top: .4rem; }
.btns { display: flex; gap: .5rem; margin: .5rem 0 .3rem; }
button { padding: .2rem .7rem; border-radius: 6px; background: #2563eb; color: white; }
button:disabled { opacity: .4; }
button + button { background: #64748b; }
.seq { font-family: ui-monospace, monospace; font-size: .7rem; opacity: .8; }
table { font-size: .7rem; margin-top: .3rem; }
td, th { padding: 1px 6px !important; }
.cf { color: #dc2626; } .ci { color: #16a34a; } .co { color: #7c3aed; } .cs { color: #2563eb; }
</style>
