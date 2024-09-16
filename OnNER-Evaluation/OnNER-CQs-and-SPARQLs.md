1. Which "chemicals" are mentioned in conjunction with the term "permeability"? In which publications and paragraphs?
	
	```
	SELECT ?chemical ?paragraph ?publication WHERE {
		?pubublicationId rdf:type onner:ScholarlyPublication ;
						 onner:publicationTitle ?publication ;
						 onner:containsDocumentPart ?paragraphId .
		
		?paragraphId rdf:type onner:Paragraph ;
					 onner:paragraphText ?paragraph ;
					 onner:directlyContainsLabeledTerm ?termId1 , ?termId2 .
		
		?termId1 onner:labeledTermText 'permeability'^^xsd:string .
		
		?termId2 onner:labeledTermText ?chemical ;
				 onner:hasLabeledTermStatus ?status2 .
		?status2 onner:hasLabeledTermLabel ?labelId2 .
		?labelId2 onner:labelText 'CHEMICAL'^^xsd:string . 
	}
	```

2. Which "chemicals" are mentioned in conjunction with the "property" (label) "permeability"? In which publications and paragraphs?

SELECT ?chemical ?paragraph ?publication WHERE {
    ?pubublicationId rdf:type onner:ScholarlyPublication ;
					 onner:publicationTitle ?publication ;
					 onner:containsDocumentPart ?paragraphId .
    
    ?paragraphId rdf:type onner:Paragraph ;
				 onner:paragraphText ?paragraph ;
				 onner:directlyContainsLabeledTerm ?termId1 , ?termId2 .
    
    ?termId1 onner:labeledTermText 'permeability'^^xsd:string ;
			 onner:hasLabeledTermStatus ?status1 .
    ?status1 onner:hasLabeledTermLabel ?labelId1 .
    ?labelId1 onner:labelText 'PROPERTY'^^xsd:string . 
    
    ?termId2 onner:labeledTermText ?chemical ;
			 onner:hasLabeledTermStatus ?status2 .
    ?status2 onner:hasLabeledTermLabel ?labelId2 .
    ?labelId2 onner:labelText 'CHEMICAL'^^xsd:string . 
}



3. What are the most recent publications that mention "bacterial cellulose" or "BC nanofibers" at least three times?

SELECT ?publication ?date ?doi WHERE {    
    ?pubublicationId rdf:type onner:ScholarlyPublication ;
					 onner:publicationTitle ?publication ;
					 onner:publicationDate ?date ;
					 onner:doi ?doi ;
					 onner:containsDocumentPart ?paragraphId .
    
    ?paragraphId rdf:type onner:Paragraph ;
				 onner:directlyContainsLabeledTerm ?termId .
    
    ?termId rdf:type onner:LabeledTerm ;
			onner:labeledTermText ?term .
    
    FILTER(?term = "bacterial cellulose" || ?term = "BC nanofibers")
}
GROUP BY ?publication ?date ?doi
HAVING (COUNT(?term) >= 3)



4. Retrieve all paragraphs from publications since 2017 that include named entities labeled as "application" in conjunction with the "property" (label) "tensile strength".

SELECT DISTINCT ?term ?paragraph ?publication WHERE {
    ?publicationId rdf:type onner:ScholarlyPublication ;
                   onner:publicationTitle ?publication ;
                   onner:publicationDate ?date ;
                   onner:containsDocumentPart ?paragraphId .
    
    ?paragraphId rdf:type onner:Paragraph ;
                 onner:paragraphText ?paragraph ;
                 onner:directlyContainsLabeledTerm ?termId1 , ?termId2 .

    ?termId1 onner:labeledTermText ?term ;
         	 onner:hasLabeledTermStatus ?status1 .
    ?status1 onner:hasLabeledTermLabel ?labelId .
    ?labelId rdf:type onner:Label ;
        	 onner:labelText 'APPLICATION'^^xsd:string .
    
    ?termId2 onner:labeledTermText 'tensile strength'^^xsd:string .
    
    BIND(YEAR(?date) AS ?year)
    FILTER(?year >= 2017)
}



