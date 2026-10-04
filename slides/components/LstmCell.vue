<script setup lang="ts">
import { computed } from 'vue'

// active: phần nào được làm nổi bật ('f' | 'i' | 'c' | 'o' | 'state' | 'all')
// values: nếu có, hiện số trên sơ đồ (dùng cho slide mô phỏng)
const props = withDefaults(defineProps<{
  active?: string
  values?: Record<string, number> | null
  width?: string
}>(), { active: 'all', values: null, width: '100%' })

const on = (k: string) => props.active === 'all' || props.active.split(',').includes(k)
const cls = (k: string) => (on(k) ? `part on ${k}` : 'part off')
const fmt = (v?: number) => (v === undefined ? '' : v.toFixed(2))
const v = computed(() => props.values || {})
</script>

<template>
  <svg viewBox="0 0 660 340" :style="{ width }" class="lstm-cell" font-family="inherit">
    <defs>
      <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="currentColor" />
      </marker>
    </defs>

    <rect x="60" y="40" width="520" height="240" rx="18" class="box" />

    <!-- cell state: băng chuyền -->
    <g :class="cls('state')">
      <line x1="10" y1="80" x2="152" y2="80" />
      <line x1="188" y1="80" x2="312" y2="80" />
      <line x1="348" y1="80" x2="645" y2="80" marker-end="url(#arr)" />
      <text x="12" y="68" class="lbl">c<tspan dy="4" style="font-size:12px;font-style:italic">t-1</tspan></text>
      <text x="612" y="68" class="lbl">c<tspan dy="4" style="font-size:12px;font-style:italic">t</tspan></text>
      <text v-if="values" x="12" y="102" class="num">{{ fmt(v.cPrev) }}</text>
      <text v-if="values" x="600" y="102" class="num">{{ fmt(v.c) }}</text>
    </g>

    <!-- đầu vào -->
    <g class="part on input">
      <line x1="10" y1="255" x2="470" y2="255" />
      <line x1="100" y1="330" x2="100" y2="255" />
      <text x="12" y="245" class="lbl">h<tspan dy="4" style="font-size:12px;font-style:italic">t-1</tspan></text>
      <text x="110" y="326" class="lbl">x<tspan dy="4" style="font-size:12px;font-style:italic">t</tspan></text>
      <text v-if="values" x="12" y="276" class="num">{{ fmt(v.hPrev) }}</text>
      <text v-if="values" x="126" y="306" class="num">{{ fmt(v.x) }}</text>
    </g>

    <!-- forget gate -->
    <g :class="cls('f')">
      <line x1="170" y1="255" x2="170" y2="218" />
      <line x1="170" y1="182" x2="170" y2="98" marker-end="url(#arr)" />
      <rect x="148" y="182" width="44" height="36" rx="6" class="gate" />
      <text x="170" y="206" class="op">σ</text>
      <circle cx="170" cy="80" r="18" class="node" />
      <text x="170" y="86" class="op">×</text>
      <text x="124" y="150" class="glbl">f<tspan dy="4" style="font-size:12px;font-style:italic">t</tspan></text>
      <text v-if="values" x="178" y="150" class="num">{{ fmt(v.f) }}</text>
    </g>

    <!-- input gate + candidate -->
    <g :class="cls('i')">
      <line x1="260" y1="255" x2="260" y2="218" />
      <rect x="238" y="182" width="44" height="36" rx="6" class="gate" />
      <text x="260" y="206" class="op">σ</text>
      <polyline points="260,182 260,140 312,140" fill="none" />
      <text x="222" y="160" class="glbl">i<tspan dy="4" style="font-size:12px;font-style:italic">t</tspan></text>
      <text v-if="values" x="210" y="130" class="num">{{ fmt(v.i) }}</text>
    </g>
    <g :class="cls('c')">
      <line x1="330" y1="255" x2="330" y2="218" />
      <rect x="300" y="182" width="60" height="36" rx="6" class="gate" />
      <text x="330" y="206" class="op small">tanh</text>
      <line x1="330" y1="182" x2="330" y2="158" />
      <text x="370" y="176" class="glbl">c̃<tspan dy="4" style="font-size:12px;font-style:italic">t</tspan></text>
      <text v-if="values" x="370" y="200" class="num">{{ fmt(v.g) }}</text>
    </g>
    <g :class="on('i') || on('c') ? 'part on ic' : 'part off'">
      <circle cx="330" cy="140" r="18" class="node" />
      <text x="330" y="146" class="op">×</text>
      <line x1="330" y1="122" x2="330" y2="98" marker-end="url(#arr)" />
    </g>
    <g :class="cls('state')">
      <circle cx="330" cy="80" r="18" class="node plus" />
      <text x="330" y="87" class="op">+</text>
    </g>

    <!-- output gate -->
    <g :class="cls('o')">
      <line x1="450" y1="255" x2="450" y2="218" />
      <rect x="428" y="182" width="44" height="36" rx="6" class="gate" />
      <text x="450" y="206" class="op">σ</text>
      <line x1="472" y1="200" x2="502" y2="200" marker-end="url(#arr)" />
      <line x1="530" y1="80" x2="530" y2="122" />
      <ellipse cx="530" cy="140" rx="30" ry="17" class="gate" />
      <text x="530" y="145" class="op small">tanh</text>
      <line x1="530" y1="157" x2="530" y2="182" />
      <circle cx="530" cy="200" r="18" class="node" />
      <text x="530" y="206" class="op">×</text>
      <polyline points="530,218 530,300 645,300" fill="none" marker-end="url(#arr)" />
      <text x="430" y="170" class="glbl">o<tspan dy="4" style="font-size:12px;font-style:italic">t</tspan></text>
      <text x="612" y="290" class="lbl">h<tspan dy="4" style="font-size:12px;font-style:italic">t</tspan></text>
      <text v-if="values" x="480" y="236" class="num">{{ fmt(v.o) }}</text>
      <text v-if="values" x="600" y="324" class="num">{{ fmt(v.h) }}</text>
    </g>
  </svg>
</template>

<style scoped>
.lstm-cell { color: var(--ink, #1f2937); display: block; margin: 0 auto; }
.box { fill: var(--cell-bg, #f1f5f9); stroke: #94a3b8; stroke-width: 1.5; }
line, polyline { stroke: currentColor; stroke-width: 2.5; }
.gate { fill: #ffffff; stroke: currentColor; stroke-width: 2; }
.node { fill: #ffffff; stroke: currentColor; stroke-width: 2; }
.op { text-anchor: middle; font-size: 20px; fill: currentColor; font-weight: 600; }
.op.small { font-size: 14px; }
.lbl { font-size: 18px; fill: currentColor; font-style: italic; }
.glbl { font-size: 18px; font-weight: 700; fill: currentColor; font-style: italic; }
.num { font-size: 14px; font-family: ui-monospace, monospace; fill: #0f172a; font-weight: 700; }
.part { transition: opacity .4s, color .4s; }
.part.off { opacity: .18; }
.part.on.f { color: #dc2626; }
.part.on.i, .part.on.c, .part.on.ic { color: #16a34a; }
.part.on.o { color: #7c3aed; }
.part.on.state { color: #2563eb; }
.part.on.input { color: #475569; }
</style>
