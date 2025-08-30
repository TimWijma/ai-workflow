import { defineStore } from 'pinia'
import { ref } from 'vue'
import type {
  Flow,
  FlowCreate,
  FlowUpdate,
  Step,
  StepCreate,
  StepUpdate,
  StepConnection,
  StepConnectionCreate,
} from '@/types'
import { Fetch } from '@/scripts/fetch'

const API_BASE = 'http://localhost:8000'

export const useFlowStore = defineStore('flow', () => {
  // State
  const steps = ref<Step[]>([])
  const stepConnections = ref<StepConnection[]>([])
  const flows = ref<Flow[]>([])
  const flowId = ref<string | null>(null)
  const flowName = ref<string>('')
  const flowResult = ref<any>(null)
  const selectedStep = ref<Step | null>(null)
  const dirty = ref<boolean>(false)
  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)

  // Actions
  const loadFlows = async (): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      const data = await Fetch.get<Flow[]>(`${API_BASE}/flows/`)
      flows.value = data
    } catch (err: any) {
      error.value = err.message || 'Failed to load flows'
      console.error('Error loading flows:', err)
    } finally {
      loading.value = false
    }
  }

  const loadFlow = async (id: string): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      const data = await Fetch.get<Flow>(`${API_BASE}/flows/${id}`)

      flowId.value = data.id
      flowName.value = data.name
      steps.value = data.steps || []

      // Extract all connections from steps
      const allConnections: StepConnection[] = []
      data.steps?.forEach((step: Step) => {
        if (step.source_connections) {
          allConnections.push(...step.source_connections)
        }
      })
      stepConnections.value = allConnections

      dirty.value = false
    } catch (err: any) {
      error.value = err.message || 'Failed to load flow'
      console.error('Error loading flow:', err)
    } finally {
      loading.value = false
    }
  }

  const saveFlow = async (): Promise<void> => {
    if (!flowId.value || !flowName.value.trim()) return

    try {
      loading.value = true
      error.value = null
      const updateData: FlowUpdate = {
        name: flowName.value.trim(),
      }

      await Fetch.put(`${API_BASE}/flows/${flowId.value}`, updateData)
      dirty.value = false
    } catch (err: any) {
      error.value = err.message || 'Failed to save flow'
      console.error('Error saving flow:', err)
    } finally {
      loading.value = false
    }
  }

  const createFlow = async (flowData: FlowCreate): Promise<string | null> => {
    try {
      loading.value = true
      error.value = null
      const data = await Fetch.post<Flow>(`${API_BASE}/flows/`, flowData)

      flows.value.push(data)
      return data.id
    } catch (err: any) {
      error.value = err.message || 'Failed to create flow'
      console.error('Error creating flow:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  const runFlow = async (): Promise<void> => {
    if (!flowId.value) return

    try {
      loading.value = true
      error.value = null

      let data = await Fetch.post(`${API_BASE}/flows/${flowId.value}/run`)

      flowResult.value = data
    } catch (err: any) {
      error.value = err.message || 'Failed to run flow'
      console.error('Error running flow:', err)
    } finally {
      loading.value = false
    }
  }

  const addStep = async (step: StepCreate): Promise<void> => {
    if (!flowId.value) return

    try {
      loading.value = true
      error.value = null
      const data = await Fetch.post<Step>(`${API_BASE}/flows/${flowId.value}/steps`, step)

      steps.value.push(data)
      dirty.value = true
    } catch (err: any) {
      error.value = err.message || 'Failed to add step'
      console.error('Error adding step:', err)
    } finally {
      loading.value = false
    }
  }

  const updateStep = async (stepId: string, stepUpdate: StepUpdate): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      console.log(stepUpdate)

      const data = await Fetch.put<Step>(`${API_BASE}/steps/${stepId}`, stepUpdate)

      const index = steps.value.findIndex((s) => s.id === stepId)
      if (index !== -1) {
        steps.value[index] = data
      }
      dirty.value = true
    } catch (err: any) {
      error.value = err.message || 'Failed to update step'
      console.error('Error updating step:', err)
    } finally {
      loading.value = false
    }
  }

  const removeStep = async (stepId: string): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      await Fetch.delete(`${API_BASE}/steps/${stepId}`)

      steps.value = steps.value.filter((s) => s.id !== stepId)
      stepConnections.value = stepConnections.value.filter(
        (c) => c.from_step_id !== stepId && c.to_step_id !== stepId,
      )

      if (selectedStep.value?.id === stepId) {
        selectedStep.value = null
      }

      dirty.value = true
    } catch (err: any) {
      error.value = err.message || 'Failed to remove step'
      console.error('Error removing step:', err)
    } finally {
      loading.value = false
    }
  }

  const addStepConnection = async (connection: StepConnectionCreate): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      const data = await Fetch.post<StepConnection>(`${API_BASE}/steps/connections`, connection)

      stepConnections.value.push(data)
      dirty.value = true
    } catch (err: any) {
      error.value = err.message || 'Failed to add connection'
      console.error('Error adding connection:', err)
    } finally {
      loading.value = false
    }
  }

  const removeStepConnection = async (connectionId: string): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      await Fetch.delete(`${API_BASE}/steps/connections/${connectionId}`)

      stepConnections.value = stepConnections.value.filter((c) => c.id !== connectionId)
      dirty.value = true
    } catch (err: any) {
      error.value = err.message || 'Failed to remove connection'
      console.error('Error removing connection:', err)
    } finally {
      loading.value = false
    }
  }

  const setSelectedStep = (step: Step | null): void => {
    selectedStep.value = step
  }

  const markDirty = (): void => {
    dirty.value = true
  }

  const clearError = (): void => {
    error.value = null
  }

  return {
    // State
    steps,
    stepConnections,
    flows,
    flowId,
    flowName,
    flowResult,
    selectedStep,
    dirty,
    loading,
    error,

    // Actions
    loadFlows,
    loadFlow,
    saveFlow,
    createFlow,
    runFlow,
    addStep,
    updateStep,
    removeStep,
    addStepConnection,
    removeStepConnection,
    setSelectedStep,
    markDirty,
    clearError,
  }
})
