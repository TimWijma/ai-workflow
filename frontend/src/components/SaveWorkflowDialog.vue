<script setup lang="ts">
import { ref, defineEmits, watch } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'

const props = defineProps<{
  visible: boolean
}>()
const emit = defineEmits(['update:visible', 'save'])

const name = ref('')
const description = ref('')

function save() {
  emit('save', { name: name.value, description: description.value })
  emit('update:visible', false)
}
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="$emit('update:visible', $event)"
    header="Save Workflow"
    :modal="true"
  >
    <div class="p-fluid">
      <div class="p-field">
        <label for="name">Name</label>
        <InputText id="name" v-model="name" />
      </div>
      <div class="p-field">
        <label for="description">Description</label>
        <Textarea id="description" v-model="description" rows="3" />
      </div>
    </div>
    <template #footer>
      <Button
        label="Cancel"
        icon="pi pi-times"
        @click="emit('update:visible', false)"
        class="p-button-text"
      />
      <Button label="Save" icon="pi pi-check" @click="save" autofocus />
    </template>
  </Dialog>
</template>

<style scoped>
.p-field > label {
  display: block;
  margin-bottom: 0.5rem;
}
</style>
