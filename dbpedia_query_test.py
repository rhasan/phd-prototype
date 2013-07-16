from SPARQLWrapper import SPARQLWrapper, JSON
import util
sparql = SPARQLWrapper("http://dbpedia-test.inria.fr/sparql")
queryStr = """
SELECT ?m count(?m) AS ?num
WHERE
{
	<http://dbpedia.org/resource/Inception> dcterms:subject ?o.
	?m dcterms:subject ?o.
	?m a dbpedia-owl:Film.
	FILTER (?m != <http://dbpedia.org/resource/Inception>)

}

GROUP BY ?m ORDER BY DESC(?num)
LIMIT 50
""";
sparql.setQuery(queryStr)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    #print util.url_decode(result["m"]["value"]), result["num"]["value"]
    print result["m"]["value"], result["num"]["value"]
    