<script setup lang="ts">
// Giá trị MINH HỌA (không phải số đo từ mô hình thật) cho câu ví dụ "Pháp … tiếng ___"
const words = ['Tôi', 'lớn', 'lên', 'ở', 'Pháp', ',', '…', '…', 'nên', 'tôi', 'nói', 'tiếng']
const rows = [
  { name: 'f (quên)', color: '220,38,38', v: [0.5, 0.9, 0.9, 0.9, 0.9, 0.98, 0.99, 0.99, 0.98, 0.97, 0.97, 0.95] },
  { name: 'i (ghi)', color: '22,163,74', v: [0.3, 0.1, 0.1, 0.2, 0.95, 0.05, 0.05, 0.05, 0.1, 0.1, 0.2, 0.3] },
  { name: 'o (đọc)', color: '124,58,237', v: [0.2, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.2, 0.2, 0.5, 0.95] },
]
</script>

<template>
  <table class="hm"><tbody>
    <tr><th></th><th v-for="(w, k) in words" :key="k" :class="{ key: w === 'Pháp' || w === 'tiếng' }">{{ w }}</th><th>___</th></tr>
    <tr v-for="r in rows" :key="r.name">
      <td class="nm">{{ r.name }}</td>
      <td v-for="(x, k) in r.v" :key="k" :style="{ background: `rgba(${r.color},${x})`, color: x > 0.55 ? '#fff' : '#111' }">{{ x.toFixed(2) }}</td>
      <td></td>
    </tr>
  </tbody></table>
  <div class="note">* Số liệu minh họa để giải thích ý tưởng, không phải đo từ một mô hình đã huấn luyện.</div>
</template>

<style scoped>
.hm { font-size: .72rem; border-collapse: collapse; }
.hm td, .hm th { padding: 4px 6px !important; text-align: center; border: 1px solid #e2e8f0; }
.hm th.key { color: #2563eb; font-weight: 800; }
.nm { font-weight: 700; text-align: left !important; white-space: nowrap; }
.note { font-size: .65rem; opacity: .7; margin-top: .4rem; }
</style>
