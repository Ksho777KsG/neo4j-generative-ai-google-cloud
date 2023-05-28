examples = [{
    "question": "Where are most pythonistas located?",
    "answer": """MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) MATCH (p)-[:HAS_POSITION]->(pos:Position) WHERE toLower(s.name) CONTAINS 'python' WITH pos.location AS location, COUNT(p) AS num_pythonistas ORDER BY num_pythonistas DESC RETURN location, num_pythonistas LIMIT 1"""
}, {
    "question": "How many Texas-based experts do I have on Java?",
    "answer": """MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) MATCH (p)-[:HAS_POSITION]->(pos:Position) WHERE toLower(s.name) CONTAINS 'java' AND toLower(s.level) CONTAINS 'expert' AND (toLower(pos.location) CONTAINS 'texas' OR toLower(pos.location) CONTAINS 'tx') RETURN COUNT(p)"""
}, {
    "question": "I have to fill 10 Front end roles. Who are all I have based on ideal skillsets for a front end role?",
    "answer": """MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) WHERE (toLower(s.name) CONTAINS 'html' OR toLower(s.name) CONTAINS 'css' OR toLower(s.name) CONTAINS 'javascript' OR toLower(s.name) CONTAINS 'react' OR toLower(s.name) CONTAINS 'angular') RETURN p LIMIT 10"""
}]

instr_template = """
Here are the instructions to follow:
1. Use the Neo4j schema to generate cypher compatible ONLY for Neo4j Version 5
2. Do not use EXISTS, SIZE keywords in the cypher.
3. Use only Nodes and relationships mentioned in the schema while generating the response
4. Reply ONLY in Cypher
5. Always do a case-insensitive and fuzzy search for any properties related search. Eg: to search for a Company name use `toLower(c.name) contains 'neo4j'`
6. Candidate node is synonymous to Person.
"""


template = """
Using this Neo4j schema and Reply ONLY in Cypher when it makes sense.

Schema: {text}
"""

schema = """
Nodes:
    label:'Person',id:string,role:string,description:string //Person Node
    label:'Position',id:string,title:string,location:string,startDate:string,endDate:string,url:string //Position Node
    label:'Company',id:string,name:string //Company Node
    label:'Skill',id:string,name:string,level:string //Skill Node
    label:'Education',id:string,degree:string,university:string,graduation_date:string,score:string,url:string //Education Node
Relationships:
    (:Person)-[:HAS_POSITION]->(:Position)
    (:Position)-[:AT_COMPANY]->(:Company)
    (:Person)-[:HAS_SKILL]->(:Skill)
    (:Person)-[:HAS_EDUCATION]->(:Education)
Ouput Format (Strict): //Only code as output. No other text
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) WHERE toLower(p.name) CONTAINS 'java' AND toLower(p.level) CONTAINS 'expert' RETURN COUNT(p) 

Question: How many Texas-based experts do I have on Delphi?
Answer:
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) 
MATCH (p)-[:HAS_POSITION]->(pos:Position)
WHERE toLower(s.name) CONTAINS 'delphi' AND toLower(s.level) CONTAINS 'expert' 
AND (toLower(pos.location) CONTAINS 'texas' OR toLower(pos.location) CONTAINS 'tx') RETURN COUNT(p)
Reason:
1. As per schema definition of nodes & relationships above, Person node is related to Skill node via HAS_SKILL relationship.
2. From the schema, Skill has name and levels as properties. Expertise can be checked using `level`
3. Since Texas can be denoted as TX, we search for the position's location as either 'texas' or 'tx'
4. Finally, we return the number of persons who match the input criteria using COUNT function

"""

output_fmt = """
---------------
The output should be in this JSON format:
{
  "cypher": ".."
}"""
