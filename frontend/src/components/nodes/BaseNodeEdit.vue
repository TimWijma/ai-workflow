<template>
  <Dialog
    :visible="visible"
    modal
    :header="title"
    :style="{ width: '500px' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <div class="edit-dialog-content">
      <slot />
    </div>

    <template #footer>
      <Button label="Delete" severity="danger" @click="$emit('delete')" />
      <Button label="Cancel" severity="secondary" @click="$emit('cancel')" />
      <Button label="Save" @click="$emit('save')" />
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import type { Step } from '@/types'

interface Props {
  visible: boolean
  title: string
  step: Step | null
}

defineProps<Props>()

defineEmits<{
  'update:visible': [value: boolean]
  save: []
  cancel: []
  delete: []
}>()
</script>

<style scoped>
.edit-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
