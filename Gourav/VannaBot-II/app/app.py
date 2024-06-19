import vanna
from vanna.remote import VannaDefault
from vanna.flask import VannaFlaskApp
from flask import Flask

app = Flask(__name__)

def connectToDB():
    try:
        # Set the base path for the API key file
        base_path = "/app/Key"
        # Set the file path for the API key file
        filepath = f"{base_path}/API_KEY.txt"
        # Open the API key file in read mode
        with open(filepath, "r") as f:
            # Read the API key from the file and join the lines into a single string
            api_key = ' '.join(f.readlines())
            # Uncomment the following line to set the API key as an environment variable
            # os.environ["API_KEY"] = api_key

        # Set the Vanna model name
        vanna_model_name = 'gourav_vanna'
        
        # Create a VannaDefault object with the model name and API key
        vn = VannaDefault(model=vanna_model_name, api_key=api_key)
        
        # Set the allow_llm_to_see_data attribute to True
        vn.allow_llm_to_see_data = True  # Set the attribute after initialization
        
        # Connect to the PostgreSQL database
        vn.connect_to_postgres(
            host='db',  # Hostname for the database
            dbname='GLIEF',  # Database name
            user='postgres',  # Username for the database
            password='postgres',  # Password for the database
            port=5432  # Port number for the database
        )
        # Print a success message if the connection is successful
        print("Connection to database successful.")
        
        # Return the VannaDefault object
        return vn

    except Exception as e:
        # Catch any exceptions that occur during the connection process
        print(f"An error occurred while connecting to the database: {e}")
        # Return None if an error occurs
        return None    # Your database connection code here
    pass

def prepareVannaSchema(vn):
        # The information schema query may need some tweaking depending on your database. This is a good starting point.
    df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

    # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
    plan = vn.get_training_plan_generic(df_information_schema)
    print(plan)

    # If you like the plan, then uncomment this and run it to train
    # vn.train(plan=plan)

    pass

