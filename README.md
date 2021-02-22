# CPF Guesser and Validator

CPF is a Python class to guess and extract information from Brazilian's CPF (person's identification) number.

## Instalation

Clone the following repository inside your project, then reference it as any other file.

```bash
git clone https://github.com/oniforo/cpf-validator.git
```

## Usage

The class contains methods for both complete (11 digits long) and incomplete CPFs.
It accepts numeric and text values where only numeric data will be taken into consideration.

### formatted_cpf
This method applied in an 11 digit CPF instance, returns a formatted string of that CPF.
```python
from cpf import CPF
obj = CPF("100 200 300 x40")
cpf = obj.formatted_cpf()
print(cpf)
# 100.200.300-40
```

### get_full_cpf
This method applied in both 9 and 10 digits CPF instances, returns the full CPF.
The 9 digit will return a validated CPF. The 10 digit, not necessarily.
```python
from cpf import CPF
obj = CPF("100 200 300")
cpf = obj.get_full_cpf()
print(cpf)
# 10020030088
```

### get_state
This method applied to an at least 9 digit long CPF instace returns the state from which the CPF was emitted.
```python
from cpf import CPF
obj = CPF("100 200 300")
cpf = obj.get_state()
print(cpf)
# RS
```

### validate_cpf
This method applied to a full CPF returns if its valid.
```python
from cpf import CPF
obj = CPF("100 200 300 40")
cpf = obj.validate_cpf()
print(cpf)
# False
```

### get_possible_cpf_values
This method receives a string of numbers and underscores (11 in total) and returns a list of all possible valid CPF combinations.
```python
from cpf import CPF
obj = CPF("100.200.30_-4_")
cpf = obj.get_possible_cpf_values()
print(cpf)
# []
```