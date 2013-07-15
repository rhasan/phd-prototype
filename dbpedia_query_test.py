from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia-test.inria.fr/sparql")
sparql.setQuery("""
SELECT ?m count(?m) AS ?num
WHERE
{
	dbpedia:The_Matrix dcterms:subject ?o.
	?m dcterms:subject ?o.
	?m a dbpedia-owl:Film.
	FILTER (?m != dbpedia:The_Matrix)

}

GROUP BY ?m ORDER BY DESC(?num)
LIMIT 50
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print result["m"]["value"], result["num"]["value"]
    