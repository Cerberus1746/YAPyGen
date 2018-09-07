def gene_based(specie, handler):
    from yapygen.genes import gene
    from yapygen.genes import gene_group

    if type(handler) not in (gene.Gene, gene_group.GeneGroup):
        handler = gene.Gene(handler)
    specie.fitness = specie.genes.count(handler)


def group_based(specie, handler):
    for groupName, group in specie.groups.items():
        specie.fitness += group.genes.count(handler.get(groupName, 0))