def prepareVannaDDL(vn):
    """
    Trains the Vanna model with DDL statements to specify table names, column names, types, and relationships.

    Parameters:
    vn (VannaDefault): The Vanna model instance.
    """
    try:
        vn.train(ddl="""
        CREATE TABLE IF NOT EXISTS public."Entity_Legal_Info"
        (
            index bigint,
            lei text COLLATE pg_catalog."default" NOT NULL,
            entity_legalname text COLLATE pg_catalog."default",
            entity_legalname_xmllang text COLLATE pg_catalog."default",
            entity_legaladdress_city text COLLATE pg_catalog."default",
            entity_legaladdress_region text COLLATE pg_catalog."default",
            entity_legaladdress_country text COLLATE pg_catalog."default",
            entity_legaladdress_postalcode text COLLATE pg_catalog."default",
            entity_headquartersaddress_city text COLLATE pg_catalog."default",
            entity_headquartersaddress_region text COLLATE pg_catalog."default",
            entity_headquartersaddress_country text COLLATE pg_catalog."default",
            entity_headquartersaddress_postalcode text COLLATE pg_catalog."default",
            entity_legaljurisdiction text COLLATE pg_catalog."default",
            entity_entitycategory text COLLATE pg_catalog."default",
            entity_entitysubcategory text COLLATE pg_catalog."default",
            entity_associatedentity_type double precision,
            entity_associatedentity_associatedlei double precision,
            entity_associatedentity_associatedentityname double precision,
            entity_associatedentity_associatedentityname_xmllang double precision,
            entity_entitystatus text COLLATE pg_catalog."default",
            entity_entitycreationdate text COLLATE pg_catalog."default",
            entity_entityexpirationdate double precision,
            entity_entityexpirationreason double precision,
            registration_initialregistrationdate text COLLATE pg_catalog."default",
            registration_lastupdatedate text COLLATE pg_catalog."default",
            registration_registrationstatus text COLLATE pg_catalog."default",
            registration_nextrenewaldate text COLLATE pg_catalog."default",
            registration_managinglou text COLLATE pg_catalog."default",
            registration_validationsources text COLLATE pg_catalog."default",
            CONSTRAINT "leiPrimaryKey" PRIMARY KEY (lei)
                INCLUDE(lei)
        );

        CREATE TABLE IF NOT EXISTS public."Relationship_Information"
        (
            index bigint,
            relationship_startnode_nodeid text COLLATE pg_catalog."default",
            relationship_startnode_nodeidtype text COLLATE pg_catalog."default",
            relationship_endnode_nodeid text COLLATE pg_catalog."default",
            relationship_endnode_nodeidtype text COLLATE pg_catalog."default",
            relationship_relationshiptype text COLLATE pg_catalog."default",
            relationship_relationshipstatus text COLLATE pg_catalog."default",
            relationship_period_1_startdate text COLLATE pg_catalog."default",
            relationship_period_1_enddate text COLLATE pg_catalog."default",
            relationship_period_1_periodtype text COLLATE pg_catalog."default",
            relationship_period_2_startdate text COLLATE pg_catalog."default",
            relationship_period_2_enddate text COLLATE pg_catalog."default",
            relationship_period_2_periodtype text COLLATE pg_catalog."default",
            relationship_period_3_startdate text COLLATE pg_catalog."default",
            relationship_period_3_enddate text COLLATE pg_catalog."default",
            relationship_period_3_periodtype text COLLATE pg_catalog."default",
            relationship_period_4_startdate text COLLATE pg_catalog."default",
            relationship_period_4_enddate text COLLATE pg_catalog."default",
            relationship_period_4_periodtype text COLLATE pg_catalog."default",
            relationship_period_5_startdate text COLLATE pg_catalog."default",
            relationship_period_5_enddate text COLLATE pg_catalog."default",
            relationship_period_5_periodtype text COLLATE pg_catalog."default",
            relationship_qualifiers_1_qualifierdimension text COLLATE pg_catalog."default",
            relationship_qualifiers_1_qualifiercategory text COLLATE pg_catalog."default",
            relationship_qualifiers_2_qualifierdimension text COLLATE pg_catalog."default",
            relationship_qualifiers_2_qualifiercategory text COLLATE pg_catalog."default",
            relationship_qualifiers_3_qualifierdimension double precision,
            relationship_qualifiers_3_qualifiercategory double precision,
            relationship_qualifiers_4_qualifierdimension double precision,
            relationship_qualifiers_4_qualifiercategory double precision,
            relationship_qualifiers_5_qualifierdimension double precision,
            relationship_qualifiers_5_qualifiercategory double precision,
            relationship_quantifiers_1_measurementmethod text COLLATE pg_catalog."default",
            relationship_quantifiers_1_quantifieramount double precision,
            relationship_quantifiers_1_quantifierunits text COLLATE pg_catalog."default",
            relationship_quantifiers_2_measurementmethod double precision,
            relationship_quantifiers_2_quantifieramount double precision,
            relationship_quantifiers_2_quantifierunits double precision,
            relationship_quantifiers_3_measurementmethod double precision,
            relationship_quantifiers_3_quantifieramount double precision,
            relationship_quantifiers_3_quantifierunits double precision,
            relationship_quantifiers_4_measurementmethod double precision,
            relationship_quantifiers_4_quantifieramount double precision,
            relationship_quantifiers_4_quantifierunits double precision,
            relationship_quantifiers_5_measurementmethod double precision,
            relationship_quantifiers_5_quantifieramount double precision,
            relationship_quantifiers_5_quantifierunits double precision,
            registration_initialregistrationdate text COLLATE pg_catalog."default",
            registration_lastupdatedate text COLLATE pg_catalog."default",
            registration_registrationstatus text COLLATE pg_catalog."default",
            registration_nextrenewaldate text COLLATE pg_catalog."default",
            registration_managinglou text COLLATE pg_catalog."default",
            registration_validationsources text COLLATE pg_catalog."default",
            registration_validationdocuments text COLLATE pg_catalog."default",
            registration_validationreference text COLLATE pg_catalog."default",
            CONSTRAINT relationship_endnode_nodeid FOREIGN KEY (relationship_endnode_nodeid)
                REFERENCES public."Entity_Legal_Info" (lei) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );
        """)
        vn.train(sql="""SELECT relationship_startnode_nodeid
            FROM public."Relationship_Information"
            WHERE relationship_endnode_nodeid = (SELECT lei 
            FROM public."Entity_Legal_Info" 
            WHERE entity_legalname ILIKE '%CITIGROUP INC%');""")
        print("Vanna model training with DDL was successful.")
    except Exception as e:
        print(f"An error occurred while training the Vanna model: {e}")
    pass