5. What named entities have been assigned classification labels by an NER System that have been corrected by human labelers?

SELECT ?term ?latestLabel ?previousLabel WHERE {
    ?termId rdf:type onner:LabeledTerm ;
            onner:labeledTermText ?term ;
            onner:hasLabeledTermStatus ?latestStatus .
    ?latestStatus rdf:type onner:SuggestedStatus ;
                  onner:statusAssignmentDate ?latestDate ;
                  onner:hasLabeledTermLabel ?latestLabelId .
    ?latestLabelId onner:labelText ?latestLabel .
    
    {
        SELECT ?termId (MAX(?date) AS ?maxDate) WHERE {
            ?termId rdf:type onner:LabeledTerm ;
                    onner:hasLabeledTermStatus ?status .
            ?status onner:statusAssignmentDate ?date .
        }
        GROUP BY ?termId
        HAVING (COUNT(?status) > 1)
    }
    
    FILTER (?latestDate = ?maxDate)
    
    OPTIONAL {
        ?termId onner:hasLabeledTermStatus ?previousStatus .
        ?previousStatus onner:statusAssignmentDate ?previousDate ;
                        onner:hasLabeledTermLabel ?previousLabelId .
    	?previousLabelId onner:labelText ?previousLabel .
        FILTER (?previousDate < ?latestDate)
    }
}



6. In which paragraphs appear both "nanoparticle shape" and "permeability" as entities?

SELECT DISTINCT ?paragraph ?publication WHERE {
    ?publicationId rdf:type onner:ScholarlyPublication ;
                   onner:publicationTitle ?publication ;
                   onner:containsDocumentPart ?paragraphId .
    
    ?paragraphId rdf:type onner:Paragraph ;
                 onner:paragraphText ?paragraph ;
                 onner:directlyContainsLabeledTerm ?term1 , ?term2 .
    
    ?term1 onner:labeledTermText 'nanoparticle shape'^^xsd:string .
    ?term2 onner:labeledTermText 'permeability'^^xsd:string .
}



7. Give me a list of the most frequent terms labeled as "property" from a particular publication (or all publications by a particular author).

SELECT ?term (COUNT(?term) AS ?termCount) WHERE {
    ?publicationId rdf:type onner:ScholarlyPublication ;
                   onner:publicationTitle 'How the shape of fillers affects the barrier properties of polymer/non-porous particles nanocomposites: A review'^^xsd:string .
    
    ?termID rdf:type onner:LabeledTerm ;
            onner:labeledTermText ?term ;
            onner:hasLabeledTermStatus ?status .
    
    ?status onner:hasLabeledTermLabel ?labelId .
    
    ?labelId rdf:type onner:Label ;
             onner:labelText 'PROPERTY'^^xsd:string .
}
GROUP BY ?term
ORDER BY DESC(?termCount)



8. Retrieve all paragraphs from publications containing labeled terms that include the word "cellulose".

SELECT ?term ?paragraph ?publication WHERE {
    ?publicationId rdf:type onner:ScholarlyPublication ;
                   onner:publicationTitle ?publication ;
                   onner:containsDocumentPart ?paragraphId .
    
    ?paragraphId rdf:type onner:Paragraph ;
                 onner:paragraphText ?paragraph ;
                 onner:directlyContainsLabeledTerm ?termId .
    
    ?termId onner:labeledTermText ?term .
    
    FILTER(CONTAINS(?term, 'cellulose') && ?term != 'cellulose')
}



9. Is the term "cellulose" labeled anywhere as "property"?

SELECT ?termId ?paragraph ?publication
WHERE {
    ?publicationId rdf:type onner:ScholarlyPublication ;
                   onner:publicationTitle ?publication ;
                   onner:containsDocumentPart ?paragraphId .
    
    ?paragraphId rdf:type onner:Paragraph ;
                 onner:paragraphText ?paragraph ;
                 onner:directlyContainsLabeledTerm ?termId .

    ?termId rdf:type onner:LabeledTerm ;
            onner:labeledTermText 'cellulose'^^xsd:string ;
            onner:hasLabeledTermStatus ?status .
    ?status onner:hasLabeledTermLabel ?labelId .
    ?labelId rdf:type onner:Label ;
             onner:labelText 'PROPERTY'^^xsd:string .
}



