# qcedo
Generates exact quantum circuits for exponentiating diagonal operators. Supports symbolics.

For example, here is a circuit for ![](https://latex.codecogs.com/gif.latex?e%5E%7B-i%20t%20%5Chat%7BH%7D%7D) with
<p align="center"> 
<img src="https://latex.codecogs.com/gif.latex?%5Chat%7BH%7D%3D%5Ctext%7Bdiag%7D%281%2C%202%2C%204%2C%208%2C%2016%2C%2032%2C%2064%2C%20128%29">
</p>

![circuit example](samples/example1.png)

Supply a function that maps *i → H<sub>i,i</sub>* and the program will output QASM code for the circuit implementing *e<sup>i H</sup>*.

Note this is a work in progress -- the CNOT gates still need to be optimised. Once complete, there will be at most one CNOT between any two given phase gates.

<br>

[1] J. L. Shanks, 1969, IEEE Transactions on Computers 18-5 457

[2] Jonathan Welch et al, 2014, New J. Phys. 16 033040
