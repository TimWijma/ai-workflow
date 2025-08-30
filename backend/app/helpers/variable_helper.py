from typing import Dict, List
import uuid

class VariableHelper:
    def __init__(self):
        # Each node's output variables
        self.variable_outputs: Dict[uuid.UUID, Dict[str, str]] = {}
        # Each node's input variables
        self.variable_inputs: Dict[uuid.UUID, Dict[str, str]] = {}

    def update_output_variables(self, step_id: uuid.UUID, variables: Dict[str, str], response: Dict[str, str]):
        for variable in variables:
            if variable in response:
                self.set_output_variable(step_id, variable, response[variable])

    def set_output_variable(self, step_id: uuid.UUID, variable_name: str, value: str):
        if step_id not in self.variable_outputs:
            self.variable_outputs[step_id] = {}
        self.variable_outputs[step_id][variable_name] = value

    def get_output_variables(self, step_id: uuid.UUID) -> Dict[str, str]:
        return self.variable_outputs.get(step_id, {})

    def update_input_variables(self, step_id: uuid.UUID, mappings: List[Dict[str, str]]) -> Dict[tuple[str, str], str]:
        for mapping in mappings:
            source_step_id = mapping.get("source_node")
            field = mapping.get("field")

            if source_step_id and field:
                source_step_id = uuid.UUID(source_step_id)
                self.set_input_variable(step_id, source_step_id, field)

    def set_input_variable(self, current_step_id: uuid.UUID, source_node_id: uuid.UUID, variable_name: str):
        if current_step_id not in self.variable_inputs:
            self.variable_inputs[current_step_id] = {}
        self.variable_inputs[current_step_id][source_node_id] = variable_name

    def get_input_variables(self, step_id: uuid.UUID) -> Dict[str, str]:
        return self.variable_inputs.get(step_id, {})

    def replace_input_variables(self, step_id: uuid.UUID, text: str) -> str:
        input_variables = self.get_input_variables(step_id)

        for source_node, var_name in input_variables.items():
            output_variables = self.get_output_variables(source_node)
            if var_name in output_variables:
                value = output_variables[var_name]
                text = text.replace(f"{{{{{str(source_node)}.{var_name}}}}}", str(value))
        return text