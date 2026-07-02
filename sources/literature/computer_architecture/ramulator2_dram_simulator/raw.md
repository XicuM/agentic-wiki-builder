1
|     | Ramulator |     |            |     | 2.0: | A   | Modern, |     |           | Modular, |     |     | and |     |     |
| --- | --------- | --- | ---------- | --- | ---- | --- | ------- | --- | --------- | -------- | --- | --- | --- | --- | --- |
|     |           |     | Extensible |     |      |     | DRAM    |     | Simulator |          |     |     |     |     |     |
Haocong Luo, Yahya Can Tug˘rul, F. Nisa Bostancı, Ataberk Olgun, A. Giray Yag˘lıkc¸ı, and Onur Mutlu
Abstract—WepresentRamulator2.0,ahighlymodularandextensibleDRAMsimulatorthatenablesrapidandagileimplementation
andevaluationofdesignchangesinthememorycontrollerandDRAMtomeettheincreasingresearcheffortinimprovingthe
performance,security,andreliabilityofmemorysystems.Ramulator2.0abstractsandmodelskeycomponentsinaDRAM-based
memorysystemandtheirinteractionsintosharedinterfacesandindependentimplementations.Doingsoenableseasymodification
andextensionofthemodeledfunctionsofthememorycontrollerandDRAMinRamulator2.0.TheDRAMspecificationsyntaxof
Ramulator2.0isconciseandhuman-readable,facilitatingeasymodificationsandextensions.Ramulator2.0implementsalibraryof
reusabletemplatedlambdafunctionstomodelthefunctionalitiesofDRAMcommandstosimplifytheimplementationofnewDRAM
standards,includingDDR5,LPDDR5,HBM3,andGDDR6.WeshowcaseRamulator2.0’smodularityandextensibilitybyimplementing
andevaluatingawidevarietyofRowHammermitigationtechniquesthatrequiredifferentmemorycontrollerdesignchanges.These
3202 voN 92  ]RA.sc[  2v03011.8032:viXra
techniquesareaddedmodularlyasseparateimplementationswithoutchangingany codeinthebaselinememorycontroller
implementation.Ramulator2.0isrigorouslyvalidatedandmaintainsafastsimulationspeedcomparedtoexistingcycle-accurate
DRAMsimulators.Ramulator2.0isopen-sourcedunderthepermissiveMITlicenseathttps://github.com/CMU-SAFARI/ramulator2.
1 INTRODUCTION Second,tofacilitateeasymodificationofDRAMspecifi-
|                |             |         |            |     |                 |            |          | cations    | (e.g.,      | DRAM organization, |            | commands,      |         | timing | con-       |
| -------------- | ----------- | ------- | ---------- | --- | --------------- | ---------- | -------- | ---------- | ----------- | ------------------ | ---------- | -------------- | ------- | ------ | ---------- |
| Cycle-accurate |             | DRAM    | simulators |     | enable modeling |            | and      |            |             |                    |            |                |         |        |            |
|                |             |         |            |     |                 |            |          | straints), | Ramulator   | 2.0                | implements |                | concise | and    | human-     |
| evaluation     | of detailed |         | operations | in  | the memory      | controller |          |            |             |                    |            |                |         |        |            |
|                |             |         |            |     |                 |            |          | readable   | definitions | of                 | DRAM       | specifications |         | on     | top of the |
| and the        | DRAM        | device. | In recent  |     | years, growing  |            | research |            |             |                    |            |                |         |        |            |
lookuptablebasedhierarchicalDRAMdevicemodelinRa-
| and design | efforts | in  | improving | the | performance, |     | security, |     |     |     |     |     |     |     |     |
| ---------- | ------- | --- | --------- | --- | ------------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
and reliability of DRAM-based memory systems require mulator1.0.Ramulator2.0’sDRAMspecifications1)arede-
a cycle-accurate simulator that facilitates rapid and agile finedwithsimplestringliterals,2)leveragepermutationsof
implementationandevaluationofintrusivedesignchanges differentDRAMcommandstoconciselydefinetimingcon-
(i.e.,modificationoffunctionalitiesofthesimulatedsystem straints,and3)usealibraryoftemplatedlambdafunctions
as opposed to simple parameter changes) in the mem- thatarereusableacrossdifferentDRAMstandardstodefine
ory controller and DRAM. Unfortunately, existing cycle- thefunctionalitiesofDRAMcommands(e.g.,thesameRFM
commandimplementationcanbe(andis)usedbyDDR5[7],
| accurate | DRAM | simulators | are | not | modular | and extensible |     |        |      |           |      |      |        |       |          |
| -------- | ---- | ---------- | --- | --- | ------- | -------------- | --- | ------ | ---- | --------- | ---- | ---- | ------ | ----- | -------- |
|          |      |            |     |     |         |                |     | LPDDR5 | [8], | and GDDR6 | [9], | HBM3 | [10]). | These | improve- |
enoughtomeetsucharequirement.
mentsareimplementedwiththenewfeaturesofC++20[11]
Weidentifytwokeyissuesinthedesignandimplemen-
(e.g.,constant-evaluatedimmediatefunctions),enablingsig-
| tation | of existing | cycle-accurate |     | DRAM | simulators. |     | First, |     |     |     |     |     |     |     |     |
| ------ | ----------- | -------------- | --- | ---- | ----------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
nificantduplicate-codereductionandeasymodificationand
| they do | not model |      | key components |     | of a         | DRAM-based |     |           |     |             |      |     |          |                 |     |
| ------- | --------- | ---- | -------------- | --- | ------------ | ---------- | --- | --------- | --- | ----------- | ---- | --- | -------- | --------------- | --- |
|         |           |      |                |     |              |            |     | extension | of  | the modeled | DRAM |     | device’s | functionalities |     |
| memory  | system    | in a | fundamentally  |     | modular way, | making     |     | it        |     |             |      |     |          |                 |     |
withoutsacrificingsimulationspeed.
| difficult | to implement |     | and maintain |     | different | intrusive | de- |     |          |     |            |     |               |     |        |
| --------- | ------------ | --- | ------------ | --- | --------- | --------- | --- | --- | -------- | --- | ---------- | --- | ------------- | --- | ------ |
|           |              |     |              |     |           |           |     | We  | showcase | the | modularity | and | extensibility |     | of Ra- |
signchanges.Forexample,USIMM[1]doesnotseparatethe
|      |               |      |     |        |             |            |     | mulator | 2.0       | by implementing |            | and        | evaluating |       | a vari- |
| ---- | ------------- | ---- | --- | ------ | ----------- | ---------- | --- | ------- | --------- | --------------- | ---------- | ---------- | ---------- | ----- | ------- |
| DRAM | specification | from | the | memory | controller. | Similarly, |     |         |           |                 |            |            |            |       |         |
|      |               |      |     |        |             |            |     | ety of  | RowHammer |                 | mitigation | techniques |            | (PARA | [12],   |
thetemplatedimplementationsoftheDRAMspecifications
|     |     |     |     |     |     |     |     | TWiCe | [13], | Graphene | [14], Hydra | [15], | Randomized |     | Row- |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | -------- | ----------- | ----- | ---------- | --- | ---- |
inRamulator[2](referredtoasRamulator1.0inthispaper)
causeundesiredcouplingbetweentheDRAMspecification Swap(RRS)[16],andanidealrefresh-basedmitigation[17])
andthememorycontroller. that require different additional functionalities in the mem-
Second, existing simulators do not implement DRAM ory controller. These RowHammer mitigations plug them-
specifications in a concise and intuitive way, making it selves into the same baseline memory controller imple-
difficult to add new DRAM commands and define new mentation without changing the memory controller’s code,
timing constraints. For example, both DRAMsim2 [3] and whichwasnotpossibleinRamulator1.0[2]andisnotpos-
DRAMsim3 [4] implement a single DRAM device model sibleinanyotherDRAMsimulatorweareawareof[1,3,4].
that aggregates all the DRAM specifications from all sup- ThekeyfeaturesandcontributionsofRamulator2.0are:
|        |      |           |     |          |            |           |     | Ramulator |     | 2.0 is a modular |     | and | extensible | DRAM | sim- |
| ------ | ---- | --------- | --- | -------- | ---------- | --------- | --- | --------- | --- | ---------------- | --- | --- | ---------- | ---- | ---- |
| ported | DRAM | standards | in  | a single | C++ class. | Ramulator |     | •         |     |                  |     |     |            |      |      |
1.0’s DRAM specifications are based on low-level and ver- ulator written in C++20 that enables rapid and agile
bose C++ syntax (e.g., it uses eight full lines of C++ code implementation and evaluation of design changes in the
tCCD_L
just to specify solely a single timing constraint in memory system. Ramulator 2.0 can either work as a
DDR4[5]). standalone simulator, or be used as a memory system
To address these issues, we present Ramulator 2.0 [6], librarybyasystemsimulator(e.g.,gem5[18],zsim[19]).
a successor to Ramulator 1.0 [2] that provides an easy- • We showcase the modularity and extensibility of Ramu-
to-use, modular, and extensible software infrastructure for lator 2.0 by implementing and evaluating six different
rapid and agile implementation and evaluation of DRAM- RowHammermitigationtechniquesaspluginstoasingle
related research and design ideas. Ramulator 2.0 has two unmodifiedmemorycontrollerimplementation.
distinguishing features. First, it implements a modular and • Ramulator 2.0 implements a wide range of new DRAM
extensiblecodeframeworkbyidentifyingandmodelingthe standards, including DDR5 [7], LPDDR5 [8], HBM3 [10],
key components in a DRAM-based memory system into and GDDR6 [9] (as well as old ones, e.g., DDR3 [20],
separateinterfacesandimplementations.Withthisframework, DDR4[5],HBM(2)[21]).
different design changes (e.g., different address mapping • Ramulator 2.0 is rigorously validated and maintains a
schemes, request scheduling policies, new DRAM stan- fastsimulationspeedcomparedtoexistingcycle-accurate
dards, RowHammer mitigations) can be implemented as DRAMsimulators.
independent implementations that share the same interface, We open-source Ramulator 2.0 [6] under the permissive
•
enablingeasymodificationandextensionofRamulator2.0. MITlicensetofacilitateandencourageopenresearchand

