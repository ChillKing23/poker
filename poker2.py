import random
from itertools import combinations

# Define card ranks and suits
RANKS = "23456789TJQKA"
SUITS = "CDHS"
DECK = [rank + suit for rank in RANKS for suit in SUITS]

# Function to evaluate hand rankings
def evaluate_hand(hand):
    """Simple hand evaluator - will rank hands based on combinations."""
    ranks = ''.join(sorted([card[0] for card in hand], key=lambda x: RANKS.index(x), reverse=True))
    suits = [card[1] for card in hand]
    unique_ranks = set(ranks)
    is_flush = len(set(suits)) == 1
    is_straight = len(unique_ranks) == 5 and RANKS.index(ranks[0]) - RANKS.index(ranks[-1]) == 4

    if is_flush and is_straight:
        return (8, ranks)  # Straight flush
    elif len(unique_ranks) == 2:
        return (7, ranks)  # Four of a kind or full house
    elif is_flush:
        return (6, ranks)  # Flush
    elif is_straight:
        return (5, ranks)  # Straight
    elif len(unique_ranks) == 3:
        return (4, ranks)  # Three of a kind or two pairs
    elif len(unique_ranks) == 4:
        return (3, ranks)  # Pair
    else:
        return (2, ranks)  # High card

# Calculate odds
def calculate_odds(players, hole_cards, flop):
    # Initialize remaining deck
    used_cards = set(hole_cards + flop)
    remaining_deck = [card for card in DECK if card not in used_cards]

    # Generate possible hands for remaining cards
    possible_hands = list(combinations(remaining_deck, 2))
    win_count = 0
    total_simulations = 0

    for _ in range(10000):  # Monte Carlo simulation
        # Shuffle deck and draw for opponents
        random.shuffle(remaining_deck)
        opponent_hands = [remaining_deck[i:i+2] for i in range(0, players * 2, 2)]

        # Evaluate hands
        player_hand = hole_cards + flop
        player_score = evaluate_hand(player_hand)
        opponent_scores = [evaluate_hand(op_hand + flop) for op_hand in opponent_hands]

        # Determine winner
        if all(player_score > opp_score for opp_score in opponent_scores):
            win_count += 1
        total_simulations += 1

    # Calculate odds
    win_odds = win_count / total_simulations * 100
    return win_odds

# Main function to input details and calculate odds
def main():
    # Input number of players
    players = int(input("Enter the number of players: "))
    
    # Input hole cards
    hole_cards = input("Enter your hole cards (e.g., 'AH KH'): ").split()
    
    # Input flop cards
    flop = input("Enter the flop cards (e.g., '2H 7D 9C'): ").split()
    
    # Calculate odds
    win_odds = calculate_odds(players, hole_cards, flop)
    print(f"Your chance of winning is approximately {win_odds:.2f}%")

if __name__ == "__main__":
    main()
