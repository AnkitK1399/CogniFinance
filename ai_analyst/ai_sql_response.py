from langchain_community.utilities import SQLDatabase
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain
from .few_shots import few_shots
from django.conf import settings
import os
from pathlib import Path


current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

to_vectorize = [" ".join(example.values()) for example in few_shots]

vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)

example_prompt = PromptTemplate(
                        input_variables=["Question", "SQLquery", "Results", "Answers"],
                        template="\nQuestion: {Question}\nSQLQuery: {SQLquery}\nSQLResult: {Results}\nAnswer: {Answers}",)
few_shot_prompt = FewShotPromptTemplate(
                        example_selector=example_selector,
                        example_prompt=example_prompt,
                        # Prefix sets the "personality" and rules
                        prefix="""You are a MySQL expert. Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
                        Use the following format:
                        
                        Question: "Question here"
                        SQLQuery: "SQL Query to run"
                        SQLResult: "Result of the SQLQuery"
                        Answer: "Final answer here"
                        """,
        
                        suffix="""Question: {input}
                         SQLQuery:
                         Answer:
                          """,
                        input_variables=["input", "table_info", "dialect"], 
                    )

def run_this(llm,question):
    db_path = project_root / 'db.sqlite3'
    if not db_path.exists():
        print("not found")
        return

    target_tables =['users_user', 'transactions_transaction','ai_analyst_aisummary']

    db = SQLDatabase.from_uri(f'sqlite:///{db_path}',include_tables = target_tables, sample_rows_in_table_info=3)
    
    
    db_chain = SQLDatabaseChain.from_llm(
        llm, 
        db, 
        prompt=few_shot_prompt, 
        verbose=True, 
        return_intermediate_steps=False # Set to False so 'result' is the final text
    )

    try:
        response = db_chain.invoke({"query": question})
        final_answer = response.get('result')
        
        return final_answer
    
    except Exception as e:
        # Log the full error to your terminal for debugging
        print(f"Error in SQL Chain: {e}")
        return f"I couldn't process that request. (Error: {str(e)})"

if __name__ == '__main__':
    run_this()






