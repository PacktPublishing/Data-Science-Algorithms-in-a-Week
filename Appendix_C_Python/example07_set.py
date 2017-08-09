from sets import Set

boys = Set(['Adam', 'Samuel', 'Benjamin'])
girls = Set(['Eva', 'Mary'])
teenagers = Set(['Samuel', 'Benjamin', 'Mary'])
print 'Adam' in boys
print 'Jane' in girls
girls.add('Jane')
print 'Jane' in girls
teenage_girls = teenagers & girls  # intersection
mixed = boys | girls  # union
non_teenage_girls = girls - teenage_girls  # difference
print teenage_girls
print mixed
print non_teenage_girls
