# Ramulator 2.0: A Modern, Modular, and Extensible DRAM Simulator

- **Authors**: Haocong Luo, Yahya Can Tuğrul, F. Nisa Bostancı, Ataberk Olgun, A. Giray Yağlıkçı, Onur Mutlu
- **Type**: Preprint (arXiv)
- **Year**: 2023
- **Venue**: arXiv:2308.11030 [cs.AR]
- **DOI**: 10.48550/arXiv.2308.11030
- **License**: MIT
- **Status**: Open Access
- **Keywords**: DRAM simulation, cycle-accurate simulator, memory controller, DDR5, LPDDR5, HBM3, GDDR6, RowHammer, memory systems

## Abstract

We present Ramulator 2.0, a highly modular and extensible DRAM simulator that enables rapid and agile implementation and evaluation of design changes in the memory controller and DRAM to meet the increasing research effort in improving the performance, security, and reliability of memory systems. Ramulator 2.0 abstracts and models key components in a DRAM-based memory system and their interactions into shared interfaces and independent implementations. Doing so enables easy modification and extension of the modeled functions of the memory controller and DRAM in Ramulator 2.0. The DRAM specification syntax of Ramulator 2.0 is concise and human-readable, facilitating easy modifications and extensions. Ramulator 2.0 implements a library of reusable templated lambda functions to model the functionalities of DRAM commands to simplify the implementation of new DRAM standards, including DDR5, LPDDR5, HBM3, and GDDR6. We showcase Ramulator 2.0's modularity and extensibility by implementing and evaluating a wide variety of RowHammer mitigation techniques that require different memory controller design changes. These techniques are added modularly as separate implementations without changing any code in the baseline memory controller implementation. Ramulator 2.0 is rigorously validated and maintains a fast simulation speed compared to existing cycle-accurate DRAM simulators. Ramulator 2.0 is open-sourced under the permissive MIT license at https://github.com/CMU-SAFARI/ramulator2.

## Key Contributions

1. Modular plugin architecture: key components modeled as shared interfaces with independent implementations
2. Concise, human-readable DRAM specification syntax using simple string literals and permuted command definitions
3. Templated lambda function library for reusable DRAM command implementations across standards (DDR5, LPDDR5, HBM3, GDDR6)
4. Drop-in RowHammer mitigation implementations (no baseline code modification required)
5. Open source under permissive MIT license
