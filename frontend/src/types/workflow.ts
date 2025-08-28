export interface Step {
  id: number;
  type: string;
  label: string;
  config: any;
  pos_x: number;
  pos_y: number;
}

export interface StepConnection {
  id?: number;
  from_step_id: number;
  to_step_id: number;
}

export interface Flow {
  id?: number;
  name: string;
  description: string;
  steps: Step[];
  connections: StepConnection[];
}