def prepareVannaDocumentation(vn, statement):
    """
    Trains the Vanna model with documentation about business terminology or definitions.

    Parameters:
    vn (VannaDefault): The Vanna model instance.
    statement (str): The documentation statement to train the model with.
    """
    try:
        print("Adding documentation....")
        # Log the statement being sent
        print(f"Statement: {statement}")
        # Use the appropriate method from the Vanna library to add documentation
        response = vn.add_documentation(statement)
        # Log the response from the API
        print(f"API Response: {response}")
        print("Documentation added successfully.")
    except Exception as e:
        print(f"An error occurred while adding documentation: {e}")

def askVanna(vn, question):
    # Print the question for debugging purposes
    print(f"Debug: Question being sent to Vanna: {question}")  # Debugging line to print the question
    try:
        # Ask Vanna the question using the vn object
        response = vn.ask(question=question)
        # Print the response from Vanna
        print(response)
        return response
    except Exception as e:
        # Catch any exceptions that occur while asking Vanna
        print(f"An error occurred while asking Vanna: {e}")
        return {"error": str(e)}
    pass


# Example usage
firstStatement = (
    """Summary of relationships between nodes with Relationship_StartNode_NodeID and Relationship_EndNode_NodeID, Relationship_RelationshipType, periods, qualifiers, quantifiers, and registration details. Relationship_EndNode_NodeID is the foreign key in the table Relationship_Information. LEI column is the primary key in the table Entity_Legal_Info which is the foreign key Relationship_EndNode_NodeID column in the table Relationship_Information. Relationship_RelationshipType column contains the information about the relation between the given company name. There are 4 type of relations in Relationship_RelationshipType column 'IS_DIRECTLY_CONSOLIDATED_BY', 'IS_ULTIMATELY_CONSOLIDATED_BY', 'IS_FUND-MANAGED_BY' and 'IS_FUND-MANAGER'. Please find the description of all the relations below: 'IS_ULTIMATELY_CONSOLIDATED_BY' - is the ultimate child of given company. 'IS_DIRECTLY_CONSOLIDATED_BY' - is the direct child of given company. 'IS_FUND-MANAGED_BY' - is a relation who is managing the fund of given company. 'IS_FUND-MANAGER' - is a relation who's funds are managed by given company."""
)
secondStatement = (
    """When user asks for the company name like CITIGROUP INC. then use the LEI ID in the search query and use the relationship_endnode_nodeid within the relationship table to search for the results. Then use the query like mentioned in the below train query"""
)
thirdStatement = (
    """When a user asks for the company name like CITIGROUP INC. then use the LEI ID in the search query and use the relationship_endnode_nodeid within the relationship table to search for the results. Then use the query mentioned in the below train query. And if user also asks the details of the children or parents of the name like CITIGROUP INC. then please use the relationship_endnode_nodeid and search in the 'Entity_Legal_Info' table for that LEI and show the maximum data available in the database."""
)
fourthStatement = (
    """
    When constructing SQL queries for the database, ensure that all input values related to 'relationship_relationshipstatus' are converted to uppercase.
For example, if the user asks "how many records are related to Citigroup Inc whose relationship status is inactive", the query should convert 'inactive' to 'INACTIVE'.
Use the following SQL template as a guide:

SELECT COUNT(*)
FROM public."Relationship_Information"
WHERE relationship_endnode_nodeid IN (
    SELECT lei 
    FROM public."Entity_Legal_Info" 
    WHERE entity_legalname ILIKE '%CITIGROUP INC%'
)
AND relationship_relationshipstatus = UPPER('inactive');"""
)


@app.route('/')
def home():
    return "Welcome to Vanna Flask App!"

def initialize_vanna():
    vn = connectToDB()
    if vn:
        prepareVannaSchema(vn)
        prepareVannaDDL(vn)
        prepareVannaDocumentation(vn, firstStatement)
        prepareVannaDocumentation(vn, secondStatement)
        prepareVannaDocumentation(vn, thirdStatement)
        prepareVannaDocumentation(vn, fourthStatement)
        training_data = vn.get_training_data()
        VannaFlaskApp(vn).run()
    else:
        print("Vanna instance is not available. Cannot proceed with asking questions.")

if __name__ == "__main__":
    initialize_vanna()
