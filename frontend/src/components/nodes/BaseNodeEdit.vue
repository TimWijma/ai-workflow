<template>
  <Dialog
    :visible="visible"
    modal
    :header="title"
    :style="{ width: '500px' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <template #header>
      <div class="edit-header">
        <span class="edit-title">{{ title }}</span>
        <div>
          <span class="edit-id">{{ step?.id }}</span>
          <Button
            icon="pi pi-copy"
            size="small"
            variant="text"
            rounded
            aria-label="Filter"
            @click="copyStepId"
          />
        </div>
      </div>
    </template>

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

const props = defineProps<Props>()

defineEmits<{
  'update:visible': [value: boolean]
  save: []
  cancel: []
  delete: []
}>()

const copyStepId = () => {
  if (props.step) {
    navigator.clipboard.writeText(props.step.id)
  }
}
</script>

<style scoped>
.edit-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.edit-header {
  display: flex;
  flex-direction: column;
  font-weight: var(--p-dialog-title-font-weight);
  font-size: var(--p-dialog-title-font-size);
}

.edit-id {
  font-size: 0.8rem;
  opacity: 0.7;
}
</style>
