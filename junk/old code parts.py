'''def add_element(self, circuit):
        try:
            if not issubclass(type(circuit), BaseCircuitElement):
                raise ValueError("Incorrect circuit type!")
        except TypeError as e:
            raise e

        self._elements.append(circuit)
        return circuit'''

'''def update(self, structure=""):
    """Updates structure state, using topology sorting"""
    if not structure:
        structure = self
    circuits = self.get_circuits_list()
    independent_circuits = []
    circuits_dependence = {}
    for circuit in circuits:
        circuits_dependence[circuit] = len(circuit.get_parent_circuits())
        if circuits_dependence[circuit] == 0:
            independent_circuits.append(circuit)

    while independent_circuits:
        circuit = independent_circuits.pop(0)
        circuit.update()
        for dependent_circuit in circuit.get_dependent_circuits():
            circuits_dependence[dependent_circuit] -= 1
            if circuits_dependence[dependent_circuit] == 0:
                independent_circuits.append(dependent_circuit)
        circuits.remove(circuit)
    for circuit in circuits:
        circuit.cycle_processing()'''
