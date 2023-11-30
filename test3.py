from rdflib import Graph, Literal, Namespace, RDF
from rdflib.plugins.sparql import prepareQuery

if __name__ == "__main__":
    # Load the RDF data from the file
    g = Graph()
    g.parse("film_data_updated.rdf", format="turtle")

    # Define a namespace for our data
    ns = Namespace("http://example.org/films/")

    # Get user inputs for genre, release year, and actor
    user_genre = input("Enter the genre you're interested in (press Enter to skip): ").strip()
    user_release_year = input("Enter the release year you're interested in (press Enter to skip): ").strip()
    user_actor = input("Enter the lead actor you're interested in (press Enter to skip): ").strip()

    # Define a SPARQL query to get movies based on user inputs
    query_str = f"""
        PREFIX ns: <http://example.org/films/>
        SELECT ?title ?year ?director ?leadActor ?leadActress ?runningTime
        WHERE {{
            ?movie ns:title ?title ;
                   ns:releaseYear ?year ;
                   {f'ns:genre "{user_genre}" ;' if user_genre else ''}
                   ns:runningTime ?runningTime ;
                   ns:director ?director ;
                   ns:leadActor ?leadActor ;
                   ns:leadActress ?leadActress .
            {f'FILTER(?year > {user_release_year} || !BOUND(?year))' if user_release_year else ''}
            {f'FILTER(CONTAINS(?leadActor, "{user_actor}") || !BOUND(?leadActor))' if user_actor else ''}
        }}
    """

    query = prepareQuery(query_str, initNs={"ns": ns})

    # Execute the query and print the results
    results = list(g.query(query))

    if not results and (user_genre or user_release_year or user_actor):
        print("No results found.")
    else:
        print("\nResults:")
        print("{:<20} {:<10} {:<20} {:<20} {:<20} {:<15}".format("Title", "Release Year", "Director", "Lead Actor", "Lead Actress", "Running Time"))
        print("-" * 110)
        for row in results:
            print("{:<20} {:<10} {:<20} {:<20} {:<20} {:<15}".format(row.title, row.year, row.director, row.leadActor, row.leadActress, row.runningTime))
