# Ramulator: A Fast and Extensible DRAM Simulator

- **Authors**: Yoongu Kim, Weikun Yang, Onur Mutlu
- **Type**: Conference Paper (IEEE Computer Architecture Letters)
- **Year**: 2015
- **Venue**: IEEE Computer Architecture Letters, vol. 15, no. 1, pp. 45–48, 2016
- **DOI**: 10.1109/LCA.2015.2414456
- **License**: BSD
- **Status**: Open Access (author-hosted PDF)
- **Keywords**: DRAM simulation, cycle-accurate simulator, memory systems, DDR3/4, LPDDR3/4, GDDR5, HBM, RowHammer, memory controller

## Abstract

Recently, both industry and academia have proposed many different roadmaps for the future of DRAM. Consequently, there is a growing need for an extensible DRAM simulator, which can be easily modified to judge the merits of today's DRAM standards as well as those of tomorrow. In this paper, we present Ramulator, a fast and cycle-accurate DRAM simulator that is built from the ground up for extensibility. Unlike existing simulators, Ramulator is based on a generalized template for modeling a DRAM system, which is only later infused with the specific details of a DRAM standard. Thanks to such a decoupled and modular design, Ramulator is able to provide out-of-the-box support for a wide array of DRAM standards: DDR3/4, LPDDR3/4, GDDR5, WIO1/2, HBM, as well as some academic proposals (SALP, AL-DRAM, TL-DRAM, RowClone, and SARP). Importantly, Ramulator does not sacrifice simulation speed to gain extensibility: according to our evaluations, Ramulator is 2.5× faster than the next fastest simulator. Ramulator is released under the permissive BSD license.

## Key Contributions

1. Generalized template-based DRAM modeling: DRAM as a hierarchy of reconfigurable state-machines, consolidated into a single class per standard
2. Extensibility without sacrificing speed: 2.5× faster than next-fastest simulator despite highly modular design
3. Out-of-the-box support for DDR3/4, LPDDR3/4, GDDR5, WIO1/2, HBM, and academic proposals (SALP, AL-DRAM, TL-DRAM, RowClone, SARP)
4. Decoupled query/update logic from standard-specific implementation via lookup-tables
5. Open source under permissive BSD license, enabling widespread adoption
