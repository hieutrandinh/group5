<script setup lang="ts">
// Điều khiển bằng chuột: chuột trái = bước tiếp theo, chuột phải = quay lại.
// Bỏ qua khi bấm vào nút, thanh trượt, ô nhập… và vùng có data-no-nav (các demo tương tác).
import { onBeforeUnmount, onMounted } from 'vue'
import { useNav } from '@slidev/client'

const { next, prev, isPlaying, isPresenter } = useNav()

const IGNORE = 'a, button, input, select, textarea, label, [contenteditable], [data-no-nav], .slidev-nav, .slidev-icon-btn'

function skip(e: MouseEvent) {
  if (!isPlaying.value && !isPresenter.value) return true
  const t = e.target as HTMLElement | null
  if (t?.closest(IGNORE)) return true
  if (window.getSelection()?.toString()) return true
  return false
}
function onClick(e: MouseEvent) {
  if (e.button !== 0 || skip(e)) return
  next()
}
function onContext(e: MouseEvent) {
  if (skip(e)) return
  e.preventDefault()
  e.stopImmediatePropagation() // chặn menu chuột phải mặc định của Slidev
  prev()
}

// global layer có thể được mount nhiều lần (presenter mode) → chỉ gắn listener một lần
const w = window as any
onMounted(() => {
  w.__mouseNavCount = (w.__mouseNavCount || 0) + 1
  if (w.__mouseNavCount > 1) return
  window.addEventListener('click', onClick)
  window.addEventListener('contextmenu', onContext, true)
  w.__mouseNavOff = () => {
    window.removeEventListener('click', onClick)
    window.removeEventListener('contextmenu', onContext, true)
  }
})
onBeforeUnmount(() => {
  w.__mouseNavCount--
  if (w.__mouseNavCount === 0) w.__mouseNavOff?.()
})
</script>

<template><div v-if="false" /></template>
