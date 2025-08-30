import type { StepConnection } from './StepConnection'

export enum StepType {
  API_CALL = 'api_call',
  LLM_CALL = 'llm_call',
}

export interface Step {
  id: string
  flow_id: string
  type: StepType
  config: StepConfig | null
  pos_x: number
  pos_y: number
  created_at: string
  source_connections: StepConnection[]
  target_connections: StepConnection[]
}

export interface StepCreate {
  flow_id: string
  type: StepType
  config?: StepConfig | null
  pos_x?: number
  pos_y?: number
}

export interface StepUpdate {
  type?: StepType
  config?: StepConfig | null
  pos_x?: number
  pos_y?: number
}

export type StepConfig = ApiNodeConfig | LlmNodeConfig

export interface ApiNodeConfig {
  apiUrl?: string
  method?: string
  data?: any
}

export interface LlmNodeConfig {
  prompt?: string
  model?: string
  temperature?: number
}