2
agile implementation of new ideas in memory systems. sponsiblefor1)tickingtherefreshmanager 4,whichcould
Wealsointegrateitwithgem5[18]. enqueuehigh-prioritymaintenancerequests(e.g.,refreshes)
|     |     |     |     |     |     |     | back to | the controller, |     | 2) querying |     | the request | scheduler |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------------- | --- | ----------- | --- | ----------- | --------- |
2 RAMULATOR 2.0 DESIGN FEATURES 5, which in turn consults the DRAM device model 6
|     |     |     |     |     |     |     | to decode | the best | DRAM | command |     | to issue 7 | to serve |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------- | ---- | ------- | --- | ---------- | -------- |
WewalkthroughthetwokeydesignfeaturesofRamulator
|          |              |     |       |                |     |           | a memory | request, | and | 3)  | issuing | the DRAM command |     |
| -------- | ------------ | --- | ----- | -------------- | --- | --------- | -------- | -------- | --- | --- | ------- | ---------------- | --- |
| 2.0 that | enable rapid | and | agile | implementation |     | of design |          |          |     |     |         |                  |     |
changes in the memory system. Section 2.1 introduces the 8, which updates the behavior and timing information of
high-level software architecture of Ramulator 2.0 based on the DRAM device model. Finally, the memory controller
the key concepts of interface(s) and implementation(s). Sec- executes the finished request’s callback 9 to notify the
tion 2.1.1 provides a deeper look into the modularity and frontendofthecompletionofthememoryrequest.
extensibility enabled by Ramulator 2.0 by showcasing how UserscaneasilyextendRamulator2.0withoutintrusive
|                         |           |               |     |                |                |             | changes  | to existing   | code      | by  | creating | different implementa- |           |
| ----------------------- | --------- | ------------- | --- | -------------- | -------------- | ----------- | -------- | ------------- | --------- | --- | -------- | --------------------- | --------- |
| different               | RowHammer | mitigations   |     | can all        | be implemented |             |          |               |           |     |          |                       |           |
|                         |           |               |     |                |                |             | tions of | each existing | interface |     | in three | easy steps:           | 1) create |
| as plugins              | of the    | same baseline |     | unmodified     | memory         | con-        |          |               |           |     |          |                       |           |
|                         |           |               |     |                |                |             | a new    | .cpp file,    | 2) create |     | the new  | implementation        | class     |
| troller implementation. |           | Section       |     | 2.2 introduces |                | the concise |          |               |           |     |          |                       |           |
and human-readable DRAM specification syntax of Ramu- that inherits from both the implementation base class and
lator 2.0 that facilitates easy modification and extension of theexistinginterfaceclass,and3)implementthenewfunc-
thefunctionalityoftheDRAMdevice. tionality in the new implementation class. Similarly, a new
.h
|     |     |     |     |     |     |     | interface | can be | added | simply | adding | a file containing |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------ | ----- | ------ | ------ | ----------------- | --- |
2.1 ModularandExtensibleSoftwareArchitecture
theabstractinterfaceclassdefinitions.Allinterfacesandim-
Ramulator2.0modelsallcomponentsinaDRAM-based plementations in Ramulator 2.0 register themselves to a class
memory system with two fundamental concepts, Interface registry that bookkeeps the relationship among different
andImplementation,toachievehighmodularityandextensi- interfaces and implementations. Using this registry, Ramu-
bility. An interface is an abstract C++ class defined in a .h lator 2.0 automatically recognizes and instantiates different
headerfilethatmodelsthecommonhigh-levelfunctionality implementations for each interface from a human-readable
ofacomponentasseenbyothercomponentsinthesystem. configuration file. Users do not need to manually maintain
An implementation is a concrete C++ class defined in a any boilerplate code to describe the relationships between
.cppfilethatinheritsfromaninterface,modelingtheactual interfacesandimplementations.
| behavior | of a component. |     | Components | interact |     | with each |     |     |     |     |     |     |     |
| -------- | --------------- | --- | ---------- | -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
2.1.1 MemoryControllerPlugins
| other through        | pointers | to   | each | other’s interfaces |                   | stored in |     |        |                 |     |      |              |       |
| -------------------- | -------- | ---- | ---- | ------------------ | ----------------- | --------- | --- | ------ | --------------- | --- | ---- | ------------ | ----- |
| the implementations. |          | With | such | a design,          | the functionality |           |     |        |                 |     |      |              |       |
|                      |          |      |      |                    |                   |           | We  | make a | key observation |     | that | many modeled | func- |
of a component can be easily changed by instantiating a tions in the memory controller (e.g., controller-based
different implementation for the same interface, involving RowHammer mitigations that tracks the issued activation
nochangesinthecodeofunrelatedcomponents. commands)andutilitiesneededforevaluation(e.g.,collect-
Figure 1 shows the high-level software architecture of ingstatisticsfromtheissuedDRAMcommandsandanalyz-
Ramulator 2.0 with the key interfaces we identify in a ingthememoryaccesspatterns)aretriggered(updated)by
DRAM-basedmemorysystem(darkboxes)andtheirtypical thecurrently-scheduledDRAMcommand.Toavoidhaving
implementations(lightboxes)whenmodelingaDDR5sys- manysimilarmemorycontrollerimplementationsforevery
temwithRowHammermitigation.Thearrowsillustratethe single such modeled function and utility, we model these
relationshipsamongdifferentcomponentsinthesimulated functions as plugins to the memory controller. As an ex-
system(i.e.,howtheycalleachother’sinterfacefunctions). ample, Figure 2 shows in detail how various RowHammer
We highlight the memory request path with red arrows, mitigation techniques (e.g., PARA [12], Graphene [14], Hy-
DRAMcommandpathwithbluearrows,andDRAMmain- dra[15],TRR[22,23],RFM[7])canbeimplementedassuch
tenancerequests(e.g.,refreshes)withgreenarrows.Atypi- memorycontrollerplugins.
cal execution of the simulation is as follows: First, memory update(DRAM_CMD,
|     |     |     |     |     |     |     | The | plugin interface |     | has | a simple |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | -------- | --- | --- |
requests are sent 1 from the frontend (either parsed from ADDR) function that the controller calls ( 1 in Figure 1
traces or generated by another simulator, e.g., gem5 [18]) and 2) to notify the plugin implementations about the
to the memory system, where the memory addresses are DRAM command and address issued by the memory con-
mapped 2 totheDRAMorganizationthroughtheaddress troller. The RowHammer mitigation implementation then
mapper. Then, the requests are enqueued 3 in the request updates its internal state (e.g., generates a random number
buffersoftheDRAMcontroller.TheDRAMcontrollerisre- for PARA, updates the row activation count table (bank
gem5 DRAM Memory MOP4CLXOR Generic Controller FRFCFS DDR5 All Bank PARA
Frontend Memory System Address Mapper DRAM Controller Request Scheduler DRAM Device Refresh Manager Plugin
|     | tick() | ❶send(mem_req) |     | ❷map(mem_req) |     | ❸enqueue(mem_req) |     |     |     |     |     |     |     |
| --- | ------ | -------------- | --- | ------------- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
Legend
❹tick()
| Implementation |     |     | tick() |     |     | tick() |     |     |     |     |     |     |     |
| -------------- | --- | --- | ------ | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
priority_enqueue(refresh)
Interface
decode_req
|     |     |     |     |     |     |     | ❺schedule_req() |     | ❻ (mem_req) |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ----------- | --- | --- | --- | --- |
Memory Request Path
return cmd
DRAM Command Path
|     |     |     |     |     |     |     | ❼return cmd |     | check_ready (cmd) |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----------------- | --- | --- | --- | --- |
Maintenance Request Path
➀update(cmd)
Plugin Update Path
➁priority_enqueue(victim_row_refresh)
|     |     |     |     | ❾mem_req.call_back() |     |     |     | ❽issue_cmd(cmd) |     |     |     |     |     |
| --- | --- | --- | --- | -------------------- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- |
Fig.1:High-levelsoftwarearchitectureofRamulator2.0usinganexampleDDR5systemconfiguration

3
Generic Controller idea is to define timing constraints based on the permu-
➁priority_enqueue(victim_row_refresh)
DRAM Controller Interface tation of the preceding and following DRAM commands.
➀update Doing so reduces redundant code by merging the timing
|     |     | (DRAM_CMD,ADDR) |     |     |     | ... |     |     |     |     |     |     |     |     |     |
| --- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
P lu g in PARA Graphene TRR Hydra RFM constraint definitions that have the same numerical value
|     |                             |     | In te | r fa ce                         |     |     |         |          |           |      |          |              |     |     |           |
| --- | --------------------------- | --- | ----- | ------------------------------- | --- | --- | ------- | -------- | --------- | ---- | -------- | ------------ | --- | --- | --------- |
|     |                             |     |       |                                 |     |     | but are | between  | different |      | pairs    | of preceding |     | and | following |
|     | DRAM Device Model Interface |     |       | Possible Plugin Implementations |     |     |         |          |           |      |          |              |     |     |           |
|     |                             |     |       |                                 |     |     | DRAM    | commands |           | into | a single | definition.  |     | For | example,  |
Listing2showsthedefinitionofthetimingconstraintnRCD
Fig.2:ImplementingRowHammermitigationtechniquesas
thatspecifiestheminimumdelaybetweenaprecedingACT
controllerplugins.LegendisinFigure1.
commandandeitherafollowingRDorWRcommandatthe
|     |     |     |     |     |     |     | bank | level. | With | this modeling, |     | Ramulator |     | 2.0 defines | the |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------ | ---- | -------------- | --- | --------- | --- | ----------- | --- |
activationcounter)forGrapheneandTRR(RFM),orqueries
the row count cache for Hydra). If the implementation key DDR4 timing constraints with only 32 lines of code,
detectstheneedtorefreshthepotentialRowHammervictim a 61% reduction from Ramulator 1.0’s 82 lines. Such code
rows, it calls the priority_enqueue() function (2 in deduplicationenablestheadditionofnewDRAMstandards
Figure1and2)ofthememorycontrollerinterfacetosenda inaneasierandlesserror-proneway.
high-priority refresh request for the identified victim rows, Listing2:ExampleDefinitionofTimingConstraints
readytobescheduledinthefollowingcycles,asdetermined
|     |     |     |     |     |     |     | 1   | {.level | = "bank", |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --- | --- | --- | --- | --- | --- |
by the mitigation techniques. To showcase the modularity 2 .preceding = {"ACT"}, .following = {"RD", "WR"},
|     |                   |                   |               |            |          |                  | 3       | .latency | = V("nRCD")}, |         |                |        |        |      |      |
| --- | ----------------- | ----------------- | ------------- | ---------- | -------- | ---------------- | ------- | -------- | ------------- | ------- | -------------- | ------ | ------ | ---- | ---- |
|     | and extensibility |                   | of memory     | controller | plugins, | Section          | 3.3     |          |               |         |                |        |        |      |      |
|     | provides          | a cross-sectional |               | evaluation | of       | the performance  |         |          |               |         |                |        |        |      |      |
|     |                   |                   |               |            |          |                  | Second, |          | Ramulator     |         | 2.0 implements |        | the    | DRAM | com- |
|     | overhead          | of                | six different | RowHammer  |          | mitigation tech- |         |          |               |         |                |        |        |      |      |
|     |                   |                   |               |            |          |                  | mands   | (e.g.,   | the state     | changes |                | caused | by the | DRAM | com- |
niques,allimplementedasmemorycontrollerplugins.
mandsandtheprerequisitecommandsbasedonthecurrent
2.2 ConciseandIntuitiveDRAMSpecifications state) using a library of lambda functions. These functions
areimplementedinatemplatedwaysothattheyaredefined
Ramulator2.0facilitateseasymodificationandextension
|     |     |     |     |     |     |     | only | once, | but can | be reused | many | times | for | similar | DRAM |
| --- | --- | --- | --- | --- | --- | --- | ---- | ----- | ------- | --------- | ---- | ----- | --- | ------- | ---- |
ofDRAMspecifications(e.g.,theorganizationoftheDRAM
commandsacrossdifferentstandards.Asanexample,Listing
|     | device | hierarchy, | DRAM | commands, | timing | constraints, |     |     |     |     |     |     |     |     |     |
| --- | ------ | ---------- | ---- | --------- | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3showsapartofimplementationsoftheRFMabcommand
mappingbetweenDRAMcommandsandorganizationlev-
(all-bankrefreshmanagement,whichexistsintheDDR5[7],
els)intwomajorways.First,Ramulator2.0allowstheuser
|     |             |        |     |                     |     |                | LPDDR5 | [8], | GDDR6 | [9], | and | HBM3 | [10] | standards) | that |
| --- | ----------- | ------ | --- | ------------------- | --- | -------------- | ------ | ---- | ----- | ---- | --- | ---- | ---- | ---------- | ---- |
|     | to directly | define | the | DRAM specifications |     | by their names |        |      |       |      |     |      |      |            |      |
withhuman-readablestringliterals,asListing1shows. requiresallthebankstobeclosedbeforeitcanbeissued.
|     |     |     |     |     |     |     | Listing | 3: Example |     | Implementation |     | of a DRAM | Command, |     | RFMab |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---------- | --- | -------------- | --- | --------- | -------- | --- | ----- |
Listing1:ExampleDefinitionofDRAMOrganizationandCommands
|     |     |     |     |     |     |     | (shared | across | different | DRAM | standards, |     | including | DDR5, | LPDDR5, |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------ | --------- | ---- | ---------- | --- | --------- | ----- | ------- |
GDDR6,HBM3)
| 1   | //         | Different | levels    | in the organizaton |          | hierarchy |     |          |        |         |     |     |     |     |     |
| --- | ---------- | --------- | --------- | ------------------ | -------- | --------- | --- | -------- | ------ | ------- | --- | --- | --- | --- | --- |
| 2   | inline     | static    | constexpr | ImplDef            | m_levels | = {       |     |          |        |         |     |     |     |     |     |
| 3   | "channel", |           | "rank",   | "bankgroup",       |          |           | 1   | template | <class | DRAM_t> |     |     |     |     |     |
4 "bank", "row", "column", 2 int RequireAllBanksClosed(typename DRAM_t::Node* node,
| 5   | };     |           |               |         |            |     |     | int    | cmd, | int target_id, |     | Clk_t | clk) | {   |     |
| --- | ------ | --------- | ------------- | ------- | ---------- | --- | --- | ------ | ---- | -------------- | --- | ----- | ---- | --- | --- |
| 6   | //     | Different | DRAM commands |         |            |     | 3   | // for | all  | banks {        |     |       |      |     |     |
| 7   | inline | static    | constexpr     | ImplDef | m_commands | = { | 4   | // ... |      |                |     |       |      |     |     |
8 "ACT", "PRE", "PREab", "RD", "WR", "REF" 5 if (bank->m_state == DRAM_t::m_states["Closed"]) {
| 9   | };  |         |         |              |        |     | 6   | continue; |     |     |     |     |     |     |     |
| --- | --- | ------- | ------- | ------------ | ------ | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
| 10  | //  | Mapping | between | commands and | levels |     | 7   | } else    | {   |     |     |     |     |     |     |
11 inline static const ImplLUT m_cmd_scopes = LUT ( 8 return T::m_commands["PREab"];
| 12  | m_commands, |         | m_levels,  | {                 |     |     | 9   | }      |      |     |     |     |     |     |     |
| --- | ----------- | ------- | ---------- | ----------------- | --- | --- | --- | ------ | ---- | --- | --- | --- | --- | --- | --- |
| 13  |             | {"ACT", | "row"},    | {"PRE", "bank"},  |     |     | 10  | // }   |      |     |     |     |     |     |     |
|     |             | {"RD",  | "column"}, | {"WR", "column"}, |     |     | 11  | return | cmd; |     |     |     |     |     |     |
14
| 15  |     | {"REF", | "rank"}, | {"PREab","rank"}, |     |     | 12  | };             |     |     |     |     |     |     |     |
| --- | --- | ------- | -------- | ----------------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
| 16  | }   |         |          |                   |     |     | 13  |                |     |     |     |     |     |     |     |
|     | );  |         |          |                   |     |     | 14  | // In DDR5.cpp |     |     |     |     |     |     |     |
17
|     |     |     |     |     |     |     | 15  | m_preqs[m_levels["rank"]][m_commands["RFMab"]] |     |     |     |     |     |     | =   |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
RequireAllBanksClosed<DDR5>;
Internally, Ramulator 2.0 automatically encodes these string 16 // In LPDDR5.cpp
literals into integers. These integers are used to efficiently 17 m_preqs[m_levels["rank"]][m_commands["RFMab"]] =
RequireAllBanksClosed<LPDDR5>;
index the the lookup table-based finite state machines that 18 // In GDDR6.cpp
Ramulator 2.0 uses to model the hierarchical organization 19 m_pre q s [ m _ l e v e l s [ " c h a n n e l " ] ] [ m _ c o mmands["RFMab"]] =
|     |     |     |     |     |     |     |     | R e | q u i r e A l | l B a n k s | C l o s e d | < G D D R 6 > | ;   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | ----------- | ----------- | ------------- | --- | --- | --- |
and behavior of DRAM devices, similarly to Ramulator 20 // In HBM3.cpp
1.0[2].Thisencodingisdonestaticallyatcompile-timewithin 21 m_preqs[m_levels["channel"]][m_commands["RFMab"]] =
RequireAllBanksClosed<HBM3>;
thefrequentlyqueriedandupdatedDRAMdevicemodelso
|     |     | not |     |     |     |     |     |     |     |     |     | RequireAllBanksClosed |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- |
that it does incur any run-time performance overhead Ramulator 2.0 defines a
|     |     |     | m_levels["bank"] |     |     | consteval |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ---------------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(e.g., the expression is a generic function that checks for all banks in the organiza-
expression that is evaluated to the integer “3” by the com- tion hierarchy if all of them are closed (lines 6-7). If so,
piler).Othercomponentsinthesimulatedsystemthatneed it simply returns the input command argument cmd (line
to know the DRAM device’s specifications (e.g., the orga- 12), indicating that no prerequisite command is needed
nizationoftheDRAMdevicehierarchy,DRAMcommands, for cmd. Otherwise, it returns the PREab (precharge all-
timingconstraints,themappingbetweenDRAMcommands bank) command to close all the banks first. This function
andorganizationlevels)canquerytheDRAMspecification is templated on the DRAM standard implementation (i.e.,
withstringliteralsduringinitializationtogettheunderlying the DRAM_t template parameter on line 2) so that it can
integer encoding (or an error indicating the component automatically get the correct integer encoding of the com-
is incompatible with the DRAM specification). Doing so mandsandstatesfordifferentDRAMstandardsatcompile-
completely decouples the DRAM specifications from other time.ByreusingthistemplatedfunctionindifferentDRAM
parts of the simulated system, thereby achieving higher standards (lines 16, 18, 20, and 22), implementing the pre-
modularityandextensibilitythanRamulator1.0. requisitechecksfortheRFMabcommandneedsonlyasingle
Based on these string-literal based definitions, Ramu- line of code in each standard (instead of duplicating the
lator 2.0 develops a concise and human-readable way to entireRequireAllBanksClosedfunctionforeachDRAM
modelthetimingconstraintsofDRAMcommands.Thekey standardasinRamulator1.0).

