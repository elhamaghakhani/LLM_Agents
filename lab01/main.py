from typing import Dict, List
from autogen import ConversableAgent
import sys
import os
import math
from autogen import register_function



def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    data_file = "/Users/ea664/Downloads/lab01_release/restaurant-data.txt"
    restaurant_reviews = {}

    restaurant_name = restaurant_name.lower()

    with open(data_file, 'r') as file:
        lines = [line.lower() for line in file] 
    for line in lines:
        name, review = line.split('.', 1)
        name = name.strip()  
        if name not in restaurant_reviews:
            restaurant_reviews[name] = []
        restaurant_reviews[name].append(review.strip())

    if restaurant_name not in restaurant_reviews:
        restaurant_name = restaurant_name.replace(' ', '-')

    return {restaurant_name: restaurant_reviews.get(restaurant_name, [])}

def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[str, float]:
    """
    Calculate the overall score for a restaurant based on food and customer service scores.
    """
    N = len(food_scores)
    if N == 0:
        return {restaurant_name: 0.000}
    overall_score = sum(math.sqrt(food_scores[i]**2 * customer_service_scores[i]) for i in range(N)) * (1 / (N * math.sqrt(125))) * 10
    formatted_score = f"{overall_score:.3f}"
    return {restaurant_name: formatted_score}

def get_entrypoint_agent_prompt() -> str:
    return (

    """You are an assistant that supervises the workflow of fetching, analyzing, and scoring restaurant reviews.
        You have to follow these steps carefully:
        1. First, you have to communicate with fetch agent to get the restaurant reviews using fetch_restaurant_data function.
        2. second, after getting the reviews, send ALL the reviews to analyser agent for analysis
        3. Third, after getting the scores from the analyzer agent, ask the scoring agent to calculate the final score using 
        calculate_overall_score function. Remeber to only pass the scores to the scoring agent NOTHING ELSE! """
        )
        


def get_data_fetch_agent_prompt(restaurant_query: str) -> str:
    return f"""You are a data fetch agent responsible for extracting restaurant name from user query and fetching their reviews: 
    Your task is:
    1. Extract the restaurant name from the user query: "{restaurant_query}"
    2. Call the fetch_restaurant_data function and fetch reviews for the restaurant. 
    Keep in mind that you fetch All the reviews!"""

def get_analysis_agent_prompt() -> str:
    return (
            """ You are a review analyzer agent. For each review, extract the food quality score (1-5) and the customer service score (1-5).
            Scores are based on adjectives found in the review, as follows:\n
            - Score 1: awful, horrible, disgusting\n
            - Score 2: bad, unpleasant, offensive\n
            - Score 3: average, uninspiring, forgettable\n
            - Score 4: good, enjoyable, satisfying\n
            - Score 5: awesome, incredible, amazing\n

            Find exactly one keyword for food quality and one for service quality and map keywords to scores using the mappings.
            Provide the scores in a list format like this:
            food_scores = [score1, score2, ...]
            customer_service_scores = [score1, score2, ...]"""
        )

def get_scoring_agent_prompt() -> str:
    return f"""You are a scoring agent. Use the scores sent to you to calculate the final score for the restaurant using the scores for food and customer service.
     You have to call the function calculate_overall_score."""

# Do not modify the signature of the "main" function.
def main(user_query: str):
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}

    entrypoint_agent = ConversableAgent(
        "entrypoint_agent", 
        system_message=
        llm_config=llm_config,
        function_map={"fetch_restaurant_data": fetch_restaurant_data}
        )



    fetch_agent = ConversableAgent(
        name="fetch_agent",
        system_message=get_data_fetch_agent_prompt(user_query),
        llm_config=llm_config
    )

    analyzer_agent = ConversableAgent(
        name="analysis_agent",
        system_message= get_analysis_agent_prompt(),
        llm_config=llm_config
    )

   
    
   
    scoring_agent = ConversableAgent(
        name="scoring_agent",
        system_message=get_scoring_agent_prompt(),
        llm_config=llm_config
    )

    register_function(
        fetch_restaurant_data,
        caller=entrypoint_agent,  
        executor=fetch_agent, 
        name="fetch_restaurant_data", 
        description="Fetches the reviews for a specific restaurant."
    )
    
    register_function(
        calculate_overall_score,
        caller=entrypoint_agent,  
        executor=scoring_agent, 
        name="calculate_overall_score", 
        description="Calculates the final score for a restaurant."
    )
  
    
    
    fetch_result = entrypoint_agent.initiate_chats(
        [
            {
                "recipient": fetch_agent,
                "message": f"Fetch reviews for the query: {user_query}",
                "max_turns": 2,
                "summary_method": "reflection_with_llm",
                "summary_args": {"summary_prompt": "Give ALL the fetched reviews to the analyzer."}
            },
            {
                "recipient": analyzer_agent,
                "message": "Analyze the reviews given to you and extract food and service scores. For each review, find the keywords for food quality and service quality, then map them to scores 1-5 according to the scoring rules. ",
                "max_turns": 2,
                "summary_method": "reflection_with_llm",
                "summary_args": {"summary_prompt": "Give food scores and customer service scores. You should Only send the list of scores, Nothing Else!"}
            },
            {
                "recipient": scoring_agent,
                "message": "Use the list of food_scores and customer_service_scores and calculate the final scoring using the calculate_overall_score function.",
                "max_turns": 2,
                "summary_method": "reflection_with_llm",
                "summary_args": {"summary_prompt": "ONLY give the final score."}
            }
        ])
    return fetch_result

    
    
    
  
# DO NOT modify this code below.
if __name__ == "__main__":  
    assert len(sys.argv) > 1, "Please ensure you include a query for some restaurant when executing main."
    main(sys.argv[1])