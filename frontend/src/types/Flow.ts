import type { Step } from './Step'

export interface Flow {
  id: string
  name: string
  description?: string
  created_at: string
  steps: Step[]
}

export interface FlowCreate {
  name: string
  description?: string
}

export interface FlowUpdate {
  name: string
  description?: string
}