4
3 VALIDATION & EVALUATION a simplistic out-of-order core model (the complete set of
scriptsandtracestoreproducetheseexperimentsarein[6]).
3.1 ValidatingtheCorrectnessofRamulator2.0
Wemakethefollowingtwoobservations.First,alleval-
To make sure Ramulator 2.0’s memory controller and uated RowHammer mitigations (except for Ideal) cause
DRAM device model implementation is correct (i.e., the significant performance overhead compared to the ideal
DRAM commands issued by the controller obey both the mitigationast decreasestoverylowvalues.Second,for
RH
timing constraints and the state transition rules), we verify t < 50, the performance overhead of RRS becomes too
RH
the DRAM command trace against Micron’s DDR4 Verilog high for the simulation to make progress. This is because
Model [24] using a similar methodology to prior works [2– the activation caused by a row swap triggers even more
4]. To do so, we implement a DRAM command trace rowswaps,preventingDRAMfromservingmemoryaccess
recorder as a DRAM controller plugin that can store the requests.WeconcludethatexistingRowHammermitigation
issued DRAM commands with the addresses and time techniquesarenotscalableenoughtolowt RHvalues(<50).
| stamps using | the     | DDR4   | Verilog | Model’s |                  | format. | We collect |     |       |               |        |           |     |         |      |
| ------------ | ------- | ------ | ------- | ------- | ---------------- | ------- | ---------- | --- | ----- | ------------- | ------ | --------- | --- | ------- | ---- |
|              |         |        |         |         |                  |         |            | As  | such, | more research | effort | is needed | to  | develop | more |
| DRAM         | command | traces | from    | eight   | streaming-access |         | and        |     |       |               |        |           |     |         |      |
efficientandscalableRowHammermitigationtechniques.
| eight random-access                                   |     |     | synthetic | memory | traces | and | different |     |     |     |     |     |     |     |     |
| ----------------------------------------------------- | --- | --- | --------- | ------ | ------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
| intensities(i.e.,thenumberofnon-memoryinstructionsbe- |     |     |           |        |        |     |           |     | 1.0 |     |     |     |     |     |     |
SW dezilamroN 0.8
tweenmemoryinstructions).WefeedtheDRAMcommand
| trace to | the Verilog |     | Model, | configured |     | to use | the same |     | 0.6 | PARA |     |     |     |     |     |
| -------- | ----------- | --- | ------ | ---------- | --- | ------ | -------- | --- | --- | ---- | --- | --- | --- | --- | --- |
Hydra
| DRAM | organization |     | and timings | as  | we  | use in | Ramulator |     | 0.4 |     |     |     |     |     |     |
| ---- | ------------ | --- | ----------- | --- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
TWiCe-Ideal
| 2.0.Wefindnotimingorstatetransitionviolations. |     |     |     |     |     |     |     |     |     | Graphene |     |     |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
0.2 RRS
| 3.2 PerformanceofRamulator2.0 |     |     |     |     |     |     |     |     | 0    | Ideal     |     |         |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --------- | --- | ------- | --- | --- | --- |
|                               |     |     |     |     |     |     |     |     | 5000 | 2000 1000 | 500 | 200 100 | 50  | 20  | 10  |
WecomparethesimulationspeedofRamulator2.0with RowHammer Threshold (tRH)
three other cycle-accurate DRAM simulators: Ramulator Fig. 3: Performance overhead of RowHammer mitigation
1.0 [2], DRAMsim2 [3], DRAMsim3 [4], and USIMM [1]. techniquesvs.differentRowHammerthresholds
| All four   | simulators |            | are compiled | with   | gcc-12      |     | -O3, and  |     |            |     |     |     |     |     |     |
| ---------- | ---------- | ---------- | ------------ | ------ | ----------- | --- | --------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
|            |            |            |              |        |             |     |           | 4   | CONCLUSION |     |     |     |     |     |     |
| configured | with       | comparable |              | system | parameters. |     | We gener- |     |            |     |     |     |     |     |     |
ate two memory traces, one with a random access pattern WepresentRamulator2.0,amodern,modular,andextensi-
and another with a streaming access pattern, each con- ble DRAM simulator as a successor to Ramulator 1.0. We
taining five million memory requests (read-write ratio = introduce the key design features of Ramulator 2.0 and
4:1). For each simulator and trace, we run the simulation demonstrate its high modularity, extensibility, and perfor-
for each trace ten times on a machine with an Intel Xeon mance.WehopethatRamulator2.0’smodularandextensi-
Gold5118processor.Table1showstheminimum,average, blesoftwarearchitectureandconciseandintuitivemodeling
and maximum simulation runtimes across the ten runs. ofDRAMfacilitatesmoreagilememorysystemsresearch.
| We conclude |     | that, despite |     | the increased |     | modularity | and |     |     |     |     |     |     |     |     |
| ----------- | --- | ------------- | --- | ------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
REFERENCES
extensibility,Ramulator2.0achievesacomparablyfast(and
|              |            |     |       |        |       |          |        | [1] | N. Chatterjee | et al., “USIMM: | the | Utah SImulated | Memory | Module,” | in  |
| ------------ | ---------- | --- | ----- | ------ | ----- | -------- | ------ | --- | ------------- | --------------- | --- | -------------- | ------ | -------- | --- |
| even faster) | simulation |     | speed | versus | other | existing | cycle- |     |               |                 |     |                |        |          |     |
UUCS-12-002,2012.
accurate DRAM simulators. We provide the scripts, config- [2] Y.Kimetal.,“Ramulator:AFastandExtensibleDRAMSimulator,”CAL,
| urations,           | and traces |     | to reproduce | our | results | in  | Ramulator |     | 2016.                                                            |     |     |     |     |     |     |
| ------------------- | ---------- | --- | ------------ | --- | ------- | --- | --------- | --- | ---------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|                     |            |     |              |     |         |     |           | [3] | P.Rosenfeldetal.,“Dramsim2:Acycleaccuratememorysystemsimulator,” |     |     |     |     |     |     |
| 2.0’srepository[6]. |            |     |              |     |         |     |           |     | inCAL,2011.                                                      |     |     |     |     |     |     |
|                     |            |     |              |     |         |     |           | [4] | S.Lietal.,“DRAMsim3:ACycle-Accurate,Thermal-CapableDRAMSimu-     |     |     |     |     |     |     |
lator,”inCAL,2020.
Runtime(sec)
Simulator Avg.Requests/sec [5] JEDEC,JESD79-4C:DDR4SDRAMStandard,2020.
min./avg./max. [6] SAFARIResearchGroup,“Ramulator2GitHubRepository,”https://github.
(gcc-12-O3)
|              |     | Random         |     | Stream         |     | Random | Stream |     | com/CMU-SAFARI/ramulator2,2023.                             |     |     |     |     |     |     |
| ------------ | --- | -------------- | --- | -------------- | --- | ------ | ------ | --- | ----------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|              |     |                |     |                |     |        |        | [7] | JEDEC,JESD79-5:DDR5SDRAMStandard,2020.                      |     |     |     |     |     |     |
|              |     |                |     |                |     |        |        | [8] | JEDEC,JESD209-5A:LPDDR5SDRAMStandard,2020.                  |     |     |     |     |     |     |
| Ramulator2.0 |     | 50.3/50.6/51.4 |     | 26.1/26.2/26.4 |     | 98.8K  | 190.8K |     |                                                             |     |     |     |     |     |     |
|              |     |                |     |                |     |        |        | [9] | JEDEC,JESD250C:GraphicsDoubleDataRate6(GDDR6)Standard,2021. |     |     |     |     |     |     |
Ramulator1.0 58.2/59.0/62.3 31.7/31.9/33.0 84.7K 156.7K [10] JEDEC,JESD238A:HighBandwidthMemory(HBM3)DRAM,2023.
DRAMsim3 51.4/51.7/52.3 37.5/37.8/38.6 96.7K 132.3K [11] ISO,ISO/IEC14882:2020Programminglanguages—C++.
DRAMsim2 51.6/51.9/52.4 53.7/53.9/54.1 96.3K 92.8K [12] Y. Kim et al., “Flipping Bits in Memory Without Accessing Them: An
USIMM 402.9/407.0/410.0 31.2/31.3/31.4 12.3K 159.7K ExperimentalStudyofDRAMDisturbanceErrors,”inISCA,2014.
|     |     |     |     |     |     |     |     | [13] | E. Lee | et al., “TWiCe: | Preventing | Row-Hammering |     | by Exploiting | Time |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | ------ | --------------- | ---------- | ------------- | --- | ------------- | ---- |
WindowCounters,”inISCA,2019.
TABLE1:SimulationPerformanceComparison
|     |     |     |     |     |     |     |     | [14] | Y.Parketal.,“Graphene:StrongyetLightweightRowHammerProtection,” |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
inMICRO,2020.
3.3 Cross-SectionalStudyofRowHammerMitigations [15] M. Qureshi et al., “Hydra: Enabling Low-Overhead Mitigation of Row-
HammeratUltra-LowThresholdsviaHybridTracking,”inISCA,2022.
|     |     |     |     |     |     |     |     |     |     | et al., |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
To demonstrate the modularity and extensibility of [16] G. Saileshwar “Randomized Row-Swap: Mitigating Row Hammer
byBreakingSpatialCorrelationBetweenAggressorandVictimRows,”in
| Ramulator | 2.0, | we  | implement | six | different | RowHammer |     |     | ASPLOS,2022. |     |     |     |     |     |     |
| --------- | ---- | --- | --------- | --- | --------- | --------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- |
mitigation techniques, PARA [12], an idealized version of [17] J. S. Kim et al., “Revisiting RowHammer: An Experimental Analysis of
ModernDevicesandMitigationTechniques,”inISCA,2020.
| TWiCe [13], | Graphene |     | [14], | Hydra | [15], Randomized |     | Row- |      |               |         |           |            |         |         |       |
| ----------- | -------- | --- | ----- | ----- | ---------------- | --- | ---- | ---- | ------------- | ------- | --------- | ---------- | ------- | ------- | ----- |
|             |          |     |       |       |                  |     |      | [18] | J. Lowe-Power | et al., | “The gem5 | simulator: | Version | 20.0+,” | 2020, |
Swap (RRS) [16], and an ideal refresh-based mitigation arXiv:2007.03152[cs.AR].
|               |     |     |       |            |     |                 |     | [19] | D.SanchezandC.Kozyrakis,“Zsim:Fastandaccuratemicroarchitectural |     |     |     |     |     |     |
| ------------- | --- | --- | ----- | ---------- | --- | --------------- | --- | ---- | --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
| (Ideal) [17]. | All | of  | these | mechanisms |     | are implemented |     |      |                                                                 |     |     |     |     |     |     |
simulationofthousand-coresystems,”inISCA,2013.
in the form of memory controller plugins as described [20] JEDEC,JESD79-3:DDR3SDRAMStandard,2012.
in Section 2.1.1. Figure 3 shows the performance overhead [21] JEDEC,JESD235D:HighBandwidthMemoryDRAM(HBM1,HBM2),2021.
|           |         |            |     |      |          |               |     | [22] | P. Frigo | et al., “TRRespass: | Exploiting | the Many | Sides | of Target | Row |
| --------- | ------- | ---------- | --- | ---- | -------- | ------------- | --- | ---- | -------- | ------------------- | ---------- | -------- | ----- | --------- | --- |
| (weighted | speedup | normalized |     | to a | baseline | configuration |     |      |          |                     |            |          |       |           |     |
Refresh,”inS&P,2020.
running the same workloads without any RowHammer [23] H. Hassan et al., “Uncovering in-DRAM RowHammer Protection Mecha-
nisms:ANewMethodology,CustomRowHammerPatterns,andImplica-
| mitigation, | y-axis) | of  | different | RowHammer |     | mitigations | as  |     |     |     |     |     |     |     |     |
| ----------- | ------- | --- | --------- | --------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tions,”inMICRO,2021.
the RowHammer threshold (i.e., the minimum number of [24] Micron Technology, “Micron DDR4 Verilog Model,” https://media-
DRAM row activations to cause at least one bitflip, t RH, x- www.micron.com/-/media/client/global/documents/products/sim-
|                 |     |      |      |           |     |        |           |      | model/dram/ddr4/ddr4                                         |     | verilog | models.zip,2018. |     |     |     |
| --------------- | --- | ---- | ---- | --------- | --- | ------ | --------- | ---- | ------------------------------------------------------------ | --- | ------- | ---------------- | --- | --- | --- |
| axis) decreases |     | from | 5000 | to 10. We | use | traces | generated |      |                                                              |     |         |                  |     |     |     |
|                 |     |      |      |           |     |        |           | [25] | StandardPerformanceEvaluationCorp.,“SPECCPU2006,”http://www. |     |         |                  |     |     |     |
from SPEC2006 [25] and SPEC2017 [26] to form 25 four- spec.org/cpu2006/.
|                      |     |     |           |     |      |         |         | [26] | StandardPerformanceEvaluationCorp.,“SPECCPU2017,”http://www. |     |     |     |     |     |     |
| -------------------- | --- | --- | --------- | --- | ---- | ------- | ------- | ---- | ------------------------------------------------------------ | --- | --- | --- | --- | --- | --- |
| core multiprogrammed |     |     | workloads |     | that | we feed | through |      |                                                              |     |     |     |     |     |     |
spec.org/cpu2017/.
