export interface StepConnection {
  id: string
  from_step_id: string
  to_step_id: string
}

export interface StepConnectionCreate {
  from_step_id: string
  to_step_id: string
}
