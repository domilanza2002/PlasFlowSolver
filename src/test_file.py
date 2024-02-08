import mutationpp as mpp
print("START")
mix=mpp.Mixture("nitrogen2")
print("T=" + str(mix.T()))
print("P=" + str(mix.P()))
for i in range(mix.nSpecies()):
    print("Species " + str(i) + " " + mix.speciesName(i))
print("Composition=",mix.X())
print("EQUILIBRATE")
off=0#280K
mix.equilibrate(1378.651803+off,3022.517)
print("H=" + str(mix.mixtureHMass()))
#print("E=" + str(mix.mixtureEnergyMass()))
print("HMinusH0=" + str(mix.mixtureHMinusH0Mass()))
print("H=" + str(mix.mixtureEquilibriumCpMass()*mix.T()))
exit()
print("composition=",mix.X())
# nElements
print("nElements=",mix.nElements())
#nAtoms
print("nAtoms=",mix.nAtoms())
#nMolecules
print("nMolecules=",mix.nMolecules())
#nHeavy
print("nHeavy=",mix.nHeavy())
#nSpecies
print("nSpecies=",mix.nSpecies())
#nPhases
print("nPhases=",mix.nPhases())
#nGas
print("nGas=",mix.nGas())
#nCondensed
print("nCondensed=",mix.nCondensed())
#nEnergyEqns
print("nEnergyEqns=",mix.nEnergyEqns())
#nMassEqns
print("nMassEqns=",mix.nMassEqns())
#nReactions
print("nReactions=",mix.nReactions())
#nCollisionPairs
print("nCollisionPairs=",mix.nCollisionPairs())

