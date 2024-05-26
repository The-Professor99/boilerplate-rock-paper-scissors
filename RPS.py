from itertools import product
from typing import List, Dict, Optional, Tuple

def make_play_list(order: int = 1) -> Dict[str, List[str]]:
    """Generate a play list dictionary for a given order."""
    plays = ["R", "P", "S"]
    return {''.join(combination): [] for combination in product(plays, repeat=order)}

def remove_values_from_list(the_list: List[str], value_to_remove: str) -> List[str]:
    """Custom `remove` function. Removes all occurrences of a value in a list."""
    return [value for value in the_list if value != value_to_remove]

def reset_play_list(play_list, order):
    """Resets the play list and repopulates it with default values"""
    play_list.clear()
    play_list.extend(make_play_list(i) for i in range(1, order + 1))
    
def retrieve(
    prev_opponent_play: str,
    opponent_history: List[str],
    play_list: List[Dict[str, List[str]]],
    order: int = 1,
    samples_to_use: int = 100,
    reset: bool = False,
) -> Tuple[List[Dict[str, List[str]]], Optional[str]]:
    """Retrieve the next play based on the opponent's history."""

    def update_value_history(play_list: List[Dict[str, List[str]]], value_name: str, order: int, value: str):
        """Update the play list. 

        Params
        ----
        play_list: The playlist to be updated.
        value_name: The value within the playlist that will be updated.
        order: What order the value is in within the playlist.
        value: The value to be added to [value_name] which is within [order] in [play_list]"""

        play_list[order][value_name].append(value)

    def get_value_history(play_list: List[Dict[str, List[str]]], value_name: str, order: int):
        return play_list[order][value_name]  

    def decide_potential_response(value_history):
        # return the value with the most occurrences in value_history. later values in the value_history are preferred in cases of equal occurrences 
        return max(value_history[::-1], default=None, key=value_history.count)         
    def get_potential_next_play(potential_next_plays):
        valid_plays = remove_values_from_list(potential_next_plays, None)

        # return the value with the most occurrences in valid_plays. later values in the valid_plays are preferred in cases of equal occurrences
        potential_next_play = max(valid_plays[::-1], default=None, key=valid_plays.count)
        return potential_next_play

    def get_potential_response(opponent_history, play_list, order):
        # copy opponent_history so it remains same over multiple iterations
        opponent_history_cp = opponent_history[:]

        #update playlist. E.g1 supposing opponent history is [R, P, S, P], order is 1, and prev_opponent_play is R, the play_list should be {R: [P], P: [S, R], S: [P]}
        # E.g2 supposing opponent history is [R, P, S, P, P, R, S, P], order is 2, and prev_opponent_play is R, the play_list should be {RP: [S], PS: [P], SP: [P, R], PP: [R], PR: [S], RS: [P]}
        # i.e it considers the previous plays of the opponent and add the next play to the list of likely plays the opponent will play after
        value_name = "".join(opponent_history_cp[-order:])  
        update_value_history(play_list, value_name, order - 1, prev_opponent_play)

        # append prev_opponent_play and update value_name
        opponent_history_cp.append(prev_opponent_play)   
        value_name = "".join(opponent_history_cp[-order:])

        # Get value history, eg if order is 2 and play_list is {RP: [S], PS: [P], SP: [P, R], PP: [R], PR: [S], RS: [P]}. if last plays of the opponent is "SP" it returns [P, R]
        value_history = get_value_history(play_list, value_name, order - 1)

        value_history = value_history[-samples_to_use:] if len(value_history) else [None] 
        
        potential_response = decide_potential_response(value_history)
        
        return potential_response
   
    def get_potential_responses(opponent_history, play_list, order): 
        potential_responses = []
        
        for i in range(1, order + 1):
            potential_response = get_potential_response(opponent_history, play_list, i)
            potential_responses.append(potential_response)

        return potential_responses
    
    potential_response = None
    if reset:
        reset_play_list(play_list, order)
    else:
        # order is only valid if len(opponent_history) >= order else, use len(opponent_history) as order size
        len_opp = len(opponent_history)  
        order_used = min(order, len_opp)  
        
        potential_responses = get_potential_responses(opponent_history, play_list, order_used)

        potential_response = get_potential_next_play(potential_responses)
                     
    return play_list, potential_response



def player(
    prev_opponent_play: str,
    opponent_history: List[str] = [],
    play_list: List[Dict[str, List[str]]] = [],
    samples_to_use: int = 30,
    order: int = 5):
    default_next_play = "S"
    reset = False
    
    if not prev_opponent_play:
        # if prev_opponent_play is "", it means the game just started. Reset.
        prev_opponent_play = "R"
        opponent_history.clear()
        reset = True
    else: 
        reset = False

    play_list, potential_response = retrieve(prev_opponent_play, opponent_history, play_list=play_list, order=order, samples_to_use=samples_to_use, reset=reset)
    opponent_history.append(prev_opponent_play)
    

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    
    potential_response = potential_response or default_next_play

    return ideal_response[potential_response]