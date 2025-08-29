import type { StepConnection } from './StepConnection'

export interface StepConfig {
  apiUrl?: string
  prompt?: string
  [key: string]: any
}

export interface Step {
  id: string
  flow_id: string
  type: 'api_call' | 'llm_call'
  config: StepConfig | null
  pos_x: number
  pos_y: number
  created_at: string
  source_connections: StepConnection[]
  target_connections: StepConnection[]
}

export interface StepCreate {
  flow_id: string
  type: 'api_call' | 'llm_call'
  config?: StepConfig | null
  pos_x?: number
  pos_y?: number
}

export interface StepUpdate {
  type?: 'api_call' | 'llm_call'
  config?: StepConfig | null
  pos_x?: number
  pos_y?: number
}