10. Which terms have been classified by some NER system using different classification labels?

SELECT ?paragraph ?term ?label1 ?label2 WHERE {
    ?publicationId rdf:type onner:ScholarlyPublication ;
                   onner:publicationTitle ?publication ;
                   onner:containsDocumentPart ?paragraphId .
    
    ?paragraphId rdf:type onner:Paragraph ;
                 onner:paragraphText ?paragraph ;
                 onner:directlyContainsLabeledTerm ?termId .
    
    ?termId rdf:type onner:LabeledTerm ;
          	onner:labeledTermText ?term ;
          	onner:hasLabeledTermStatus ?status1, ?status2 .

    ?status1 onner:statusAssignedBy ?labeler1 ;
             onner:hasLabeledTermLabel ?labelId1 .
    ?labeler1 rdf:type onner:NER_System .
    ?labelId1 onner:labelText ?label1 .

    ?status2 onner:statusAssignedBy ?labeler2 ;
             onner:hasLabeledTermLabel ?labelId2 .
    ?labeler2 rdf:type onner:NER_System .
    ?labelId2 onner:labelText ?label2 .

    FILTER(?labelId1 != ?labelId2)
    FILTER(STR(?labelId1) < STR(?labelId2))
}



11. Provide the five publications with the highest number of terms labeled as "property" in paragraphs that mention "cellulose", published in 2017 or later.

SELECT ?publication ?paragraph WHERE {
    ?publicationId rdf:type onner:ScholarlyPublication ;
                   onner:publicationTitle ?publication ;
                   onner:publicationDate ?date .
    
    {
        SELECT ?publicationId ?paragraph (COUNT(?termId1) AS ?termCount) WHERE {
        ?publicationId rdf:type onner:ScholarlyPublication ;
                       onner:containsDocumentPart ?paragraphId .

        ?paragraphId rdf:type onner:Paragraph ;
                     onner:paragraphText ?paragraph ;
                     onner:directlyContainsLabeledTerm ?termId1 , ?termId2 .

        ?termId1 onner:hasLabeledTermStatus ?status1 .
        ?status1 onner:hasLabeledTermLabel ?labelId1 .
        ?labelId1 onner:labelText 'PROPERTY'^^xsd:string .

        ?termId2 onner:labeledTermText 'cellulose'^^xsd:string .
        }
        GROUP BY ?publicationId ?paragraph
        ORDER BY DESC(COUNT(?termId1))
        LIMIT 1
    }
    BIND(YEAR(?date) AS ?year)
    FILTER(?year >= 2017)
} LIMIT 5


12. Retrieve all paragraphs where the term "tensile strength" labeled as "property" appears with the term "cellulose" in the same paragraph.

SELECT DISTINCT ?paragraph ?publication WHERE {
    ?publicationId rdf:type onner:ScholarlyPublication ;
                   onner:publicationTitle ?publication ;
                   onner:containsDocumentPart ?paragraphId .
    
    ?paragraphId rdf:type onner:Paragraph ;
                 onner:paragraphText ?paragraph ;
                 onner:directlyContainsLabeledTerm ?termId1 , ?termId2 .

    ?termId1 rdf:type onner:LabeledTerm ;
             onner:labeledTermText 'tensile strength'^^xsd:string ;
             onner:hasLabeledTermStatus ?status1 .
    ?status1 onner:hasLabeledTermLabel ?labelId1 .
    ?labelId1 onner:labelText 'PROPERTY'^^xsd:string .
    
    ?termId2 onner:labeledTermText 'cellulose'^^xsd:string .  
}



13. What are all the terms labeled as "material" in the "results" section of the paper X.

14. What is the distribution ratio of confirmed, rejected, and suggested statuses for the labeled terms in paper X?

